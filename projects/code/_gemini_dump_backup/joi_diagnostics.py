"""
modules/joi_diagnostics.py

Adds a real, callable "system diagnostic" tool + /diagnostics endpoint.
Designed to be additive (no core rewrites) and safe (never prints API keys).
"""

from __future__ import annotations

import os
import time
import json
import platform
from typing import Any, Dict, Optional

import joi_companion

from flask import jsonify, request as flask_req
from modules.joi_memory import require_user

START_TS = time.time()


def _bool_env(name: str) -> bool:
    v = os.getenv(name, "")
    return bool((v or "").strip())


def _http_json(url: str, timeout: float = 4.0) -> Dict[str, Any]:
    import requests
    r = requests.get(url, timeout=timeout)
    try:
        data = r.json()
    except Exception:
        data = {"_non_json": (r.text or "")[:500]}
    return {"status_code": r.status_code, "data": data}


def _check_lm_studio() -> Dict[str, Any]:
    """
    Joi uses an OpenAI-compatible local server (LM Studio).
    We check:
      - can we reach it?
      - what models does it report?
      - does JOI_LOCAL_MODEL exist there?
    """
    base = (os.getenv("JOI_LOCAL_BASE_URL") or os.getenv("LOCAL_BASE_URL") or "").strip()
    model = (os.getenv("JOI_LOCAL_MODEL") or os.getenv("LOCAL_MODEL") or "").strip()

    if not base:
        return {"ok": False, "error": "No local base URL set", "hint": "Set JOI_LOCAL_BASE_URL (or LOCAL_BASE_URL) to your LM Studio server, e.g. http://localhost:1234"}

    # Normalize base (strip trailing slash)
    base = base.rstrip("/")

    models_url = f"{base}/v1/models"
    try:
        resp = _http_json(models_url, timeout=5.0)
        if resp["status_code"] != 200:
            return {
                "ok": False,
                "error": f"LM Studio returned HTTP {resp['status_code']}",
                "models_url": models_url,
                "details": resp["data"],
            }

        # OpenAI-compatible format: {"data":[{"id":"..."}...]}
        ids = []
        data = resp["data"]
        if isinstance(data, dict) and isinstance(data.get("data"), list):
            for item in data["data"]:
                if isinstance(item, dict) and item.get("id"):
                    ids.append(str(item["id"]))

        out: Dict[str, Any] = {
            "ok": True,
            "base_url": base,
            "models_url": models_url,
            "reported_models": ids[:50],
            "configured_model": model or None,
        }

        if model:
            out["configured_model_found"] = model in ids
            if not out["configured_model_found"] and ids:
                out["hint"] = f'Your JOI_LOCAL_MODEL is "{model}" but LM Studio reports: {ids[:8]}... Set JOI_LOCAL_MODEL to one of those IDs.'
        else:
            if ids:
                out["hint"] = f'Set JOI_LOCAL_MODEL to one of: {ids[:8]}...'
            else:
                out["hint"] = "LM Studio reachable but returned no model IDs. Make sure a model is loaded in LM Studio Local Server."

        return out

    except Exception as e:
        return {"ok": False, "error": f"{type(e).__name__}: {e}", "models_url": models_url}


def _check_openai() -> Dict[str, Any]:
    """
    Lightweight check: do we have a key AND can we ping a tiny chat completion?
    If you don't want external calls, set JOI_DIAG_OPENAI_PING=0.
    """
    have_key = _bool_env("OPENAI_API_KEY")
    if not have_key:
        return {"ok": False, "error": "No key (OPENAI_API_KEY missing)"}

    ping = (os.getenv("JOI_DIAG_OPENAI_PING", "1").strip() not in ("0", "false", "False"))
    if not ping:
        return {"ok": True, "note": "Key present; ping disabled (JOI_DIAG_OPENAI_PING=0)"}

    try:
        # Reuse your existing LLM module if possible
        from modules import joi_llm

        model = getattr(joi_llm, "OPENAI_TOOL_MODEL", None) or os.getenv("JOI_MODEL", "gpt-4o")
        client = getattr(joi_llm, "client", None)

        if not client:
            return {"ok": False, "error": "OpenAI client not initialized in joi_llm (check joi_llm.py)", "model": model}

        client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "ping"}],
            max_tokens=3,
        )
        return {"ok": True, "model": model}

    except Exception as e:
        return {"ok": False, "error": f"{type(e).__name__}: {str(e)[:180]}"}


def run_system_diagnostic(**params) -> Dict[str, Any]:
    """
    Tool callable by the LLM.
    """
    # Require a logged-in session for safety (matches your other routes/tools).
    require_user()

    report: Dict[str, Any] = {
        "ok": True,
        "uptime_seconds": round(time.time() - START_TS, 2),
        "platform": {
            "python": platform.python_version(),
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
        },
        "env": {
            "OPENAI_API_KEY": _bool_env("OPENAI_API_KEY"),
            "ANTHROPIC_API_KEY": _bool_env("ANTHROPIC_API_KEY"),
            "GEMINI_API_KEY": _bool_env("GEMINI_API_KEY"),
            # local server config (names used across variants)
            "JOI_LOCAL_BASE_URL": bool((os.getenv("JOI_LOCAL_BASE_URL") or "").strip()),
            "LOCAL_BASE_URL": bool((os.getenv("LOCAL_BASE_URL") or "").strip()),
            "JOI_LOCAL_MODEL": bool((os.getenv("JOI_LOCAL_MODEL") or "").strip()),
            "LOCAL_MODEL": bool((os.getenv("LOCAL_MODEL") or "").strip()),
        },
        "providers": {
            "local": _check_lm_studio(),
            "openai": _check_openai(),
        }
    }

    # overall ok if all provider checks ok
    report["ok"] = all(v.get("ok") for v in report["providers"].values())

    return report


# -------------------------
# Tool registration
# -------------------------

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "run_system_diagnostic",
        "description": "Run a full system diagnostic: env keys present (no values), LM Studio reachability + model IDs, OpenAI ping (optional). Returns a structured health report.",
        "parameters": {"type": "object", "properties": {}}
    }},
    run_system_diagnostic
)


# -------------------------
# Optional route for browser/manual testing
# -------------------------

def diagnostics_route():
    require_user()
    return jsonify(run_system_diagnostic(**(flask_req.get_json(silent=True) or {})))

joi_companion.register_route("/diagnostics", ["GET", "POST"], diagnostics_route, "diagnostics_route")
