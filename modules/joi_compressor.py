"""
Semantic Compression (Memory Tiering)
=====================================
When the message DB exceeds a threshold, summarize the oldest messages into a
single "Memory Block," store it in working memory, and archive the raw messages.
Reduces context clutter and keeps signal-to-noise high as the DB grows.
"""

from __future__ import annotations

import json
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

BASE_DIR = Path(__file__).resolve().parent.parent

# Thresholds
COMPRESSION_MESSAGE_THRESHOLD = 50
COMPRESSION_BATCH_SIZE = 40
COMPRESSION_COOLDOWN_SEC = 60  # Don't run again within this period
_last_compression_ts: float = 0


def _get_message_count() -> int:
    """Return total number of messages in the messages table."""
    from modules.joi_db import db_connect
    conn = db_connect()
    row = conn.execute("SELECT COUNT(*) as c FROM messages").fetchone()
    conn.close()
    return row["c"] if row else 0


def _fetch_oldest_messages(limit: int) -> List[Dict[str, Any]]:
    """Fetch the oldest N messages (by id)."""
    from modules.joi_db import db_connect
    conn = db_connect()
    rows = conn.execute(
        "SELECT id, ts, role, content, metadata FROM messages ORDER BY id ASC LIMIT ?",
        (limit,),
    ).fetchall()
    conn.close()
    return [
        {"id": r["id"], "ts": r["ts"], "role": r["role"], "content": r["content"], "metadata": r["metadata"]}
        for r in rows
    ]


def _summarize_with_fast_llm(messages: List[Dict[str, Any]]) -> Optional[str]:
    """Use a fast-tier LLM (gpt-4o-mini or Gemini Flash) to summarize the conversation batch."""
    if not messages:
        return None
    # Build a plain transcript
    lines = []
    for m in messages:
        role = m.get("role", "?")
        content = m.get("content", "")
        if isinstance(content, list):
            content = " ".join(p.get("text", "") for p in content if isinstance(p, dict))
        content = (content or "")[:800]
        lines.append(f"{role}: {content}")
    transcript = "\n".join(lines)
    if len(transcript) > 12000:
        transcript = transcript[:12000] + "\n... (truncated)"

    prompt = """Summarize this conversation segment in one short block. Include:
1. Key takeaways (decisions, facts, preferences mentioned)
2. Any unresolved tasks or open questions
3. Tone/topic in one line

Keep the summary under 400 words. Use clear bullets or short paragraphs."""

    try:
        from modules.joi_llm import _call_openai, OPENAI_TOOL_MODEL
        llm_messages = [
            {"role": "system", "content": "You are a concise summarizer. Output only the summary, no preamble."},
            {"role": "user", "content": f"{prompt}\n\n---\n{transcript}"},
        ]
        resp = _call_openai(llm_messages, tools=None, max_tokens=600, model=OPENAI_TOOL_MODEL)
        if resp and resp.choices and resp.choices[0].message.content:
            return resp.choices[0].message.content.strip()
    except Exception as e:
        print(f"  [COMPRESSOR] Fast LLM summarize failed: {e}")
    # Fallback: minimal extract
    user_lines = [m["content"][:200] for m in messages if m.get("role") == "user" and m.get("content")]
    return "Previous conversation (summary unavailable): " + "; ".join(user_lines[:5]) if user_lines else None


def _add_compression_slot_to_working_memory(summary: str, message_count: int) -> None:
    """Add the compression block as a slot in MemGPT working memory."""
    try:
        from modules.joi_memory import _load_working_memory, _save_working_memory
        data = _load_working_memory()
        slots = data.get("slots", [])
        turn = data.get("turn_counter", 0)
        slots.append({
            "text": f"[Compressed context] {summary[:1500]}",
            "type": "compression",
            "source": "joi_compressor",
            "added_turn": turn,
            "message_count": message_count,
            "created_at": datetime.now().isoformat(),
        })
        # Cap slots; keep recent compressions
        from modules.joi_memory import MAX_WORKING_SLOTS
        if len(slots) > MAX_WORKING_SLOTS:
            slots = slots[-MAX_WORKING_SLOTS:]
        data["slots"] = slots
        _save_working_memory(data)
    except Exception as e:
        print(f"  [COMPRESSOR] Working memory add failed: {e}")


def _archive_messages_and_delete(messages: List[Dict], block_id: str) -> None:
    """Move messages to message_archive and delete from messages."""
    from modules.joi_db import db_connect
    if not messages:
        return
    ids = [m["id"] for m in messages]
    conn = db_connect()
    try:
        for m in messages:
            conn.execute(
                """INSERT INTO message_archive (ts, role, content, metadata, compression_block_id)
                   VALUES (?, ?, ?, ?, ?)""",
                (m["ts"], m["role"], m["content"], m.get("metadata"), block_id),
            )
        placeholders = ",".join("?" * len(ids))
        conn.execute(f"DELETE FROM messages WHERE id IN ({placeholders})", ids)
        conn.commit()
    finally:
        conn.close()


def run_compression_if_needed() -> Dict[str, Any]:
    """
    If message count exceeds COMPRESSION_MESSAGE_THRESHOLD, summarize the oldest
    batch, add to working memory, and archive raw messages.
    Returns a result dict for logging.
    """
    global _last_compression_ts
    now = time.time()
    if now - _last_compression_ts < COMPRESSION_COOLDOWN_SEC:
        return {"ok": False, "reason": "cooldown"}

    count = _get_message_count()
    if count < COMPRESSION_MESSAGE_THRESHOLD:
        return {"ok": False, "reason": "below_threshold", "count": count}

    batch_size = min(COMPRESSION_BATCH_SIZE, count - 10)
    if batch_size < 5:
        return {"ok": False, "reason": "batch_too_small", "count": count}

    oldest = _fetch_oldest_messages(batch_size)
    if not oldest:
        return {"ok": False, "reason": "no_messages"}

    summary = _summarize_with_fast_llm(oldest)
    if not summary:
        return {"ok": False, "reason": "summarize_failed"}

    block_id = f"block_{int(now)}"
    _add_compression_slot_to_working_memory(summary, len(oldest))
    _archive_messages_and_delete(oldest, block_id)
    _last_compression_ts = now

    print(f"  [COMPRESSOR] Compressed {len(oldest)} messages -> block {block_id}")
    return {"ok": True, "archived": len(oldest), "block_id": block_id, "summary_length": len(summary)}


def run_compression_in_background() -> None:
    """Run compression in a daemon thread so the request path is not blocked."""
    def _run():
        try:
            run_compression_if_needed()
        except Exception as e:
            print(f"  [COMPRESSOR] Background run failed: {e}")

    t = threading.Thread(target=_run, name="joi_compressor", daemon=True)
    t.start()
