"""
modules/joi_watchdog.py

Git Safety Watchdog -- Circuit Breaker for Self-Editing
=======================================================
Wraps all of Joi's self-modification operations with a Git safety net:

  1. PRE-EDIT:  Auto-commit current state ("AI Backup: Pre-flight save before self-edit")
  2. EXECUTE:   Perform the actual code change
  3. VALIDATE:  Run sanity_check.py
  4. CIRCUIT BREAKER: If sanity check fails -> git reset --hard HEAD (instant revert)

This ensures that no amount of "hallucination loops" or broken self-repairs
can permanently damage Joi's codebase. The .git folder is an immutable
time machine of her past selves.

Tools:
  - watchdog_status: Check watchdog state, recent activity, git status
  - manual_checkpoint: Create a named git checkpoint
  - manual_revert: Revert to last checkpoint

Routes:
  - GET /watchdog: Status JSON
  - POST /watchdog: Actions (checkpoint, revert, toggle)
"""

import json
import os
import subprocess
import threading
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import joi_companion
from flask import jsonify, request as flask_req

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
STAGING_DIR = BASE_DIR / "staging"
STAGING_DIR.mkdir(exist_ok=True)
WATCHDOG_LOG_PATH = DATA_DIR / "watchdog_log.json"
SANITY_CHECK_PATH = BASE_DIR / "sanity_check.py"

# ── Configuration ────────────────────────────────────────────────────────────
WATCHDOG_ENABLED = True
MAX_LOG_ENTRIES = 100
HEALTH_CHECK_TIMEOUT = 30  # seconds
AUTO_COMMIT_COOLDOWN = 5   # seconds between auto-commits (prevent spam)

# ── State ────────────────────────────────────────────────────────────────────
_watchdog_lock = threading.Lock()
_last_commit_time = 0.0
_activity_log: List[Dict] = []
_circuit_broken = False  # True if last edit caused a revert


def _load_log():
    """Load activity log from disk."""
    global _activity_log
    try:
        if WATCHDOG_LOG_PATH.exists():
            with open(WATCHDOG_LOG_PATH, "r", encoding="utf-8") as f:
                _activity_log = json.load(f)
    except Exception:
        _activity_log = []


def _save_log():
    """Persist activity log to disk."""
    try:
        with open(WATCHDOG_LOG_PATH, "w", encoding="utf-8") as f:
            json.dump(_activity_log[-MAX_LOG_ENTRIES:], f, indent=2, default=str)
    except Exception as e:
        print(f"  [WATCHDOG] Log save failed: {e}")


def _log_event(event_type: str, detail: str, success: bool = True):
    """Record a watchdog event."""
    entry = {
        "time": time.time(),
        "type": event_type,
        "detail": detail,
        "success": success,
    }
    _activity_log.append(entry)
    if len(_activity_log) > MAX_LOG_ENTRIES:
        _activity_log.pop(0)
    _save_log()
    icon = "[OK]" if success else "[FAIL]"
    print(f"  [WATCHDOG] {icon} {event_type}: {detail}")


_load_log()


# ══════════════════════════════════════════════════════════════════════════════
# GIT OPERATIONS
# ══════════════════════════════════════════════════════════════════════════════

def _git(cmd: str, timeout: int = 15) -> Dict[str, Any]:
    """Run a git command in the project root. Returns {ok, stdout, stderr, code}."""
    try:
        result = subprocess.run(
            f"git {cmd}",
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(BASE_DIR),
        )
        return {
            "ok": result.returncode == 0,
            "stdout": (result.stdout or "").strip(),
            "stderr": (result.stderr or "").strip(),
            "code": result.returncode,
        }
    except subprocess.TimeoutExpired:
        return {"ok": False, "stdout": "", "stderr": "Git command timed out", "code": -1}
    except Exception as e:
        return {"ok": False, "stdout": "", "stderr": str(e), "code": -1}


def _git_has_changes() -> bool:
    """Check if there are uncommitted changes in tracked files."""
    result = _git("status --porcelain")
    if not result["ok"]:
        return False
    # Filter to only tracked/modified files (not untracked '??')
    lines = [l for l in result["stdout"].split("\n") if l.strip() and not l.startswith("??")]
    return len(lines) > 0


def _git_auto_commit(message: str = "AI Backup: Pre-flight save before self-edit") -> bool:
    """
    Auto-commit all changes with the given message.
    Returns True if commit was made (or nothing to commit).
    Respects cooldown to prevent commit spam.
    """
    global _last_commit_time

    if not WATCHDOG_ENABLED:
        return True

    now = time.time()
    if now - _last_commit_time < AUTO_COMMIT_COOLDOWN:
        return True  # Too soon, skip (previous commit is recent enough)

    with _watchdog_lock:
        # Stage tracked files only (not untracked)
        _git("add -u")

        if not _git_has_changes():
            return True  # Nothing to commit

        result = _git(f'commit -m "{message}"', timeout=30)
        if result["ok"]:
            _last_commit_time = time.time()
            _log_event("AUTO_COMMIT", message)
            return True
        else:
            _log_event("AUTO_COMMIT_FAIL", result["stderr"], success=False)
            return False


def _git_revert_hard() -> bool:
    """
    CIRCUIT BREAKER: git reset --hard HEAD
    Reverts ALL changes to the last commit.
    This is the nuclear option -- only used when sanity check fails.
    """
    global _circuit_broken
    with _watchdog_lock:
        result = _git("reset --hard HEAD")
        if result["ok"]:
            _circuit_broken = True
            _log_event("CIRCUIT_BREAKER", "Reverted to last commit via git reset --hard HEAD")
            return True
        else:
            _log_event("REVERT_FAIL", result["stderr"], success=False)
            return False


def _git_get_head_hash() -> str:
    """Get current HEAD commit hash."""
    result = _git("rev-parse --short HEAD")
    return result["stdout"] if result["ok"] else "unknown"


def _git_get_log(count: int = 5) -> List[str]:
    """Get recent git log entries."""
    result = _git(f"log --oneline -{count}")
    if result["ok"]:
        return result["stdout"].split("\n")
    return []


# ══════════════════════════════════════════════════════════════════════════════
# SANITY CHECK RUNNER
# ══════════════════════════════════════════════════════════════════════════════

def run_sanity_check() -> Dict[str, Any]:
    """
    Run sanity_check.py and return results.
    Uses the same Python that's running Joi (sys.executable).
    """
    import sys

    if not SANITY_CHECK_PATH.exists():
        return {"passed": False, "error": "sanity_check.py not found"}

    try:
        result = subprocess.run(
            [sys.executable, str(SANITY_CHECK_PATH)],
            capture_output=True,
            text=True,
            timeout=HEALTH_CHECK_TIMEOUT,
            cwd=str(BASE_DIR),
        )
        return {
            "passed": result.returncode == 0,
            "exit_code": result.returncode,
            "stdout": (result.stdout or "")[-2000:],  # last 2K chars
            "stderr": (result.stderr or "")[-500:],
        }
    except subprocess.TimeoutExpired:
        return {"passed": False, "error": f"Sanity check timed out ({HEALTH_CHECK_TIMEOUT}s)"}
    except Exception as e:
        return {"passed": False, "error": str(e)}


# ══════════════════════════════════════════════════════════════════════════════
# SAFE EDIT WRAPPER -- The Core Safety Net
# ══════════════════════════════════════════════════════════════════════════════

def safe_edit(edit_fn, *args, **kwargs) -> Dict[str, Any]:
    """
    Wrap ANY code modification function with the Git safety net.

    Flow:
      1. git commit -am "AI Backup: Pre-flight save before self-edit"
      2. Call edit_fn(*args, **kwargs)
      3. Run sanity_check.py
      4. If sanity fails -> git reset --hard HEAD

    Returns the edit function's result, plus watchdog metadata.
    """
    global _circuit_broken

    if not WATCHDOG_ENABLED:
        return edit_fn(*args, **kwargs)

    # Step 1: Pre-flight commit
    pre_hash = _git_get_head_hash()
    _git_auto_commit("AI Backup: Pre-flight save before self-edit")
    checkpoint_hash = _git_get_head_hash()

    # Broadcast to terminal if orchestrator is active (need app context in background/edit context)
    try:
        from modules.joi_orchestrator import _broadcast
        with joi_companion.app.app_context():
            _broadcast({"type": "info", "message": f"[WATCHDOG] Pre-flight checkpoint: {checkpoint_hash}"})
    except Exception:
        pass

    # Step 2: Execute the edit
    try:
        result = edit_fn(*args, **kwargs)
    except Exception as e:
        _log_event("EDIT_EXCEPTION", str(e), success=False)
        # Revert on exception
        _git_revert_hard()
        return {"ok": False, "error": f"Edit threw exception: {e}", "watchdog": "reverted"}

    # Step 3: Sanity check
    sanity = run_sanity_check()

    if sanity.get("passed"):
        _circuit_broken = False
        _log_event("SAFE_EDIT_OK", f"Edit passed sanity check (commit {checkpoint_hash})")

        # Enrich result with watchdog metadata
        if isinstance(result, dict):
            result["watchdog"] = {
                "status": "healthy",
                "checkpoint": checkpoint_hash,
                "sanity_passed": True,
            }
        return result

    else:
        # Step 4: CIRCUIT BREAKER -- Revert!
        _log_event("SANITY_FAILED", f"Sanity check failed -- reverting to {checkpoint_hash}",
                    success=False)

        reverted = _git_revert_hard()

        # Broadcast revert to terminal (app context for Flask)
        try:
            from modules.joi_orchestrator import _broadcast
            with joi_companion.app.app_context():
                _broadcast({
                    "type": "error",
                    "message": f"[WATCHDOG] CIRCUIT BREAKER: Sanity check failed! Reverted to {checkpoint_hash}"
                })
        except Exception:
            pass

        error_detail = sanity.get("error", sanity.get("stdout", "Unknown failure")[:300])
        return {
            "ok": False,
            "error": f"Edit failed sanity check -- automatically reverted. Detail: {error_detail}",
            "watchdog": {
                "status": "reverted",
                "checkpoint": checkpoint_hash,
                "sanity_passed": False,
                "sanity_detail": error_detail,
                "reverted": reverted,
            },
        }


# ══════════════════════════════════════════════════════════════════════════════
# INCREMENTAL CHECKPOINTING -- Per-File Snapshot/Restore
# ══════════════════════════════════════════════════════════════════════════════

def _snapshot_files(file_paths: List[str]) -> Dict[str, Optional[str]]:
    """Read and cache file contents for later rollback. Returns {path: content_or_None}."""
    snapshots = {}
    for fp in file_paths:
        p = Path(fp)
        if p.exists() and p.is_file():
            try:
                snapshots[str(p)] = p.read_text(encoding="utf-8")
            except Exception:
                snapshots[str(p)] = None
        else:
            snapshots[str(p)] = None  # File didn't exist before
    return snapshots


def _restore_files(snapshots: Dict[str, Optional[str]]) -> List[str]:
    """Restore files from snapshot. Returns list of restored paths."""
    restored = []
    for fp, content in snapshots.items():
        p = Path(fp)
        try:
            if content is None:
                # File didn't exist before — delete if it was created
                if p.exists():
                    p.unlink()
                    restored.append(f"{fp} (deleted)")
            else:
                p.write_text(content, encoding="utf-8")
                restored.append(fp)
        except Exception as e:
            print(f"  [WATCHDOG] Failed to restore {fp}: {e}")
    return restored


def safe_edit_incremental(
    edit_fn,
    target_files: Optional[List[str]] = None,
    *args,
    **kwargs,
) -> Dict[str, Any]:
    """
    Incremental checkpointing: only revert the files that were changed.

    Flow:
      1. Snapshot target files (in-memory)
      2. Run preflight validation on any modified content
      3. Call edit_fn(*args, **kwargs)
      4. Run sanity_check.py
      5. On failure: restore only changed files from snapshot
      6. Fallback: git reset --hard HEAD if per-file restore fails

    Args:
        edit_fn: The function that modifies files
        target_files: List of file paths that will be modified
        *args, **kwargs: Passed to edit_fn
    """
    global _circuit_broken

    if not WATCHDOG_ENABLED:
        return edit_fn(*args, **kwargs)

    # Step 1: Snapshot target files
    snapshots = {}
    if target_files:
        snapshots = _snapshot_files(target_files)
        _log_event("INCREMENTAL_SNAPSHOT",
                   f"Snapshotted {len(snapshots)} file(s) for rollback")

    # Still do a git pre-flight commit for the full safety net
    _git_auto_commit("AI Backup: Pre-flight (incremental checkpointing)")
    checkpoint_hash = _git_get_head_hash()

    # Broadcast
    try:
        from modules.joi_orchestrator import _broadcast
        with joi_companion.app.app_context():
            _broadcast({"type": "info",
                        "message": f"[WATCHDOG] Incremental checkpoint: {checkpoint_hash} "
                                   f"({len(snapshots)} file(s) snapshotted)"})
    except Exception:
        pass

    # Step 2: Execute the edit
    try:
        result = edit_fn(*args, **kwargs)
    except Exception as e:
        _log_event("EDIT_EXCEPTION", str(e), success=False)
        if snapshots:
            restored = _restore_files(snapshots)
            _log_event("INCREMENTAL_RESTORE",
                       f"Restored {len(restored)} file(s) after exception")
        else:
            _git_revert_hard()
        return {"ok": False, "error": f"Edit threw exception: {e}",
                "watchdog": "incremental_restored"}

    # Step 3: Sanity check
    sanity = run_sanity_check()

    if sanity.get("passed"):
        _circuit_broken = False
        _log_event("SAFE_EDIT_OK",
                   f"Edit passed sanity check (incremental, checkpoint {checkpoint_hash})")
        if isinstance(result, dict):
            result["watchdog"] = {
                "status": "healthy",
                "checkpoint": checkpoint_hash,
                "sanity_passed": True,
                "mode": "incremental",
            }
        return result

    else:
        # Step 4: INCREMENTAL RESTORE — only revert the files we changed
        error_detail = sanity.get("error", sanity.get("stdout", "Unknown failure")[:300])

        if snapshots:
            restored = _restore_files(snapshots)
            _log_event("INCREMENTAL_RESTORE",
                       f"Sanity failed -- restored {len(restored)} file(s): "
                       f"{', '.join(restored[:5])}")

            # Verify sanity is now OK after incremental restore
            recheck = run_sanity_check()
            if recheck.get("passed"):
                _circuit_broken = False
                try:
                    from modules.joi_orchestrator import _broadcast
                    with joi_companion.app.app_context():
                        _broadcast({
                            "type": "warning",
                            "message": f"[WATCHDOG] Incremental restore successful "
                                       f"({len(restored)} file(s)) -- avoided nuclear revert"
                        })
                except Exception:
                    pass

                return {
                    "ok": False,
                    "error": f"Edit failed sanity check -- incrementally restored. Detail: {error_detail}",
                    "watchdog": {
                        "status": "incremental_restored",
                        "checkpoint": checkpoint_hash,
                        "sanity_passed": False,
                        "restored_files": restored[:10],
                        "sanity_detail": error_detail,
                    },
                }

        # Fallback: nuclear revert if incremental restore didn't fix it
        _log_event("SANITY_FAILED",
                   f"Incremental restore insufficient -- falling back to git reset --hard",
                   success=False)
        _git_revert_hard()

        try:
            from modules.joi_orchestrator import _broadcast
            with joi_companion.app.app_context():
                _broadcast({
                    "type": "error",
                    "message": f"[WATCHDOG] CIRCUIT BREAKER: Incremental restore failed, "
                               f"nuclear revert to {checkpoint_hash}"
                })
        except Exception:
            pass

        return {
            "ok": False,
            "error": f"Edit failed sanity check -- nuclear revert applied. Detail: {error_detail}",
            "watchdog": {
                "status": "nuclear_reverted",
                "checkpoint": checkpoint_hash,
                "sanity_passed": False,
                "sanity_detail": error_detail,
            },
        }


# ══════════════════════════════════════════════════════════════════════════════
# MONKEY-PATCH: Wrap existing code_edit with safety net
# ══════════════════════════════════════════════════════════════════════════════

_original_code_edit = None
_original_creative_edit = None


def _install_safety_hooks():
    """
    Wrap code_edit and creative_edit with the watchdog safety net.
    Called once at module load time.
    """
    global _original_code_edit, _original_creative_edit

    try:
        import modules.joi_code_edit as code_edit_mod

        # Wrap code_edit
        if hasattr(code_edit_mod, 'code_edit') and _original_code_edit is None:
            _original_code_edit = code_edit_mod.code_edit

            def safe_code_edit(**kwargs):
                return safe_edit(_original_code_edit, **kwargs)

            code_edit_mod.code_edit = safe_code_edit

            # Also update the tool executor registry
            if "code_edit" in joi_companion.TOOL_EXECUTORS:
                joi_companion.TOOL_EXECUTORS["code_edit"] = safe_code_edit

            print("    [WATCHDOG] Wrapped code_edit with git safety net")

        # Wrap creative_edit
        if hasattr(code_edit_mod, 'creative_edit') and _original_creative_edit is None:
            _original_creative_edit = code_edit_mod.creative_edit

            def safe_creative_edit(**kwargs):
                return safe_edit(_original_creative_edit, **kwargs)

            code_edit_mod.creative_edit = safe_creative_edit

            if "creative_edit" in joi_companion.TOOL_EXECUTORS:
                joi_companion.TOOL_EXECUTORS["creative_edit"] = safe_creative_edit

            print("    [WATCHDOG] Wrapped creative_edit with git safety net")

    except Exception as e:
        print(f"    [WATCHDOG] Could not install safety hooks: {e}")


# Install hooks after a brief delay (let other modules load first)
def _deferred_install():
    time.sleep(2)
    _install_safety_hooks()

threading.Thread(target=_deferred_install, daemon=True, name="watchdog-install").start()


# ══════════════════════════════════════════════════════════════════════════════
# ORCHESTRATOR INTEGRATION
# ══════════════════════════════════════════════════════════════════════════════

def pre_orchestrator_checkpoint(task_description: str = "") -> str:
    """Called by orchestrator before starting a pipeline. Returns checkpoint hash."""
    msg = f"AI Backup: Pre-orchestration -- {task_description[:80]}" if task_description else \
          "AI Backup: Pre-orchestration checkpoint"
    _git_auto_commit(msg)
    return _git_get_head_hash()


def post_orchestrator_sanity(modified_files: Optional[List[str]] = None) -> Dict[str, Any]:
    """Called by orchestrator after pipeline completes.
    Uses incremental restore if modified_files is provided, otherwise nuclear revert."""
    sanity = run_sanity_check()
    if sanity.get("passed"):
        _git_auto_commit("AI Checkpoint: Post-orchestration -- sanity passed")
        return {"ok": True, "message": "Post-orchestration sanity check passed"}
    else:
        detail = sanity.get("error", sanity.get("stdout", ""))[:300]
        # Try incremental restore first if we know which files changed
        if modified_files:
            snapshots = _snapshot_files(modified_files)
            _restore_files(snapshots)
            recheck = run_sanity_check()
            if recheck.get("passed"):
                _log_event("POST_ORCH_INCREMENTAL",
                           f"Incremental restore fixed post-orchestration sanity")
                return {
                    "ok": False,
                    "message": "Post-orchestration sanity FAILED -- incrementally restored",
                    "detail": detail,
                    "mode": "incremental",
                }
        # Fallback to nuclear
        _git_revert_hard()
        return {
            "ok": False,
            "message": "Post-orchestration sanity FAILED -- reverted to pre-orchestration state",
            "detail": detail,
        }


# ══════════════════════════════════════════════════════════════════════════════
# STAGING GATEWAY (Requirement 4)
# ══════════════════════════════════════════════════════════════════════════════

def validate_and_apply_to_live(file_path: str, content: str) -> Dict[str, Any]:
    """
    Staging & Pre-Commit Safety Bridge.
    1. Write content to /staging/[filename]
    2. Run joi_staging_validator.py
    3. If passed: fs_write to live + git commit
    4. If failed: return error to agent
    """
    from modules.joi_staging_validator import validate_staging_file
    
    p = Path(file_path)
    staging_path = STAGING_DIR / p.name
    
    # 1. Write to Staging
    try:
        staging_path.write_text(content, encoding="utf-8")
    except Exception as e:
        return {"passed": False, "errors": [f"Failed to write to staging: {e}"], "suggestions": []}
        
    # 2. Validate
    result = validate_staging_file(str(staging_path))
    
    if result["passed"]:
        # 3. Apply to Live
        try:
            # Check for changes using git auto-commit before writing
            _git_auto_commit(f"AI Backup: Before applying {p.name}")
            
            p.write_text(content, encoding="utf-8")
            
            # Post-write commit
            _git_auto_commit(f"AI Update: Applied {p.name} (Staging passed)")
            
            # Cleanup staging
            if staging_path.exists():
                staging_path.unlink()
                
            return {"passed": True, "errors": [], "suggestions": []}
        except Exception as e:
            return {"passed": False, "errors": [f"Failed to write to live file: {e}"], "suggestions": []}
    else:
        # 4. Failed: Return error to Coder
        # Keep staging file for debugging if needed (or delete if too much clutter)
        return result




# ══════════════════════════════════════════════════════════════════════════════
# TOOL FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

def watchdog_status(**kwargs) -> Dict[str, Any]:
    """Get watchdog state, git status, recent activity."""
    head_hash = _git_get_head_hash()
    recent_log = _git_get_log(5)
    git_status = _git("status --short")

    return {
        "ok": True,
        "enabled": WATCHDOG_ENABLED,
        "circuit_broken": _circuit_broken,
        "head_commit": head_hash,
        "recent_commits": recent_log,
        "git_status": git_status["stdout"][:500] if git_status["ok"] else "unavailable",
        "recent_events": _activity_log[-10:],
        "total_events": len(_activity_log),
    }


def manual_checkpoint(**kwargs) -> Dict[str, Any]:
    """Create a named git checkpoint."""
    name = kwargs.get("name", "manual checkpoint")
    message = f"Manual checkpoint: {name}"

    # Stage all tracked changes
    _git("add -u")
    result = _git(f'commit -m "{message}"', timeout=30)

    if result["ok"]:
        _log_event("MANUAL_CHECKPOINT", message)
        return {"ok": True, "message": f"Checkpoint created: {_git_get_head_hash()}",
                "hash": _git_get_head_hash()}
    elif "nothing to commit" in result["stdout"] + result["stderr"]:
        return {"ok": True, "message": "Nothing to commit -- already at latest"}
    else:
        return {"ok": False, "error": result["stderr"]}


def manual_revert(**kwargs) -> Dict[str, Any]:
    """Revert to last commit (same as circuit breaker, but user-initiated)."""
    steps = kwargs.get("steps", 1)

    pre_hash = _git_get_head_hash()
    result = _git("reset --hard HEAD")

    if result["ok"]:
        post_hash = _git_get_head_hash()
        _log_event("MANUAL_REVERT", f"Reverted from {pre_hash} to {post_hash}")
        return {"ok": True, "message": f"Reverted to {post_hash}", "from": pre_hash, "to": post_hash}
    else:
        return {"ok": False, "error": result["stderr"]}


# ══════════════════════════════════════════════════════════════════════════════
# FLASK ROUTES
# ══════════════════════════════════════════════════════════════════════════════

@joi_companion.app.route("/watchdog", methods=["GET"])
def watchdog_get():
    """Return watchdog status."""
    return jsonify(watchdog_status())


@joi_companion.app.route("/watchdog", methods=["POST"])
def watchdog_post():
    """Handle watchdog actions: checkpoint, revert, sanity."""
    data = flask_req.get_json(force=True) or {}
    action = data.get("action", "")

    if action == "checkpoint":
        return jsonify(manual_checkpoint(name=data.get("name", "manual")))
    elif action == "revert":
        return jsonify(manual_revert())
    elif action == "sanity":
        result = run_sanity_check()
        return jsonify({"ok": True, "sanity": result})
    elif action == "toggle":
        global WATCHDOG_ENABLED
        WATCHDOG_ENABLED = not WATCHDOG_ENABLED
        return jsonify({"ok": True, "enabled": WATCHDOG_ENABLED})
    else:
        return jsonify({"ok": False, "error": f"Unknown action: {action}"}), 400


def manage_watchdog(**kwargs) -> Dict[str, Any]:
    """Unified tool for managing Git Watchdog operations."""
    action = kwargs.get("action")
    if not action:
        return {"ok": False, "error": "action parameter is required"}
        
    try:
        if action == "status": return watchdog_status(**kwargs)
        elif action == "checkpoint": return manual_checkpoint(**kwargs)
        elif action == "revert": return manual_revert(**kwargs)
        else: return {"ok": False, "error": f"Unknown action: {action}"}
    except Exception as exc:
        return {"ok": False, "error": f"Watchdog action {action} failed: {exc}"}

# ══════════════════════════════════════════════════════════════════════════════
# TOOL REGISTRATION
# ══════════════════════════════════════════════════════════════════════════════

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "manage_watchdog",
        "description": "Unified tool to manage Git Watchdog operations (status, checkpoint, revert).",
        "parameters": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "description": "Action to perform",
                    "enum": ["status", "checkpoint", "revert"]
                },
                "name": {
                    "type": "string",
                    "description": "Name for this checkpoint (for checkpoint)"
                },
                "steps": {
                    "type": "integer",
                    "description": "Number of steps to revert (for revert)"
                }
            },
            "required": ["action"]
        }
    }},
    manage_watchdog,
)

print("    [OK] joi_watchdog (Git Safety Net: unified tool, 2 routes, circuit breaker)")
