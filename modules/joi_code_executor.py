"""
modules/joi_code_executor.py

JOI CODE — Real-Time Bash Executor & Atomic Staging Bridge
===========================================================
Replaces ad-hoc subprocess.run calls with a unified streaming executor.

Features:
- run_command()        — Popen-based, streams stdout+stderr line-by-line via SSE
- run_py_compile()     — calls `python -m py_compile`; exit 0 = clean
- stage_and_verify()   — writes to staging/, runs py_compile, broadcasts results
- apply_staged()       — atomically moves verified file to live path via watchdog
- is_risky()           — checks command against blocklist
- request_user_permission() — broadcasts permission_request, blocks on Event (30s)

Routes: POST /joicode/permission/<action>  (approve / reject)
Tool:   joicode_run_bash
"""

import ast
import json
import os
import queue
import re
import shlex
import shutil
import subprocess
import threading
import time
import traceback
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

import joi_companion
from flask import Response, jsonify, request as flask_req

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR    = Path(__file__).resolve().parent.parent
STAGING_DIR = BASE_DIR / "staging"
STAGING_DIR.mkdir(exist_ok=True)

PYTHON_EXE = str(BASE_DIR / "venv311" / "Scripts" / "python.exe")
if not Path(PYTHON_EXE).exists():
    # Fallback to system Python
    PYTHON_EXE = "python"

# ── Blocklist: commands that require explicit user permission ─────────────────
_RISKY_PATTERNS: List[str] = [
    r"rm\s+-rf",
    r"git\s+reset\s+--hard",
    r"git\s+push\s+--force",
    r"drop\s+table",
    r"\bformat\b",
    r"del\s+/f",
    r"rmdir\s+/s",
    r"git\s+clean\s+-f",
    r"mkfs",
    r"dd\s+if=",
]

# ── Permission gate state ─────────────────────────────────────────────────────
_perm_event: threading.Event = threading.Event()
_perm_result: Dict[str, bool] = {"allowed": False}
_perm_lock = threading.Lock()

# ── SSE helpers (reuse orchestrator's _broadcast if available) ────────────────

def _emit(event: Dict):
    """Best-effort broadcast through orchestrator SSE channel."""
    try:
        from modules.joi_orchestrator import _broadcast
        _broadcast(event)
    except Exception:
        pass  # Not fatal — SSE is informational only


# ══════════════════════════════════════════════════════════════════════════════
# CORE UTILITIES
# ══════════════════════════════════════════════════════════════════════════════

def is_risky(cmd: str) -> bool:
    """Return True if cmd matches any blocklist pattern."""
    cmd_lower = cmd.lower()
    for pattern in _RISKY_PATTERNS:
        if re.search(pattern, cmd_lower):
            return True
    return False


def request_user_permission(cmd: str, timeout: float = 30.0) -> bool:
    """
    Broadcast a permission_request event and block until user approves/rejects.
    Returns True if approved, False if rejected or timed out.
    """
    with _perm_lock:
        _perm_event.clear()
        _perm_result["allowed"] = False

    _emit({
        "type": "permission_request",
        "command": cmd,
        "message": f"Permission required to run: {cmd}",
        "timestamp": time.time(),
    })

    granted = _perm_event.wait(timeout=timeout)
    if not granted:
        _emit({
            "type": "info",
            "message": f"[JOICODE] Permission request timed out after {timeout}s — denied by default",
        })
        return False

    return _perm_result.get("allowed", False)


# ══════════════════════════════════════════════════════════════════════════════
# STREAMING COMMAND EXECUTOR
# ══════════════════════════════════════════════════════════════════════════════

def run_command(
    cmd: str,
    cwd: Optional[str] = None,
    timeout: float = 120.0,
    broadcast_fn: Optional[Callable[[Dict], None]] = None,
) -> Dict[str, Any]:
    """
    Execute a shell command with real-time streaming of stdout/stderr.

    Never uses shell=True — cmd is split via shlex.split().
    Each line is broadcast as bash_stdout or bash_stderr.

    Returns:
        {"ok": bool, "returncode": int, "stdout": str, "stderr": str, "timed_out": bool}
    """
    broadcast = broadcast_fn or _emit
    cwd = cwd or str(BASE_DIR)

    # Safety check
    if is_risky(cmd):
        allowed = request_user_permission(cmd)
        if not allowed:
            msg = f"[JOICODE] Blocked risky command (user denied): {cmd}"
            broadcast({"type": "bash_stderr", "line": msg, "cmd": cmd})
            return {"ok": False, "returncode": -1, "stdout": "", "stderr": msg, "timed_out": False}

    env = {
        **os.environ,
        "PYTHONPATH": str(BASE_DIR),
        "PYTHONIOENCODING": "utf-8",
    }

    broadcast({"type": "bash_stdout", "line": f"$ {cmd}", "cmd": cmd})

    try:
        args = shlex.split(cmd, posix=False)  # posix=False preserves Windows paths
    except ValueError as e:
        err = f"[JOICODE] Command parse error: {e}"
        broadcast({"type": "bash_stderr", "line": err, "cmd": cmd})
        return {"ok": False, "returncode": -1, "stdout": "", "stderr": err, "timed_out": False}

    try:
        proc = subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            cwd=cwd,
            env=env,
        )
    except FileNotFoundError as e:
        err = f"[JOICODE] Command not found: {e}"
        broadcast({"type": "bash_stderr", "line": err, "cmd": cmd})
        return {"ok": False, "returncode": -1, "stdout": "", "stderr": err, "timed_out": False}

    stdout_lines: List[str] = []
    stderr_lines: List[str] = []

    def _read_stream(stream, lines_list, event_type):
        for line in stream:
            stripped = line.rstrip("\n\r")
            lines_list.append(stripped)
            broadcast({"type": event_type, "line": stripped, "cmd": cmd})
        stream.close()

    t_out = threading.Thread(target=_read_stream, args=(proc.stdout, stdout_lines, "bash_stdout"), daemon=True)
    t_err = threading.Thread(target=_read_stream, args=(proc.stderr, stderr_lines, "bash_stderr"), daemon=True)
    t_out.start()
    t_err.start()

    timed_out = False
    try:
        proc.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        proc.kill()
        timed_out = True
        broadcast({"type": "bash_stderr", "line": f"[JOICODE] Command timed out after {timeout}s", "cmd": cmd})

    t_out.join(timeout=5)
    t_err.join(timeout=5)

    returncode = proc.returncode or 0
    ok = (returncode == 0) and not timed_out

    broadcast({
        "type": "bash_stdout",
        "line": f"[exit {returncode}{'  (TIMEOUT)' if timed_out else ''}]",
        "cmd": cmd,
    })

    return {
        "ok": ok,
        "returncode": returncode,
        "stdout": "\n".join(stdout_lines),
        "stderr": "\n".join(stderr_lines),
        "timed_out": timed_out,
    }


# ══════════════════════════════════════════════════════════════════════════════
# PY_COMPILE CHECKER
# ══════════════════════════════════════════════════════════════════════════════

def run_py_compile(file_path: str) -> Dict[str, Any]:
    """
    Run `python -m py_compile <file>` synchronously.
    Returns {"passed": bool, "error": str}
    """
    p = Path(file_path)
    if not p.exists():
        return {"passed": False, "error": f"File not found: {file_path}"}
    if p.suffix != ".py":
        return {"passed": True, "error": ""}  # non-Python files pass by default

    try:
        result = subprocess.run(
            [PYTHON_EXE, "-m", "py_compile", str(p)],
            capture_output=True,
            text=True,
            timeout=15,
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        )
        if result.returncode == 0:
            return {"passed": True, "error": ""}
        else:
            error = (result.stderr or result.stdout or "py_compile failed").strip()
            return {"passed": False, "error": error}
    except subprocess.TimeoutExpired:
        return {"passed": False, "error": "py_compile timed out"}
    except Exception as e:
        return {"passed": False, "error": f"py_compile error: {e}"}


# ══════════════════════════════════════════════════════════════════════════════
# STAGING + VERIFY
# ══════════════════════════════════════════════════════════════════════════════

def stage_and_verify(
    content: str,
    dest_path: str,
    broadcast_fn: Optional[Callable[[Dict], None]] = None,
) -> Dict[str, Any]:
    """
    Write content to staging/ first, run py_compile, broadcast results.

    Returns:
        {"ok": bool, "staging_path": str, "errors": list[str]}
    """
    broadcast = broadcast_fn or _emit
    errors: List[str] = []

    STAGING_DIR.mkdir(exist_ok=True)

    dest = Path(dest_path)
    staging_name = f"{dest.stem}_{int(time.time()*1000)}{dest.suffix}"
    staging_path = STAGING_DIR / staging_name

    try:
        staging_path.write_text(content, encoding="utf-8")
        broadcast({"type": "staged", "file": str(staging_path), "dest": str(dest_path)})
    except Exception as e:
        errors.append(f"Write to staging failed: {e}")
        return {"ok": False, "staging_path": str(staging_path), "errors": errors}

    # py_compile check for Python files
    if dest.suffix == ".py":
        compile_result = run_py_compile(str(staging_path))
        broadcast({
            "type": "compile_check",
            "passed": compile_result["passed"],
            "error": compile_result.get("error", ""),
            "file": str(staging_path),
        })
        if not compile_result["passed"]:
            errors.append(f"py_compile: {compile_result['error']}")
            return {"ok": False, "staging_path": str(staging_path), "errors": errors}

    # joi_staging_validator (optional extra check)
    try:
        from modules.joi_staging_validator import validate_staged_file
        val = validate_staged_file(str(staging_path))
        if not val.get("passed", True):
            val_errors = val.get("errors", [])
            for ve in val_errors:
                errors.append(f"staging_validator: {ve}")
            if errors:
                return {"ok": False, "staging_path": str(staging_path), "errors": errors}
    except ImportError:
        pass
    except Exception as e:
        broadcast({"type": "info", "message": f"[JOICODE] staging_validator skipped: {e}"})

    return {"ok": True, "staging_path": str(staging_path), "errors": []}


def apply_staged(staging_path: str, live_path: str) -> Dict[str, Any]:
    """
    Move verified staged file to live path via watchdog.
    Falls back to direct copy if watchdog unavailable.
    """
    content = Path(staging_path).read_text(encoding="utf-8")

    try:
        from modules.joi_watchdog import validate_and_apply_to_live
        result = validate_and_apply_to_live(live_path, content)
        if result.get("passed"):
            _emit({"type": "applied", "file": live_path, "method": "staged+watchdog"})
            return {"ok": True}
        else:
            errors = result.get("errors", [])
            _emit({"type": "error", "message": f"[WATCHDOG] Apply blocked: {'; '.join(errors[:3])}"})
            return {"ok": False, "errors": errors}
    except ImportError:
        # Watchdog not available — direct copy
        try:
            dest = Path(live_path)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(staging_path, live_path)
            _emit({"type": "applied", "file": live_path, "method": "staged+direct"})
            return {"ok": True}
        except Exception as e:
            return {"ok": False, "errors": [str(e)]}
    except Exception as e:
        return {"ok": False, "errors": [str(e)]}


# ══════════════════════════════════════════════════════════════════════════════
# FLASK ROUTES
# ══════════════════════════════════════════════════════════════════════════════

@joi_companion.app.route("/joicode/permission/<action>", methods=["POST"])
def joicode_permission(action: str):
    """Handle user approve/reject for risky command permission gate."""
    with _perm_lock:
        if action == "approve":
            _perm_result["allowed"] = True
        else:
            _perm_result["allowed"] = False
        _perm_event.set()
    return jsonify({"ok": True, "action": action})


@joi_companion.app.route("/joicode/status", methods=["GET"])
def joicode_status():
    """Return JOI CODE executor status and staging directory info."""
    staging_files = []
    try:
        staging_files = [f.name for f in sorted(STAGING_DIR.glob("*")) if f.is_file()]
    except Exception:
        pass
    return jsonify({
        "ok": True,
        "staging_dir": str(STAGING_DIR),
        "staging_files": staging_files,
        "python_exe": PYTHON_EXE,
    })


@joi_companion.app.route("/joicode/run", methods=["POST"])
def joicode_run():
    """Execute a bash command with streaming output (non-SSE, synchronous)."""
    data = flask_req.get_json(force=True) or {}
    cmd = data.get("command", "")
    cwd = data.get("working_dir", str(BASE_DIR))
    timeout = float(data.get("timeout", 60))

    if not cmd:
        return jsonify({"ok": False, "error": "No command provided"})

    result = run_command(cmd, cwd=cwd, timeout=timeout)
    return jsonify(result)


# ══════════════════════════════════════════════════════════════════════════════
# TOOL REGISTRATION
# ══════════════════════════════════════════════════════════════════════════════

def _tool_joicode_run_bash(**kwargs) -> Dict[str, Any]:
    """Tool executor: run a bash/shell command with real-time output streaming."""
    cmd = kwargs.get("command", "")
    cwd = kwargs.get("working_dir", str(BASE_DIR))
    timeout = float(kwargs.get("timeout", 60))

    if not cmd:
        return {"ok": False, "error": "command is required"}

    result = run_command(cmd, cwd=cwd, timeout=timeout)
    return {
        "ok": result["ok"],
        "returncode": result["returncode"],
        "stdout": result["stdout"][-3000:] if result["stdout"] else "",
        "stderr": result["stderr"][-2000:] if result["stderr"] else "",
        "timed_out": result["timed_out"],
    }


joi_companion.register_tool(
    {
        "type": "function",
        "function": {
            "name": "joicode_run_bash",
            "description": (
                "Run a shell/bash command with real-time output streaming to the JOI CODE terminal. "
                "Output is shown line-by-line. Risky commands (rm -rf, git reset --hard, etc.) "
                "trigger a user permission gate before execution."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The command to execute (e.g. 'python -m pytest tests/', 'pip install requests')",
                    },
                    "working_dir": {
                        "type": "string",
                        "description": "Working directory. Defaults to Joi project root.",
                    },
                    "timeout": {
                        "type": "number",
                        "description": "Max seconds to wait before killing the process. Default 60.",
                    },
                },
                "required": ["command"],
            },
        },
    },
    _tool_joicode_run_bash,
)

print("  [OK] joi_code_executor — JOI CODE bash executor loaded")
