from __future__ import annotations
import subprocess, os, shutil
from typing import Any, Dict
from joi_registry import register_tool

def _tool_launch_app(args: Dict[str, Any]) -> Dict[str, Any]:
    app = (args.get("app") or "").strip()
    if not app:
        return {"ok": False, "error": "app required"}
    # Minimal: try to open via OS 'start' on Windows; on other OS, use 'open'/'xdg-open'
    try:
        if os.name == "nt":
            subprocess.Popen(["cmd", "/c", "start", "", app], shell=False)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", "-a", app])
        else:
            subprocess.Popen(["xdg-open", app])
        return {"ok": True, "launched": app}
    except Exception as e:
        return {"ok": False, "error": str(e)}

register_tool({
  "type":"function",
  "function":{
    "name":"launch_app",
    "description":"Attempt to launch an app by name/path (best-effort).",
    "parameters":{"type":"object","properties":{"app":{"type":"string"}}, "required":["app"]}
  }
}, _tool_launch_app)
