"""
modules/joi_workspace.py

Unified Workspace (Shared State) for 3-Tier Coding & TDR
=========================================================
Single source of truth for Plan → Execute → Verify. All agents (Architect,
Developer, Tester) read/write the same workspace so context doesn't drift.

Stores:
  - plan.md / plan steps (from Planner)
  - status.json (phase, current_file_focus, current_step, pending_tasks)
  - diff_history (summarized every N steps to avoid overload)
  - coding_session_cache compatible with skill_library and DPO
"""

from __future__ import annotations

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# Coding session cache directory
WORKSPACE_DIR = DATA_DIR / "coding_session_cache"
WORKSPACE_DIR.mkdir(exist_ok=True)

WORKSPACE_JSON = WORKSPACE_DIR / "workspace.json"
PLAN_MD = WORKSPACE_DIR / "plan.md"
STATUS_JSON = WORKSPACE_DIR / "status.json"
DEBUG_LOGS_DIR = BASE_DIR / "data" / "debug_logs"
DEBUG_LOGS_DIR.mkdir(parents=True, exist_ok=True)

# Summarize diff_history every N steps to keep Implementer from being overwhelmed
SUMMARIZE_EVERY_N_STEPS = 3
MAX_DIFF_HISTORY_ENTRIES = 30
MAX_DIFF_SUMMARY_CHARS = 4000

_workspace_cache: Optional[Dict[str, Any]] = None
_workspace_ts: float = 0
CACHE_TTL = 5.0


def _load_workspace() -> Dict[str, Any]:
    """Load workspace state from disk."""
    global _workspace_cache, _workspace_ts
    now = time.time()
    if _workspace_cache is not None and (now - _workspace_ts) < CACHE_TTL:
        return _workspace_cache
    if WORKSPACE_JSON.exists():
        try:
            data = json.loads(WORKSPACE_JSON.read_text(encoding="utf-8"))
            _workspace_cache = data
            _workspace_ts = now
            return data
        except Exception:
            pass
    default = {
        "current_file_focus": None,
        "diff_history": [],
        "diff_summary": "",
        "pending_tasks": [],
        "completed_tasks": [],
        "current_step_index": 0,
        "goal": "",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "step_count": 0,
        "phase": "complete",
        "paused_reason": None,
        "last_error": None,
        "failed_step_index": None,
        "failed_step_description": None,
        "debug_log_path": None,
        "correction_hint": None,
    }
    _workspace_cache = default
    _workspace_ts = now
    return default


def _save_workspace(data: Dict[str, Any]) -> None:
    global _workspace_cache
    data["updated_at"] = datetime.now().isoformat()
    try:
        WORKSPACE_JSON.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")
    except Exception as e:
        print(f"  [WORKSPACE] Save failed: {e}")
    _workspace_cache = None


def get_workspace() -> Dict[str, Any]:
    """Return current workspace state (read-only copy)."""
    return dict(_load_workspace())


def set_plan(goal: str, steps: List[Dict[str, Any]], plan_md_content: Optional[str] = None) -> None:
    """
    Set the current execution plan. Called by Planner (Tier 1) when use_heavy_reasoning.
    Stores plan in workspace and writes plan.md.
    """
    data = _load_workspace()
    data["goal"] = goal[:2000]
    data["pending_tasks"] = [{"step": s.get("step", i + 1), "description": str(s.get("description", ""))[:500]} for i, s in enumerate(steps)]
    data["completed_tasks"] = []
    data["current_step_index"] = 0
    data["step_count"] = 0
    data["diff_history"] = []
    data["diff_summary"] = ""
    data["phase"] = "plan_ready"
    data["paused_reason"] = None
    data["last_error"] = None
    data["failed_step_index"] = None
    data["failed_step_description"] = None
    data["debug_log_path"] = None
    data["correction_hint"] = None
    _save_workspace(data)

    if plan_md_content is not None:
        try:
            PLAN_MD.write_text(plan_md_content, encoding="utf-8")
        except Exception as e:
            print(f"  [WORKSPACE] plan.md write failed: {e}")

    # status.json for UI/diagnostics
    status = {
        "phase": "plan_ready",
        "goal": goal[:500],
        "pending_count": len(data["pending_tasks"]),
        "current_step_index": 0,
        "updated_at": data["updated_at"],
    }
    try:
        STATUS_JSON.write_text(json.dumps(status, indent=2), encoding="utf-8")
    except Exception:
        pass


def get_pending_tasks() -> List[Dict[str, Any]]:
    """Return remaining tasks from the plan."""
    return list(_load_workspace().get("pending_tasks", []))


def complete_step(step_index: int, output_summary: str = "") -> None:
    """Mark a step complete and optionally append to diff_history."""
    data = _load_workspace()
    pending = data.get("pending_tasks", [])
    if 0 <= step_index < len(pending):
        task = pending.pop(step_index)
        data["completed_tasks"] = data.get("completed_tasks", []) + [task]
        data["pending_tasks"] = pending
        data["current_step_index"] = min(step_index, len(pending) - 1) if pending else 0
        data["step_count"] = data.get("step_count", 0) + 1
        if output_summary:
            data["diff_history"] = data.get("diff_history", []) + [{"step": task.get("step"), "summary": output_summary[:500]}]
            if data["step_count"] % SUMMARIZE_EVERY_N_STEPS == 0:
                _summarize_diff_history(data)
        _save_workspace(data)
        _write_status(data)


def append_diff(file_path: str, diff_preview: str) -> None:
    """Append a diff entry (e.g. after Developer applies an edit)."""
    data = _load_workspace()
    data.setdefault("diff_history", []).append({"file": file_path, "diff_preview": diff_preview[:800]})
    if len(data["diff_history"]) > MAX_DIFF_HISTORY_ENTRIES:
        data["diff_history"] = data["diff_history"][-MAX_DIFF_HISTORY_ENTRIES:]
        _summarize_diff_history(data)
    _save_workspace(data)


def set_current_file_focus(path: Optional[str]) -> None:
    """Set which file is currently being edited."""
    data = _load_workspace()
    data["current_file_focus"] = path
    _save_workspace(data)


def _summarize_diff_history(data: Dict[str, Any]) -> None:
    """Compress diff_history into diff_summary so context doesn't explode."""
    history = data.get("diff_history", [])
    if not history:
        return
    parts = []
    for h in history[-15:]:
        if "file" in h:
            parts.append(f"- {h.get('file', '?')}: {h.get('diff_preview', '')[:200]}")
        else:
            parts.append(f"- Step {h.get('step', '?')}: {h.get('summary', '')[:200]}")
    data["diff_summary"] = "\n".join(parts)[:MAX_DIFF_SUMMARY_CHARS]
    data["diff_history"] = history[-10:]  # keep last 10 raw entries
    return


def _write_status(data: Dict[str, Any]) -> None:
    """Write status.json for UI."""
    phase = data.get("phase")
    if not phase and data.get("pending_tasks"):
        phase = "executing"
    if not phase:
        phase = "complete"
    status = {
        "phase": phase,
        "goal": data.get("goal", "")[:500],
        "pending_count": len(data.get("pending_tasks", [])),
        "completed_count": len(data.get("completed_tasks", [])),
        "current_step_index": data.get("current_step_index", 0),
        "current_file_focus": data.get("current_file_focus"),
        "updated_at": data.get("updated_at"),
        "paused_reason": data.get("paused_reason"),
        "failed_step_index": data.get("failed_step_index"),
        "debug_log_path": data.get("debug_log_path"),
    }
    try:
        STATUS_JSON.write_text(json.dumps(status, indent=2), encoding="utf-8")
    except Exception:
        pass


def get_plan_md_content() -> str:
    """Return plan.md content if it exists."""
    if PLAN_MD.exists():
        try:
            return PLAN_MD.read_text(encoding="utf-8")
        except Exception:
            pass
    return ""


def get_workspace_phase() -> str:
    """Return 'executing' | 'plan_ready' | 'complete' | 'PAUSED_FOR_INTERVENTION'."""
    data = _load_workspace()
    if data.get("phase") == "PAUSED_FOR_INTERVENTION":
        return "PAUSED_FOR_INTERVENTION"
    pending = data.get("pending_tasks", [])
    goal = data.get("goal", "")
    if not goal and not pending:
        return "complete"
    if pending:
        return "executing"
    return "plan_ready"


def set_paused_for_intervention(
    step_index: int,
    step_description: str,
    reason: str,
    last_error: str,
    stdout: str = "",
    stderr: str = "",
    code_snippet: str = "",
) -> str:
    """
    Set workspace to PAUSED_FOR_INTERVENTION and write full debug trace to data/debug_logs/.
    Returns path to the debug log file.
    """
    data = _load_workspace()
    data["phase"] = "PAUSED_FOR_INTERVENTION"
    data["paused_reason"] = reason
    data["last_error"] = last_error
    data["failed_step_index"] = step_index
    data["failed_step_description"] = (step_description or "")[:500]
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_name = f"critical_failure_{ts}.txt"
    log_path = DEBUG_LOGS_DIR / log_name
    data["debug_log_path"] = str(log_path)
    _save_workspace(data)
    _write_status(data)
    try:
        log_path.write_text(
            f"CRITICAL_FAILURE {ts}\n"
            f"Reason: {reason}\n"
            f"Step index: {step_index}\n"
            f"Step description: {step_description}\n\n"
            f"=== STDERR ===\n{stderr}\n\n=== STDOUT ===\n{stdout}\n\n=== CODE SNIPPET ===\n{code_snippet}\n",
            encoding="utf-8",
        )
    except Exception as e:
        print(f"  [WORKSPACE] Debug log write failed: {e}")
    return str(log_path)


def get_paused_state() -> Optional[Dict[str, Any]]:
    """Return intervention payload for UI if phase is PAUSED_FOR_INTERVENTION, else None."""
    data = _load_workspace()
    if data.get("phase") != "PAUSED_FOR_INTERVENTION":
        return None
    return {
        "status": "intervention_required",
        "reason": data.get("paused_reason", "Execution failed after 3 retries"),
        "last_error": data.get("last_error", ""),
        "failed_step_index": data.get("failed_step_index"),
        "failed_step_description": data.get("failed_step_description"),
        "debug_log_path": data.get("debug_log_path"),
    }


def clear_paused() -> None:
    """Clear PAUSED state so execution can resume or complete."""
    data = _load_workspace()
    data["phase"] = "executing" if data.get("pending_tasks") else "complete"
    data["paused_reason"] = None
    data["last_error"] = None
    data["failed_step_index"] = None
    data["failed_step_description"] = None
    data["debug_log_path"] = None
    _save_workspace(data)
    _write_status(data)


def force_complete_step(step_index: int, output_summary: str = "[User force-completed]") -> None:
    """Mark the step at index as complete without verification. Clears PAUSED."""
    complete_step(step_index, output_summary)
    clear_paused()


def set_correction_hint(hint: str) -> None:
    """Store a correction hint and clear PAUSED so the next resume can retry with this hint."""
    data = _load_workspace()
    data["correction_hint"] = (hint or "").strip()[:2000]
    data["phase"] = "executing"
    data["paused_reason"] = None
    data["last_error"] = None
    data["failed_step_index"] = None
    data["failed_step_description"] = None
    data["debug_log_path"] = None
    _save_workspace(data)
    _write_status(data)


def get_and_clear_correction_hint() -> Optional[str]:
    """Return the stored correction hint and clear it (for one-time use on resume)."""
    data = _load_workspace()
    hint = data.get("correction_hint")
    if hint:
        data["correction_hint"] = None
        _save_workspace(data)
    return hint


def get_workspace_context_for_prompt() -> str:
    """
    Build a concise context block for the Implementer/Architect so they share state.
    Includes goal, pending tasks, diff summary (not full history).
    """
    data = _load_workspace()
    goal = data.get("goal", "")
    pending = data.get("pending_tasks", [])
    summary = data.get("diff_summary", "")
    focus = data.get("current_file_focus")
    if not goal and not pending:
        return ""
    lines = ["[CODING WORKSPACE — shared state]"]
    if goal:
        lines.append(f"Goal: {goal[:400]}")
    if pending:
        lines.append("Pending steps: " + "; ".join(f"{t.get('step')}. {t.get('description', '')[:60]}" for t in pending[:5]))
    if summary:
        lines.append("Recent changes summary: " + summary[:1500])
    if focus:
        lines.append(f"Current file focus: {focus}")
    return "\n".join(lines) + "\n"


def clear_workspace() -> None:
    """Reset workspace (e.g. when session ends or user starts fresh)."""
    global _workspace_cache
    default = {
        "current_file_focus": None,
        "diff_history": [],
        "diff_summary": "",
        "pending_tasks": [],
        "completed_tasks": [],
        "current_step_index": 0,
        "goal": "",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "step_count": 0,
        "phase": "complete",
        "paused_reason": None,
        "last_error": None,
        "failed_step_index": None,
        "failed_step_description": None,
        "debug_log_path": None,
        "correction_hint": None,
    }
    _save_workspace(default)
    _workspace_cache = None
    for f in (PLAN_MD, STATUS_JSON):
        if f.exists():
            try:
                f.write_text("")
            except Exception:
                pass


# Ensure status exists on first import
if not STATUS_JSON.exists():
    _write_status(_load_workspace())


# ── manual_override tool (Hard Stop escape hatch) ───────────────────────────
MANUAL_OVERRIDE_SCHEMA = {
    "type": "function",
    "function": {
        "name": "manual_override",
        "description": "When execution is PAUSED_FOR_INTERVENTION (step failed 3x): (A) force_complete marks the step done without verification; (B) correction_hint gives the AI a hint and resets retries so you can say 'continue' to resume.",
        "parameters": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["force_complete", "correction_hint"],
                    "description": "force_complete: mark the failed step done (you fixed code yourself). correction_hint: provide a hint and clear pause so AI can retry.",
                },
                "step_index": {
                    "type": "integer",
                    "description": "Required for force_complete: the failed step index (0-based).",
                },
                "correction_hint": {
                    "type": "string",
                    "description": "Required for correction_hint: short hint for the AI to fix the step (e.g. 'Use pathlib instead of os.path').",
                },
            },
            "required": ["action"],
        },
    },
}


def _exec_manual_override(action: str, step_index: Optional[int] = None, correction_hint: Optional[str] = None) -> str:
    if action == "force_complete":
        if step_index is None:
            return "Error: step_index is required for force_complete."
        try:
            force_complete_step(step_index)
            return f"Step {step_index} marked complete. You can continue the plan."
        except Exception as e:
            return f"Error: {e}"
    if action == "correction_hint":
        if not (correction_hint or str(correction_hint).strip()):
            return "Error: correction_hint is required for correction_hint action."
        set_correction_hint(str(correction_hint).strip())
        return "Correction hint saved. Say 'continue' or 'resume' to retry the step with this hint."
    return "Error: action must be force_complete or correction_hint."


def _register_manual_override_tool():
    try:
        import joi_companion
        def executor(**kwargs):
            return _exec_manual_override(
                action=kwargs.get("action", ""),
                step_index=kwargs.get("step_index"),
                correction_hint=kwargs.get("correction_hint"),
            )
        joi_companion.register_tool(MANUAL_OVERRIDE_SCHEMA, executor)
    except Exception as e:
        print(f"  [WORKSPACE] manual_override tool registration failed: {e}")


_register_manual_override_tool()

print(f"  [OK] Workspace module loaded ({WORKSPACE_DIR.name})")
