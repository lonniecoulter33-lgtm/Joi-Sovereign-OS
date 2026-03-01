"""
modules/joi_wellness.py

Unified Wellness & Diagnostics System
======================================
Combines system health monitoring, deep diagnostics, 
and autonomous self-healing capabilities.
"""

import os
import sys
import time
import json
import platform
import traceback
import subprocess
import shutil
import importlib
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import joi_companion
from flask import jsonify, request as flask_req
# from modules.joi_auth import require_user (moved to lazy)

# ── Configuration & Paths ────────────────────────────────────────────────────
START_TS = time.time()
BASE_DIR = Path(__file__).resolve().parent.parent
MODULES_DIR = BASE_DIR / "modules"
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
HEAL_LOG_PATH = DATA_DIR / "self_heal_log.json"

_LAST_SUPERVISOR_REPORT: Dict[str, Any] = {"ok": True, "ts": time.time(), "note": "Wellness initialized"}
_MANIFEST: Optional[Dict[str, Any]] = None

# ── Utilities ────────────────────────────────────────────────────────────────
def _now() -> float: return time.time()

def _now_iso() -> str: return datetime.now().isoformat()

def _safe_err(e: Exception) -> Dict[str, Any]:
    return {
        "type": type(e).__name__,
        "message": str(e)[:300],
        "traceback": traceback.format_exc()[-4000:],
    }

def _bool_env(name: str) -> bool:
    v = os.getenv(name, "")
    return bool((v or "").strip())

# ── Diagnostics Core ─────────────────────────────────────────────────────────
def _check_ollama() -> Dict[str, Any]:
    try:
        from modules.joi_ollama import ollama_health_ping, OLLAMA_BASE_URL, OLLAMA_PRIVACY_MODEL, OLLAMA_CODER_MODEL
        return {"ok": ollama_health_ping(), "base_url": OLLAMA_BASE_URL, "privacy_model": OLLAMA_PRIVACY_MODEL, "coder_model": OLLAMA_CODER_MODEL}
    except Exception as e: return {"ok": False, "error": str(e)}

def _check_openai() -> Dict[str, Any]:
    if not _bool_env("OPENAI_API_KEY"): return {"ok": False, "error": "Missing OPENAI_API_KEY"}
    try:
        from modules import joi_llm
        model = getattr(joi_llm, "OPENAI_TOOL_MODEL", "gpt-4o-mini")
        client = getattr(joi_llm, "client", None)
        if not client: return {"ok": False, "error": "OpenAI client not initialized"}
        client.chat.completions.create(model=model, messages=[{"role": "user", "content": "ping"}], max_tokens=3)
        return {"ok": True, "model": model}
    except Exception as e: return {"ok": False, "error": str(e)[:180]}

def run_system_diagnostic(**params) -> Dict[str, Any]:
    """Structured health report of environment and providers."""
    from modules.joi_auth import require_user
    require_user()
    report = {
        "ok": True,
        "uptime_seconds": round(_now() - START_TS, 2),
        "platform": {"python": platform.python_version(), "system": platform.system(), "release": platform.release()},
        "env": {"OPENAI_API_KEY": _bool_env("OPENAI_API_KEY"), "GEMINI_API_KEY": _bool_env("GEMINI_API_KEY")},
        "providers": {"openai": _check_openai(), "ollama": _check_ollama()},
        "capability_status": get_manifest().get("capability_status", {})
    }
    report["ok"] = any(v.get("ok") for v in report["providers"].values())
    return report

# ── Manifest & Capabilities ─────────────────────────────────────────────────
def generate_manifest() -> Dict[str, Any]:
    from modules.joi_llm import client as openai_client, HAVE_GEMINI
    tool_names = sorted([t.get("function", {}).get("name", "?") for t in joi_companion.TOOLS])
    
    capability_status = {}
    try:
        from modules import joi_browser
        capability_status["browser"] = {"available": getattr(joi_browser, "HAVE_SELENIUM", False)}
    except: capability_status["browser"] = {"available": False}
    
    return {
        "timestamp": _now_iso(),
        "tools": tool_names,
        "tool_count": len(tool_names),
        "providers": {"openai": bool(openai_client), "gemini": HAVE_GEMINI},
        "capability_status": capability_status
    }

def get_manifest() -> Dict[str, Any]:
    global _MANIFEST
    if _MANIFEST is None: _MANIFEST = generate_manifest()
    return _MANIFEST

def get_manifest_summary() -> str:
    m = get_manifest()
    p = [k for k, v in m.get("providers", {}).items() if v]
    return f"\n[VERIFIED CAPABILITIES: providers={','.join(p)}, tools={m.get('tool_count')} registered]\n"

# ── Self-Healing ─────────────────────────────────────────────────────────────
def _log_heal_event(event: Dict[str, Any]):
    events = []
    if HEAL_LOG_PATH.exists():
        try: events = json.loads(HEAL_LOG_PATH.read_text(encoding="utf-8"))
        except: pass
    event["timestamp"] = _now_iso()
    events.append(event)
    HEAL_LOG_PATH.write_text(json.dumps(events[-200:], indent=2), encoding="utf-8")

def self_diagnose(**kwargs) -> Dict[str, Any]:
    """Run comprehensive self-diagnosis across modules and tools."""
    from modules.joi_auth import require_user
    require_user()
    issues = []
    module_results = []
    for mod_file in sorted(MODULES_DIR.glob("joi_*.py")):
        try:
            importlib.import_module(f"modules.{mod_file.stem}")
            module_results.append({"module": mod_file.stem, "status": "ok"})
        except Exception as e:
            issues.append({"type": "broken_module", "module": mod_file.stem, "error": str(e)[:200]})
    
    diag = run_system_diagnostic()
    _log_heal_event({"action": "self_diagnose", "issue_count": len(issues)})
    return {"ok": True, "issues": issues, "diag": diag, "summary": f"Found {len(issues)} issues. Modules: {len(module_results)} OK."}

def self_fix(**kwargs) -> Dict[str, Any]:
    """Attempt to fix a diagnosed issue using available tools."""
    from modules.joi_auth import require_user
    require_user()
    issue = kwargs.get("issue", "").strip()
    if not issue: return {"ok": False, "message": "No issue provided"}
    
    # Placeholder for Claude Code delegation or patching logic
    _log_heal_event({"action": "self_fix", "issue": issue})
    return {"ok": True, "message": f"Fix attempt logged for: {issue}. Propose a patch if you have a solution."}

# ── Routes & Tools ───────────────────────────────────────────────────────────
def health_route():
    return jsonify({"ok": True, "uptime": round(_now() - START_TS, 2)})

def diagnostics_route():
    from modules.joi_auth import require_user
    require_user()
    return jsonify(run_system_diagnostic())

def manifest_route():
    from modules.joi_auth import require_user
    require_user()
    return jsonify(get_manifest())

def supervisor_route():
    from modules.joi_auth import require_user
    require_user()
    global _LAST_SUPERVISOR_REPORT
    _LAST_SUPERVISOR_REPORT = run_system_diagnostic()
    return jsonify(_LAST_SUPERVISOR_REPORT)

# Registration
joi_companion.register_tool({"type": "function", "function": {"name": "run_system_diagnostic", "description": "Run system health & provider check."}}, run_system_diagnostic)
joi_companion.register_tool({"type": "function", "function": {"name": "self_diagnose", "description": "Run deep module & tool audit."}}, self_diagnose)

joi_companion.register_route("/diagnostics/manifest", ["GET"], manifest_route, "wellness_manifest")
joi_companion.register_route("/health", ["GET"], health_route, "wellness_health")
joi_companion.register_route("/supervisor", ["GET"], supervisor_route, "wellness_supervisor")
joi_companion.register_route("/diagnostics", ["GET"], diagnostics_route, "wellness_diagnostics")
