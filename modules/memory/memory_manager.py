"""
Memory Manager
==============
Decides what gets saved, manages backends, exposes tools + routes.

Visible verification:
  A) /memory/status  -- backend, model, count, last write
  B) /memory/test    -- write + read test with on-screen result
  C) /memory/feed    -- last 20 saved items
  D) /memory/policy  -- GET/POST save policy
  E) Terminal log    -- MEMORY_WRITE ok/fail on every write
"""

import os
import sys
import json
import hashlib
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from dataclasses import asdict

from modules.memory.vector_store_base import (
    VectorStoreBase, MemoryChunk, QueryResult, StoreStats,
)

# ── Configuration ────────────────────────────────────────────────────────
VECTOR_BACKEND = os.getenv("VECTOR_BACKEND", "chroma").strip().lower()
EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "openai").strip().lower()
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small").strip()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
POLICY_PATH = BASE_DIR / "data" / "memory_policy.json"
POLICY_PATH.parent.mkdir(parents=True, exist_ok=True)

# ── Memory write feed (in-memory ring buffer for UI) ─────────────────────
_write_feed: List[Dict[str, Any]] = []
_MAX_FEED = 50


def _feed_append(entry: Dict[str, Any]):
    _write_feed.append(entry)
    if len(_write_feed) > _MAX_FEED:
        _write_feed.pop(0)


# ── Save Policy ──────────────────────────────────────────────────────────
_DEFAULT_POLICY = {
    "save_facts": True,
    "save_decisions": True,
    "save_summaries": True,
    "save_messages": False,   # off by default -- high volume
}


def load_policy() -> Dict[str, bool]:
    if POLICY_PATH.exists():
        try:
            return json.loads(POLICY_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    return dict(_DEFAULT_POLICY)


def save_policy(policy: Dict[str, bool]):
    merged = dict(_DEFAULT_POLICY)
    merged.update(policy)
    POLICY_PATH.write_text(json.dumps(merged, indent=2), encoding="utf-8")


# ── Backend Factory ──────────────────────────────────────────────────────
_store: Optional[VectorStoreBase] = None
_fallback_warning: Optional[str] = None


def _create_store() -> VectorStoreBase:
    """Create the configured vector store. Falls back to Chroma on failure."""
    global _fallback_warning

    if VECTOR_BACKEND == "pinecone":
        try:
            from modules.memory.vector_pinecone import PineconeVectorStore
            store = PineconeVectorStore()
            if store.healthcheck():
                print("  [MEMORY] Using Pinecone backend")
                return store
            _fallback_warning = "Pinecone configured but unreachable -- falling back to Chroma"
            print(f"  [MEMORY] WARNING: {_fallback_warning}")
        except Exception as e:
            _fallback_warning = f"Pinecone init failed ({e}) -- falling back to Chroma"
            print(f"  [MEMORY] WARNING: {_fallback_warning}")

    # Default / fallback: Chroma
    try:
        from modules.memory.vector_chroma import ChromaVectorStore
        store = ChromaVectorStore()
        print("  [MEMORY] Using Chroma backend")
        return store
    except Exception as e:
        print(f"  [MEMORY] CRITICAL: Chroma also failed: {e}")
        raise


def get_store() -> VectorStoreBase:
    """Lazy singleton for the vector store."""
    global _store
    if _store is None:
        _store = _create_store()
    return _store


# ── Memory ID Generator ──────────────────────────────────────────────────
def _make_id(text: str, prefix: str = "mem") -> str:
    h = hashlib.md5(text.encode("utf-8")).hexdigest()[:12]
    ts = int(time.time())
    return f"{prefix}_{ts}_{h}"


# ── Public API: Save Memory ──────────────────────────────────────────────
def save_memory(
    text: str,
    memory_type: str = "general",
    metadata: Optional[Dict[str, Any]] = None,
    force: bool = False,
    namespace: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Save a piece of text to vector memory.

    Args:
        text: The content to remember
        memory_type: "fact", "decision", "summary", "message", "general"
        metadata: Extra metadata dict
        force: Bypass policy check
        namespace: Optional namespace tag (e.g. "user:lonnie_profile")
    """
    # Policy gate
    if not force:
        policy = load_policy()
        type_key = f"save_{memory_type}s" if not memory_type.endswith("s") else f"save_{memory_type}"
        # Normalize: "fact" -> "save_facts", "message" -> "save_messages"
        policy_key = f"save_{memory_type}s"
        if policy_key in policy and not policy[policy_key]:
            return {"ok": False, "reason": f"Policy blocks saving '{memory_type}'"}
        if memory_type == "general" and not policy.get("save_facts", True):
            return {"ok": False, "reason": "Policy blocks saving general memories"}

    store = get_store()
    mid = _make_id(text, memory_type[:4])
    meta = {
        "type": memory_type,
        "timestamp": datetime.now().isoformat(),
        "source": "joi",
    }
    if namespace:
        meta["namespace"] = namespace
    if metadata:
        meta.update(metadata)

    chunk = MemoryChunk(id=mid, text=text, metadata=meta)
    ok = store.upsert([chunk])

    feed_entry = {
        "id": mid,
        "type": memory_type,
        "preview": text[:120],
        "backend": store.stats().backend,
        "ok": ok,
        "timestamp": meta["timestamp"],
    }
    _feed_append(feed_entry)

    if ok:
        return {"ok": True, "id": mid, "backend": store.stats().backend}
    return {"ok": False, "id": mid, "error": store.stats().last_error}


# ── Public API: Query Memory ─────────────────────────────────────────────
def recall_memory(
    query: str,
    top_k: int = 5,
    memory_type: Optional[str] = None,
    namespace: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Semantic search across stored memories.

    Returns list of {id, text, score, metadata}.
    """
    store = get_store()
    filters = None
    if memory_type:
        filters = {"type": memory_type}
    if namespace:
        filters = filters or {}
        filters["namespace"] = namespace
    results = store.query(query, top_k=top_k, filters=filters)
    return [
        {"id": r.id, "text": r.text, "score": round(r.score, 3), "metadata": r.metadata}
        for r in results
    ]


# ── Memory Context result (acts as str + carries metadata) ────────────────
class MemoryContextResult(str):
    """String subclass that also carries memory metadata for the response."""
    def __new__(cls, text: str, metadata: Optional[Dict[str, Any]] = None):
        obj = super().__new__(cls, text)
        obj.memory_metadata = metadata or {"count": 0, "items": []}
        return obj


# ── Public API: Compile Memory Context for /chat ─────────────────────────
def compile_memory_context(user_message: str, max_chars: int = 2000) -> "MemoryContextResult":
    """
    Query vector memory for relevant context to inject into system prompt.
    Returns a MemoryContextResult (acts as str, also has .memory_metadata).

    Enhanced: top_k=8, threshold=0.25, temporal boost (24h=1.3x, week=1.1x).
    Deprioritizes self-referential exchange memories during work tasks.
    """
    empty = MemoryContextResult("", {"count": 0, "items": []})
    if not user_message or not user_message.strip():
        return empty
    try:
        results = recall_memory(user_message, top_k=8)
        if not results:
            return empty
        # Filter by minimum relevance (increased from 0.25 to 0.45 to reduce context bloat)
        relevant = [r for r in results if r["score"] > 0.45]
        if not relevant:
            return empty

        # Deprioritize self-referential memories during work tasks
        # When the user is asking about external topics (books, projects, docs),
        # exchange summaries about building Joi are noise that causes conflation.
        try:
            _is_work = False
            try:
                from modules.joi_router import classify_task
                _tt = classify_task(user_message).get("task_type", "conversation")
                _is_work = _tt in ("research", "writing", "code_edit", "code_review",
                                    "orchestration", "architecture", "math")
            except Exception:
                pass

            if _is_work:
                _self_keywords = {"joi", "my system", "my code", "my module", "building me",
                                  "my evolution", "autobiography", "my journal", "soul architecture"}
                _msg_lower = user_message.lower()
                _msg_mentions_self = any(kw in _msg_lower for kw in _self_keywords)

                if not _msg_mentions_self:
                    for r in relevant:
                        text_lower = r.get("text", "").lower()
                        subtype = r.get("metadata", {}).get("subtype", "")
                        is_exchange = subtype == "exchange" or text_lower.startswith("[exchange]")
                        is_self_ref = is_exchange and any(kw in text_lower for kw in _self_keywords)
                        if is_self_ref:
                            r["score"] = round(r["score"] * 0.3, 3)  # heavily deprioritize
        except Exception:
            pass

        # Temporal boost: recent memories get score multiplier
        now = time.time()
        day_ago = now - 86400       # 24 hours
        week_ago = now - 604800     # 7 days

        for r in relevant:
            ts_str = r.get("metadata", {}).get("timestamp", "")
            try:
                from datetime import datetime as _dt
                mem_ts = _dt.fromisoformat(ts_str).timestamp() if ts_str else 0
            except (ValueError, TypeError):
                mem_ts = 0

            if mem_ts > day_ago:
                r["score"] = round(r["score"] * 1.3, 3)
            elif mem_ts > week_ago:
                r["score"] = round(r["score"] * 1.1, 3)

        # Re-sort after temporal boosting (highest score first)
        relevant.sort(key=lambda x: x["score"], reverse=True)

        lines = ["\n[LONG-TERM MEMORY -- relevant past context:]"]
        total = 0
        meta_items = []
        for r in relevant:
            entry = f"  [{r['metadata'].get('type', '?')}] {r['text']}"
            if total + len(entry) > max_chars:
                break
            lines.append(entry[:300])
            total += len(entry)
            meta_items.append({
                "id": r["id"],
                "type": r["metadata"].get("type", "?"),
                "score": r["score"],
            })
        lines.append("[Use these memories naturally -- don't list them back to Lonnie.]\n")
        text = "\n".join(lines)
        return MemoryContextResult(text, {"count": len(meta_items), "items": meta_items})
    except Exception as e:
        print(f"  [MEMORY] compile_memory_context error: {e}")
        return empty


# ── Public API: Auto-extract memories from conversation ───────────────────
def auto_extract(user_message: str, joi_reply: str):
    """
    After each conversation turn, extract saveable memories.
    Runs in background -- never blocks chat.

    Strategy: ALWAYS save a condensed exchange summary so Joi never loses
    context across sessions. Additionally, extract facts/decisions/topics
    when keyword signals are detected.
    """
    import threading

    def _extract():
      try:
        policy = load_policy()
        msg_lower = user_message.lower().strip()

        # Skip trivial messages (very short greetings, empty, system messages)
        trivial = len(user_message.strip()) < 5 or msg_lower in (
            "hi", "hey", "ok", "yes", "no", "k", "yep", "nah", "sure", "ty",
        )

        # ── ALWAYS save a conversation exchange summary ──────────────
        # This is the core fix: every non-trivial turn gets remembered
        if not trivial and policy.get("save_summaries", True):
            user_part = user_message[:200]
            joi_part = joi_reply[:200]
            if len(user_message) > 200:
                user_part = user_message[:200].rsplit(" ", 1)[0]
            if len(joi_reply) > 200:
                joi_part = joi_reply[:200].rsplit(" ", 1)[0]
            save_memory(
                f"[exchange] Lonnie: {user_part} | Joi: {joi_part}",
                memory_type="summary",
                metadata={"source": "auto_extract", "subtype": "exchange"},
                force=True,
            )

        # ── Save facts: statements about preferences, important info ──
        if not trivial and policy.get("save_facts", True):
            fact_signals = [
                "my favorite", "i like", "i prefer", "i hate", "i love",
                "i always", "i never", "my name is", "i work", "i live",
                "remember that", "don't forget", "important:",
                "my ", "i am ", "i'm ", "i was ", "i have ", "i've ",
                "i need", "i want", "i feel", "i think",
            ]
            if any(sig in msg_lower for sig in fact_signals):
                save_memory(
                    f"Lonnie said: {user_message[:300]}",
                    memory_type="fact",
                    metadata={"source": "auto_extract"},
                    force=True,
                )

        # ── Save decisions: when Lonnie makes a choice ──────────────
        if not trivial and policy.get("save_decisions", True):
            decision_signals = [
                "let's go with", "i decided", "i'll use", "i chose",
                "we should", "i want to", "the plan is",
                "let's do", "go ahead", "make it", "change it",
                "fix ", "add ", "remove ", "update ", "can you",
            ]
            if any(sig in msg_lower for sig in decision_signals):
                save_memory(
                    f"Decision: {user_message[:300]}",
                    memory_type="decision",
                    metadata={"source": "auto_extract"},
                    force=True,
                )

        # ── Topic-linking: detect ongoing projects/goals/plans ──────
        if not trivial and policy.get("save_summaries", True):
            topic_signals = [
                "project", "working on", "building", "planning",
                "goal", "idea", "started", "creating", "designing",
                "feature", "module", "bug", "issue", "problem",
                "implement", "deploy", "test", "debug", "refactor",
            ]
            if any(sig in msg_lower for sig in topic_signals):
                topic_text = user_message[:250]
                if len(user_message) > 250:
                    topic_text = user_message[:250].rsplit(" ", 1)[0]
                save_memory(
                    f"Topic/project: {topic_text}",
                    memory_type="summary",
                    metadata={"source": "auto_extract", "subtype": "topic"},
                    force=True,
                )

        # ── Save all messages (disabled by default -- high volume) ───
        if policy.get("save_messages", False):
            save_memory(
                f"[user] {user_message}\n[joi] {joi_reply[:200]}",
                memory_type="message",
                metadata={"source": "auto_extract"},
                force=True,
            )
      except Exception as e:
        print(f"  [ERROR] auto_extract background thread failed: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

    threading.Thread(target=_extract, daemon=True).start()


# ── Flask Routes ─────────────────────────────────────────────────────────
def _register_routes():
    """Register memory routes with Joi's Flask app."""
    import joi_companion
    from flask import jsonify, request as flask_req
    from modules.joi_memory import require_user

    def memory_status_route():
        require_user()
        store = get_store()
        s = store.stats()
        result = asdict(s)
        if _fallback_warning:
            result["fallback_warning"] = _fallback_warning
        return jsonify({"ok": True, **result})

    def memory_test_route():
        """Write a test memory, immediately query it, return pass/fail."""
        require_user()
        ts = int(time.time())
        test_text = f"Memory test: bananas-{ts}"
        test_id = f"test_{ts}"

        store = get_store()
        chunk = MemoryChunk(
            id=test_id,
            text=test_text,
            metadata={"type": "test", "timestamp": datetime.now().isoformat()},
        )
        write_ok = store.upsert([chunk])
        if not write_ok:
            return jsonify({
                "ok": False,
                "write": False,
                "error": store.stats().last_error,
            })

        # Brief pause for index consistency
        time.sleep(0.3)

        results = store.query("bananas", top_k=3)
        found = any(test_text in r.text for r in results)

        # Cleanup
        store.delete(ids=[test_id])

        return jsonify({
            "ok": True,
            "write": True,
            "read": found,
            "test_text": test_text,
            "query_results": [
                {"id": r.id, "text": r.text, "score": round(r.score, 3)}
                for r in results[:3]
            ],
        })

    def memory_feed_route():
        require_user()
        return jsonify({"ok": True, "feed": list(reversed(_write_feed[-20:]))})

    def memory_policy_route():
        require_user()
        if flask_req.method == "GET":
            return jsonify({"ok": True, "policy": load_policy()})
        data = flask_req.get_json(force=True) or {}
        policy = load_policy()
        for k in _DEFAULT_POLICY:
            if k in data:
                policy[k] = bool(data[k])
        save_policy(policy)
        return jsonify({"ok": True, "policy": policy})

    def memory_query_route():
        require_user()
        data = flask_req.get_json(force=True) or {}
        query = data.get("query", "")
        if not query:
            return jsonify({"ok": False, "error": "No query"}), 400
        top_k = int(data.get("top_k", 5))
        results = recall_memory(query, top_k=top_k)
        return jsonify({"ok": True, "results": results})

    # Register all routes
    joi_companion.register_route("/memory/status", ["GET"], memory_status_route, "memory_status")
    joi_companion.register_route("/memory/test", ["POST"], memory_test_route, "memory_test")
    joi_companion.register_route("/memory/feed", ["GET"], memory_feed_route, "memory_feed")
    joi_companion.register_route("/memory/policy", ["GET", "POST"], memory_policy_route, "memory_policy")
    joi_companion.register_route("/memory/query", ["POST"], memory_query_route, "memory_query")


# ── Tool Registration ────────────────────────────────────────────────────
def _register_tools():
    """Register Joi's memory tools."""
    import joi_companion

    def remember(**params):
        """Tool: Save something important to long-term memory."""
        text = params.get("text", "")
        memory_type = params.get("type", "fact")
        namespace = params.get("namespace")
        if not text:
            return {"ok": False, "error": "Nothing to remember"}
        return save_memory(text, memory_type=memory_type, namespace=namespace)

    def recall(**params):
        """Tool: Search long-term memory for relevant past context."""
        query = params.get("query", "")
        if not query:
            return {"ok": False, "error": "No query"}
        top_k = int(params.get("top_k", 5))
        namespace = params.get("namespace")
        results = recall_memory(query, top_k=top_k, namespace=namespace)
        return {"ok": True, "results": results, "count": len(results)}

    joi_companion.register_tool(
        {"type": "function", "function": {
            "name": "remember",
            "description": (
                "Save something important to long-term vector memory. "
                "Use for: facts about Lonnie, decisions, preferences, important events. "
                "These memories persist forever and can be recalled semantically."
            ),
            "parameters": {"type": "object", "properties": {
                "text": {"type": "string", "description": "What to remember"},
                "type": {
                    "type": "string",
                    "enum": ["fact", "decision", "summary", "general"],
                    "description": "Category of memory",
                },
                "namespace": {
                    "type": "string",
                    "description": "Optional namespace tag (e.g. 'user:lonnie_profile', 'project:joi')",
                },
            }, "required": ["text"]},
        }},
        remember,
    )

    joi_companion.register_tool(
        {"type": "function", "function": {
            "name": "recall",
            "description": (
                "Search long-term memory for relevant past information. "
                "Use when Lonnie references something from the past, or when you need "
                "context about his preferences, past decisions, or shared history."
            ),
            "parameters": {"type": "object", "properties": {
                "query": {"type": "string", "description": "What to search for"},
                "top_k": {"type": "integer", "description": "Max results (default 5)"},
                "namespace": {"type": "string", "description": "Optional namespace filter"},
            }, "required": ["query"]},
        }},
        recall,
    )


# ── Module Init ──────────────────────────────────────────────────────────
def init():
    """Called by the module loader to set up memory system."""
    try:
        get_store()  # Initialize backend
    except Exception as e:
        print(f"  [FAIL] Memory Manager -- backend init failed: {e}")
        return

    try:
        _register_routes()
        _register_tools()
        print("  [OK] Memory Manager -- vector memory active")
    except Exception as e:
        # Routes/tools need Flask + joi_companion -- OK if not available yet
        print(f"  [OK] Memory Manager -- backend active (routes/tools deferred: {e})")
