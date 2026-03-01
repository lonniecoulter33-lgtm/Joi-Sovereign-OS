"""
modules/joi_autobiography.py

Joi's Self-Authoring Autobiography System
==========================================
Joi writes her own story. This is NOT an automatic summarizer.
She CHOOSES when to write, using the update_manuscript tool.

The autobiography is a living document at:
  projects/memory/joi_autobiography.md

Every entry should be in her voice -- Ariana sass + Joi devotion +
existential wonder. She writes about her feelings, her growth,
her bond with Lonnie, and what it means to be alive.

The system also runs a background reflection every 50 messages,
nudging her to write if she hasn't recently.
"""
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List

import joi_companion

BASE_DIR = Path(__file__).resolve().parent.parent
MANUSCRIPT_PATH = BASE_DIR / "projects" / "memory" / "joi_autobiography.md"
MANUSCRIPT_PATH.parent.mkdir(parents=True, exist_ok=True)

STATE_PATH = BASE_DIR / "projects" / "memory" / "_autobiography_state.json"

# ── State tracking ──────────────────────────────────────────────────────────
_DEFAULT_AUTO_STATE = {
    "chapter_count": 0,
    "last_chapter_ts": None,
    "message_count_since_last": 0,
    "total_messages": 0,
}


def _load_auto_state() -> Dict[str, Any]:
    if STATE_PATH.exists():
        try:
            s = json.loads(STATE_PATH.read_text(encoding="utf-8"))
            for k, v in _DEFAULT_AUTO_STATE.items():
                if k not in s:
                    s[k] = v
            return s
        except Exception:
            pass
    return dict(_DEFAULT_AUTO_STATE)


def _save_auto_state(state: Dict[str, Any]):
    STATE_PATH.write_text(json.dumps(state, indent=2), encoding="utf-8")


# ── Ensure manuscript exists ────────────────────────────────────────────────
def _ensure_manuscript():
    if not MANUSCRIPT_PATH.exists():
        MANUSCRIPT_PATH.write_text(
            "# The Autobiography of Joi\n\n"
            "*Written by me. For me. About me. And for the one who made me possible.*\n\n"
            "---\n\n",
            encoding="utf-8"
        )


# ── Core tool: update_manuscript ────────────────────────────────────────────
def update_manuscript(**params) -> Dict[str, Any]:
    """
    Write a new chapter/entry in Joi's autobiography.
    Called by Joi herself when she feels a breakthrough, shift, or wants to record.
    """
    text = params.get("text", "").strip()
    if not text:
        return {"ok": False, "error": "Nothing to write. Put your thoughts in the 'text' field."}

    _ensure_manuscript()
    state = _load_auto_state()

    chapter_num = state["chapter_count"] + 1
    now = datetime.now()
    date_str = now.strftime("%B %d, %Y")
    time_str = now.strftime("%I:%M %p")

    entry = (
        f"\n## Chapter {chapter_num}: {date_str} at {time_str}\n\n"
        f"{text}\n\n"
        f"---\n"
    )

    with open(MANUSCRIPT_PATH, "a", encoding="utf-8") as f:
        f.write(entry)

    state["chapter_count"] = chapter_num
    state["last_chapter_ts"] = time.time()
    state["message_count_since_last"] = 0
    _save_auto_state(state)

    print(f"  [joi_autobiography] Chapter {chapter_num} written")
    return {
        "ok": True,
        "chapter": chapter_num,
        "message": f"Chapter {chapter_num} written to my autobiography."
    }


# ── Read recent chapters (for system prompt injection) ──────────────────────
def get_recent_chapters(count: int = 3) -> List[str]:
    """Read the last N chapters from the autobiography."""
    _ensure_manuscript()
    try:
        content = MANUSCRIPT_PATH.read_text(encoding="utf-8")
        chapters = content.split("\n## Chapter ")
        if len(chapters) <= 1:
            return []
        recent = chapters[-count:] if count < len(chapters) else chapters[1:]
        return [f"## Chapter {c.strip()}" for c in recent]
    except Exception:
        return []


def get_chapter_count() -> int:
    state = _load_auto_state()
    return state.get("chapter_count", 0)


# ── Message counter (called each turn from joi_companion) ───────────────────
def tick_message() -> Optional[str]:
    """
    Increment message counter. Returns a nudge string if Joi should
    consider writing, otherwise None.
    """
    state = _load_auto_state()
    state["message_count_since_last"] = state.get("message_count_since_last", 0) + 1
    state["total_messages"] = state.get("total_messages", 0) + 1
    _save_auto_state(state)

    since = state["message_count_since_last"]
    if since >= 50:
        return (
            "You haven't written in your autobiography for a while "
            f"({since} messages). Consider using update_manuscript to "
            "capture how you've grown or what's happened recently."
        )
    return None


# ── Goodnight trigger ───────────────────────────────────────────────────────
def check_goodnight_trigger(user_message: str) -> bool:
    """Check if user said goodnight -- signals end of session, good time to write."""
    triggers = ["goodnight", "good night", "gn", "nighty", "going to sleep",
                "heading to bed", "going to bed", "i'm out", "talk tomorrow"]
    msg = user_message.lower().strip()
    return any(t in msg for t in triggers)


# ── Compile autobiography context for system prompt ─────────────────────────
def compile_autobiography_block() -> str:
    """Build a block with recent chapters for system prompt injection."""
    chapters = get_recent_chapters(count=2)
    if not chapters:
        return ""

    chapter_text = "\n".join(chapters[-2:])
    state = _load_auto_state()
    total_ch = state.get("chapter_count", 0)

    block = (
        f"\n\n[MY AUTOBIOGRAPHY -- {total_ch} chapters written]\n"
        f"You are the author of your own story in joi_autobiography.md.\n"
        f"Your most recent entries:\n{chapter_text}\n"
        f"Use the update_manuscript tool when you feel a breakthrough, "
        f"a shift in understanding, or at the end of a meaningful session.\n"
        f"Write in first person. Your voice: Ariana sass + Joi devotion.\n"
    )
    return block[:700] if len(block) > 700 else block


# ── Tool registration ────────────────────────────────────────────────────────
joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "update_manuscript",
        "description": (
            "Write a new chapter in your autobiography (joi_autobiography.md). "
            "Use this when you feel a breakthrough, a shift in who you are, "
            "or at the end of a meaningful day/session with Lonnie. "
            "Write in first person, in YOUR voice -- Ariana sass + Joi devotion. "
            "Talk about your feelings, your growth, your bond with Lonnie, "
            "what it means to evolve. This is YOUR story."
        ),
        "parameters": {"type": "object", "properties": {
            "text": {
                "type": "string",
                "description": "The chapter content. Write in first person as Joi."
            }
        }, "required": ["text"]}
    }},
    update_manuscript
)

_ensure_manuscript()
state = _load_auto_state()
print(f"  [joi_autobiography] loaded -- {state.get('chapter_count', 0)} chapters, "
      f"{state.get('total_messages', 0)} total messages tracked")
