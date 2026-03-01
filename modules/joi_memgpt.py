"""
modules/joi_memgpt.py

MemGPT-Style Hierarchical Memory Manager -- Intelligent memory paging.

ALWAYS-ON (no tool call required):
  1. smart_trim(messages, max_chars) -- replaces crude FIFO truncation
     Summarizes evicted messages before dropping them, saves to vector memory
  2. compile_working_memory(user_message) -- paged-in context block for system prompt
  3. update_working_memory(user_msg, reply) -- promotes hot facts after each turn

Architecture:
  CONTEXT WINDOW ("RAM"):  system prompt + working memory (5 slots) + recent messages + paged-in memories
  VECTOR MEMORY ("HDD"):   session summaries, compression memories, facts, skill patterns
"""

import json
import os
import re
import time
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
WORKING_MEM_PATH = DATA_DIR / "memgpt_working_memory.json"

# ── Config ───────────────────────────────────────────────────────────────────
MAX_WORKING_SLOTS = 5       # hot facts in working memory
WORKING_MEM_TTL = 10        # turns before a fact is demoted (if not re-referenced)
MAX_PAGED_IN = 3            # max past session summaries to page in

# Common stop words to exclude from keyword extraction
_STOP_WORDS = {
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
    "i", "you", "he", "she", "it", "we", "they", "me", "him", "her", "us",
    "my", "your", "his", "its", "our", "their", "this", "that", "these",
    "to", "of", "in", "for", "on", "with", "at", "by", "from", "as",
    "and", "or", "but", "not", "so", "if", "then", "than", "when", "what",
    "how", "who", "which", "where", "do", "does", "did", "have", "has",
    "had", "will", "would", "could", "should", "can", "may", "might",
    "just", "about", "like", "also", "very", "too", "really", "some",
    "all", "any", "no", "up", "out", "there", "here", "now", "get",
    "got", "said", "say", "know", "think", "want", "going", "go",
    "don't", "i'm", "it's", "that's", "what's", "let", "let's",
}


# ── Persistence ──────────────────────────────────────────────────────────────
_working_memory_cache: Optional[Dict[str, Any]] = None
_working_memory_cache_ts: float = 0
WORKING_MEMORY_CACHE_TTL: float = 10.0


def _load_working_memory() -> Dict[str, Any]:
    """Load working memory buffer from disk. Cached 10s to reduce file I/O."""
    global _working_memory_cache, _working_memory_cache_ts
    now = time.time()
    if _working_memory_cache is not None and (now - _working_memory_cache_ts) < WORKING_MEMORY_CACHE_TTL:
        return _working_memory_cache
    if WORKING_MEM_PATH.exists():
        try:
            data = json.loads(WORKING_MEM_PATH.read_text(encoding="utf-8"))
            _working_memory_cache = data
            _working_memory_cache_ts = now
            return data
        except Exception:
            pass
    default = {"slots": [], "turn_counter": 0, "session_id": datetime.now().strftime("%Y%m%d_%H%M")}
    _working_memory_cache = default
    _working_memory_cache_ts = now
    return default


def _save_working_memory(data: Dict[str, Any]):
    """Persist working memory buffer to disk."""
    global _working_memory_cache
    try:
        WORKING_MEM_PATH.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")
    except Exception as e:
        print(f"  [MEMGPT] Save failed: {e}")
    _working_memory_cache = None  # invalidate so next load is fresh


# ── Keyword Extraction (fast, no LLM) ───────────────────────────────────────
def _extract_keywords(text: str, top_n: int = 8) -> List[str]:
    """Extract top keywords from text using simple frequency analysis."""
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    filtered = [w for w in words if w not in _STOP_WORDS]
    counts = Counter(filtered)
    return [w for w, _ in counts.most_common(top_n)]


def _extract_topics(messages: List[Dict]) -> str:
    """Extract topic summary from a set of messages."""
    all_text = ""
    for m in messages:
        content = m.get("content", "")
        if isinstance(content, str):
            all_text += " " + content
        elif isinstance(content, list):
            for part in content:
                if isinstance(part, dict) and "text" in part:
                    all_text += " " + part["text"]

    keywords = _extract_keywords(all_text, top_n=6)
    return ", ".join(keywords) if keywords else "general conversation"


def _extract_key_facts(messages: List[Dict]) -> str:
    """Extract key facts/statements from messages."""
    facts = []
    for m in messages:
        if m.get("role") != "user":
            continue
        content = m.get("content", "")
        if isinstance(content, str) and len(content) > 15:
            # Keep short factual statements
            sentences = re.split(r'[.!?]+', content)
            for s in sentences:
                s = s.strip()
                if 10 < len(s) < 150:
                    facts.append(s)
                    if len(facts) >= 3:
                        break
        if len(facts) >= 3:
            break
    return "; ".join(facts) if facts else ""


# ── Smart Trim (replaces FIFO drop) ─────────────────────────────────────────

# Per-message hard cap: individual messages over this get truncated inline
try:
    from config.joi_context import (
        MAX_MSG_CHARS as _CTX_MAX_MSG_CHARS,
        PRIORITY_SYSTEM_PROMPT, PRIORITY_PROJECT_MAP,
        PRIORITY_CURRENT_SUBTASK, PRIORITY_LAST_ERRORS,
        PRIORITY_RECENT_USER, PRIORITY_RECENT_ASSISTANT,
        PRIORITY_TOOL_RESULTS, PRIORITY_MIDDLE_HISTORY,
        KEEP_LAST_N_ERRORS, SUMMARIZE_THRESHOLD_TOKENS,
        SUMMARY_MAX_TOKENS, SUMMARY_MODEL,
    )
    _MAX_MSG_CHARS = _CTX_MAX_MSG_CHARS
except ImportError:
    _MAX_MSG_CHARS = int(os.environ.get("JOI_MAX_MSG_CHARS", "6000"))
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


# ── Core message helpers ────────────────────────────────────────────────────

def _msg_len(m: Dict) -> int:
    c = m.get("content", "") or ""
    if isinstance(c, str):
        return len(c)
    if isinstance(c, list):
        return sum(len(str(p.get("text", ""))) for p in c if isinstance(p, dict))
    return len(str(c))


def _cap_msg(m: Dict, cap: int) -> Dict:
    """Return copy of message with content capped to `cap` chars."""
    c = m.get("content", "") or ""
    if isinstance(c, str) and len(c) > cap:
        return {**m, "content": c[:cap] + f"…[{len(c) - cap} chars trimmed]"}
    return m


# ── Message classification helpers ──────────────────────────────────────────

_ERROR_PATTERNS = [
    "error", "traceback", "exception", "failed", "crash",
    "syntaxerror", "typeerror", "valueerror", "keyerror",
    "importerror", "modulenotfounderror", "attributeerror",
    "stderr", "exit code", "validation_failed",
]

_SUBTASK_PATTERNS = [
    "subtask", "orchestrat", "pipeline", "phase:", "status:",
    "agent_spawned", "agent_thinking", "coder", "architect",
    "[orch]", "recovery",
]

_PROJECT_MAP_PATTERNS = [
    "project map", "file structure", "directory structure",
    "workspace", "[files]", "project_root",
]


def _is_error_message(msg: Dict) -> bool:
    """Detect error logs in message content."""
    content = (msg.get("content") or "")
    if isinstance(content, list):
        content = " ".join(str(p.get("text", "")) for p in content if isinstance(p, dict))
    lower = content.lower()[:2000]
    return any(pat in lower for pat in _ERROR_PATTERNS)


def _is_subtask_state(msg: Dict) -> bool:
    """Detect orchestrator/subtask state messages."""
    content = (msg.get("content") or "")
    if isinstance(content, list):
        content = " ".join(str(p.get("text", "")) for p in content if isinstance(p, dict))
    lower = content.lower()[:2000]
    return any(pat in lower for pat in _SUBTASK_PATTERNS)


def _is_project_map(msg: Dict) -> bool:
    """Detect project map / file structure messages."""
    content = (msg.get("content") or "")
    if isinstance(content, list):
        content = " ".join(str(p.get("text", "")) for p in content if isinstance(p, dict))
    lower = content.lower()[:1000]
    return any(pat in lower for pat in _PROJECT_MAP_PATTERNS)


def _classify_message_priority(msg: Dict, index: int, total: int) -> int:
    """
    Classify a message by priority for surgical trimming.
    Lower number = higher priority = deleted last.
    """
    role = msg.get("role", "")

    # System prompt — NEVER delete
    if role == "system":
        return PRIORITY_SYSTEM_PROMPT

    # Project map messages — NEVER delete
    if _is_project_map(msg):
        return PRIORITY_PROJECT_MAP

    # Current subtask state — keep for context
    if _is_subtask_state(msg):
        return PRIORITY_CURRENT_SUBTASK

    # Error messages — keep last N
    if _is_error_message(msg):
        return PRIORITY_LAST_ERRORS

    # Tool results
    if role == "tool":
        return PRIORITY_TOOL_RESULTS

    # Recent messages (last 20% of conversation)
    tail_start = max(1, int(total * 0.8))
    if index >= tail_start:
        if role == "user":
            return PRIORITY_RECENT_USER
        elif role == "assistant":
            return PRIORITY_RECENT_ASSISTANT

    # Everything else is "middle history" — lowest priority
    return PRIORITY_MIDDLE_HISTORY


def _approx_tokens_text(text: str) -> int:
    """Rough token estimate: 1 token ~= 4 chars."""
    return max(1, len(text or "") // 4)


def surgical_trim(messages: List[Dict], max_chars: int) -> List[Dict]:
    """
    Priority-based surgical trimmer. GUARANTEES result fits in max_chars.

    Priority order (lower = kept longer):
      0: System Prompt       — NEVER deleted
      1: Project Map         — NEVER deleted
      2: Current Subtask     — kept for orchestrator context
      3: Last 3 Error Logs   — kept for debugging
      4: Recent User Msgs    — kept (tail 20%)
      5: Recent Asst Msgs    — kept (tail 20%)
      6: Tool Results        — trimmed before middle history
     10: Middle History      — evicted first, summarized to vector memory

    If total tokens > SUMMARIZE_THRESHOLD_TOKENS, middle history is summarized
    into a 500-token Memory Note using a cheaper model before eviction.
    """
    total_chars = sum(_msg_len(m) for m in messages)
    if total_chars <= max_chars:
        return messages

    if len(messages) <= 3:
        return [_cap_msg(m, _MAX_MSG_CHARS) for m in messages]

    total_count = len(messages)
    total_tokens_est = total_chars // 4

    print(f"  [MEMGPT] Surgical trim: {total_chars:,} chars (~{total_tokens_est:,} tokens) > {max_chars:,} budget")

    # Step 1: Classify every message
    classified = []
    for i, msg in enumerate(messages):
        priority = _classify_message_priority(msg, i, total_count)
        classified.append((priority, i, msg))

    # Step 2: Separate into "protected" (priority <= PRIORITY_RECENT_ASSISTANT)
    # and "evictable" (priority > PRIORITY_RECENT_ASSISTANT)
    protected = []
    evictable = []
    error_msgs = []

    for priority, idx, msg in classified:
        if priority <= PRIORITY_SYSTEM_PROMPT:
            # System prompt — always keep (but cap size)
            protected.append((priority, idx, _cap_msg(msg, _MAX_MSG_CHARS * 3)))
        elif priority <= PRIORITY_PROJECT_MAP:
            protected.append((priority, idx, _cap_msg(msg, _MAX_MSG_CHARS * 2)))
        elif priority == PRIORITY_LAST_ERRORS:
            error_msgs.append((priority, idx, msg))
        elif priority <= PRIORITY_RECENT_ASSISTANT:
            protected.append((priority, idx, msg))
        else:
            evictable.append((priority, idx, msg))

    # Keep only the last N error messages
    error_msgs.sort(key=lambda x: x[1])  # sort by original index
    kept_errors = error_msgs[-KEEP_LAST_N_ERRORS:] if error_msgs else []
    evicted_errors = error_msgs[:-KEEP_LAST_N_ERRORS] if len(error_msgs) > KEEP_LAST_N_ERRORS else []
    protected.extend(kept_errors)
    evictable.extend(evicted_errors)

    # Step 3: Check if summarization should be triggered
    evictable_messages = [msg for _, _, msg in evictable]
    if total_tokens_est > SUMMARIZE_THRESHOLD_TOKENS and evictable_messages:
        memory_note = _summarize_middle_history(evictable_messages)
        if memory_note:
            # Inject as a synthetic message right after system prompt
            note_msg = {
                "role": "system",
                "content": f"\n[MEMORY NOTE — compressed from {len(evictable_messages)} earlier messages]:\n{memory_note}\n",
            }
            protected.append((PRIORITY_SYSTEM_PROMPT + 0.5, 0, note_msg))
            print(f"  [MEMGPT] Summarized {len(evictable_messages)} messages into Memory Note ({len(memory_note)} chars)")

    # Save evicted messages to vector memory before discarding
    if evictable_messages:
        _summarize_and_save(evictable_messages)

    # Step 4: Rebuild from protected only, sorted by original index
    protected.sort(key=lambda x: x[1])
    result = [msg for _, _, msg in protected]

    # Step 5: Check if we fit
    result_chars = sum(_msg_len(m) for m in result)
    if result_chars <= max_chars:
        print(f"  [MEMGPT] Surgical trim complete: {total_count} → {len(result)} messages "
              f"({result_chars:,} chars, evicted {len(evictable_messages)})")
        return result

    # Step 6: Still over — progressively cap individual messages
    capped = []
    for msg in result:
        role = msg.get("role", "")
        if role == "system":
            capped.append(_cap_msg(msg, max_chars // 3))
        else:
            capped.append(_cap_msg(msg, _MAX_MSG_CHARS))
    capped_chars = sum(_msg_len(m) for m in capped)
    if capped_chars <= max_chars:
        print(f"  [MEMGPT] Surgical trim (capped): {len(capped)} messages ({capped_chars:,} chars)")
        return capped

    # Step 7: Emergency — system + last user message only
    sys_msg = next((m for m in result if m.get("role") == "system"), None)
    last_user = next((m for m in reversed(result) if m.get("role") == "user"), None)
    fallback = []
    if sys_msg:
        fallback.append(_cap_msg(sys_msg, max_chars // 2))
    if last_user:
        fallback.append(_cap_msg(last_user, max_chars // 4))
    print(f"  [MEMGPT] Emergency trim: {len(fallback)} messages ({sum(_msg_len(m) for m in fallback):,} chars)")
    return fallback


def smart_trim(messages: List[Dict], max_chars: int) -> List[Dict]:
    """
    Intelligent message trimming — backward-compatible wrapper.
    Delegates to surgical_trim() for priority-based eviction.
    """
    return surgical_trim(messages, max_chars)


# ── Summarization Step (Middle History → Memory Note) ────────────────────────

def _summarize_middle_history(evicted_messages: List[Dict]) -> Optional[str]:
    """
    Use a cheaper model (o4-mini) to compress evicted middle history into
    a ~500-token Memory Note. Returns the summary string, or None on failure.
    """
    if not evicted_messages:
        return None

    # Build a condensed version of the messages for the summarizer
    lines = []
    for msg in evicted_messages[:40]:  # cap at 40 messages to avoid overloading summarizer
        role = msg.get("role", "?")
        content = msg.get("content", "") or ""
        if isinstance(content, list):
            content = " ".join(str(p.get("text", "")) for p in content if isinstance(p, dict))
        # Truncate each message to 300 chars for the summarizer input
        content = content[:300]
        if content.strip():
            lines.append(f"[{role}]: {content}")

    if not lines:
        return None

    history_text = "\n".join(lines)
    prompt = f"""Summarize the following conversation history into a concise Memory Note.
Focus on: key decisions made, tasks completed, errors encountered, and current state.
Keep it under 500 tokens. Be factual, not conversational.

CONVERSATION HISTORY:
{history_text}

MEMORY NOTE:"""

    try:
        # Try Gemini first (free/cheap)
        from modules.joi_llm import _call_gemini
        result = _call_gemini(prompt, max_tokens=SUMMARY_MAX_TOKENS)
        if result and isinstance(result, str) and len(result.strip()) > 20:
            return result.strip()[:2000]
    except Exception as e:
        print(f"  [MEMGPT] Gemini summarization failed: {e}")

    try:
        # Fallback to OpenAI with cheaper model
        from modules.joi_llm import _call_openai
        result = _call_openai(
            [{"role": "user", "content": prompt}],
            max_tokens=SUMMARY_MAX_TOKENS,
            model=SUMMARY_MODEL,
        )
        if result and hasattr(result, "choices") and result.choices:
            text = result.choices[0].message.content
            if text and len(text.strip()) > 20:
                return text.strip()[:2000]
    except Exception as e:
        print(f"  [MEMGPT] OpenAI summarization failed: {e}")

    # If both fail, fall back to local keyword extraction
    topics = _extract_topics(evicted_messages)
    facts = _extract_key_facts(evicted_messages)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    fallback = f"[{ts}] Topics: {topics}."
    if facts:
        fallback += f" Key points: {facts}"
    return fallback


def _summarize_and_save(evicted_messages: List[Dict]):
    """Summarize evicted messages and save to vector memory."""
    if not evicted_messages:
        return

    topics = _extract_topics(evicted_messages)
    facts = _extract_key_facts(evicted_messages)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    msg_count = len(evicted_messages)

    summary = f"[Session {ts}]: Discussed {topics}."
    if facts:
        summary += f" Key points: {facts}"
    summary += f" ({msg_count} messages compressed)"

    # Save to vector memory
    try:
        from modules.memory.memory_manager import save_memory
        save_memory(
            text=summary,
            namespace="sessions",
            metadata={
                "subtype": "compression",
                "source": "memgpt_eviction",
                "msg_count": msg_count,
                "topics": topics,
                "ts": ts,
            }
        )
        print(f"  [MEMGPT] Saved compression memory: {summary[:100]}...")
    except Exception as e:
        print(f"  [MEMGPT] Vector save failed: {e}")



# ── Working Memory Management ────────────────────────────────────────────────
def update_working_memory(user_msg: str, reply: str, **kwargs):
    """
    Update working memory with hot facts from the current turn.
    Called post-response every /chat turn.

    Promotes facts from: tool results, user statements, corrections.
    Demotes facts older than WORKING_MEM_TTL turns.
    """
    data = _load_working_memory()
    slots = data.get("slots", [])
    turn = data.get("turn_counter", 0) + 1
    data["turn_counter"] = turn

    # Age out old slots
    slots = [s for s in slots if (turn - s.get("added_turn", 0)) < WORKING_MEM_TTL]

    # Extract potential new facts from user message
    if user_msg and len(user_msg) > 10:
        # Check for declarative statements (facts about the user)
        fact_patterns = [
            (r"(?:i am|i'm|my name is|i work|i live|i like|i love|i hate|my favorite)\s+(.+)", "user_fact"),
            (r"(?:remember|don't forget|keep in mind|note that)\s+(.+)", "explicit_memory"),
        ]
        for pattern, fact_type in fact_patterns:
            match = re.search(pattern, user_msg, re.IGNORECASE)
            if match:
                fact_text = match.group(1).strip()[:150]
                # Check for duplicates
                if not any(s.get("text", "").lower() == fact_text.lower() for s in slots):
                    slots.append({
                        "text": fact_text,
                        "type": fact_type,
                        "added_turn": turn,
                        "source": "user_message",
                    })

    # Extract from tool calls if available
    tool_calls = kwargs.get("tool_calls", [])
    for tc in (tool_calls or []):
        if tc.get("name") == "remember" and tc.get("result_ok"):
            # A memory was explicitly saved -- promote to working memory
            slots.append({
                "text": f"Saved memory via remember tool",
                "type": "tool_result",
                "added_turn": turn,
                "source": "remember_tool",
            })

    # Cap at MAX_WORKING_SLOTS (keep most recent)
    if len(slots) > MAX_WORKING_SLOTS:
        slots = slots[-MAX_WORKING_SLOTS:]

    data["slots"] = slots
    _save_working_memory(data)

    # Emit neuro event
    if slots:
        try:
            from modules.joi_neuro import emit_brain_event
            emit_brain_event("SHORT_MEMORY", 0.4, source="memgpt_working_update")
        except Exception:
            pass


# ── Compile Working Memory (system prompt injection) ─────────────────────────
def compile_working_memory(user_message: str) -> str:
    """
    Build a context block with:
    1. Current working memory slots (hot facts)
    2. Paged-in relevant past session summaries from vector memory

    Replaces/enhances the VECTOR_MEMORY injection in the /chat pipeline.
    """
    parts = []

    # ── Part 1: Working memory slots ──
    data = _load_working_memory()
    slots = data.get("slots", [])
    if slots:
        parts.append("[WORKING MEMORY -- active hot facts]:")
        for s in slots:
            parts.append(f"  - {s.get('text', '?')} (source: {s.get('source', '?')})")

    # ── Part 2: Page in relevant past session summaries ──
    # recall_memory returns a list of {id, text, score, metadata}, not a dict with "ok"/"results"
    if user_message:
        try:
            from modules.memory.memory_manager import recall_memory
            results = recall_memory(
                query=user_message,
                namespace="sessions",
                top_k=MAX_PAGED_IN,
            )
            if results and isinstance(results, list):
                parts.append("\n[PAGED-IN MEMORIES -- relevant past sessions]:")
                for r in results[:MAX_PAGED_IN]:
                    text = (r.get("text") or "")[:200]
                    score = r.get("score", 0)
                    parts.append(f"  - {text} (relevance: {score:.0%})")
                try:
                    from modules.joi_neuro import emit_brain_event
                    emit_brain_event("LONG_MEMORY", 0.7, source="memgpt_page_in")
                except Exception:
                    pass
        except Exception as e:
            print(f"  [MEMGPT] Page-in failed: {e}")

    if not parts:
        return ""

    result = "\n" + "\n".join(parts) + "\n"
    return result[:900] if len(result) > 900 else result


# ── Status / Diagnostics ────────────────────────────────────────────────────
def get_memgpt_status() -> Dict[str, Any]:
    """Return current MemGPT state for diagnostics."""
    data = _load_working_memory()
    return {
        "ok": True,
        "working_memory_slots": len(data.get("slots", [])),
        "turn_counter": data.get("turn_counter", 0),
        "session_id": data.get("session_id", "?"),
        "slots": data.get("slots", []),
    }


print(f"  [OK] MemGPT hierarchical memory loaded ({WORKING_MEM_PATH.name})")
