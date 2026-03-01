"""
modules/joi_swarm.py

Queen/Worker Swarm Coordination Engine
========================================
Parallel multi-agent execution with:
  - Queen loop (background scheduler)
  - Worker threads (role-based agent dispatch)
  - Inter-agent messaging bus
  - Sequential verify+apply (prevents git conflicts)
  - LLM semaphore (caps concurrent API calls)

Tools: swarm_orchestrate, swarm_status, swarm_cancel, send_agent_message
Routes: GET/POST /swarm, GET /swarm/stream, GET /swarm/agent/<id>
"""

import json
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

# ── Constants ────────────────────────────────────────────────────────────────
MAX_PARALLEL_WORKERS = 10
MAX_CONCURRENT_LLM = 4

# ── State ────────────────────────────────────────────────────────────────────
_swarm_session: Optional[Dict] = None
_swarm_lock = threading.Lock()
_message_bus: List[Dict] = []
_bus_lock = threading.Lock()
_active_workers: Dict[str, Dict] = {}
_workers_lock = threading.Lock()
_llm_semaphore = threading.Semaphore(MAX_CONCURRENT_LLM)
_queen_thread: Optional[threading.Thread] = None
_queen_running = False


# ══════════════════════════════════════════════════════════════════════════════
# SSE — reuses orchestrator's broadcast infrastructure
# ══════════════════════════════════════════════════════════════════════════════

def _broadcast(event: Dict):
    """Broadcast event to orchestrator SSE clients."""
    try:
        from modules.joi_orchestrator import _broadcast as orch_broadcast
        orch_broadcast(event)
    except ImportError:
        pass  # orchestrator not loaded


# ══════════════════════════════════════════════════════════════════════════════
# INTER-AGENT MESSAGING
# ══════════════════════════════════════════════════════════════════════════════

def send_agent_message(**kwargs) -> Dict[str, Any]:
    """Send a message between agents. Security auditor -> Coder, etc."""
    from_agent = kwargs.get("from_agent", "unknown")
    to_agent = kwargs.get("to_agent", "all")
    message = kwargs.get("message", "")
    severity = kwargs.get("severity", "info")

    if not message:
        return {"ok": False, "error": "message is required"}

    msg = {
        "id": f"msg_{int(time.time()*1000)}",
        "from_agent": from_agent,
        "to_agent": to_agent,
        "message": message,
        "severity": severity,
        "timestamp": time.time(),
    }

    with _bus_lock:
        _message_bus.append(msg)
        # Keep last 100 messages
        if len(_message_bus) > 100:
            _message_bus[:] = _message_bus[-100:]

    _broadcast({
        "type": "agent_message",
        "from_agent": from_agent,
        "to_agent": to_agent,
        "message": message,
        "severity": severity,
    })

    return {"ok": True, "message_id": msg["id"]}


def get_messages_for(agent_id: str) -> List[Dict]:
    """Get messages addressed to this agent or 'all'."""
    with _bus_lock:
        return [m for m in _message_bus
                if m["to_agent"] in (agent_id, "all")]


# ══════════════════════════════════════════════════════════════════════════════
# WORKER FUNCTION — runs in thread, role-based routing
# ══════════════════════════════════════════════════════════════════════════════

def _worker_fn(worker_id: str, subtask: Dict, session: Dict):
    """Execute a single subtask in a worker thread."""
    role = subtask.get("role", "coder")
    task_id = subtask.get("id", 0)
    description = subtask.get("description", "")
    files = subtask.get("files", [])
    project_root = session.get("project_root", str(BASE_DIR))

    # Update worker state
    with _workers_lock:
        if worker_id in _active_workers:
            _active_workers[worker_id]["status"] = "running"
            _active_workers[worker_id]["history"].append({
                "event": "started", "time": time.time()
            })

    _broadcast({
        "type": "worker_claimed",
        "worker_id": worker_id,
        "role": role,
        "task_id": task_id,
        "description": description,
    })

    try:
        from modules.joi_agents import (
            call_explore, call_security_auditor, call_uiux_specialist,
            call_test_engineer, call_coder, call_analyst, call_report_writer,
            call_doc_writer, _read_files
        )

        # Read files for context
        file_contents = _read_files(files) if files else {}
        joi_ctx = session.get("joi_ctx", "")

        # Check for incoming inter-agent messages
        messages = get_messages_for(worker_id)
        extra_context = ""
        if messages:
            msg_texts = [f"[{m['from_agent']}→{m['to_agent']}] {m['message']}" for m in messages[-5:]]
            extra_context = "\n\nINTER-AGENT MESSAGES:\n" + "\n".join(msg_texts)

        # Acquire LLM semaphore before calling model
        _llm_semaphore.acquire()
        try:
            if role == "explore":
                result = call_explore(description + extra_context, file_contents, joi_ctx)
            elif role == "security":
                result = call_security_auditor(description + extra_context, file_contents)
                # If critical issues found, alert coders
                if result.get("issues"):
                    critical = [i for i in result["issues"]
                                if i.get("severity") in ("critical", "high")]
                    if critical:
                        send_agent_message(
                            from_agent=worker_id,
                            to_agent="all",
                            message=f"SECURITY ALERT: {len(critical)} critical/high issues found: "
                                    + "; ".join(i.get("description", "")[:80] for i in critical[:3]),
                            severity="critical",
                        )
            elif role == "uiux":
                result = call_uiux_specialist(description + extra_context, file_contents)
            elif role == "test":
                result = call_test_engineer(description + extra_context, file_contents, project_root)
            elif role == "analyst":
                result = call_analyst(description + extra_context, file_contents, joi_ctx)
            elif role == "report_writer":
                # Collect findings from other completed subtasks in this session
                findings = _collect_analyst_findings(session)
                result = call_report_writer(description + extra_context, findings, joi_ctx)
            elif role == "doc_writer":
                result = call_doc_writer(description + extra_context, file_contents, joi_ctx)
            elif role == "scaffold":
                try:
                    from modules.joi_app_factory import scaffold_project
                    result = scaffold_project(
                        template=subtask.get("template", "python_cli"),
                        project_path=project_root,
                        project_name=subtask.get("project_name", Path(project_root).name),
                        run_setup=True,
                    )
                except Exception as e:
                    result = {"ok": False, "error": str(e)}
            else:  # coder (default)
                file_content = ""
                if files:
                    target_path = files[0]
                    if not Path(target_path).is_absolute():
                        target_path = str(Path(project_root) / target_path)
                    if Path(target_path).exists():
                        try:
                            file_content = Path(target_path).read_text(encoding="utf-8")
                        except Exception:
                            file_content = ""

                # Include extra context in the subtask description
                if extra_context:
                    subtask = {**subtask, "description": description + extra_context}

                result = call_coder(subtask, file_content, joi_ctx)
        finally:
            _llm_semaphore.release()

        # Store result in subtask
        subtask["result"] = result
        subtask["status"] = "verifying"

        with _workers_lock:
            if worker_id in _active_workers:
                _active_workers[worker_id]["status"] = "complete"
                _active_workers[worker_id]["result"] = result
                _active_workers[worker_id]["history"].append({
                    "event": "complete", "time": time.time()
                })

        _broadcast({
            "type": "worker_complete",
            "worker_id": worker_id,
            "role": role,
            "task_id": task_id,
            "has_changes": bool(result.get("changes")),
            "summary": result.get("summary", result.get("error", "Done")),
        })

    except Exception as e:
        subtask["status"] = "failed"
        subtask["result"] = {"error": str(e)}

        with _workers_lock:
            if worker_id in _active_workers:
                _active_workers[worker_id]["status"] = "failed"
                _active_workers[worker_id]["error"] = str(e)

        _broadcast({
            "type": "worker_complete",
            "worker_id": worker_id,
            "role": role,
            "task_id": task_id,
            "has_changes": False,
            "summary": f"Error: {e}",
        })


# ══════════════════════════════════════════════════════════════════════════════
# VERIFICATION + APPLY — called by Queen SEQUENTIALLY
# ══════════════════════════════════════════════════════════════════════════════

def _verify_and_apply(subtask: Dict, session: Dict) -> bool:
    """Verify and apply a completed worker's changes. Returns True if applied."""
    role = subtask.get("role", "coder")
    task_id = subtask.get("id", 0)
    result = subtask.get("result", {})
    project_root = session.get("project_root", str(BASE_DIR))

    # Non-code roles: informational only, mark done
    if role in ("explore", "security", "uiux", "test", "analyst", "report_writer"):
        subtask["status"] = "applied"
        return True

    # Scaffold: already applied during worker
    if role == "scaffold":
        subtask["status"] = "applied" if result.get("ok") else "failed"
        return result.get("ok", False)

    # Coder role: verify + apply changes
    changes = result.get("changes", [])
    if not changes:
        subtask["status"] = "failed"
        _broadcast({"type": "worker_blocked", "task_id": task_id,
                     "reason": "No changes produced"})
        return False

    files = subtask.get("files", [])
    if not files:
        subtask["status"] = "failed"
        return False

    target_path = files[0]
    if not Path(target_path).is_absolute():
        target_path = str(Path(project_root) / target_path)

    is_new_file = not Path(target_path).exists()

    # Preview changes
    from modules.joi_agents import preview_changes, preview_new_file
    if is_new_file:
        preview = preview_new_file(changes, target_path)
    else:
        preview = preview_changes(target_path, changes)

    if not preview["valid"]:
        subtask["status"] = "failed"
        _broadcast({"type": "worker_blocked", "task_id": task_id,
                     "reason": f"Changes don't apply: {preview.get('errors', [])}"})
        return False

    # Broadcast diff
    _broadcast({
        "type": "diff_ready",
        "subtask_id": task_id,
        "diff": preview.get("diff", ""),
        "file_path": target_path,
        "confidence": result.get("confidence", 50),
        "changes": changes,
    })

    # Architect gate evaluation
    try:
        from modules.joi_architect import _evaluate_change
        eval_result = _evaluate_change(
            subtask.get("description", ""),
            target_path,
            "orchestration",
        )
        if eval_result.get("avg_score", 7) < 6.0:
            subtask["status"] = "failed"
            _broadcast({"type": "worker_blocked", "task_id": task_id,
                         "reason": f"Architect blocked (score {eval_result.get('avg_score', 0):.1f}): "
                                   f"{eval_result.get('reason', 'Below threshold')}"})
            return False
    except ImportError:
        pass  # Architect not available, skip gate

    # Apply changes to disk
    try:
        from modules.joi_orchestrator import _apply_changes
        success = _apply_changes(target_path, changes)
    except ImportError:
        success = False

    if not success:
        subtask["status"] = "failed"
        _broadcast({"type": "worker_blocked", "task_id": task_id,
                     "reason": "Failed to apply changes to disk"})
        return False

    # Watchdog sanity check
    try:
        from modules.joi_watchdog import run_sanity_check
        sanity = run_sanity_check()
        if not sanity.get("ok"):
            try:
                from modules.joi_watchdog import _git_revert_hard
                _git_revert_hard()
            except Exception:
                pass
            subtask["status"] = "failed"
            _broadcast({"type": "worker_reverted", "task_id": task_id,
                         "reason": "Watchdog sanity check failed -- reverted"})
            return False
    except ImportError:
        pass  # Watchdog not available

    subtask["status"] = "applied"
    _broadcast({"type": "applied", "subtask_id": task_id,
                "message": f"Subtask #{task_id} applied successfully"})
    return True


# ══════════════════════════════════════════════════════════════════════════════
# QUEEN LOOP — background scheduler
# ══════════════════════════════════════════════════════════════════════════════

def _queen_loop():
    """Background thread: dispatch workers, collect results, verify+apply."""
    global _swarm_session, _queen_running

    while _queen_running and _swarm_session:
        session = _swarm_session
        subtasks = session.get("subtasks", [])

        if not subtasks:
            time.sleep(0.5)
            continue

        # Count active workers
        active_count = 0
        with _workers_lock:
            active_count = sum(1 for w in _active_workers.values()
                               if w.get("status") in ("running", "verifying"))

        # Find claimable tasks
        for st in subtasks:
            if st.get("status") != "pending":
                continue

            # Check dependencies resolved
            depends_on = st.get("depends_on", [])
            deps_ok = True
            for dep_id in depends_on:
                dep = next((s for s in subtasks if s.get("id") == dep_id), None)
                if dep and dep.get("status") not in ("applied", "complete"):
                    deps_ok = False
                    break
                if dep and dep.get("status") == "failed":
                    st["status"] = "failed"
                    _broadcast({"type": "worker_blocked", "task_id": st.get("id"),
                                 "reason": f"Dependency #{dep_id} failed"})
                    deps_ok = False
                    break

            if not deps_ok:
                continue

            # Dispatch if under limit
            if active_count >= MAX_PARALLEL_WORKERS:
                break

            _dispatch_worker(st, session)
            active_count += 1

        # Collect completed workers and verify+apply SEQUENTIALLY
        completed_workers = []
        with _workers_lock:
            for wid, wdata in list(_active_workers.items()):
                if wdata.get("status") == "complete":
                    completed_workers.append((wid, wdata))

        for wid, wdata in completed_workers:
            task_id = wdata.get("task_id")
            st = next((s for s in subtasks if s.get("id") == task_id), None)
            if st and st.get("status") == "verifying":
                _verify_and_apply(st, session)

            with _workers_lock:
                _active_workers.pop(wid, None)

        # Broadcast task list update
        _broadcast({
            "type": "swarm_task_list",
            "tasks": [
                {"id": s.get("id"), "description": s.get("description", "")[:80],
                 "role": s.get("role", "coder"), "status": s.get("status", "pending"),
                 "claimed_by": s.get("claimed_by", "")}
                for s in subtasks
            ],
        })

        # Check if all tasks resolved
        all_resolved = all(s.get("status") in ("applied", "failed", "complete")
                           for s in subtasks)
        if all_resolved:
            completed = sum(1 for s in subtasks if s.get("status") == "applied")
            failed = sum(1 for s in subtasks if s.get("status") == "failed")

            # Build phase
            build_cfg = session.get("build_config")
            if build_cfg and completed > 0 and failed == 0:
                try:
                    from modules.joi_app_factory import build_project
                    build_result = build_project(
                        build_type=build_cfg.get("type", ""),
                        project_path=session.get("project_root", str(BASE_DIR)),
                        entry_point=build_cfg.get("entry_point", ""),
                    )
                    _broadcast({"type": "build_complete", "ok": build_result.get("ok"),
                                "message": build_result.get("message", "Build done")})
                except Exception as e:
                    _broadcast({"type": "info", "message": f"[BUILD] Skipped: {e}"})

            with _swarm_lock:
                if _swarm_session:
                    _swarm_session["phase"] = "COMPLETE" if failed == 0 else "FAILED"

            _broadcast({
                "type": "swarm_complete",
                "status": "complete" if failed == 0 else "partial",
                "message": f"Swarm complete: {completed}/{len(subtasks)} applied"
                           + (f" ({failed} failed)" if failed else ""),
                "completed": completed,
                "total": len(subtasks),
                "failed": failed,
            })
            _queen_running = False
            break

        time.sleep(0.5)


def _collect_analyst_findings(session: Dict) -> Dict[str, Any]:
    """Collect findings from completed analyst/explore/security subtasks in this session."""
    findings: Dict[str, Any] = {}
    for st in session.get("subtasks", []):
        role = st.get("role", "coder")
        if role in ("analyst", "explore", "security", "uiux", "test") and st.get("result"):
            findings[f"{role}_{st.get('id', 0)}"] = st["result"]
    return findings


def _dispatch_worker(subtask: Dict, session: Dict):
    """Create and start a worker thread for a subtask."""
    role = subtask.get("role", "coder")
    task_id = subtask.get("id", 0)
    worker_id = f"{role}_{task_id}"

    subtask["status"] = "claimed"
    subtask["claimed_by"] = worker_id

    with _workers_lock:
        _active_workers[worker_id] = {
            "thread": None,
            "role": role,
            "task_id": task_id,
            "status": "spawned",
            "history": [{"event": "spawned", "time": time.time()}],
            "result": None,
            "error": None,
        }

    _broadcast({
        "type": "worker_spawned",
        "worker_id": worker_id,
        "role": role,
        "task_id": task_id,
        "description": subtask.get("description", "")[:80],
    })

    t = threading.Thread(
        target=_worker_fn,
        args=(worker_id, subtask, session),
        daemon=True,
        name=f"swarm-worker-{worker_id}",
    )

    with _workers_lock:
        _active_workers[worker_id]["thread"] = t

    t.start()


# ══════════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

def swarm_orchestrate(**kwargs) -> Dict[str, Any]:
    """Start a swarm orchestration for a coding task."""
    global _swarm_session, _queen_running, _queen_thread

    task_description = kwargs.get("task_description", "")
    project_path = kwargs.get("project_path", str(BASE_DIR))

    if not task_description:
        return {"ok": False, "error": "No task description provided"}

    # Check for active session
    if _swarm_session and _swarm_session.get("phase") not in ("COMPLETE", "FAILED", None):
        return {"ok": False, "error": "Swarm session already in progress",
                "session_id": _swarm_session.get("session_id")}

    # Clean up previous state
    with _swarm_lock:
        _swarm_session = {
            "session_id": f"swarm_{int(time.time()*1000)}",
            "task": task_description,
            "phase": "PLAN",
            "subtasks": [],
            "plan_summary": "",
            "project_root": project_path,
            "joi_ctx": "",
            "build_config": None,
            "created_at": time.time(),
        }

    with _workers_lock:
        _active_workers.clear()

    with _bus_lock:
        _message_bus.clear()

    _broadcast({"type": "info", "message": f"[SWARM] Starting: {task_description}"})

    # Run planning + queen in background thread
    app = joi_companion.app

    def _swarm_main():
        global _swarm_session, _queen_running
        with app.app_context():
            try:
                _swarm_plan_and_run(task_description, project_path)
            except Exception as e:
                with _swarm_lock:
                    if _swarm_session:
                        _swarm_session["phase"] = "FAILED"
                _broadcast({"type": "error", "message": f"Swarm crashed: {e}"})
                _broadcast({"type": "swarm_complete", "status": "failed",
                            "message": f"Swarm crashed: {e}"})
                traceback.print_exc()

    _queen_thread = threading.Thread(target=_swarm_main, daemon=True, name="swarm-queen")
    _queen_thread.start()

    return {
        "ok": True,
        "session_id": _swarm_session["session_id"],
        "message": f"Swarm orchestration started: {task_description}",
        "phase": "PLAN",
    }


def _swarm_plan_and_run(task: str, project_path: str):
    """Plan with architect, then start queen loop."""
    global _swarm_session, _queen_running

    from modules.joi_agents import load_context_file, call_architect, _read_files

    project_root = project_path or str(BASE_DIR)
    joi_ctx = load_context_file(project_path)

    with _swarm_lock:
        if _swarm_session:
            _swarm_session["joi_ctx"] = joi_ctx

    # Guess relevant files
    try:
        from modules.joi_orchestrator import _guess_relevant_files
        candidate_files = _guess_relevant_files(task, project_root)
    except ImportError:
        candidate_files = []

    file_contents = _read_files(candidate_files)

    _broadcast({"type": "agent_spawned", "agent": "ARCHITECT", "model": "Brain Router",
                "message": "Spawning Architect for swarm planning..."})

    plan = call_architect(task, file_contents, joi_ctx, project_root)

    if plan.get("error"):
        with _swarm_lock:
            if _swarm_session:
                _swarm_session["phase"] = "FAILED"
        _broadcast({"type": "error", "agent": "ARCHITECT",
                    "message": f"Architect failed: {plan['error']}"})
        _broadcast({"type": "swarm_complete", "status": "failed",
                    "message": "Planning phase failed"})
        return

    # Store plan
    subtasks = plan.get("subtasks", [])
    for st in subtasks:
        st.setdefault("status", "pending")
        st.setdefault("claimed_by", "")
        st.setdefault("result", None)
        st.setdefault("role", "coder")

    with _swarm_lock:
        if _swarm_session:
            _swarm_session["subtasks"] = subtasks
            _swarm_session["plan_summary"] = plan.get("plan_summary", "")
            _swarm_session["build_config"] = plan.get("build_config")
            _swarm_session["phase"] = "EXECUTE"

    _broadcast({
        "type": "plan_generated",
        "plan_summary": plan.get("plan_summary", ""),
        "subtask_count": len(subtasks),
        "risk": plan.get("risk_assessment", "Unknown"),
        "subtasks": [{"id": s.get("id"), "description": s.get("description", ""),
                      "role": s.get("role", "coder")}
                     for s in subtasks],
    })

    # Run global setup commands
    global_setup = plan.get("global_setup_commands", [])
    if global_setup:
        _broadcast({"type": "info", "message": f"Running {len(global_setup)} setup commands..."})
        for cmd in global_setup:
            try:
                from modules.joi_app_factory import is_command_safe, run_setup_command
                safe, reason = is_command_safe(cmd)
                if not safe:
                    _broadcast({"type": "error", "message": f"Blocked: {cmd} ({reason})"})
                    continue
                result = run_setup_command(command=cmd, project_root=project_root)
                _broadcast({"type": "command_result", "command": cmd,
                            "status": "OK" if result.get("ok") else "FAILED"})
            except Exception as e:
                _broadcast({"type": "info", "message": f"[SETUP] Skipped: {e}"})

    # Broadcast initial task list
    _broadcast({
        "type": "swarm_task_list",
        "tasks": [{"id": s.get("id"), "description": s.get("description", "")[:80],
                    "role": s.get("role", "coder"), "status": "pending", "claimed_by": ""}
                   for s in subtasks],
    })

    # Start queen loop
    _queen_running = True
    _queen_loop()


# ══════════════════════════════════════════════════════════════════════════════
# STATUS + CANCEL
# ══════════════════════════════════════════════════════════════════════════════

def swarm_status(**kwargs) -> Dict[str, Any]:
    """Get current swarm session state."""
    if not _swarm_session:
        return {"ok": True, "session": None, "message": "No active swarm session"}

    with _workers_lock:
        workers = {
            wid: {"role": w["role"], "task_id": w["task_id"],
                   "status": w["status"]}
            for wid, w in _active_workers.items()
        }

    return {
        "ok": True,
        "session": {
            "session_id": _swarm_session.get("session_id"),
            "task": _swarm_session.get("task"),
            "phase": _swarm_session.get("phase"),
            "subtasks": [
                {"id": s.get("id"), "description": s.get("description", "")[:80],
                 "role": s.get("role", "coder"), "status": s.get("status"),
                 "claimed_by": s.get("claimed_by", "")}
                for s in _swarm_session.get("subtasks", [])
            ],
            "active_workers": workers,
            "message_count": len(_message_bus),
        }
    }


def swarm_cancel(**kwargs) -> Dict[str, Any]:
    """Cancel the current swarm session."""
    global _queen_running, _swarm_session

    if not _swarm_session:
        return {"ok": False, "error": "No active swarm session"}

    _queen_running = False
    with _swarm_lock:
        if _swarm_session:
            _swarm_session["phase"] = "FAILED"

    _broadcast({"type": "swarm_complete", "status": "cancelled",
                "message": "Swarm cancelled by user"})

    return {"ok": True, "message": "Swarm session cancelled"}


# ══════════════════════════════════════════════════════════════════════════════
# CONTEXT BLOCK (injected into /chat system prompt)
# ══════════════════════════════════════════════════════════════════════════════

def compile_swarm_block() -> str:
    """Return context block for system prompt injection."""
    block = (
        "\n[SWARM COORDINATION]:\n"
        "You have a parallel swarm mode for multi-agent tasks.\n"
        "  - swarm_orchestrate: Start parallel execution with Queen/Worker pattern\n"
        "  - swarm_status: Check active swarm session\n"
        "  - swarm_cancel: Cancel active swarm\n"
        "  - send_agent_message: Send inter-agent messages\n"
        "Use swarm for large tasks (multiple files, full apps). Sequential mode is default.\n"
    )

    if _swarm_session and _swarm_session.get("phase") not in ("COMPLETE", "FAILED", None):
        phase = _swarm_session.get("phase", "IDLE")
        task = _swarm_session.get("task", "")[:80]
        block += f"\n  ACTIVE SWARM: [{phase}] {task}\n"

    return block


# ══════════════════════════════════════════════════════════════════════════════
# FLASK ROUTES
# ══════════════════════════════════════════════════════════════════════════════

@joi_companion.app.route("/swarm", methods=["GET"])
def swarm_get():
    """Return current swarm session state."""
    return jsonify(swarm_status())


@joi_companion.app.route("/swarm", methods=["POST"])
def swarm_post():
    """Handle swarm actions: start, cancel."""
    data = flask_req.get_json(force=True) or {}
    action = data.get("action", "start")

    if action == "start":
        return jsonify(swarm_orchestrate(
            task_description=data.get("task", ""),
            project_path=data.get("project_path", str(BASE_DIR)),
        ))
    elif action == "cancel":
        return jsonify(swarm_cancel())
    else:
        return jsonify({"ok": False, "error": f"Unknown action: {action}"}), 400


@joi_companion.app.route("/swarm/stream", methods=["GET"])
def swarm_stream():
    """SSE endpoint for swarm events (reuses orchestrator stream)."""
    try:
        from modules.joi_orchestrator import _sse_clients, _sse_lock, _sse_generator
        client_queue = queue.Queue(maxsize=100)
        with _sse_lock:
            _sse_clients.append(client_queue)
        return Response(
            _sse_generator(client_queue),
            mimetype="text/event-stream",
            headers={"Cache-Control": "no-cache", "Connection": "keep-alive",
                     "X-Accel-Buffering": "no"},
        )
    except ImportError:
        return jsonify({"ok": False, "error": "Orchestrator not available"}), 500


@joi_companion.app.route("/swarm/agent/<agent_id>", methods=["GET"])
def swarm_agent_detail(agent_id):
    """Get detailed info for a specific worker agent."""
    with _workers_lock:
        worker = _active_workers.get(agent_id)
        if worker:
            return jsonify({
                "ok": True,
                "agent_id": agent_id,
                "role": worker.get("role"),
                "task_id": worker.get("task_id"),
                "status": worker.get("status"),
                "history": worker.get("history", []),
                "error": worker.get("error"),
            })

    # Check completed tasks for this worker
    if _swarm_session:
        for st in _swarm_session.get("subtasks", []):
            if st.get("claimed_by") == agent_id:
                return jsonify({
                    "ok": True,
                    "agent_id": agent_id,
                    "role": st.get("role", "coder"),
                    "task_id": st.get("id"),
                    "status": st.get("status"),
                    "result_summary": str(st.get("result", {}))[:500],
                    "messages": get_messages_for(agent_id),
                })

    return jsonify({"ok": False, "error": "Agent not found"}), 404


# ══════════════════════════════════════════════════════════════════════════════
# TOOL REGISTRATION
# ══════════════════════════════════════════════════════════════════════════════

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "swarm_orchestrate",
        "description": "Start a parallel swarm orchestration (Queen/Worker pattern) for complex multi-file tasks. "
                       "Workers run in parallel with LLM semaphore. Changes are verified and applied sequentially.",
        "parameters": {"type": "object", "properties": {
            "task_description": {"type": "string", "description": "Description of the coding task"},
            "project_path": {"type": "string", "description": "Optional project root path"},
        }, "required": ["task_description"]},
    }},
    swarm_orchestrate,
)

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "swarm_status",
        "description": "Get the current state of the swarm orchestration session.",
        "parameters": {"type": "object", "properties": {}, "required": []},
    }},
    swarm_status,
)

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "swarm_cancel",
        "description": "Cancel the active swarm session and stop all workers.",
        "parameters": {"type": "object", "properties": {}, "required": []},
    }},
    swarm_cancel,
)

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "send_agent_message",
        "description": "Send a message between swarm agents (e.g., security alert to coders).",
        "parameters": {"type": "object", "properties": {
            "from_agent": {"type": "string", "description": "Sender agent ID"},
            "to_agent": {"type": "string", "description": "Recipient agent ID or 'all'"},
            "message": {"type": "string", "description": "Message content"},
            "severity": {"type": "string", "enum": ["info", "warning", "critical"],
                        "description": "Message severity level"},
        }, "required": ["message"]},
    }},
    send_agent_message,
)

print("    [OK] joi_swarm (Swarm Engine: 4 tools, 4 routes, 3 new roles: analyst/report_writer/doc_writer)")
