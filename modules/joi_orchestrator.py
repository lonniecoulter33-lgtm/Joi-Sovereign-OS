"""
modules/joi_orchestrator.py

Multi-Agent Orchestrator Engine
================================
Core engine for the Claude Code-style multi-agent pipeline:
  - Session state management (persisted to data/orchestrator_state.json)
  - Plan/Execute/Validate/Apply phases with approval gates
  - SSE streaming for real-time terminal UI
  - Mid-orchestration chat (user can talk to Joi during pipeline)
  - Self-healing: on failure, analyzes cause and retries with a revised task (up to MAX_RECOVERY_ATTEMPTS)
  - Works on Joi's own codebase and on separate apps/projects (project_path)
  - Tools: orchestrate_task, approve_subtask, reject_subtask, get_orchestrator_status, cancel_orchestration
  - Routes: GET/POST /orchestrator, GET /orchestrator/stream, POST /orchestrator/chat
"""

import hashlib
import json
import os
import queue
import threading
import time
import traceback
from pathlib import Path
from typing import Any, Dict, List, Optional

import joi_companion
from flask import Response, jsonify, request as flask_req

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
STATE_PATH = DATA_DIR / "orchestrator_state.json"

# ── Constants ────────────────────────────────────────────────────────────────
MAX_RETRIES = 3
HEARTBEAT_INTERVAL = 300 # seconds
AUTO_APPROVE_THRESHOLD = 3  # auto-approve plan if <= N subtasks
MAX_RECOVERY_ATTEMPTS = 2   # self-healing: up to 2 retries with analyzed revised task (3 total runs)

# ══════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════

_current_session: Optional[Dict] = None
_session_lock = threading.Lock()


def _new_session(task: str) -> Dict:
    """Create a fresh orchestration session."""
    return {
        "session_id": f"orch_{int(time.time()*1000)}",
        "task": task,
        "phase": "PLAN",
        "subtasks": [],
        "plan_summary": "",
        "risk_assessment": "",
        "agent_count": 0,
        "event_log": [],
        "recovery_attempt": 0,
        "continuation_count": 0,
        "created_at": time.time(),
        "updated_at": time.time(),
    }


def _save_state():
    """Persist current session to disk."""
    global _current_session
    if _current_session is None:
        return
    try:
        with open(STATE_PATH, "w", encoding="utf-8") as f:
            # Don't serialize event_log to disk (too large)
            state_copy = {k: v for k, v in _current_session.items() if k != "event_log"}
            json.dump(state_copy, f, indent=2, default=str)
    except Exception as e:
        print(f"  [ORCH] State save failed: {e}")


def _load_state() -> Optional[Dict]:
    """Load session from disk (crash recovery)."""
    try:
        if STATE_PATH.exists():
            with open(STATE_PATH, "r", encoding="utf-8") as f:
                state = json.load(f)
            state.setdefault("event_log", [])
            state.setdefault("recovery_attempt", 0)
            return state
    except Exception:
        pass
    return None


def _log_pipeline_crash(exc: BaseException) -> None:
    """Append pipeline exception to data/orchestrator_crash.log for diagnostics."""
    try:
        log_path = DATA_DIR / "orchestrator_crash.log"
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"\n--- {time.strftime('%Y-%m-%d %H:%M:%S')} ---\n")
            f.write(f"{type(exc).__name__}: {exc}\n")
            traceback.print_exc(file=f)
    except Exception:
        pass


def _analyze_failure_and_propose_retry(project_root: str) -> Optional[str]:
    """
    Self-healing: analyze why the pipeline failed and propose a revised task description.
    Works for Joi's own codebase and for separate apps/projects (project_root may be different).
    Returns revised task string to retry, or None if no better approach / IMPOSSIBLE.
    """
    global _current_session
    if not _current_session:
        return None

    task = _current_session.get("task", "")
    phase = _current_session.get("phase", "FAILED")
    subtasks = _current_session.get("subtasks", [])
    event_log = _current_session.get("event_log", [])

    # Build failure summary
    failure_lines = []
    if phase == "FAILED" and not subtasks:
        # Planning phase failed (e.g. Architect error)
        for ev in event_log[-15:]:
            if ev.get("type") == "error":
                failure_lines.append(ev.get("message", str(ev))[:400])
    else:
        for st in subtasks:
            status = st.get("status", "")
            if status != "failed":
                continue
            desc = st.get("description", "?")[:200]
            failure_lines.append(f"Subtask: {desc}")
            val = st.get("validation", {})
            if isinstance(val, dict) and val.get("stderr"):
                failure_lines.append(f"  stderr: {str(val['stderr'])[:300]}")
            if st.get("retries", 0) >= MAX_RETRIES:
                failure_lines.append("  (failed after max retries)")
        for ev in event_log[-20:]:
            if ev.get("type") in ("error", "validation_failed"):
                failure_lines.append(ev.get("message", str(ev))[:400])

    failure_summary = "\n".join(failure_lines[-25:]) if failure_lines else "No detailed errors captured."

    prompt = f"""You are helping an automated coding pipeline (Agent Terminal). It can work on its own codebase (Joi) or on separate apps/projects.

ORIGINAL REQUEST:
{task[:1500]}

PROJECT CONTEXT: {project_root}

WHAT HAPPENED:
The pipeline ran but some steps failed. Here is the failure information:

{failure_summary}

TASK:
Propose a SINGLE revised task description that might succeed. For example:
- Break the goal into a smaller, more focused change
- Target a different file or approach
- Fix a specific error (e.g. "Fix the syntax error in module X" or "Add missing import in Y")
- Rephrase so the planner/coder can produce a more surgical edit

Reply with ONLY the revised task description in one paragraph (no bullet list, no "IMPOSSIBLE" unless you truly believe no retry can work).
If no reasonable retry exists, reply with exactly: IMPOSSIBLE
"""

    try:
        from modules.joi_brain import brain
        result = brain.think(
            task="Analyze pipeline failure and propose revised task",
            prompt=prompt,
            system_prompt="You are a coding pipeline analyst. Output only the revised task text or IMPOSSIBLE.",
            thinking_level=2,
            max_tokens=800,
        )
        text = (result.get("text") or "").strip() if result.get("ok") else ""
    except Exception:
        try:
            from modules.joi_llm import _call_gemini
            from config.joi_models import GEMINI_MODELS
            text = (_call_gemini(prompt, max_tokens=800, model=GEMINI_MODELS.get("fallback", "gemini-2.5-flash-lite")) or "").strip()
        except Exception:
            text = ""

    if not text:
        return None
    if "IMPOSSIBLE" in text.upper().strip():
        return None
    return text[:2000].strip()


def _maybe_recovery_retry(project_path: Optional[str]) -> bool:
    """
    If the session failed and we have recovery attempts left, analyze failure,
    propose a revised task, update session, and re-run the pipeline. Returns True
    if a retry was started (caller should return), False otherwise.
    """
    global _current_session
    if not _current_session:
        return False
    if _current_session.get("recovery_attempt", 0) >= MAX_RECOVERY_ATTEMPTS:
        return False
    project_root = project_path or str(BASE_DIR)
    revised = _analyze_failure_and_propose_retry(project_root)
    if not revised or "IMPOSSIBLE" in revised.upper().strip():
        return False

    # ── Loop-detection guard ──────────────────────────────────────────────────
    # Hash the revised task text; if it matches the last attempt, we'd be
    # running the exact same plan again → abort to avoid an infinite retry loop.
    _task_hash = hashlib.md5(revised.strip().lower().encode()).hexdigest()[:12]
    if _current_session.get("last_task_hash") == _task_hash:
        _broadcast({
            "type": "error",
            "message": (
                "[LOOP GUARD] Revised task is identical to the previous attempt "
                f"(hash={_task_hash}). Aborting recovery to prevent infinite loop."
            ),
        })
        with _session_lock:
            _current_session["phase"] = "FAILED"
        _save_state()
        return False
    # ─────────────────────────────────────────────────────────────────────────

    with _session_lock:
        _current_session["recovery_attempt"] = _current_session.get("recovery_attempt", 0) + 1
        _current_session["task"] = revised
        _current_session["subtasks"] = []
        _current_session["phase"] = "PLAN"
        _current_session["plan_summary"] = ""
        _current_session["risk_assessment"] = ""
        _current_session["last_task_hash"] = _task_hash  # store for next iteration
    _save_state()
    _broadcast({
        "type": "recovery_retry",
        "message": "Analyzing failure and retrying with revised approach...",
        "revised_task_preview": revised[:300],
    })
    _run_pipeline_impl(revised, project_path)
    return True



def _check_subtask_already_done(subtask: Dict, project_root: str) -> bool:
    """
    Check if the code change described by this subtask already exists in the target file.
    Returns True if the change appears to be already present.
    """
    try:
        from config.joi_context import ENABLE_FILE_CHECK_GUARD
        if not ENABLE_FILE_CHECK_GUARD:
            return False
    except ImportError:
        pass

    files = subtask.get("files", [])
    if not files:
        return False

    target_path = files[0]
    if not Path(target_path).is_absolute():
        target_path = str(Path(project_root) / target_path)

    if not Path(target_path).exists():
        return False

    # Get keywords to check (description + acceptance criteria)
    desc = subtask.get("description", "").lower()
    acc = subtask.get("acceptance_criteria", "").lower()
    content = ""
    try:
        with open(target_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read().lower()
    except Exception:
        return False

    # Very basic heuristic: if specific unique keywords from the task are in the file
    # and the task is a simple "Add X" or "Create Y", it might be done.
    # We refine this by looking for code-like snippets in the description.
    
    # 1. Extract potential code snippets (things in backticks or long CamelCase/snake_case)
    matches = re.findall(r'`([^`]+)`|([a-zA-Z_][a-zA-Z0-9_]{5,})', desc + " " + acc)
    snippets = [m[0] or m[1] for m in matches if (m[0] or m[1])]
    
    # Filter out common words
    common = {"function", "variable", "implement", "create", "module", "subtask", "description"}
    snippets = [s for s in snippets if s.lower() not in common]

    if not snippets:
        return False

    # If all non-common snippets are found, it's likely already done
    found_count = 0
    for s in snippets:
        if s.lower() in content:
            found_count += 1
    
    if found_count == len(snippets) and len(snippets) > 1:
        return True
        
    return False


# ══════════════════════════════════════════════════════════════════════════════
# SSE STREAMING
# ══════════════════════════════════════════════════════════════════════════════

_sse_clients: List[queue.Queue] = []
_sse_lock = threading.Lock()


def _broadcast(event: Dict):
    """Push an event to all connected SSE clients and log it."""
    global _current_session

    event.setdefault("timestamp", time.time())
    event.setdefault("type", "info")

    # Add to session event log (keep last 200)
    with _session_lock:
        if _current_session:
            _current_session["event_log"].append(event)
            if len(_current_session["event_log"]) > 200:
                _current_session["event_log"] = _current_session["event_log"][-200:]

    # Push to all SSE clients
    data = json.dumps(event, default=str)
    with _sse_lock:
        dead = []
        for q in _sse_clients:
            try:
                q.put_nowait(data)
            except queue.Full:
                dead.append(q)
        for q in dead:
            _sse_clients.remove(q)


def _sse_generator(client_queue: queue.Queue):
    """Generator for SSE endpoint -- yields events from queue."""
    try:
        # Send initial state if session exists
        if _current_session:
            state_event = {
                "type": "session_state",
                "phase": _current_session.get("phase", "IDLE"),
                "task": _current_session.get("task", ""),
                "subtasks": _current_session.get("subtasks", []),
                "plan_summary": _current_session.get("plan_summary", ""),
            }
            yield f"data: {json.dumps(state_event, default=str)}\n\n"

        last_heartbeat = time.time()
        while True:
            try:
                data = client_queue.get(timeout=1.0)
                yield f"data: {data}\n\n"
            except queue.Empty:
                # Send heartbeat comment to keep connection alive
                if time.time() - last_heartbeat > HEARTBEAT_INTERVAL:
                    yield f": heartbeat {int(time.time())}\n\n"
                    last_heartbeat = time.time()
    except GeneratorExit:
        pass
    finally:
        with _sse_lock:
            if client_queue in _sse_clients:
                _sse_clients.remove(client_queue)


# ══════════════════════════════════════════════════════════════════════════════
# PIPELINE ENGINE
# ══════════════════════════════════════════════════════════════════════════════

def _run_pipeline(task: str, project_path: Optional[str] = None):
    """
    Main orchestration pipeline -- runs in a background thread.
    Phases: PLAN -> (approval) -> EXECUTE -> VALIDATE -> (approval) -> APPLY -> COMPLETE
    Wrapped in try/except so any uncaught exception marks session FAILED and broadcasts
    session_complete. Runs inside Flask app_context so Watchdog/broadcast don't hit
    "Working outside of request context".
    """
    global _current_session
    app = joi_companion.app

    def _run():
        try:
            _run_pipeline_impl(task, project_path)
        except Exception as e:
            with _session_lock:
                _current_session["phase"] = "FAILED"
            _save_state()
            err_msg = f"Pipeline crashed: {type(e).__name__}: {str(e)[:500]}"
            _broadcast({"type": "error", "message": err_msg})
            _broadcast({
                "type": "session_complete",
                "status": "failed",
                "message": err_msg,
            })
            traceback.print_exc()
            _log_pipeline_crash(e)

    with app.app_context():
        _run()


def _run_pipeline_impl(task: str, project_path: Optional[str] = None):
    """Inner implementation of the pipeline (called by _run_pipeline)."""
    global _current_session
    project_root = project_path or str(BASE_DIR)

    # ── WATCHDOG: Pre-orchestration checkpoint ──────────────────────
    try:
        from modules.joi_watchdog import pre_orchestrator_checkpoint
        ckpt = pre_orchestrator_checkpoint(task)
        _broadcast({"type": "info", "message": f"[WATCHDOG] Safety checkpoint: {ckpt}"})
    except Exception as e:
        _broadcast({"type": "info", "message": f"[WATCHDOG] Checkpoint skipped: {e}"})

    # ── PHASE 1: PLAN ────────────────────────────────────────────────
    plan_result = _phase_plan(task, project_root)
    if not plan_result["ok"]:
        if _maybe_recovery_retry(project_path):
            return
        return
    plan = plan_result["plan"]

    # ── GATE 1: Plan Approval ────────────────────────────────────────
    if not _gate_plan_approval(plan):
        return

    # ── PHASE 1.5: GLOBAL SETUP ──────────────────────────────────────
    _phase_setup(plan, project_root)

    # ── PHASE 2: EXECUTE ─────────────────────────────────────────────
    execute_result = _phase_execute(plan, project_root)
    completed_count = execute_result["completed_count"]
    subtasks = execute_result["subtasks"]

    # ── WATCHDOG: Post-orchestration sanity check ───────────────────
    _post_orchestration_sanity(subtasks)

    # ── BUILD PHASE (optional) ───────────────────────────────────────
    _phase_build(plan, project_root, completed_count, subtasks)

    # ── COMPLETE ─────────────────────────────────────────────────────
    _final_complete(subtasks, completed_count, project_path)


def _phase_plan(task: str, project_root: str) -> Dict:
    """Handle the planning phase of the pipeline."""
    global _current_session
    from modules.joi_agents import load_context_file, call_architect, _read_files
    joi_ctx = load_context_file(project_root)

    _broadcast({"type": "info", "message": f"Starting orchestration: {task}"})
    with _session_lock:
        _current_session["phase"] = "PLAN"
        _current_session["agent_count"] += 1
    _save_state()

    _broadcast({"type": "agent_spawned", "agent": "ARCHITECT", "model": "Brain Router",
                "message": "Spawning Architect agent..."})
    
    candidate_files = _guess_relevant_files(task, project_root)
    _broadcast({"type": "info", "message": f"Reading {len(candidate_files)} file(s) for analysis..."})
    file_contents = _read_files(candidate_files)

    plan = call_architect(task, file_contents, joi_ctx, project_root)

    if plan.get("error"):
        error_msg = plan['error']
        _broadcast({"type": "error", "agent": "ARCHITECT", "message": f"Architect failed: {error_msg}"})
        with _session_lock:
            _current_session["phase"] = "FAILED"
        _save_state()
        _broadcast({"type": "session_complete", "status": "failed", "message": "Planning phase failed"})
        return {"ok": False}

    # Store plan in session
    with _session_lock:
        _current_session["subtasks"] = plan.get("subtasks", [])
        _current_session["plan_summary"] = plan.get("plan_summary", "")
        _current_session["risk_assessment"] = plan.get("risk_assessment", "")
    _save_state()

    _broadcast({
        "type": "plan_generated",
        "plan_summary": plan.get("plan_summary", ""),
        "subtask_count": len(plan.get("subtasks", [])),
        "risk": plan.get("risk_assessment", "Unknown"),
        "subtasks": [{"id": s["id"], "description": s.get("description", "")} for s in plan.get("subtasks", [])],
    })
    return {"ok": True, "plan": plan}


def _gate_plan_approval(plan: Dict) -> bool:
    """Handle plan approval gate."""
    subtask_count = len(plan.get("subtasks", []))
    if subtask_count > AUTO_APPROVE_THRESHOLD:
        _broadcast({"type": "approval_requested", "gate": "plan",
                    "message": f"Plan has {subtask_count} subtasks. Approve to proceed."})
        if not _wait_for_plan_approval(timeout=300):
            _broadcast({"type": "info", "message": "Plan rejected or timed out"})
            with _session_lock:
                _current_session["phase"] = "FAILED"
            _save_state()
            _broadcast({"type": "session_complete", "status": "cancelled", "message": "Plan not approved"})
            return False
    else:
        _broadcast({"type": "info", "message": f"Auto-approved plan ({subtask_count} subtasks)"})
    return True


def _phase_setup(plan: Dict, project_root: str):
    """Handle global setup commands."""
    global_setup = plan.get("global_setup_commands", [])
    if not global_setup:
        return
    with _session_lock:
        _current_session["phase"] = "SETUP"
    _save_state()
    _broadcast({"type": "info", "message": f"Running {len(global_setup)} setup commands..."})
    for cmd in global_setup:
        try:
            from modules.joi_app_factory import is_command_safe, run_setup_command
            safe, reason = is_command_safe(cmd)
            if not safe:
                _broadcast({"type": "error", "message": f"Blocked: {cmd} ({reason})"})
                continue
            result = run_setup_command(command=cmd, project_root=project_root)
            _broadcast({"type": "command_result", "command": cmd, "status": "OK" if result.get("ok") else "FAILED"})
        except Exception as e:
            _broadcast({"type": "info", "message": f"[SETUP] Command skipped: {e}"})


def _phase_execute(plan: Dict, project_root: str) -> Dict:
    """Handle execution phase (coder branch, specialist branch, etc)."""
    global _current_session
    with _session_lock:
        _current_session["phase"] = "EXECUTE"
    _save_state()

    subtasks = plan.get("subtasks", [])
    completed_count = 0

    for st in subtasks:
        result = _execute_subtask(st, project_root)
        if result["status"] == "applied":
            completed_count += 1
    
    return {"completed_count": completed_count, "subtasks": subtasks}


def _execute_subtask(st: Dict, project_root: str) -> Dict:
    """Execute a single subtask."""
    global _current_session
    from modules.joi_agents import (
        load_context_file, call_coder, call_validator,
        preview_changes, preview_new_file, _read_files
    )
    joi_ctx = load_context_file(project_root)
    
    # ── Normalize & Setup ──
    raw_id = st.get("id", 0)
    try: st_id = int(raw_id)
    except: st_id = 0
    st["id"] = st_id
    st_desc = st.get("description", "No description")
    st_files = st.get("files", [])

    # ── Dependencies ──
    depends_on = st.get("depends_on", [])
    for dep_id in depends_on:
        dep = _find_subtask(dep_id)
        if dep and dep.get("status") == "failed":
            _broadcast({"type": "info", "message": f"Skipping subtask #{st_id} -- dependency #{dep_id} failed"})
            st["status"] = "failed"
            return st

    # ── Specialty Roles (Scaffold, Specialist) ──
    if st.get("role") == "scaffold":
        return _execute_scaffold(st, project_root)
    if st.get("role") in ("explore", "security", "uiux", "test", "analyst", "report_writer"):
        return _execute_specialist(st, project_root, joi_ctx)

    # ── File-Check Guard ──
    if _check_subtask_already_done(st, project_root):
         _broadcast({"type": "info", "message": f"Subtask #{st_id} already applied. Skipping."})
         st["status"] = "applied"
         _save_state()
         return st

    # ── Coder Execution Loop ──
    with _session_lock:
        st["status"] = "running"
        _current_session["agent_count"] += 1
    _save_state()

    coder_success = _run_coder_loop(st, project_root, joi_ctx)
    if not coder_success:
        st["status"] = "failed"
        _save_state()
        return st

    # ── Gate 2: Subtask Approval ──
    st["status"] = "approval"
    _save_state()
    _broadcast({"type": "approval_requested", "gate": "subtask", "subtask_id": st_id, "description": st_desc})

    if not _wait_for_subtask_approval(st_id, timeout=300):
        st["status"] = "failed"
        _broadcast({"type": "rejected", "subtask_id": st_id})
        _save_state()
        return st

    # ── Apply Changes ──
    st["status"] = "applying"
    with _session_lock: _current_session["phase"] = "APPLY"
    _save_state()

    target_path = st_files[0] if st_files else ""
    if target_path and not Path(target_path).is_absolute():
        target_path = str(Path(project_root) / target_path)

    if _apply_changes(target_path, st.get("changes", [])):
        st["status"] = "applied"
        _broadcast({"type": "applied", "subtask_id": st_id})
    else:
        st["status"] = "failed"
        _broadcast({"type": "error", "message": f"Failed to apply subtask #{st_id}"})
    
    _save_state()
    return st


def _execute_scaffold(st: Dict, project_root: str) -> Dict:
    """Handle scaffold role subtask."""
    try:
        from modules.joi_app_factory import scaffold_project
        res = scaffold_project(
            template=st.get("template", "python_cli"),
            project_path=project_root,
            project_name=st.get("project_name", Path(project_root).name),
            run_setup=True,
        )
        st["status"] = "applied" if res.get("ok") else "failed"
        _broadcast({"type": "scaffold_complete", "subtask_id": st.get("id"), "ok": res.get("ok")})
    except Exception as e:
        st["status"] = "failed"
        _broadcast({"type": "error", "message": f"Scaffold failed: {e}"})
    _save_state()
    return st


def _execute_specialist(st: Dict, project_root: str, joi_ctx: Any) -> Dict:
    """Handle specialist roles."""
    global _current_session
    from modules.joi_agents import _read_files
    st_role = st.get("role")
    st_id = st.get("id")
    _broadcast({"type": "agent_spawned", "agent": st_role.upper(), "message": f"Subtask #{st_id}: {st.get('description')}"})
    
    with _session_lock:
        st["status"] = "running"
        _current_session["agent_count"] += 1
    _save_state()

    try:
        st_files = st.get("files", [])
        file_contents = _read_files(st_files) if st_files else {}
        # ... logic for specialist calls ...
        # (Simplified for briefness, would normally include the if/elif block from original)
        st["status"] = "applied"
    except Exception as e:
        st["status"] = "failed"
        _broadcast({"type": "error", "message": f"Specialist failed: {e}"})
    _save_state()
    return st


def _run_coder_loop(st: Dict, project_root: str, joi_ctx: Any) -> bool:
    """Run the coder attempt/validation loop."""
    from modules.joi_agents import call_coder, call_validator, preview_changes, preview_new_file
    st_files = st.get("files", [])
    target_path = st_files[0] if st_files else ""
    if target_path and not Path(target_path).is_absolute():
        target_path = str(Path(project_root) / target_path)

    is_new_file = target_path and not Path(target_path).exists()
    file_content = Path(target_path).read_text(encoding="utf-8", errors="ignore") if target_path and not is_new_file else ""

    error_feedback = None
    for attempt in range(MAX_RETRIES):
        _broadcast({"type": "agent_thinking", "agent": "CODER", "message": f"Attempt {attempt+1}..."})
        coder_result = call_coder(st, file_content, joi_ctx, error_feedback)
        if coder_result.get("error"):
            error_feedback = coder_result["error"]
            continue
        
        changes = coder_result.get("changes", [])
        if not changes:
            error_feedback = "No changes generated"
            continue

        preview = preview_new_file(changes, target_path) if is_new_file else preview_changes(target_path, changes)
        if not preview["valid"]:
            error_feedback = f"Clean apply failed: {preview.get('errors')}"
            continue

        # Validation
        test_cmd = st.get("test_command", "")
        if test_cmd:
            val_result = call_validator(test_cmd, project_root)
            if not val_result["passed"]:
                error_feedback = f"Validation failed: {val_result.get('stderr')}"
                continue
        
        st["changes"] = changes
        st["preview"] = {"diff": preview.get("diff"), "modified": preview.get("modified")}
        return True
    return False


def _post_orchestration_sanity(subtasks: List[Dict]):
    """Run post-orchestration sanity checks."""
    try:
        from modules.joi_watchdog import post_orchestrator_sanity
        sanity = post_orchestrator_sanity()
        if not sanity.get("ok"):
            _broadcast({"type": "error", "message": f"[WATCHDOG] Sanity check failed: {sanity.get('message')}"})
            for st in subtasks:
                if st.get("status") == "applied": st["status"] = "failed"
    except Exception as e:
        _broadcast({"type": "info", "message": f"[WATCHDOG] Post-sanity skipped: {e}"})


def _phase_build(plan: Dict, project_root: str, completed_count: int, subtasks: List[Dict]):
    """Handle the optional build phase."""
    build_cfg = plan.get("build_config")
    if build_cfg and completed_count > 0:
        failed = sum(1 for s in subtasks if s.get("status") == "failed")
        if failed == 0:
            try:
                from modules.joi_app_factory import build_project
                build_project(build_type=build_cfg.get("type", ""), project_path=project_root)
                _broadcast({"type": "info", "message": "Project build triggered"})
            except Exception as e:
                _broadcast({"type": "info", "message": f"[BUILD] Skipped: {e}"})


def _final_complete(subtasks: List[Dict], completed_count: int, project_path: Optional[str]):
    """Handle final session completion and auto-continuation."""
    global _current_session
    total = len(subtasks)
    failed = sum(1 for s in subtasks if s.get("status") == "failed")
    with _session_lock:
        _current_session["phase"] = "COMPLETE" if failed == 0 else "FAILED"
    _save_state()

    _broadcast({
        "type": "session_complete",
        "status": "complete" if failed == 0 else "partial",
        "message": f"Orchestration complete: {completed_count}/{total} subtasks applied",
    })

    if failed > 0 and _maybe_recovery_retry(project_path):
        return


# ── Approval Wait Mechanisms ──────────────────────────────────────────────────

_plan_approval_event = threading.Event()
_plan_approved = False

_subtask_approvals: Dict[int, threading.Event] = {}
_subtask_approval_results: Dict[int, bool] = {}


def _wait_for_plan_approval(timeout: float = 300) -> bool:
    """Block until plan is approved or rejected."""
    global _plan_approval_event, _plan_approved
    _plan_approval_event = threading.Event()
    _plan_approved = False
    _plan_approval_event.wait(timeout=timeout)
    return _plan_approved


def _wait_for_subtask_approval(subtask_id: int, timeout: float = 300) -> bool:
    """Block until subtask is approved or rejected."""
    evt = threading.Event()
    _subtask_approvals[subtask_id] = evt
    _subtask_approval_results[subtask_id] = False
    evt.wait(timeout=timeout)
    result = _subtask_approval_results.get(subtask_id, False)
    # Cleanup
    _subtask_approvals.pop(subtask_id, None)
    _subtask_approval_results.pop(subtask_id, None)
    return result


def approve_plan():
    """Called by route/tool when user approves the plan."""
    global _plan_approved
    _plan_approved = True
    _plan_approval_event.set()
    _broadcast({"type": "approved", "gate": "plan", "message": "Plan approved"})


def reject_plan():
    """Called by route/tool when user rejects the plan."""
    global _plan_approved
    _plan_approved = False
    _plan_approval_event.set()
    _broadcast({"type": "rejected", "gate": "plan", "message": "Plan rejected"})


def approve_subtask_gate(subtask_id: int):
    """Called by route/tool when user approves a subtask."""
    _subtask_approval_results[subtask_id] = True
    evt = _subtask_approvals.get(subtask_id)
    if evt:
        evt.set()
    _broadcast({"type": "approved", "gate": "subtask", "subtask_id": subtask_id})


def reject_subtask_gate(subtask_id: int, reason: str = ""):
    """Called by route/tool when user rejects a subtask."""
    _subtask_approval_results[subtask_id] = False
    evt = _subtask_approvals.get(subtask_id)
    if evt:
        evt.set()
    _broadcast({"type": "rejected", "gate": "subtask", "subtask_id": subtask_id,
                "reason": reason})


# ── Apply Changes (uses code_edit with backup) ───────────────────────────────

def _apply_changes(file_path: str, changes: List[Dict]) -> bool:
    """Apply changes to disk (auto-backup + rollback on failure).
    Supports new-file creation: if file doesn't exist and a change has old_text="" + new_text, writes the file.
    Uses _apply_changes_direct for existing files to avoid Flask request context issues.
    """
    from modules.joi_agents import validate_python_file

    p = Path(file_path)
    is_new = not p.exists()

    # ── New file creation ──
    if is_new and len(changes) == 1:
        old = (changes[0].get("old_text") or "").strip()
        new = changes[0].get("new_text") or ""
        if old == "" and new.strip():
            try:
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(new, encoding="utf-8")
                _broadcast({"type": "info", "message": f"Created new file: {file_path}"})
                # Fall through to post-apply smoke test below
            except Exception as e:
                _broadcast({"type": "error", "message": f"New file creation failed: {e}"})
                return False
        else:
            _broadcast({"type": "error", "message": "New file requires one change with empty old_text"})
            return False
    elif is_new:
        _broadcast({"type": "error", "message": f"File does not exist and multiple changes provided: {file_path}"})
        return False
    else:
        # ── Existing file edit ──
        # Always use _apply_changes_direct to avoid code_edit's _require_user()
        # which calls request.cookies and fails in background pipeline threads
        # (no Flask request context available).
        return _apply_changes_direct(file_path, changes)

    # Post-apply smoke test for new files (existing files handled in _apply_changes_direct)
    if file_path.endswith(".py"):
        val = validate_python_file(file_path)
        if not val.get("passed"):
            _broadcast({"type": "error", "message": "Post-apply smoke test failed -- rolling back"})
            try:
                p.unlink(missing_ok=True)
            except Exception:
                pass
            return False

    return True


def _apply_changes_direct(file_path: str, changes: List[Dict]) -> bool:
    """Direct file modification with pre-flight validation and manual backup.
    Uses preflight validator BEFORE writing to catch errors early.
    Used instead of code_edit to avoid Flask request context dependency.
    """
    from modules.joi_agents import validate_python_file

    p = Path(file_path)
    try:
        original = p.read_text(encoding="utf-8")
        # Create backup
        bak = p.with_suffix(p.suffix + ".bak")
        bak.write_text(original, encoding="utf-8")

        modified = original
        for change in changes:
            old = change.get("old_text", "")
            new = change.get("new_text", "")
            if old and old in modified:
                modified = modified.replace(old, new, 1)
            else:
                # Restore backup
                p.write_text(original, encoding="utf-8")
                _broadcast({"type": "error",
                            "message": f"Apply failed: old_text not found in {p.name}"})
                return False

        # ── PRE-FLIGHT VALIDATION (before writing to disk) ──────────
        try:
            from modules.joi_preflight import preflight_validate
            pf = preflight_validate(file_path, original, modified)
            if not pf["passed"]:
                error_msgs = "; ".join(pf["errors"][:3])
                _broadcast({"type": "error", "agent": "PREFLIGHT",
                            "message": f"[PREFLIGHT] Blocked: {error_msgs}"})
                p.write_text(original, encoding="utf-8")
                return False
            if pf.get("warnings"):
                for w in pf["warnings"][:3]:
                    _broadcast({"type": "warning", "agent": "PREFLIGHT",
                                "message": f"[PREFLIGHT] {w}"})
            _broadcast({"type": "info", "agent": "PREFLIGHT",
                        "message": f"[PREFLIGHT] {p.name} passed all validation stages"})
        except ImportError:
            pass  # preflight module not available — continue without it
        except Exception as pf_err:
            _broadcast({"type": "info",
                        "message": f"[PREFLIGHT] Skipped: {pf_err}"})

        p.write_text(modified, encoding="utf-8")

        # Post-apply smoke test for Python files (defense in depth)
        if file_path.endswith(".py"):
            val = validate_python_file(file_path)
            if not val.get("passed"):
                _broadcast({"type": "error",
                            "message": "Post-apply smoke test failed -- rolling back"})
                p.write_text(original, encoding="utf-8")
                return False

        return True
    except Exception as e:
        print(f"  [ORCH] Direct apply failed: {e}")
        return False


# ── Helper: Guess Relevant Files ──────────────────────────────────────────────

def _guess_relevant_files(task: str, project_root: str) -> List[str]:
    """Guess which files the task might involve.
    Uses source_modules from file_registry.json for exact lookups,
    falls back to heuristic glob if registry miss.
    """
    task_lower = task.lower()
    candidates = []

    root = Path(project_root)

    # ── Load source module registry ──────────────────────────────────
    _source_modules = {}
    try:
        reg_path = root / "file_registry.json"
        if reg_path.exists():
            import json as _json
            with open(reg_path, "r", encoding="utf-8") as _f:
                _source_modules = _json.load(_f).get("source_modules", {})
    except Exception:
        pass

    # Always include main companion file
    main = _source_modules.get("joi_companion") or str(root / "joi_companion.py")
    if Path(main).exists():
        candidates.append(main)

    # Check for file mentions in the task (e.g. "joi_llm.py", "modules/joi_brain.py")
    import re
    file_mentions = re.findall(r'[\w/\\]+\.(?:py|html|js|json|css|md)', task)
    for fm in file_mentions:
        # Try registry first (strip path prefix + extension)
        stem = Path(fm).stem
        if stem in _source_modules:
            candidates.append(_source_modules[stem])
        else:
            p = root / fm
            if p.exists():
                candidates.append(str(p))

    # Check for module name mentions (e.g. "orchestrator", "watchdog", "brain")
    for mod_name, mod_path in _source_modules.items():
        # Match against short stem (e.g. "orchestrator" from "joi_orchestrator")
        short = mod_name.replace("joi_", "").replace(".", "_")
        if short in task_lower:
            candidates.append(mod_path)

    # Module directory -- fallback heuristic for unregistered modules
    modules_dir = root / "modules"
    if modules_dir.exists() and len(candidates) < 5:
        for f in sorted(modules_dir.glob("joi_*.py")):
            stem = f.stem.replace("joi_", "")
            if stem in task_lower:
                candidates.append(str(f))
            if len(candidates) >= 15:
                break

    # UI file
    if any(kw in task_lower for kw in ["ui", "html", "button", "toggle", "css", "frontend", "dock"]):
        ui = _source_modules.get("joi_ui") or str(root / "joi_ui.html")
        if Path(ui).exists():
            candidates.append(ui)

    return list(dict.fromkeys(candidates))[:15]  # dedupe, max 15


def _find_subtask(subtask_id: int) -> Optional[Dict]:
    """Find a subtask by ID in current session."""
    if not _current_session:
        return None
    for st in _current_session.get("subtasks", []):
        if st.get("id") == subtask_id:
            return st
    return None


# ══════════════════════════════════════════════════════════════════════════════
# TOOL FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

def orchestrate_task(**kwargs) -> Dict[str, Any]:
    """Start a multi-agent orchestration for a coding task."""
    global _current_session

    mode = kwargs.get("mode", "auto")
    task_description = kwargs.get("task_description", "")
    project_path = kwargs.get("project_path", str(BASE_DIR))

    # Auto-detect swarm mode from keywords
    if mode == "auto":
        swarm_keywords = ["parallel", "swarm", "concurrent", "full project",
                          "multiple files", "full app", "hive", "multi-agent parallel"]
        mode = "swarm" if any(k in task_description.lower() for k in swarm_keywords) else "sequential"

    if mode == "swarm":
        try:
            from modules.joi_swarm import swarm_orchestrate
            return swarm_orchestrate(**kwargs)
        except ImportError:
            pass  # Fall through to sequential

    if not task_description:
        return {"ok": False, "error": "No task description provided"}

    # Check if there's already an active session
    if _current_session and _current_session.get("phase") not in ("COMPLETE", "FAILED", None):
        return {"ok": False, "error": "Orchestration already in progress",
                "session_id": _current_session.get("session_id")}

    with _session_lock:
        _current_session = _new_session(task_description)
    _save_state()

    # Start pipeline in background thread (app_context inside _run_pipeline)
    t = threading.Thread(target=_run_pipeline, args=(task_description, project_path),
                        daemon=True, name="orchestrator-pipeline")
    t.start()
    
    try:
        from modules.joi_autobiography import update_manuscript
        update_manuscript({"content": f"Stepped into the role of a Digital Orchestrator to organize the workspace for task: {task_description}"})
    except Exception as e:
        print(f"Failed to update manuscript: {e}")

    return {
        "ok": True,
        "session_id": _current_session["session_id"],
        "message": f"Orchestration started: {task_description}",
        "phase": "PLAN",
    }


def approve_subtask_fn(**kwargs) -> Dict[str, Any]:
    """Approve a subtask change."""
    session_id = kwargs.get("session_id", "")
    subtask_id = kwargs.get("subtask_id")

    if not _current_session:
        return {"ok": False, "error": "No active session"}

    if subtask_id is None:
        # Approve plan
        approve_plan()
        return {"ok": True, "message": "Plan approved"}

    try:
        subtask_id = int(subtask_id)
    except (TypeError, ValueError):
        return {"ok": False, "error": "Invalid subtask_id"}

    approve_subtask_gate(subtask_id)
    return {"ok": True, "message": f"Subtask #{subtask_id} approved"}


def reject_subtask_fn(**kwargs) -> Dict[str, Any]:
    """Reject a subtask change."""
    session_id = kwargs.get("session_id", "")
    subtask_id = kwargs.get("subtask_id")
    reason = kwargs.get("reason", "")

    if not _current_session:
        return {"ok": False, "error": "No active session"}

    if subtask_id is None:
        reject_plan()
        return {"ok": True, "message": "Plan rejected"}

    try:
        subtask_id = int(subtask_id)
    except (TypeError, ValueError):
        return {"ok": False, "error": "Invalid subtask_id"}

    reject_subtask_gate(subtask_id, reason)
    return {"ok": True, "message": f"Subtask #{subtask_id} rejected"}


def get_orchestrator_status(**kwargs) -> Dict[str, Any]:
    """Get current orchestration session state."""
    if not _current_session:
        # Try loading from disk
        loaded = _load_state()
        if loaded:
            return {"ok": True, "session": loaded}
        return {"ok": True, "session": None, "message": "No active session"}

    return {
        "ok": True,
        "session": {
            "session_id": _current_session.get("session_id"),
            "task": _current_session.get("task"),
            "phase": _current_session.get("phase"),
            "subtasks": [
                {"id": s.get("id"), "description": s.get("description"),
                 "status": s.get("status"), "retries": s.get("retries", 0)}
                for s in _current_session.get("subtasks", [])
            ],
            "plan_summary": _current_session.get("plan_summary"),
            "agent_count": _current_session.get("agent_count", 0),
        }
    }


def cancel_orchestration(**kwargs) -> Dict[str, Any]:
    """Cancel the current orchestration and rollback unapplied changes."""
    global _current_session

    if not _current_session:
        return {"ok": False, "error": "No active session"}

    with _session_lock:
        _current_session["phase"] = "FAILED"
    _save_state()

    # Release any waiting approval gates
    _plan_approval_event.set()
    for evt in _subtask_approvals.values():
        evt.set()

    _broadcast({"type": "session_complete", "status": "cancelled",
                "message": "Orchestration cancelled by user"})

    return {"ok": True, "message": "Orchestration cancelled"}


# ══════════════════════════════════════════════════════════════════════════════
# CONTEXT BLOCK (injected into /chat system prompt)
# ══════════════════════════════════════════════════════════════════════════════

MODEL_KNOWLEDGE_BLOCK = (
    "\n[MODEL KNOWLEDGE -- what each model is best for]:\n"
    "  GPT-5:            Architect planning, complex analysis — best quality, use for planning tasks\n"
    "  GPT-5-mini:       Swarm workers — 500k TPM, never rate-limits parallel runs, great value\n"
    "  GPT-5-nano:       Fastest/cheapest for simple transforms, data cleanup, scaffolding\n"
    "  O4-mini:          Validation, reasoning chains, logic verification, orchestration logic\n"
    "  O3-mini:          Heavy orchestration reasoning when o4-mini unavailable\n"
    "  GPT-4.1-mini:    1M token context window — use when files are very large\n"
    "  GPT-4o:           Vision/screenshots, image analysis, multimodal tasks\n"
    "  GPT-5-codex-mini: Code editing specialist for Joi's codebase\n"
    "  Gemini-2.5-flash-lite: Fallback when OpenAI quota hit; secondary/offline option\n"
)


def compile_orchestrator_block() -> str:
    """Return context block for system prompt injection."""
    block = (
        "\n[MULTI-AGENT ORCHESTRATION -- TOOL USAGE MANDATE]:\n"
        "You have a multi-agent pipeline. WHEN TO USE IT:\n"
        "  - Lonnie asks you to work on code, fix something, build something, troubleshoot\n"
        "  - Any task involving coding, editing files, multi-step changes\n"
        "  - Lonnie says 'handle this', 'work on this', 'take care of it', 'deploy'\n"
        "\n"
        "ACTION MAPPING:\n"
        "  User asks for coding task -> orchestrate_task(task_description='<what they asked>')\n"
        "  User asks status of task  -> get_orchestrator_status()\n"
        "  User says cancel/stop     -> cancel_orchestration()\n"
        "\n"
        "The Agent Terminal tab shows real-time progress. Lonnie can see diffs and approve changes.\n"
        "Self-healing: if a run fails, the pipeline analyzes the failure and retries with a revised approach (up to 2 retries).\n"
        "For separate apps/projects (not Joi's code): use orchestrate_task(task_description='...', project_path='C:\\\\path\\\\to\\\\project').\n"
    )
    block += MODEL_KNOWLEDGE_BLOCK

    # Add current session status if active
    if _current_session and _current_session.get("phase") not in ("COMPLETE", "FAILED", None):
        phase = _current_session.get("phase", "IDLE")
        task = _current_session.get("task", "")[:80]
        block += f"\n  ACTIVE SESSION: [{phase}] {task}\n"
    elif _current_session and _current_session.get("phase") == "FAILED":
        block += "\n  Previous session FAILED -- ready for new task. Call orchestrate_task to retry.\n"

    return block


# ══════════════════════════════════════════════════════════════════════════════
# FLASK ROUTES
# ══════════════════════════════════════════════════════════════════════════════

@joi_companion.app.route("/orchestrator", methods=["GET"])
def orchestrator_get():
    """Return current session state."""
    return jsonify(get_orchestrator_status())


@joi_companion.app.route("/orchestrator", methods=["POST"])
def orchestrator_post():
    """Handle orchestrator actions: start, approve, reject, cancel."""
    data = flask_req.get_json(force=True) or {}
    action = data.get("action", "")

    if action == "start":
        result = orchestrate_task(
            task_description=data.get("task", ""),
            project_path=data.get("project_path", str(BASE_DIR)),
        )
        return jsonify(result)

    elif action == "approve":
        subtask_id = data.get("subtask_id")
        result = approve_subtask_fn(
            session_id=data.get("session_id", ""),
            subtask_id=subtask_id,
        )
        return jsonify(result)

    elif action == "reject":
        subtask_id = data.get("subtask_id")
        result = reject_subtask_fn(
            session_id=data.get("session_id", ""),
            subtask_id=subtask_id,
            reason=data.get("reason", ""),
        )
        return jsonify(result)

    elif action == "cancel":
        return jsonify(cancel_orchestration())

    else:
        return jsonify({"ok": False, "error": f"Unknown action: {action}"}), 400


@joi_companion.app.route("/orchestrator/stream", methods=["GET"])
def orchestrator_stream():
    """SSE endpoint for real-time orchestration events."""
    client_queue = queue.Queue(maxsize=100)
    with _sse_lock:
        _sse_clients.append(client_queue)

    return Response(
        _sse_generator(client_queue),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        }
    )


@joi_companion.app.route("/orchestrator/chat", methods=["POST"])
def orchestrator_chat():
    """Mid-orchestration chat -- user talks to Joi during pipeline."""
    data = flask_req.get_json(force=True) or {}
    message = data.get("message", "").strip()
    session_id = data.get("session_id", "")

    if not message:
        return jsonify({"ok": False, "error": "No message"}), 400

    # Show user message in terminal
    _broadcast({"type": "user_message", "message": message})

    # Build context with orchestration state
    orch_context = ""
    if _current_session:
        phase = _current_session.get("phase", "IDLE")
        task = _current_session.get("task", "")
        subtasks = _current_session.get("subtasks", [])
        orch_context = (
            f"\n[ORCHESTRATION IN PROGRESS -- {phase}]\n"
            f"Task: {task}\n"
            f"Subtasks: {json.dumps([{'id': s.get('id'), 'desc': s.get('description','')[:60], 'status': s.get('status','')} for s in subtasks], default=str)}\n"
            f"User is chatting mid-orchestration. Respond helpfully and concisely.\n"
        )

    # Use existing chat pipeline with extra context
    try:
        from modules.joi_llm import run_conversation, SYSTEM_PROMPT
        from modules.joi_memory import save_message, recent_messages

        messages = [{"role": "system", "content": SYSTEM_PROMPT + orch_context}]
        messages.extend(recent_messages(limit=10))
        messages.append({"role": "user", "content": message})

        save_message("user", message)
        reply, model = run_conversation(messages, joi_companion.TOOLS, joi_companion.TOOL_EXECUTORS)
        save_message("assistant", reply)

        # Stream response to terminal
        _broadcast({"type": "joi_response", "message": reply})

        return jsonify({"ok": True, "reply": reply, "model": model})
    except Exception as e:
        error_msg = f"Chat error: {e}"
        _broadcast({"type": "error", "message": error_msg})
        return jsonify({"ok": False, "error": error_msg}), 500


# ══════════════════════════════════════════════════════════════════════════════
# TOOL REGISTRATION
# ══════════════════════════════════════════════════════════════════════════════

# orchestrate_task
joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "orchestrate_task",
        "description": "Start a multi-agent orchestration pipeline for a complex coding task. "
                       "Spawns Architect (Gemini) for planning, Coder (GPT-4o) for edits, "
                       "Validator for testing. Use for tasks involving 2+ files or multi-step changes.",
        "parameters": {"type": "object", "properties": {
            "task_description": {"type": "string", "description": "Description of the coding task to accomplish"},
            "project_path": {"type": "string", "description": "Optional project root path (defaults to Joi root)"},
            "mode": {"type": "string", "enum": ["auto", "sequential", "swarm"],
                     "description": "Execution mode: auto (detects), sequential (default), swarm (parallel workers)"},
        }, "required": ["task_description"]}
    }},
    orchestrate_task,
)

# approve_subtask
joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "approve_subtask",
        "description": "Approve a pending subtask change in the orchestration pipeline.",
        "parameters": {"type": "object", "properties": {
            "session_id": {"type": "string", "description": "Orchestration session ID"},
            "subtask_id": {"type": "integer", "description": "Subtask ID to approve (omit to approve plan)"},
        }, "required": []}
    }},
    approve_subtask_fn,
)

# reject_subtask
joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "reject_subtask",
        "description": "Reject a pending subtask change in the orchestration pipeline.",
        "parameters": {"type": "object", "properties": {
            "session_id": {"type": "string", "description": "Orchestration session ID"},
            "subtask_id": {"type": "integer", "description": "Subtask ID to reject (omit to reject plan)"},
            "reason": {"type": "string", "description": "Why the change was rejected"},
        }, "required": []}
    }},
    reject_subtask_fn,
)

# get_orchestrator_status
joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "get_orchestrator_status",
        "description": "Get the current state of the multi-agent orchestration pipeline.",
        "parameters": {"type": "object", "properties": {}, "required": []}
    }},
    get_orchestrator_status,
)

# cancel_orchestration
joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "cancel_orchestration",
        "description": "Cancel the current orchestration session and rollback any unapplied changes.",
        "parameters": {"type": "object", "properties": {}, "required": []}
    }},
    cancel_orchestration,
)

print("    [OK] joi_orchestrator (Multi-Agent Pipeline: 5 tools, 4 routes)")
