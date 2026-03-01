from __future__ import annotations
import os
from pathlib import Path
from typing import Any, Dict
from joi_registry import register_tool

BASE_DIR = Path(__file__).resolve().parents[1]
PROJECTS_DIR = Path(os.getenv("JOI_PROJECTS_DIR", str(BASE_DIR / "projects")))

def _tool_project_scan(args: Dict[str, Any]) -> Dict[str, Any]:
    root = PROJECTS_DIR
    root.mkdir(parents=True, exist_ok=True)
    items=[]
    for p in sorted(root.rglob("*")):
        if p.is_file() and p.stat().st_size < 200000:
            items.append(str(p.relative_to(root)))
        if len(items) >= 2000:
            break
    return {"ok": True, "projects_dir": str(root), "file_count": len(items), "files": items[:200]}

register_tool({
  "type":"function",
  "function":{
    "name":"project_scan",
    "description":"Scan the projects directory and list files.",
    "parameters":{"type":"object","properties":{}, "required":[]}
  }
}, _tool_project_scan)
