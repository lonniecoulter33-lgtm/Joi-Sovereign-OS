"""
modules/joi_supervisor.py

Supervisor/Stability layer (Phase S1):
- Provides /health and /supervisor endpoints
- Provides tool: run_supervisor_check
- Records last error snapshot in memory for quick debugging
Additive module; no rewrites required.
"""

from __future__ import annotations

import os
import time
import traceback
from typing import Any, Dict, Optional

import joi_companion
from flask import jsonify, request as flask_req

# Auth helper (matches the rest of your app)
from modules.joi_memory import require_user

START_TS = time.time()
_LAST_REPORT: Dict[str, Any] = {"ok": True, "ts": time.time(), "note": "Supervisor initialized"}


def _now() -> float:
    return time.time()


def _safe_err(e: Exception) -> Dict[str, Any]:
    return {
        "type": type(e).__name__,
        "message": str(e)[:300],
        "traceback": traceback.format_exc()[-4000:],
    }


def _get_diag_report() -> Dict[str, Any]:
    """
    Try to call run_system_diagnostic if your diagnostics module exists.
    Falls back to minimal env info if not available.
    """
    report: Dict[str, Any] = {
        "ok": True,
        "uptime_seconds": round(_now() - START_TS, 2),
        "providers": {},
        "env": {},
    }

    # Minimal env snapshot (never include secret values)
    report["env"] = {
        "OPENAI_API_KEY": bool((os.getenv("OPENAI_API_KEY") or "").strip()),
        "ANTHROPIC_API_KEY": bool((os.getenv("ANTHROPIC_API_KEY") or "").strip()),
        "GEMINI_API_KEY": bool((os.getenv("GEMINI_API_KEY") or "").strip()),
        "JOI_CHAT_PROVIDER": (os.getenv("JOI_CHAT_PROVIDER") or "").strip() or None,
        "JOI_LOCAL_ENABLED": (os.getenv("JOI_LOCAL_ENABLED") or "").strip() or None,
        "JOI_LOCAL_BASE_URL": bool((os.getenv("JOI_LOCAL_BASE_URL") or "").strip()),
        "JOI_LOCAL_MODEL": (os.getenv("JOI_LOCAL_MODEL") or "").strip() or None,
    }

    # If diagnostics tool exists, use it
    try:
        # Import your diagnostics module (if present)
        from modules import joi_diagnostics  # type: ignore

        diag = joi_diagnostics.run_system_diagnostic()  # uses require_user internally
        report["providers"] = diag.get("providers", {})
        report["ok"] = bool(diag.get("ok", True))
        report["diagnostics_ok"] = True
        return report

    except Exception as e:
        report["diagnostics_ok"] = False
        report["diagnostics_error"] = _safe_err(e)
        # Supervisor still returns something useful
        report["ok"] = True
        return report


def run_supervisor_check(**params) -> Dict[str, Any]:
    """
    Tool callable by the LLM.
    Returns a readable system health report.
    """
    require_user()

    global _LAST_REPORT
    try:
        rep = _get_diag_report()
        rep["ts"] = _now()
        _LAST_REPORT = rep
        return rep
    except Exception as e:
        _LAST_REPORT = {"ok": False, "ts": _now(), "error": _safe_err(e)}
        return _LAST_REPORT


def health_route():
    """
    Fast health endpoint: returns ok + uptime.
    Does not ping providers (for speed).
    """
    require_user()
    return jsonify({
        "ok": True,
        "uptime_seconds": round(_now() - START_TS, 2),
        "ts": _now(),
    })


def supervisor_route():
    """
    Full supervisor report endpoint (calls diagnostics if available).
    """
    require_user()
    payload = flask_req.get_json(silent=True) or {}
    rep = run_supervisor_check(**payload)
    return jsonify(rep)


def last_route():
    """
    Returns last computed supervisor report (no new checks).
    """
    require_user()
    return jsonify(_LAST_REPORT)


# Register tool for the LLM
joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "run_supervisor_check",
        "description": "Run Joi supervisor health checks (diagnostics + env snapshot). Returns structured report and last-known status.",
        "parameters": {"type": "object", "properties": {}}
    }},
    run_supervisor_check
)

# Register routes
joi_companion.register_route("/health", ["GET"], health_route, "health_route")
joi_companion.register_route("/supervisor", ["GET", "POST"], supervisor_route, "supervisor_route")
joi_companion.register_route("/supervisor/last", ["GET"], last_route, "supervisor_last_route")
