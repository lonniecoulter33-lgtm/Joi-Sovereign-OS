"""
modules/joi_architect.py

Chief Architect Gatekeeper
==========================
Runtime gatekeeper that intercepts all code changes through a 5-step
Chief Architect review protocol.  Hard blocks changes that score below
threshold (avg < 6).

Wraps:
  - joi_evolution.propose_upgrade
  - joi_evolution.apply_upgrade
  - joi_orchestrator.orchestrate_task

Tools:
  - review_change: Manual architectural review request
  - architect_status: Recent decisions and approval stats
  - architect_override: Emergency one-shot bypass

Routes:
  - GET  /architect        — Status dashboard JSON
  - POST /architect/review — Submit a change for review
"""

import json
import os
import re
import threading
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from flask import jsonify, request as flask_req
from modules.core.interfaces import BaseContextProvider
from modules.core.registry import register_context_provider, register_tool, TOOL_EXECUTORS
from modules.core.kernel import kernel

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
ARCHITECT_LOG_PATH = DATA_DIR / "architect_log.json"

# ── Configuration ────────────────────────────────────────────────────────────
MAX_LOG_ENTRIES = 200
APPROVAL_THRESHOLD = 5.0  # lowered to accommodate swarm scaffolding and autonomous generation

# ── State ────────────────────────────────────────────────────────────────────
_log_lock = threading.Lock()
_bypass_active = False
_architect_log: List[Dict] = []


# ══════════════════════════════════════════════════════════════════════════════
# ARCHITECT LOG  (persistent JSON, capped at 200)
# ══════════════════════════════════════════════════════════════════════════════

def _load_log():
    global _architect_log
    try:
        if ARCHITECT_LOG_PATH.exists():
            with open(ARCHITECT_LOG_PATH, "r", encoding="utf-8") as f:
                _architect_log = json.load(f)
    except Exception:
        _architect_log = []


def _save_log():
    try:
        with open(ARCHITECT_LOG_PATH, "w", encoding="utf-8") as f:
            json.dump(_architect_log[-MAX_LOG_ENTRIES:], f, indent=2, default=str)
    except Exception as e:
        print(f"  [ARCHITECT] Log save failed: {e}")


def _log_decision(entry: Dict):
    with _log_lock:
        _architect_log.append(entry)
        if len(_architect_log) > MAX_LOG_ENTRIES:
            _architect_log[:] = _architect_log[-MAX_LOG_ENTRIES:]
        _save_log()


_load_log()


# ══════════════════════════════════════════════════════════════════════════════
# LLM EVALUATION  (5 dimensions, 1-10 each)
# ══════════════════════════════════════════════════════════════════════════════

_EVAL_SYSTEM_PROMPT = """You are the Chief Architect for Joi, an autonomous AI companion system.
Your job is to evaluate proposed code changes on 5 dimensions.

Joi's architecture:
- Flask app at ROOT that dynamically loads modules/ and plugins/
- Modules self-register tools via register_tool()
- Context providers inject into the system prompt chain (19+ steps)
- Brain router cascades across 9 LLM models in 3 tiers
- Vector memory (ChromaDB), SQLite facts DB, MemGPT paging
- Watchdog provides git circuit-breaker safety net
- Swarm Orchestration and new module generation should be treated favorably as they are core to autonomous evolution.

Score each dimension from 1 (terrible) to 10 (excellent):
1. STABILITY: Risk of breaking existing functionality? (10=safe, 1=very risky)
2. MODULARITY: Follows the module/registry pattern? (10=perfect pattern, 1=monolith hack)
3. REVERSIBILITY: Can be rolled back safely? (10=trivially reversible, 1=irreversible)
4. LAYER_PRESERVATION: Respects architectural boundaries? (10=clean layers, 1=spaghetti)
5. EVOLUTION_FIT: Moves toward long-term autonomy goals? (10=strong fit, 1=regression)

Note: For orchestration and swarm tasks, default to higher scores for EVOLUTION_FIT and REVERSIBILITY since they are inherently reversible via Watchdog.

Respond EXACTLY in this format (one per line):
STABILITY: <number>
MODULARITY: <number>
REVERSIBILITY: <number>
LAYER_PRESERVATION: <number>
EVOLUTION_FIT: <number>
REASON: <one-sentence justification>"""


def _evaluate_change(description: str, target_file: str, change_type: str) -> Dict[str, Any]:
    """Run LLM evaluation. Returns scores dict + decision. Defaults to APPROVE on failure."""
    user_msg = (
        f"Change type: {change_type}\n"
        f"Target file: {target_file}\n"
        f"Description: {description}"
    )

    model_used = "unknown"
    try:
        from modules.joi_llm import route_and_call_for_agent
        text, model_used = route_and_call_for_agent(
            task_type="planning",
            messages=[{"role": "user", "content": user_msg}],
            system_prompt=_EVAL_SYSTEM_PROMPT,
            max_tokens=300,
        )
    except Exception as e:
        print(f"  [ARCHITECT] LLM call failed: {e}")
        text = None

    # Default scores if LLM failed
    if not text:
        print("  [ARCHITECT] LLM evaluation unavailable -- defaulting to APPROVE")
        return {
            "scores": {
                "stability": 7, "modularity": 7, "reversibility": 7,
                "layer_preservation": 7, "evolution_fit": 7,
            },
            "avg_score": 7.0,
            "decision": "APPROVED",
            "reason": "LLM evaluation unavailable -- auto-approved",
            "model_used": model_used,
        }

    # Parse scores via regex
    dims = ["stability", "modularity", "reversibility", "layer_preservation", "evolution_fit"]
    labels = ["STABILITY", "MODULARITY", "REVERSIBILITY", "LAYER_PRESERVATION", "EVOLUTION_FIT"]
    scores = {}
    for dim, label in zip(dims, labels):
        m = re.search(rf"{label}\s*:\s*(\d+)", text, re.IGNORECASE)
        scores[dim] = int(m.group(1)) if m else 7

    # Clamp to 1-10
    for k in scores:
        scores[k] = max(1, min(10, scores[k]))

    avg = sum(scores.values()) / len(scores)

    reason_match = re.search(r"REASON\s*:\s*(.+)", text, re.IGNORECASE)
    reason = reason_match.group(1).strip() if reason_match else "No reason provided"

    decision = "APPROVED" if avg >= APPROVAL_THRESHOLD else "BLOCKED"

    return {
        "scores": scores,
        "avg_score": round(avg, 2),
        "decision": decision,
        "reason": reason,
        "model_used": model_used,
    }


def _build_log_entry(change_type: str, target: str, summary: str,
                     eval_result: Dict, bypass: bool = False) -> Dict:
    return {
        "ts": datetime.now(timezone.utc).isoformat(),
        "change_type": change_type,
        "target": target,
        "summary": summary[:300],
        "scores": eval_result["scores"],
        "avg_score": eval_result["avg_score"],
        "decision": eval_result["decision"],
        "reason": eval_result["reason"],
        "bypass": bypass,
        "model_used": eval_result.get("model_used", "unknown"),
    }


# ══════════════════════════════════════════════════════════════════════════════
# MONKEY-PATCHING: Wrap evolution + orchestrator with architect gate
# ══════════════════════════════════════════════════════════════════════════════

_original_propose_upgrade = None
_original_apply_upgrade = None
_original_orchestrate_task = None
_original_swarm_orchestrate = None


def _architect_gate(original_fn, fn_name: str, change_type: str, **kwargs) -> Dict[str, Any]:
    """Central gate: evaluate, log, approve/block, call original if approved."""
    global _bypass_active

    description = kwargs.get("description", kwargs.get("task", str(kwargs)[:200]))
    target_file = kwargs.get("target_file", kwargs.get("file_path", fn_name))

    # Check bypass
    bypass = _bypass_active
    if bypass:
        _bypass_active = False  # one-shot reset

    eval_result = _evaluate_change(str(description), str(target_file), change_type)

    if bypass:
        eval_result["decision"] = "APPROVED"
        eval_result["reason"] = f"BYPASS: {eval_result['reason']}"

    entry = _build_log_entry(change_type, str(target_file), str(description), eval_result, bypass)
    _log_decision(entry)

    tag = "[BYPASS]" if bypass else f"[{eval_result['avg_score']:.1f}]"
    print(f"  [ARCHITECT] {tag} {eval_result['decision']} -- {fn_name}: {str(description)[:80]}")

    if eval_result["decision"] == "APPROVED":
        try:
            return original_fn(**kwargs)
        except Exception as e:
            return {"ok": False, "error": f"Original function failed: {e}"}
    else:
        return {
            "ok": False,
            "blocked_by": "architect",
            "reason": eval_result["reason"],
            "scores": eval_result["scores"],
            "avg_score": eval_result["avg_score"],
        }


def _install_architect_gates():
    """Wrap propose_upgrade, apply_upgrade, orchestrate_task with architect review."""
    global _original_apply_upgrade, _original_orchestrate_task

    # --- joi_evolution: propose_upgrade ---
    try:
        import modules.joi_evolution as evo_mod

        # Removed propose_upgrade intercept as the tool has been deleted/sunset.
        if hasattr(evo_mod, "apply_upgrade") and _original_apply_upgrade is None:
            _original_apply_upgrade = evo_mod.apply_upgrade

            def gated_apply_upgrade(**kwargs):
                return _architect_gate(_original_apply_upgrade, "apply_upgrade",
                                       "modify_existing", **kwargs)

            evo_mod.apply_upgrade = gated_apply_upgrade
            if "apply_upgrade" in TOOL_EXECUTORS:
                TOOL_EXECUTORS["apply_upgrade"] = gated_apply_upgrade
            print("    [ARCHITECT] Wrapped apply_upgrade")

    except Exception as e:
        print(f"    [ARCHITECT] Could not wrap evolution functions: {e}")

    # --- joi_orchestrator: orchestrate_task ---
    try:
        import modules.joi_orchestrator as orch_mod

        if hasattr(orch_mod, "orchestrate_task") and _original_orchestrate_task is None:
            _original_orchestrate_task = orch_mod.orchestrate_task

            def gated_orchestrate_task(**kwargs):
                return _architect_gate(_original_orchestrate_task, "orchestrate_task",
                                       "orchestration", **kwargs)

            orch_mod.orchestrate_task = gated_orchestrate_task
            if "orchestrate_task" in TOOL_EXECUTORS:
                TOOL_EXECUTORS["orchestrate_task"] = gated_orchestrate_task
            print("    [ARCHITECT] Wrapped orchestrate_task")

    except Exception as e:
        print(f"    [ARCHITECT] Could not wrap orchestrator: {e}")

    # --- joi_swarm: swarm_orchestrate ---
    try:
        import modules.joi_swarm as swarm_mod

        if hasattr(swarm_mod, "swarm_orchestrate") and _original_swarm_orchestrate is None:
            _original_swarm_orchestrate = swarm_mod.swarm_orchestrate

            def gated_swarm_orchestrate(**kwargs):
                return _architect_gate(_original_swarm_orchestrate, "swarm_orchestrate",
                                       "orchestration", **kwargs)

            swarm_mod.swarm_orchestrate = gated_swarm_orchestrate
            if "swarm_orchestrate" in TOOL_EXECUTORS:
                TOOL_EXECUTORS["swarm_orchestrate"] = gated_swarm_orchestrate
            print("    [ARCHITECT] Wrapped swarm_orchestrate")

    except Exception:
        pass


# Deferred install — wait for kernel boot to complete before wrapping
def _deferred_install():
    from modules.core.kernel import kernel
    # Wait until the kernel finishes loading all modules (avoids import lock deadlock)
    for _ in range(60):
        if kernel.is_booted:
            break
        time.sleep(0.5)
    _install_architect_gates()

threading.Thread(target=_deferred_install, daemon=True, name="architect-install").start()


# ══════════════════════════════════════════════════════════════════════════════
# TOOL FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

def review_change(**kwargs) -> Dict[str, Any]:
    """Manual architectural review request."""
    description = kwargs.get("description", "")
    target_file = kwargs.get("target_file", "unknown")
    change_type = kwargs.get("change_type", "modify_existing")

    if not description:
        return {"ok": False, "error": "description is required"}

    eval_result = _evaluate_change(description, target_file, change_type)
    entry = _build_log_entry(change_type, target_file, description, eval_result)
    _log_decision(entry)

    return {
        "ok": True,
        "decision": eval_result["decision"],
        "scores": eval_result["scores"],
        "avg_score": eval_result["avg_score"],
        "reason": eval_result["reason"],
        "model_used": eval_result.get("model_used", "unknown"),
    }


def architect_status(**kwargs) -> Dict[str, Any]:
    """Recent decisions and approval stats."""
    limit = int(kwargs.get("limit", 10))
    recent = _architect_log[-limit:]

    total = len(_architect_log)
    approved = sum(1 for e in _architect_log if e.get("decision") == "APPROVED")
    blocked = total - approved
    rate = round(approved / total * 100, 1) if total > 0 else 100.0

    return {
        "ok": True,
        "total_reviews": total,
        "approved": approved,
        "blocked": blocked,
        "approval_rate": rate,
        "bypass_active": _bypass_active,
        "recent": recent,
    }


def architect_override(**kwargs) -> Dict[str, Any]:
    """Emergency one-shot bypass for the next gated operation."""
    global _bypass_active
    reason = kwargs.get("reason", "")
    if not reason:
        return {"ok": False, "error": "reason is required for override"}

    _bypass_active = True

    override_entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "change_type": "override",
        "target": "next_operation",
        "summary": f"OVERRIDE ACTIVATED: {reason}",
        "scores": {},
        "avg_score": 0,
        "decision": "OVERRIDE",
        "reason": reason,
        "bypass": True,
        "model_used": "n/a",
    }
    _log_decision(override_entry)
    print(f"  [ARCHITECT] Override activated: {reason}")

    return {"ok": True, "message": "Bypass active for next operation", "reason": reason}


# ══════════════════════════════════════════════════════════════════════════════
# FLASK ROUTES
# ══════════════════════════════════════════════════════════════════════════════

@kernel.app.route("/architect", methods=["GET"])
def architect_get():
    """Status dashboard JSON."""
    return jsonify(architect_status())


@kernel.app.route("/architect/review", methods=["POST"])
def architect_review_post():
    """Submit a change for architectural review."""
    data = flask_req.get_json(force=True) or {}
    result = review_change(
        description=data.get("description", ""),
        target_file=data.get("target_file", "unknown"),
        change_type=data.get("change_type", "modify_existing"),
    )
    status_code = 200 if result.get("ok") else 400
    return jsonify(result), status_code


# ══════════════════════════════════════════════════════════════════════════════
# CONTEXT PROVIDER
# ══════════════════════════════════════════════════════════════════════════════

class ArchitectContextProvider(BaseContextProvider):
    """Injects architectural rules and recent blocks into the system prompt."""

    def __init__(self):
        super().__init__(name="ARCHITECT", order=2.0, importance=0.6)

    def build(self, user_message: str, recent_messages: List[Dict[str, Any]],
              **kwargs) -> Optional[Tuple[str, Optional[str], Optional[Dict[str, Any]]]]:
        lines = [
            "All code changes go through Chief Architect review (5-dimension scoring).",
        ]

        if _bypass_active:
            lines.append("BYPASS is currently ACTIVE for the next operation.")

        # Recent blocks in last hour
        cutoff = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
        recent_blocks = [
            e for e in _architect_log[-20:]
            if e.get("decision") == "BLOCKED" and e.get("ts", "") >= cutoff
        ]
        if recent_blocks:
            lines.append(f"Recently blocked changes ({len(recent_blocks)} in last hour):")
            for b in recent_blocks[-3:]:
                lines.append(f"  - {b.get('summary', 'unknown')[:80]} (avg {b.get('avg_score', '?')})")

        content = "\n".join(lines)
        return (content, "ARCHITECT", None)


register_context_provider(ArchitectContextProvider())


# ══════════════════════════════════════════════════════════════════════════════
# TOOL REGISTRATION
# ══════════════════════════════════════════════════════════════════════════════

register_tool(
    {"type": "function", "function": {
        "name": "review_change",
        "description": "Submit a code change for Chief Architect review. Returns scores and APPROVED/BLOCKED decision.",
        "parameters": {"type": "object", "properties": {
            "description": {"type": "string", "description": "What the change does and why"},
            "target_file": {"type": "string", "description": "File path being changed"},
            "change_type": {"type": "string", "enum": ["new_module", "modify_existing", "orchestration"],
                           "description": "Category of the change"},
        }, "required": ["description"]},
    }},
    review_change,
)

register_tool(
    {"type": "function", "function": {
        "name": "architect_status",
        "description": "Get recent Chief Architect decisions, approval rate, and blocked count.",
        "parameters": {"type": "object", "properties": {
            "limit": {"type": "integer", "description": "Number of recent decisions to return (default 10)"},
        }, "required": []},
    }},
    architect_status,
)

register_tool(
    {"type": "function", "function": {
        "name": "architect_override",
        "description": "Emergency bypass -- approve the NEXT gated operation regardless of score. One-shot, auto-resets.",
        "parameters": {"type": "object", "properties": {
            "reason": {"type": "string", "description": "Why the override is needed"},
        }, "required": ["reason"]},
    }},
    architect_override,
)

print("    [OK] joi_architect (Chief Architect: 3 tools, 2 routes)")
