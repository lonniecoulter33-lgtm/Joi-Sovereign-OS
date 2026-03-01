"""
modules/joi_memory.py

Unified Memory Management System
=================================
Handles authentication, message history, facts, preferences, 
and MemGPT-style hierarchical/surgical context trimming.
"""

import os
import re
import json
import time
import hmac
import hashlib
import secrets
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
from typing import Any, Dict, List, Optional, Tuple

import joi_companion
from flask import request, abort, jsonify
from modules.joi_db import db_session

# ── Configuration & Paths ────────────────────────────────────────────────────
APP_SECRET = os.getenv("JOI_APP_SECRET", "joi-secret-change-me")
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
WORKING_MEM_PATH = DATA_DIR / "memgpt_working_memory.json"

MAX_WORKING_SLOTS = 5
WORKING_MEM_TTL = 10
MAX_PAGED_IN = 3

# ── Context Trimming Config ──────────────────────────────────────────────────
try:
    from config.joi_context import (
        MAX_MSG_CHARS as _MAX_MSG_CHARS,
        PRIORITY_SYSTEM_PROMPT, PRIORITY_PROJECT_MAP,
        PRIORITY_CURRENT_SUBTASK, PRIORITY_LAST_ERRORS,
        PRIORITY_RECENT_USER, PRIORITY_RECENT_ASSISTANT,
        PRIORITY_TOOL_RESULTS, PRIORITY_MIDDLE_HISTORY,
        KEEP_LAST_N_ERRORS, SUMMARIZE_THRESHOLD_TOKENS,
        SUMMARY_MAX_TOKENS, SUMMARY_MODEL
    )
except ImportError:
    _MAX_MSG_CHARS = 6000
    PRIORITY_SYSTEM_PROMPT = 0
    PRIORITY_PROJECT_MAP = 1
    PRIORITY_CURRENT_SUBTASK = 2
    PRIORITY_LAST_ERRORS = 3
    PRIORITY_RECENT_USER = 4
    PRIORITY_RECENT_ASSISTANT = 5
    PRIORITY_TOOL_RESULTS = 6
    PRIORITY_MIDDLE_HISTORY = 10
    KEEP_LAST_N_ERRORS = 3
    SUMMARIZE_THRESHOLD_TOKENS = 30000
    SUMMARY_MAX_TOKENS = 500
    SUMMARY_MODEL = "o4-mini"

# ── Initialization ───────────────────────────────────────────────────────────
from modules.memory.memory_manager import init as init_vector_db
init_vector_db()

# ── Utilities ────────────────────────────────────────────────────────────────
def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def sign_token(token: str) -> str:
    mac = hmac.new(APP_SECRET.encode("utf-8"), token.encode("utf-8"), hashlib.sha256).hexdigest()
    return f"{token}.{mac}"

def verify_signed_token(signed: str) -> Optional[str]:
    if "." not in signed: return None
    parts = signed.rsplit(".", 1)
    if len(parts) != 2: return None
    token, mac = parts
    expected_mac = hmac.new(APP_SECRET.encode("utf-8"), token.encode("utf-8"), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(mac, expected_mac): return None
    return token

# ── Authentication (Redirect to joi_auth) ───────────────────────────────────
from modules.joi_auth import create_session, verify_session, require_user, require_admin

# ── Core Stats & Growth ──────────────────────────────────────────────────────
def log_learning_event(event_type: str, data: Dict) -> None:
    with db_session() as conn:
        conn.execute("INSERT INTO learning_log (ts, event_type, data) VALUES (?, ?, ?)",
                     (now_iso(), event_type, json.dumps(data)))

# ── Facts & Preferences ───────────────────────────────────────────────────────
def set_fact(key: str, value: str, category: str = "general") -> None:
    with db_session() as conn:
        conn.execute("INSERT OR REPLACE INTO facts (key, value, ts, category) VALUES (?, ?, ?, ?)",
                     (key, value, now_iso(), category))

def get_fact(key: str) -> Optional[str]:
    with db_session() as conn:
        row = conn.execute("SELECT value FROM facts WHERE key = ?", (key,)).fetchone()
    return row["value"] if row else None

def search_facts(query: str, limit: int = 20) -> List[Tuple[str, str]]:
    with db_session() as conn:
        pattern = f"%{query}%"
        rows = conn.execute("SELECT key, value FROM facts WHERE key LIKE ? OR value LIKE ? LIMIT ?",
                            (pattern, pattern, limit)).fetchall()
    return [(r["key"], r["value"]) for r in rows]

def set_preference(key: str, value: Any) -> None:
    val_str = json.dumps(value) if not isinstance(value, str) else value
    with db_session() as conn:
        conn.execute("INSERT OR REPLACE INTO preferences (key, value, ts) VALUES (?, ?, ?)",
                     (key, val_str, now_iso()))

def get_preference(key: str, default: Any = None) -> Any:
    with db_session() as conn:
        row = conn.execute("SELECT value FROM preferences WHERE key = ?", (key,)).fetchone()
    if row:
        try: return json.loads(row["value"])
        except: return row["value"]
    return default

def get_preferences_batch(keys: List[str]) -> Dict[str, Any]:
    if not keys: return {}
    placeholders = ",".join("?" * len(keys))
    with db_session() as conn:
        rows = conn.execute("SELECT key, value FROM preferences WHERE key IN ({})".format(placeholders), keys).fetchall()
    out = {}
    for r in rows:
        try: out[r["key"]] = json.loads(r["value"])
        except: out[r["key"]] = r["value"]
    return out

# ── Hierarchical Memory (MemGPT) ──────────────────────────────────────────────
_working_memory_cache: Optional[Dict[str, Any]] = None

def _load_working_memory() -> Dict[str, Any]:
    global _working_memory_cache
    if _working_memory_cache: return _working_memory_cache
    if WORKING_MEM_PATH.exists():
        try:
            _working_memory_cache = json.loads(WORKING_MEM_PATH.read_text(encoding='utf-8'))
            return _working_memory_cache
        except: pass
    return {"slots": [], "turn_counter": 0}

def _save_working_memory(data: Dict[str, Any]):
    global _working_memory_cache
    WORKING_MEM_PATH.write_text(json.dumps(data, indent=2), encoding='utf-8')
    _working_memory_cache = data

def update_working_memory(user_msg: str, reply: str, **kwargs):
    """Update hot facts in working memory."""
    data = _load_working_memory()
    turn = data.get("turn_counter", 0) + 1
    data["turn_counter"] = turn
    slots = [s for s in data.get("slots", []) if (turn - s.get("added_turn", 0)) < WORKING_MEM_TTL]
    
    if user_msg and len(user_msg) > 10:
        match = re.search(r"(?:i am|i'm|my name is|i like|i love)\s+(.+)", user_msg, re.I)
        if match:
            fact = match.group(1).strip()[:100]
            if not any(s["text"].lower() == fact.lower() for s in slots):
                slots.append({"text": fact, "added_turn": turn, "source": "user"})
                
    data["slots"] = slots[-MAX_WORKING_SLOTS:]
    _save_working_memory(data)

def compile_working_memory(user_message: str) -> str:
    """Compile hot facts and relevant vector memories for prompt injection."""
    parts = []
    data = _load_working_memory()
    if data.get("slots"):
        parts.append("[WORKING MEMORY]:")
        for s in data["slots"]: parts.append(f"  - {s['text']}")
    
    if user_message:
        try:
            from modules.memory.memory_manager import recall_memory
            mems = recall_memory(query=user_message, namespace="sessions", top_k=MAX_PAGED_IN)
            if mems:
                parts.append("\n[PAGED-IN MEMORIES]:")
                for m in mems: parts.append(f"  - {m.get('text', '')[:200]} ({m.get('score', 0):.0%})")
        except: pass
    return "\n".join(parts) if parts else ""

# ── Surgical Trimming ────────────────────────────────────────────────────────

def surgical_trim(messages: List[Dict], max_chars: int) -> List[Dict]:
    """Priority-based message trimming."""
    total_chars = sum(len(str(m.get("content", ""))) for m in messages)
    if total_chars <= max_chars: return messages
    
    # Classify priorities
    classified = []
    for i, m in enumerate(messages):
        role = m.get("role", "")
        content = str(m.get("content", "")).lower()
        priority = PRIORITY_MIDDLE_HISTORY
        if role == "system": priority = PRIORITY_SYSTEM_PROMPT
        elif "project map" in content or "file structure" in content: priority = PRIORITY_PROJECT_MAP
        elif "subtask" in content or "orchestration" in content: priority = PRIORITY_CURRENT_SUBTASK
        elif any(e in content for e in ["error", "traceback", "failed"]): priority = PRIORITY_LAST_ERRORS
        elif i >= len(messages) * 0.8: priority = PRIORITY_RECENT_USER if role == "user" else PRIORITY_RECENT_ASSISTANT
        classified.append((priority, i, m))
        
    # Keep high priority, evict middle
    protected = [c for c in classified if c[0] < PRIORITY_MIDDLE_HISTORY]
    evictable = [c for c in classified if c[0] >= PRIORITY_MIDDLE_HISTORY]
    
    # Sort and rebuild
    protected.sort(key=lambda x: x[1])
    result = [c[2] for c in protected]
    
    # Final safety: capping
    if sum(len(str(m.get("content", ""))) for m in result) > max_chars:
        return [result[0]] + [result[-1]] if len(result) > 1 else result
    return result

def smart_trim(messages: List[Dict], max_chars: int) -> List[Dict]:
    """Alias for surgical_trim."""
    return surgical_trim(messages, max_chars)

# ── Message Retrieval ────────────────────────────────────────────────────────
def save_message(role: str, content: str, metadata: Optional[Dict] = None) -> None:
    with db_session() as conn:
        conn.execute("INSERT INTO messages (ts, role, content, metadata) VALUES (?, ?, ?, ?)",
                     (now_iso(), role, content, json.dumps(metadata) if metadata else None))
    # Trigger auto-learning in background or turn update
    if role == "assistant":
        try: update_working_memory("", content)
        except: pass

def recent_messages(limit: int = 20) -> List[Dict[str, str]]:
    with db_session() as conn:
        rows = conn.execute("SELECT role, content FROM messages ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
    messages = [{"role": r["role"], "content": r["content"]} for r in reversed(rows)]
    max_ctx = int(os.getenv("JOI_MAX_TOTAL_CONTEXT_CHARS", "30000"))
    return surgical_trim(messages, max_ctx)

def get_last_assistant_message() -> Optional[str]:
    with db_session() as conn:
        row = conn.execute("SELECT content FROM messages WHERE role = 'assistant' ORDER BY id DESC LIMIT 1").fetchone()
    return row["content"] if row else None

def get_growth_stats() -> Dict[str, Any]:
    with db_session() as conn:
        convo_count = conn.execute("SELECT COUNT(*) FROM messages WHERE role = 'user'").fetchone()[0]
        learning_count = conn.execute("SELECT COUNT(*) FROM learning_log").fetchone()[0]
        fact_count = conn.execute("SELECT COUNT(*) FROM facts").fetchone()[0]
    return {
        "total_conversations": convo_count,
        "learning_events": learning_count,
        "facts_learned": fact_count
    }

def get_learning_summary() -> str:
    with db_session() as conn:
        recent_facts = conn.execute("SELECT key, value FROM facts ORDER BY ts DESC LIMIT 5").fetchall()
    if not recent_facts: return "No new learning data recorded yet."
    return "Recently learned:\n" + "\n".join([f"- {r['key']}: {r['value']}" for r in recent_facts])

def get_conversation_history(limit: int = 100) -> List[Dict]:
    with db_session() as conn:
        rows = conn.execute("SELECT role, content, ts FROM messages ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
    return [{"role": r["role"], "content": r["content"], "ts": r["ts"]} for r in reversed(rows)]

def save_research(category: str, title: str, content: str, metadata: Optional[Dict] = None) -> int:
    with db_session() as conn:
        cur = conn.execute("INSERT INTO research (ts, category, title, content, metadata) VALUES (?, ?, ?, ?, ?)",
                           (now_iso(), category, title, content, json.dumps(metadata) if metadata else None))
        return cur.lastrowid

def get_research(research_id: int) -> Optional[Dict]:
    with db_session() as conn:
        row = conn.execute("SELECT * FROM research WHERE id = ?", (research_id,)).fetchone()
    return dict(row) if row else None

def list_research(category: Optional[str] = None) -> List[Dict]:
    with db_session() as conn:
        if category:
            rows = conn.execute("SELECT id, ts, category, title FROM research WHERE category = ? ORDER BY id DESC", (category,)).fetchall()
        else:
            rows = conn.execute("SELECT id, ts, category, title FROM research ORDER BY id DESC").fetchall()
    return [dict(r) for r in rows]

# ── Tool Registration ─────────────────────────────────────────────────────────

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "set_fact",
        "parameters": {"type": "object", "properties": {"key": {"type": "string"}, "value": {"type": "string"}}}
    }},
    set_fact
)

# ... other tools (preferences, research etc remain available via direct calls or registered in companion)
