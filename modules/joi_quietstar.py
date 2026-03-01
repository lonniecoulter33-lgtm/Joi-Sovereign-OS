"""
modules/joi_quietstar.py

Quiet-STaR -- Self-Taught Reasoner. Auto-reasons before responding.

ALWAYS-ON for medium/high complexity tasks:
  1. generate_rationale(user_msg, classification, messages) -- pre-reasoning
  2. inject_reasoning(messages, rationale) -- adds hidden reasoning to context
  3. post_evaluate(reply, user_msg, classification) -- scores response quality

For LOW complexity: skips entirely (zero latency cost).
For MEDIUM: uses template rationale (instant, no API call).
For HIGH: uses Gemini Flash for deeper rationale (<500 tokens, fast).
"""

import json
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
REASONING_LOG = BASE_DIR / "projects" / "memory" / "reasoning_log.json"

# ── Reasoning Templates (instant, 0ms latency) ──────────────────────────────
REASONING_TEMPLATES = {
    "code_edit": (
        "Consider: What file is being discussed? What function needs changing? "
        "What's the current behavior vs desired behavior? What could break? "
        "Check for side effects before suggesting a fix."
    ),
    "code": (
        "Consider: What language/framework? What's the actual problem? "
        "Is this a syntax issue, logic error, or architecture question? "
        "What's the simplest correct solution?"
    ),
    "research": (
        "Consider: What does Lonnie actually need to know? What are the key facts? "
        "What might be wrong or outdated? Cross-reference with stored memories."
    ),
    "memory": (
        "Consider: What context from past conversations is relevant here? "
        "Any stored facts that apply? Check recall before answering."
    ),
    "conversation": (
        "Consider: What's Lonnie's mood right now? What tone fits best? "
        "Keep it brief unless he asked for detail. Match his energy."
    ),
    "architecture": (
        "Consider: What are the constraints? What patterns already exist in the codebase? "
        "What are the tradeoffs between approaches? Think about maintainability."
    ),
    "writing": (
        "Consider: What style does Lonnie want? What audience? "
        "How long should this be? What's the emotional tone?"
    ),
    "tool_use": (
        "Consider: Which tool(s) are needed? In what order? "
        "What parameters does each need? What if the tool fails?"
    ),
    "file_ops": (
        "Consider: What file path? Does it exist? Read before writing. "
        "What format? Will this overwrite anything important?"
    ),
    "vision": (
        "Consider: What am I looking at? What's changed since last observation? "
        "What's Lonnie actively doing? Is there anything I should comment on?"
    ),
}

# Map task_type from router classification to template keys
TASK_TYPE_MAP = {
    "code_edit": "code_edit",
    "code_question": "code",
    "code_generation": "code",
    "research": "research",
    "memory_query": "memory",
    "memory_save": "memory",
    "conversation": "conversation",
    "greeting": "conversation",
    "architecture": "architecture",
    "writing": "writing",
    "creative": "writing",
    "tool_use": "tool_use",
    "file_operation": "file_ops",
    "vision": "vision",
    "desktop_action": "tool_use",
    "web_search": "research",
}


# ── Generate Rationale ──────────────────────────────────────────────────────
def generate_rationale(
    user_msg: str,
    classification: Dict[str, Any],
    messages: Optional[List[Dict]] = None,
    use_deep: bool = True,
) -> str:
    """
    Generate a pre-response rationale based on task complexity.

    - low complexity: return "" (skip, zero latency)
    - medium complexity: use template rationale (instant)
    - high complexity: use_deep=True -> Gemini Flash; use_deep=False -> template only (latency toggle)
    """
    complexity = classification.get("complexity", "low")

    if complexity == "low":
        print(f"  [QUIETSTAR] Complexity is LOW, skipping rationale.")
        return ""

    task_type = classification.get("task_type", "conversation")
    template_key = TASK_TYPE_MAP.get(task_type, "conversation")
    template = REASONING_TEMPLATES.get(template_key, REASONING_TEMPLATES["conversation"])

    # For medium: template only (instant)
    if complexity == "medium":
        rationale = f"{template}\nUser's message: \"{user_msg[:200]}\""
        _log_rationale(user_msg, rationale, "template", task_type, complexity)
        return rationale

    # For high: use_deep -> Gemini Flash; else template only (Intelligence vs. Latency)
    if complexity == "high":
        if use_deep:
            rationale = _deep_rationale(user_msg, template, task_type)
            _log_rationale(user_msg, rationale, "deep" if "Consider:" not in rationale[:20] else "template", task_type, complexity)
            try:
                from modules.joi_neuro import emit_brain_event
                emit_brain_event("REASONING", 0.8, source="quietstar_rationale")
            except Exception:
                pass
        else:
            rationale = f"{template}\nUser's message: \"{user_msg[:200]}\""
            _log_rationale(user_msg, rationale, "template", task_type, complexity)
        return rationale

    return ""


def _deep_rationale(user_msg: str, template: str, task_type: str) -> str:
    """
    Use Gemini Flash for a fast, short reasoning pass.
    Falls back to template if Gemini unavailable.
    """
    try:
        from modules.joi_llm import _call_gemini, HAVE_GEMINI
        if not HAVE_GEMINI:
            return template + f"\nUser's message: \"{user_msg[:200]}\""

        prompt = (
            f"You are an internal reasoning engine. Think about what to consider before answering this user message.\n"
            f"Task type: {task_type}\n"
            f"User message: \"{user_msg[:300]}\"\n\n"
            f"Generate 3-5 brief considerations (one line each). "
            f"Focus on what's important to get right. Be concise -- under 100 words total."
        )

        start = time.time()
        result = _call_gemini(prompt, max_tokens=200)
        elapsed = int((time.time() - start) * 1000)

        if result:
            print(f"  [QUIETSTAR] Deep rationale generated ({elapsed}ms)")
            return result
        else:
            return template + f"\nUser's message: \"{user_msg[:200]}\""
    except Exception as e:
        print(f"  [QUIETSTAR] Deep rationale failed: {e}")
        return template + f"\nUser's message: \"{user_msg[:200]}\""


# ── Inject Reasoning into Messages ──────────────────────────────────────────
def inject_reasoning(messages: List[Dict], rationale: str) -> List[Dict]:
    """
    Inject the rationale as a hidden system message BEFORE the final user message.
    The model "thinks" better with this reasoning context present.

    Returns the modified messages list.
    """
    if not rationale:
        return messages

    reasoning_msg = {
        "role": "system",
        "content": f"[INTERNAL REASONING -- think before responding]:\n{rationale}",
    }

    # Insert before the last user message
    # Find the index of the last user message
    last_user_idx = None
    for i in range(len(messages) - 1, -1, -1):
        if messages[i].get("role") == "user":
            last_user_idx = i
            break

    if last_user_idx is not None:
        messages.insert(last_user_idx, reasoning_msg)
    else:
        # No user message found, append before end
        messages.insert(-1, reasoning_msg)

    # Also log to internal monologue
    try:
        from modules.joi_reasoning import internal_monologue
        internal_monologue(rationale[:300], "quietstar")
    except Exception:
        pass

    return messages


# ── Post-Evaluate Response ──────────────────────────────────────────────────
def post_evaluate(reply: str, user_msg: str, classification: Dict[str, Any]) -> Dict[str, Any]:
    """
    Score the response quality after generation.
    Uses _score_candidate from joi_reasoning.py.
    Logs the score + reasoning chain to reasoning_log.json.
    """
    complexity = classification.get("complexity", "low")
    if complexity == "low":
        return {"score": None, "skipped": True}

    try:
        from modules.joi_reasoning import _score_candidate
        score = _score_candidate(reply, user_msg)
    except Exception:
        score = 0.5  # default if scoring unavailable

    result = {
        "score": round(score, 3),
        "complexity": complexity,
        "task_type": classification.get("task_type", "?"),
        "reply_length": len(reply),
        "flagged": score < 0.4 and complexity == "high",
    }

    if result["flagged"]:
        print(f"  [QUIETSTAR] Low score ({score:.2f}) on high-complexity task -- flagged for review")

    # Log to reasoning_log.json
    _log_evaluation(user_msg, reply, result)

    return result


# ── Logging ──────────────────────────────────────────────────────────────────
def _log_rationale(user_msg: str, rationale: str, method: str, task_type: str, complexity: str):
    """Log rationale generation to reasoning_log.json."""
    entry = {
        "ts": datetime.now().isoformat(),
        "type": "quietstar_rationale",
        "method": method,
        "task_type": task_type,
        "complexity": complexity,
        "user_preview": user_msg[:100],
        "rationale_preview": rationale[:200],
    }
    _append_to_log(entry)
    print(f"  [QUIETSTAR] Rationale ({method}/{complexity}): {rationale[:80]}...")


def _log_evaluation(user_msg: str, reply: str, result: Dict):
    """Log post-evaluation to reasoning_log.json."""
    entry = {
        "ts": datetime.now().isoformat(),
        "type": "quietstar_evaluation",
        "score": result.get("score"),
        "complexity": result.get("complexity"),
        "task_type": result.get("task_type"),
        "flagged": result.get("flagged", False),
        "user_preview": user_msg[:80],
        "reply_preview": reply[:80],
    }
    _append_to_log(entry)


def _append_to_log(entry: Dict):
    """Append an entry to reasoning_log.json (max 200 entries)."""
    try:
        if REASONING_LOG.exists():
            data = json.loads(REASONING_LOG.read_text(encoding="utf-8"))
        else:
            data = []
        if not isinstance(data, list):
            data = []
        data.append(entry)
        if len(data) > 200:
            data = data[-200:]
        REASONING_LOG.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")
    except Exception as e:
        print(f"  [QUIETSTAR] Log write failed: {e}")


print(f"  [OK] Quiet-STaR reasoning engine loaded")
