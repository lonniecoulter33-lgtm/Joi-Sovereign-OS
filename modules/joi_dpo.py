"""
modules/joi_dpo.py

Direct Preference Optimization -- Learns Lonnie's preferences from every exchange.

ALWAYS-ON (no tool call required):
  1. detect_preference_signal(user_msg, reply) -- runs every /chat turn
  2. compile_dpo_block() -- injected into system prompt at step 18
  3. get_dpo_insights tool -- Joi can self-inspect learned preferences

Preference Dimensions (0.0-1.0):
  brevity, sass_level, tool_eagerness, detail_depth,
  formality, emoji_use, question_frequency, explanation_style
"""

import json
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import joi_companion

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
DPO_PATH = DATA_DIR / "dpo_preferences.json"

# ── Default Preferences ──────────────────────────────────────────────────────
DEFAULT_PREFERENCES = {
    "brevity":              {"value": 0.7, "confidence": 0.3, "samples": 0, "last_updated": None},
    "sass_level":           {"value": 0.5, "confidence": 0.3, "samples": 0, "last_updated": None},
    "tool_eagerness":       {"value": 0.5, "confidence": 0.3, "samples": 0, "last_updated": None},
    "detail_depth":         {"value": 0.4, "confidence": 0.3, "samples": 0, "last_updated": None},
    "formality":            {"value": 0.2, "confidence": 0.3, "samples": 0, "last_updated": None},
    "emoji_use":            {"value": 0.2, "confidence": 0.3, "samples": 0, "last_updated": None},
    "question_frequency":   {"value": 0.2, "confidence": 0.3, "samples": 0, "last_updated": None},
    "explanation_style":    {"value": 0.4, "confidence": 0.3, "samples": 0, "last_updated": None},
    "coding":               {"value": 0.5, "confidence": 0.3, "samples": 0, "last_updated": None},  # Tier 2/3: style + bug feedback
}

MAX_SIGNAL_LOG = 200

# ── Signal Detection Patterns ────────────────────────────────────────────────
# (keywords, dimension, delta)  --  None dimension = general positive/negative
SIGNAL_PATTERNS = {
    "brevity_down":  (["too short", "more detail", "elaborate", "explain more", "tell me more", "go on", "keep going"], "brevity", -0.08),
    "brevity_up":    (["too long", "tldr", "shorter", "brief", "just tell me", "tl;dr", "sum it up", "summarize"], "brevity", +0.08),
    "sass_down":     (["be serious", "stop joking", "focus", "not funny", "be professional"], "sass_level", -0.08),
    "sass_up":       (["lol", "haha", "that's funny", "slay", "lmao", "dead"], "sass_level", +0.05),
    "detail_up":     (["how does that work", "why", "explain", "walk me through", "break it down"], "detail_depth", +0.06),
    "detail_down":   (["i know", "i get it", "skip the explanation", "just do it"], "detail_depth", -0.06),
    "tool_positive": (["thanks for saving", "good you remembered", "glad you searched", "nice find"], "tool_eagerness", +0.06),
    "formal_up":     (["be professional", "formal", "proper"], "formality", +0.08),
    "formal_down":   (["chill", "relax", "casual", "be yourself"], "formality", -0.06),
    "emoji_up":      (["use emojis", "more emojis"], "emoji_use", +0.10),
    "emoji_down":    (["no emojis", "stop with the emojis", "less emojis"], "emoji_use", -0.10),
    "question_down": (["stop asking", "don't ask me", "stop with the questions", "just do it"], "question_frequency", -0.10),
    "correction":    (["no", "wrong", "not what i", "that's not", "i said", "try again", "nope", "that's wrong"], None, 0),
    "praise":        (["perfect", "exactly", "yes!", "that's it", "love it", "good", "great", "nice", "awesome"], None, 0),
}

# ── Persistence ──────────────────────────────────────────────────────────────
_dpo_cache: Optional[Dict[str, Any]] = None
_dpo_cache_ts: float = 0
DPO_CACHE_TTL: float = 45.0


def _load_dpo() -> Dict[str, Any]:
    """Load DPO preferences from disk. Cached 45s to reduce file I/O per request."""
    global _dpo_cache, _dpo_cache_ts
    now = time.time()
    if _dpo_cache is not None and (now - _dpo_cache_ts) < DPO_CACHE_TTL:
        return _dpo_cache
    if DPO_PATH.exists():
        try:
            data = json.loads(DPO_PATH.read_text(encoding="utf-8"))
            _dpo_cache = data
            _dpo_cache_ts = now
            return data
        except Exception:
            pass
    default = {"preferences": dict(DEFAULT_PREFERENCES), "signal_log": []}
    _dpo_cache = default
    _dpo_cache_ts = now
    return default


def _save_dpo(data: Dict[str, Any]):
    """Persist DPO preferences to disk."""
    global _dpo_cache
    try:
        DPO_PATH.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")
    except Exception as e:
        print(f"  [DPO] Save failed: {e}")
    _dpo_cache = None  # invalidate so next load is fresh


# ── Correction Handler (Self-Correction Loop) ──────────────────────────────
# Trigger prefixes that indicate the user is correcting the previous AI response
CORRECTION_TRIGGERS = ("no,", "no ", "actually,", "actually ", "stop.", "stop ", "wait,", "wait ", "nope,", "nope ", "wrong,", "wrong ")


def is_correction_message(user_msg: str) -> bool:
    """True if the message looks like a correction of the previous reply."""
    if not user_msg or len(user_msg.strip()) < 2:
        return False
    lower = user_msg.strip().lower()
    return any(lower.startswith(t) for t in CORRECTION_TRIGGERS)


def record_correction_signal(user_msg: str, previous_reply: str) -> None:
    """
    Called when the user corrects the previous AI response (e.g. "No, ...", "Actually, ...").
    Updates DPO: reduces confidence so Joi adapts, and logs the correction.
    """
    if not previous_reply:
        return
    data = _load_dpo()
    prefs = data.get("preferences", dict(DEFAULT_PREFERENCES))
    signals = data.get("signal_log", [])

    # Apply correction: reduce confidence across preferences (be more adaptive)
    for dim_name, pref in prefs.items():
        pref["confidence"] = max(0.1, pref["confidence"] - 0.02)
        pref["last_updated"] = datetime.now().isoformat()

    # Log the correction with context for learning
    signals.append({
        "ts": datetime.now().isoformat(),
        "signal": "user_correction",
        "dimension": None,
        "trigger": "correction_handler",
        "user_preview": user_msg[:120],
        "previous_reply_preview": previous_reply[:200],
    })
    if len(signals) > MAX_SIGNAL_LOG:
        signals = signals[-MAX_SIGNAL_LOG:]

    data["preferences"] = prefs
    data["signal_log"] = signals
    _save_dpo(data)

    try:
        from modules.joi_neuro import emit_brain_event
        emit_brain_event("LEARNING", 0.7, source="correction_handler")
    except Exception:
        pass
    print(f"  [DPO] Correction recorded (previous reply excerpt: {previous_reply[:60]}...)")

# ── Coding / 3-Tier signals (Tester bug = negative, user accept = positive) ───
def record_coding_signal(positive: bool, context: str = "unknown") -> None:
    """
    When Tier 3 (Tester) finds a bug -> call with positive=False, context='tester_bug'.
    When the user accepts applied code -> call with positive=True, context='user_accept'.
    Updates the 'coding' preference and logs to signal_log for skill_library style rules.
    """
    data = _load_dpo()
    prefs = data.get("preferences", dict(DEFAULT_PREFERENCES))
    if "coding" not in prefs:
        prefs["coding"] = {"value": 0.5, "confidence": 0.3, "samples": 0, "last_updated": None}
    coding = prefs["coding"]
    delta = 0.06 if positive else -0.06
    coding["value"] = max(0.0, min(1.0, coding["value"] + delta))
    coding["samples"] = coding.get("samples", 0) + 1
    coding["confidence"] = min(1.0, coding["confidence"] + 0.02)
    coding["last_updated"] = datetime.now().isoformat()
    signals = data.get("signal_log", [])
    signals.append({
        "ts": datetime.now().isoformat(),
        "signal": "coding_positive" if positive else "coding_negative",
        "dimension": "coding",
        "trigger": context,
        "user_preview": context,
    })
    if len(signals) > MAX_SIGNAL_LOG:
        signals = signals[-MAX_SIGNAL_LOG:]
    data["preferences"] = prefs
    data["signal_log"] = signals
    _save_dpo(data)
    try:
        from modules.joi_neuro import emit_brain_event
        emit_brain_event("LEARNING", 0.5, source=f"coding_signal:{context}")
    except Exception:
        pass


# ── Signal Detection (runs every turn, no LLM call) ─────────────────────────
def detect_preference_signal(user_msg: str, reply: str):
    """
    Analyze user's message for preference signals. Called post-response every turn.
    Updates preference scores and logs signals.
    """
    if not user_msg:
        return

    data = _load_dpo()
    prefs = data.get("preferences", dict(DEFAULT_PREFERENCES))
    signals = data.get("signal_log", [])
    lower = user_msg.lower().strip()
    detected = []

    for signal_name, (keywords, dimension, delta) in SIGNAL_PATTERNS.items():
        for kw in keywords:
            if kw in lower:
                detected.append((signal_name, dimension, delta, kw))
                break  # one match per pattern group

    if not detected:
        # Implicit signal: if reply was long and user follows up with short msg,
        # might indicate they want shorter replies
        if len(reply) > 500 and len(user_msg) < 20:
            # Mild brevity signal
            detected.append(("implicit_brevity", "brevity", +0.02, "short_followup"))

    # Apply detected signals
    for signal_name, dimension, delta, trigger in detected:
        if dimension and dimension in prefs:
            pref = prefs[dimension]
            old_val = pref["value"]
            # Apply with diminishing returns as confidence grows
            effective_delta = delta * (1.0 - pref["confidence"] * 0.5)
            pref["value"] = max(0.0, min(1.0, old_val + effective_delta))
            pref["samples"] += 1
            pref["confidence"] = min(1.0, pref["confidence"] + 0.02)
            pref["last_updated"] = datetime.now().isoformat()

        # Log the signal
        signals.append({
            "ts": datetime.now().isoformat(),
            "signal": signal_name,
            "dimension": dimension,
            "delta": delta,
            "trigger": trigger,
            "user_preview": user_msg[:80],
        })

    # Trim signal log
    if len(signals) > MAX_SIGNAL_LOG:
        signals = signals[-MAX_SIGNAL_LOG:]

    # General positive/negative boost: praise lifts confidence, correction lowers it
    for signal_name, dimension, delta, trigger in detected:
        if signal_name == "praise":
            # Reinforce whatever the current style is
            for dim_name, pref in prefs.items():
                pref["confidence"] = min(1.0, pref["confidence"] + 0.01)
        elif signal_name == "correction":
            # Reduce confidence (Joi should be more adaptive)
            for dim_name, pref in prefs.items():
                pref["confidence"] = max(0.1, pref["confidence"] - 0.01)

    data["preferences"] = prefs
    data["signal_log"] = signals
    _save_dpo(data)

    # Coding acceptance: user says "yes" / "apply" / "approved" after a code/diff reply -> positive signal
    accept_phrases = ("yes", "apply", "approved", "looks good", "accept", "go ahead", "do it", "approved")
    if any(lower.startswith(p) or lower == p for p in accept_phrases) and len(lower) < 50:
        code_indicators = ("diff", "patch", "proposal", "edit", "change to", "```", "propose_patch", "code_edit")
        if any(ind in (reply or "") for ind in code_indicators):
            record_coding_signal(positive=True, context="user_accept")

    # Emit neuro brain event
    if detected:
        try:
            from modules.joi_neuro import emit_brain_event
            emit_brain_event("LEARNING", 0.6, source="dpo_signal")
        except Exception:
            pass
        print(f"  [DPO] Detected {len(detected)} signals: {[d[0] for d in detected]}")

    # Also log to SQLite for durability
    if detected:
        try:
            from modules.joi_db import db_connect
            conn = db_connect()
            cur = conn.cursor()
            for signal_name, dimension, delta, trigger in detected:
                cur.execute(
                    "INSERT INTO dpo_signals (ts, signal_type, dimension, delta, trigger_text, user_message_preview) VALUES (?, ?, ?, ?, ?, ?)",
                    (datetime.now().isoformat(), signal_name, dimension, delta, trigger, user_msg[:200])
                )
            conn.commit()
            conn.close()
        except Exception:
            pass  # table may not exist yet on first run


# ── Compile DPO Block (injected into system prompt) ─────────────────────────
def compile_dpo_block() -> str:
    """
    Generate a system prompt block describing Lonnie's learned preferences.
    Returns empty string if no data yet.
    """
    data = _load_dpo()
    prefs = data.get("preferences", {})

    total_samples = sum(p.get("samples", 0) for p in prefs.values())
    if total_samples < 3:
        return ""  # not enough data yet

    lines = [f"\n[LEARNED PREFERENCES -- from {total_samples} interactions with Lonnie]:"]

    # Brevity
    brev = prefs.get("brevity", {})
    if brev.get("samples", 0) > 0:
        level = "KEEP IT SHORT" if brev["value"] > 0.6 else "MODERATE LENGTH" if brev["value"] > 0.35 else "DETAILED IS OK"
        conf = "high" if brev["confidence"] > 0.6 else "medium" if brev["confidence"] > 0.3 else "low"
        lines.append(f"- Response length: {level} (brevity={int(brev['value']*100)}%, {conf} confidence)")

    # Sass
    sass = prefs.get("sass_level", {})
    if sass.get("samples", 0) > 0:
        level = "HIGH SASS" if sass["value"] > 0.7 else "MODERATE" if sass["value"] > 0.35 else "LOW -- be more serious"
        lines.append(f"- Sass/humor: {level} (sass={int(sass['value']*100)}%)")

    # Tool eagerness
    tool = prefs.get("tool_eagerness", {})
    if tool.get("samples", 0) > 0:
        level = "PROACTIVE -- use tools without being asked" if tool["value"] > 0.6 else "MODERATE" if tool["value"] > 0.35 else "CONSERVATIVE -- only when asked"
        lines.append(f"- Tool usage: {level} (eagerness={int(tool['value']*100)}%)")

    # Detail
    detail = prefs.get("detail_depth", {})
    if detail.get("samples", 0) > 0:
        level = "HIGH -- explain things" if detail["value"] > 0.6 else "MODERATE" if detail["value"] > 0.35 else "LOW unless asked"
        lines.append(f"- Detail level: {level} (detail={int(detail['value']*100)}%)")

    # Formality
    formal = prefs.get("formality", {})
    if formal.get("samples", 0) > 0:
        level = "FORMAL" if formal["value"] > 0.6 else "MIXED" if formal["value"] > 0.35 else "CASUAL, no formality"
        lines.append(f"- Style: {level} (formality={int(formal['value']*100)}%)")

    # Emoji
    emoji = prefs.get("emoji_use", {})
    if emoji.get("samples", 0) > 0:
        level = "YES -- use emojis" if emoji["value"] > 0.5 else "SPARINGLY" if emoji["value"] > 0.2 else "MINIMAL/NONE"
        lines.append(f"- Emojis: {level} (emoji={int(emoji['value']*100)}%)")

    # Coding (from Tester bugs / user accept)
    coding_pref = prefs.get("coding", {})
    if coding_pref.get("samples", 0) > 0:
        level = "HIGH confidence (user accepts, few bugs)" if coding_pref["value"] > 0.6 else "MODERATE" if coding_pref["value"] > 0.35 else "LOW (fix style/tests)"
        lines.append(f"- Coding: {level} (coding={int(coding_pref['value']*100)}%)")

    # Questions
    qf = prefs.get("question_frequency", {})
    if qf.get("samples", 0) > 0:
        level = "OK to ask" if qf["value"] > 0.5 else "RARELY" if qf["value"] > 0.2 else "AVOID questions"
        lines.append(f"- Questions: {level} (frequency={int(qf['value']*100)}%)")

    # Explanation style
    expl = prefs.get("explanation_style", {})
    if expl.get("samples", 0) > 0:
        level = "DETAILED explanations" if expl["value"] > 0.6 else "BRIEF explanations" if expl["value"] > 0.3 else "SKIP explanations"
        lines.append(f"- Explanations: {level} (style={int(expl['value']*100)}%)")

    lines.append(f"These override your defaults. Lonnie has taught you this through {total_samples} interactions.\n")
    result = "\n".join(lines)
    return result[:600] if len(result) > 600 else result


# ── Tool: get_dpo_insights ───────────────────────────────────────────────────
def get_dpo_insights(**kwargs) -> Dict[str, Any]:
    """Let Joi self-inspect her learned preference profile."""
    data = _load_dpo()
    prefs = data.get("preferences", {})
    signals = data.get("signal_log", [])

    summary = {}
    for dim, pref in prefs.items():
        summary[dim] = {
            "value": round(pref.get("value", 0.5), 2),
            "confidence": round(pref.get("confidence", 0.3), 2),
            "samples": pref.get("samples", 0),
        }

    recent_signals = signals[-10:] if signals else []

    return {
        "ok": True,
        "preferences": summary,
        "total_signals": len(signals),
        "recent_signals": recent_signals,
        "compile_block_preview": compile_dpo_block()[:300],
    }


# ── Register Tool ────────────────────────────────────────────────────────────
joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "get_dpo_insights",
        "description": (
            "View Joi's learned preference profile -- what she's learned about how Lonnie "
            "likes her to respond (brevity, sass, detail, etc.). Self-inspection tool."
        ),
        "parameters": {"type": "object", "properties": {}, "required": []}
    }},
    get_dpo_insights
)

print(f"  [OK] DPO preference engine loaded ({DPO_PATH.name})")
