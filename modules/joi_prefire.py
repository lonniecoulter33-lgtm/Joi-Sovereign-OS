"""joi_prefire.py — Pre-Execution Pipeline (Phase 3)

Pre-fires high-confidence tools BEFORE the first LLM call.
Eliminates one full round-trip for vision and research messages.

Old flow (2 LLM calls):
  message → [LLM call 1: decide to call tool] → tool executes → [LLM call 2: respond]

New flow (1 LLM call):
  message → classify → pre-fire tools in parallel → [LLM call 1: respond with results]

Latency savings:
  Vision queries:   ~3-5s faster (eliminates 1 LLM round-trip + tool wait)
  Research queries: ~4-6s faster (search result already in context)

Safe tools only: read-only, no side effects, idempotent.
"""

from __future__ import annotations
import time
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError as FutureTimeout
from typing import Any, Dict, List, Optional, Tuple


# ── Kwargs builders (defined BEFORE rules that reference them) ────────────────

def _screen_kwargs(msg: str) -> Dict[str, str]:
    """Pass user message as the vision question so Joi looks for what they asked."""
    return {"question": msg.strip()[:200]}


def _search_kwargs(msg: str) -> Dict[str, str]:
    """Extract a clean search query from the user message."""
    query = msg.strip()
    for prefix in ("search for", "look up", "find out about", "find", "search"):
        if query.lower().startswith(prefix):
            query = query[len(prefix):].strip()
            break
    return {"query": query[:200]}


# ── Pre-fire rule registry ───────────────────────────────────────────────────
# Each rule defines WHEN to trigger and WHAT to run.
# Rules are checked in order; multiple can fire for one message.

_PREFIRE_RULES: List[Dict[str, Any]] = [
    {
        "name": "screen_analysis",
        "tool": "analyze_screen",
        "kwargs_fn": _screen_kwargs,
        "task_types": {"vision"},
        "keywords": [
            "what's on", "what is on", "screen", "see my", "look at my",
            "what do you see", "what can you see", "show me", "monitor",
            "what am i looking at", "what's open", "my desktop",
        ],
        "timeout": 12.0,  # Vision API is slow — give it enough time
    },
    {
        "name": "web_search",
        "tool": "web_search",
        "kwargs_fn": _search_kwargs,
        "task_types": {"research", "question"},
        "keywords": [
            "search for", "look up", "find out", "latest", "current",
            "news about", "what is the", "who is", "when did", "how many",
            "right now", "today", "recently",
        ],
        "timeout": 8.0,
        "min_message_length": 10,
        "require_question_or_keyword": True,
    },
]


# ── Classification helper ────────────────────────────────────────────────────

def _classify(message: str) -> Dict[str, Any]:
    """Fast local classify — returns task_type, complexity, etc."""
    try:
        from modules.joi_router import classify_task
        return classify_task(message) or {}
    except Exception:
        return {}


def _should_fire(rule: Dict, message: str, task_type: str) -> bool:
    """Return True if a pre-fire rule should trigger for this message."""
    msg_lower = message.lower()

    # Either task type OR keyword must match
    type_match = task_type in rule.get("task_types", set())
    kw_match = any(kw in msg_lower for kw in rule.get("keywords", []))
    if not (type_match or kw_match):
        return False

    # Minimum message length guard
    if len(message.strip()) < rule.get("min_message_length", 0):
        return False

    # Require question mark or search keyword to avoid speculative searches
    if rule.get("require_question_or_keyword"):
        search_kws = rule.get("keywords", [])
        has_q = "?" in message
        has_kw = any(kw in msg_lower for kw in search_kws)
        if not (has_q or has_kw):
            return False

    return True


# ── Plan builder ─────────────────────────────────────────────────────────────

def get_prefire_plan(message: str) -> List[Dict[str, Any]]:
    """
    Determine which tools to pre-fire for this message.
    Returns a list of action dicts ready for execute_prefire_plan().
    """
    if not message or not message.strip():
        return []

    classification = _classify(message)
    task_type = classification.get("task_type", "conversation")

    plan = []
    fired_tools: set = set()

    for rule in _PREFIRE_RULES:
        if rule["tool"] in fired_tools:
            continue
        if _should_fire(rule, message, task_type):
            kwargs = {}
            fn = rule.get("kwargs_fn")
            if callable(fn):
                try:
                    kwargs = fn(message)
                except Exception:
                    kwargs = {}
            plan.append({
                "name": rule["name"],
                "tool": rule["tool"],
                "kwargs": kwargs,
                "timeout": rule.get("timeout", 5.0),
            })
            fired_tools.add(rule["tool"])

    # Mutual exclusion: screen_analysis and web_search serve different intents.
    # If the user is asking about THEIR SCREEN, don't also do a web search.
    has_screen = any(a["tool"] == "analyze_screen" for a in plan)
    has_search = any(a["tool"] == "web_search" for a in plan)
    if has_screen and has_search:
        plan = [a for a in plan if a["tool"] != "web_search"]

    return plan


# ── Executor ─────────────────────────────────────────────────────────────────

def execute_prefire_plan(
    plan: List[Dict[str, Any]],
    tool_executors: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Execute pre-fire tools in parallel with per-tool timeouts.
    Returns dict of {tool_name: result_dict}.
    """
    if not plan:
        return {}

    results: Dict[str, Any] = {}
    max_wait = max(a["timeout"] for a in plan) + 2

    def _run_one(action: Dict) -> Tuple[str, Any]:
        tool_name = action["tool"]
        executor = tool_executors.get(tool_name)
        if executor is None:
            return tool_name, {"ok": False, "error": f"tool '{tool_name}' not registered"}
        try:
            return tool_name, executor(**action["kwargs"])
        except Exception as exc:
            return tool_name, {"ok": False, "error": str(exc)}

    with ThreadPoolExecutor(max_workers=len(plan)) as pool:
        future_map = {pool.submit(_run_one, action): action for action in plan}
        for fut in as_completed(future_map, timeout=max_wait):
            action = future_map[fut]
            try:
                tool_name, result = fut.result(timeout=action["timeout"])
                results[tool_name] = result
            except FutureTimeout:
                results[action["tool"]] = {
                    "ok": False,
                    "error": f"timeout after {action['timeout']}s",
                }
            except Exception as exc:
                results[action["tool"]] = {"ok": False, "error": str(exc)}

    return results


# ── Context block compiler ────────────────────────────────────────────────────

def compile_prefire_block(results: Dict[str, Any]) -> str:
    """
    Format pre-fire results as a system prompt injection block.
    Only includes successful results — failures silently skipped.
    Returns empty string if nothing useful ran.
    """
    if not results:
        return ""

    successful = {}
    for tool_name, result in results.items():
        if not isinstance(result, dict):
            continue
        if result.get("ok", False):
            content = (
                result.get("description")
                or result.get("result")
                or result.get("text")
                or result.get("content")
                or result.get("answer")
                or result.get("output")
            )
            if content:
                successful[tool_name] = str(content)[:800]

    if not successful:
        return ""

    lines = ["\n[PRE-EXECUTED — results ready, use directly in your response]:"]
    for tool_name, content in successful.items():
        lines.append(f"  [{tool_name}]: {content}")
    lines.append(
        "IMPORTANT: These tools already ran. Do NOT call them again. "
        "Respond using the results above — no additional tool calls needed."
    )
    lines.append("")

    return "\n".join(lines)


# ── Top-level convenience ─────────────────────────────────────────────────────

def prefire_and_compile(message: str, tool_executors: Dict[str, Any]) -> str:
    """
    Full pipeline: classify → plan → execute in parallel → compile.
    Returns the formatted context block (empty string if nothing fired).
    Called from joi_companion.py context assembly.
    """
    if not message or not message.strip():
        return ""

    plan = get_prefire_plan(message)
    if not plan:
        return ""

    t0 = time.monotonic()
    results = execute_prefire_plan(plan, tool_executors)
    elapsed = time.monotonic() - t0

    successes = [k for k, v in results.items() if isinstance(v, dict) and v.get("ok")]
    all_fired = list(results.keys())
    if all_fired:
        print(f"  [PREFIRE] {all_fired} | ok={successes} | {elapsed:.1f}s")

    return compile_prefire_block(results)


print("    [OK] joi_prefire (Pre-execution pipeline: screen_analysis + web_search)")
