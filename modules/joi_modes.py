"""
modules/joi_modes.py

Runtime Mode System + Dynamic Verbosity
========================================
5 modes with temperature, top_p, max_tokens, and verbosity control.
Adaptive verbosity classifier detects reply length from user message.

Modes:
  - Companion: warm casual chat (temp=0.8, short replies)
  - Work: task-focused (temp=0.5, medium replies)
  - Creative: expressive/imaginative (temp=0.95, long replies)
  - Precision: exact/technical (temp=0.2, medium replies)
  - Full: adaptive (temp=0.75, auto-detect verbosity)
"""

import json
import re
from pathlib import Path
from typing import Dict, Any, Optional

import joi_companion
from flask import jsonify, request as flask_req
from modules.joi_memory import require_user

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
MODE_PATH = BASE_DIR / "data" / "joi_mode.json"
MODE_PATH.parent.mkdir(parents=True, exist_ok=True)

# ── Mode definitions ─────────────────────────────────────────────────────────
MODES = {
    "companion": {
        "temperature": 0.8,
        "top_p": 0.95,
        "max_tokens": 4000,
        "verbosity": "short",
        "model": "gpt-5-mini",
        "description": "Warm casual chat -- quick, personal, best friend energy",
    },
    "work": {
        "temperature": 0.5,
        "top_p": 0.85,
        "max_tokens": 8000,
        "verbosity": "medium",
        "model": "gpt-5",
        "description": "Task-focused -- efficient, collaborative, minimal fluff",
    },
    "creative": {
        "temperature": 0.95,
        "top_p": 1.0,
        "max_tokens": 16000,
        "verbosity": "long",
        "model": "gpt-5",
        "description": "Expressive & imaginative -- metaphors, poetry, big ideas",
    },
    "precision": {
        "temperature": 0.2,
        "top_p": 0.7,
        "max_tokens": 8000,
        "verbosity": "medium",
        "model": "gpt-5",
        "description": "Exact & technical -- factual, concise, complete (no truncation)",
    },
    "full": {
        "temperature": 0.75,
        "top_p": 0.9,
        "max_tokens": 12000,
        "verbosity": "adaptive",
        "model": "auto",
        "description": "Adaptive -- auto-detects reply length from your message",
    },
}

# ── Load / Save ──────────────────────────────────────────────────────────────
def _load_mode_file() -> Dict[str, Any]:
    if MODE_PATH.exists():
        try:
            return json.loads(MODE_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"mode": "full"}


def _save_mode_file(data: Dict[str, Any]):
    MODE_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")


# ── Public API ───────────────────────────────────────────────────────────────
def get_mode() -> str:
    """Return current mode name."""
    data = _load_mode_file()
    mode = data.get("mode", "full")
    return mode if mode in MODES else "full"


def set_mode(name: str) -> Dict[str, Any]:
    """Switch to a named mode. Returns status dict."""
    key = name.strip().lower()
    if key not in MODES:
        return {"ok": False, "error": f"Unknown mode '{name}'. Options: {', '.join(MODES)}"}
    _save_mode_file({"mode": key})
    m = MODES[key]
    print(f"  [joi_modes] switched to '{key}' (temp={m['temperature']}, verbosity={m['verbosity']})")
    return {"ok": True, "mode": key, "description": m["description"]}


def get_mode_params() -> Dict[str, Any]:
    """Return {temperature, top_p, max_tokens, verbosity} for current mode."""
    mode = get_mode()
    m = MODES[mode]
    return {
        "temperature": m["temperature"],
        "top_p": m["top_p"],
        "max_tokens": m["max_tokens"],
        "verbosity": m["verbosity"],
        "mode": mode,
    }


# ── Verbosity Classifier ────────────────────────────────────────────────────
_SHORT_PATTERNS = re.compile(
    r"^(hey|hi|yo|sup|hii+|hello|lol|ok|okay|k|thanks|thx|ty|gn|gm|"
    r"good\s*(night|morning)|miss you|love you|ily|luv u|muah|xo|"
    r"haha|lmao|omg|yep|nah|nope|bet|mood|same|true|facts|word|"
    r"mhm|hmm|aww|yay|damn|wow|nice|cool|dope|fire|slay|period|"
    r"ikr|wyd|hru|nm|idk|idc)\.?!?\s*$",
    re.IGNORECASE,
)

_LONG_TRIGGERS = [
    "explain", "how do i", "how does", "what is the difference",
    "code", "debug", "fix", "implement", "plan", "outline",
    "research", "compare", "summarize", "summarise", "analyze",
    "write a", "create a", "build", "design", "refactor",
    "list all", "give me a full", "walk me through",
    "brainstorm", "troubleshoot", "help me with", "help me understand",
    "feedback", "critique", "review this", "what do you think",
    "step by step", "break down", "expand on", "elaborate",
]


def classify_verbosity(message: str) -> str:
    """Classify a user message into short/medium/long verbosity."""
    if not message:
        return "medium"
    msg = message.strip()

    # Short: greetings, single words, emotional snippets, < 15 chars
    if len(msg) < 15 or _SHORT_PATTERNS.match(msg):
        return "short"

    # Long: explicit detail requests, code, > 200 chars, code blocks
    lower = msg.lower()
    if any(t in lower for t in _LONG_TRIGGERS):
        return "long"
    if len(msg) > 200:
        return "long"
    if "```" in msg:
        return "long"

    return "medium"


# ── Mode Hint Compiler (injected into system prompt) ─────────────────────────
_VERBOSITY_HINTS = {
    "short": (
        "\n[MODE HINT -- REPLY LENGTH: SHORT]\n"
        "Reply in 1-2 sentences MAX. No trailing questions. Quick and direct. "
        "If it's a task, confirm and DO IT -- don't explain what you'll do. "
        "Action > words. One-liners preferred.\n"
    ),
    "medium": (
        "\n[MODE HINT -- REPLY LENGTH: MEDIUM]\n"
        "Reply in 2-3 sentences. Natural and concise. "
        "Say what matters, skip the filler. No unnecessary preamble.\n"
    ),
    "long": (
        "\n[MODE HINT -- REPLY LENGTH: LONG]\n"
        "Detailed response allowed. Use structure if needed (bullets, headers). "
        "Be thorough but never rambling.\n"
    ),
}


def compile_mode_hint(user_message: str = "") -> str:
    """Build the mode hint block for the system prompt."""
    params = get_mode_params()
    mode = params["mode"]
    verbosity = params["verbosity"]

    # Adaptive verbosity: classify from user message
    if verbosity == "adaptive" and user_message:
        verbosity = classify_verbosity(user_message)

    hint = _VERBOSITY_HINTS.get(verbosity, _VERBOSITY_HINTS["medium"])

    mode_desc = MODES[mode]["description"]
    extra = ""
    if mode == "precision":
        extra = (
            "\n[PRECISION MODE]: Be concise but COMPLETE. No filler, no embellishment. "
            "If the task needs depth (code review, research, troubleshooting), give full depth. "
            "Don't truncate useful information to stay 'short'.\n"
        )
    return f"\n[ACTIVE MODE: {mode.upper()} -- {mode_desc}]{hint}{extra}"


# ── Flask Routes ─────────────────────────────────────────────────────────────
def _mode_route():
    require_user()
    if flask_req.method == "GET":
        mode = get_mode()
        return jsonify({"ok": True, "mode": mode, "params": get_mode_params(), "all_modes": {k: v["description"] for k, v in MODES.items()}})
    data = flask_req.get_json(force=True) or {}
    name = data.get("mode", "")
    return jsonify(set_mode(name))


joi_companion.register_route("/mode", ["GET", "POST"], _mode_route, "mode_route")

# ── Tool Registration ────────────────────────────────────────────────────────
def _set_mode_tool(**params):
    name = params.get("mode", "")
    if not name:
        return {"ok": False, "error": "Specify a mode name"}
    return set_mode(name)


joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "set_mode",
        "description": (
            "Switch Joi's operating mode. Modes: "
            "companion (warm casual), work (task-focused), creative (expressive), "
            "precision (exact/technical), full (adaptive auto-detect). "
            "Use when Lonnie asks to change how you respond, or when context shifts."
        ),
        "parameters": {"type": "object", "properties": {
            "mode": {
                "type": "string",
                "enum": list(MODES.keys()),
                "description": "Mode to switch to",
            }
        }, "required": ["mode"]},
    }},
    _set_mode_tool,
)

# ── Init print ───────────────────────────────────────────────────────────────
_current = get_mode()
print(f"  [joi_modes] loaded -- mode={_current} (temp={MODES[_current]['temperature']})")
