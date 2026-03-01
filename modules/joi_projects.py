"""
Project scanner & organizer. Also: save/load projects for staged work (new tools, apps).
"""
import json
import re
import shutil
import time
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional

BASE_DIR = Path(__file__).resolve().parent.parent
PROJECTS_DIR = BASE_DIR / "projects"
DATA_DIR = BASE_DIR / "data"
PROJECTS_REGISTRY_PATH = DATA_DIR / "projects_registry.json"

CODE_EXTS = {".py", ".js", ".java", ".cpp", ".c", ".cs", ".go", ".rs", ".rb", ".php"}
TEXT_EXTS = {".txt", ".md", ".json", ".csv"}
MAX_SIZE = 5_000_000

from modules.joi_files import FILE_ROOTS, resolve_path

def scan_projects(roots=None, extensions=None):
    if roots is None:
        roots = ["documents", "desktop", "downloads"]
    if extensions is None:
        extensions = [".txt", ".md", ".py", ".js", ".html", ".docx", ".pdf", ".csv"]
    
    found = {"books": [], "code": [], "notes": [], "other": []}
    max_per_category = 25  # cap to prevent massive results
    try:
        for root_name in roots:
            if root_name not in FILE_ROOTS:
                continue
            root_path = Path(FILE_ROOTS[root_name])
            if not root_path.exists():
                continue
            total_found = sum(len(v) for v in found.values())
            if total_found >= max_per_category * 4:
                break
            for item in root_path.rglob("*"):
                if not item.is_file():
                    continue
                if item.suffix.lower() not in extensions:
                    continue
                if item.stat().st_size > MAX_SIZE:
                    continue
                rel = str(item.relative_to(root_path))
                entry = {"name": item.name, "path": rel, "root": root_name,
                         "size": item.stat().st_size,
                         "modified": datetime.fromtimestamp(item.stat().st_mtime).isoformat()}
                
                name_lower = item.name.lower()
                if item.suffix.lower() in CODE_EXTS:
                    if len(found["code"]) < max_per_category:
                        found["code"].append(entry)
                elif any(kw in name_lower for kw in ["chapter", "book", "novel", "story"]):
                    if len(found["books"]) < max_per_category:
                        found["books"].append(entry)
                elif any(kw in name_lower for kw in ["note", "todo", "idea", "journal"]):
                    if len(found["notes"]) < max_per_category:
                        found["notes"].append(entry)
                else:
                    if len(found["other"]) < max_per_category:
                        found["other"].append(entry)
        
        total = sum(len(v) for v in found.values())
        return {"ok": True, "summary": f"Found {total} files across {len(roots)} directories.",
                "categories": found, "total": total}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def organise_into_projects(categories):
    copied = 0
    try:
        for category, files in categories.items():
            dest_dir = PROJECTS_DIR / category
            dest_dir.mkdir(exist_ok=True)
            for f in files:
                src = resolve_path(f["root"], f["path"])
                if src and src.exists():
                    dest = dest_dir / f["name"]
                    if not dest.exists():
                        shutil.copy2(src, dest)
                        copied += 1
        return {"ok": True, "message": f"Copied {copied} files into projects/", "copied": copied}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def list_projects():
    """List project folders and their files (legacy scanner view)."""
    try:
        projects = {}
        if PROJECTS_DIR.exists():
            for folder in sorted(PROJECTS_DIR.iterdir()):
                if folder.is_dir():
                    files = []
                    for f in sorted(folder.iterdir()):
                        if f.is_file():
                            files.append({"name": f.name, "size": f.stat().st_size,
                                          "url": f"/file/project/projects/{folder.name}/{f.name}"})
                    projects[folder.name] = files
        return {"ok": True, "projects": projects}
    except Exception as e:
        return {"ok": False, "error": str(e)}


# ── Saved projects registry (work in stages, save progress) ─────────────────────

def _load_registry() -> Dict[str, Any]:
    DATA_DIR.mkdir(exist_ok=True)
    if not PROJECTS_REGISTRY_PATH.exists():
        return {"projects": [], "next_id": 1}
    try:
        with open(PROJECTS_REGISTRY_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"projects": [], "next_id": 1}


def _save_registry(registry: Dict[str, Any]) -> None:
    DATA_DIR.mkdir(exist_ok=True)
    with open(PROJECTS_REGISTRY_PATH, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2)


def _sanitize_project_name(name: str) -> str:
    safe = re.sub(r"[^\w\-.]", "_", (name or "").strip()).strip("_") or "project"
    return safe[:80]


def create_project(name: str, description: str = "") -> Dict[str, Any]:
    """Create a new project folder under projects/ and register it. For new apps/tools, work in stages."""
    name = _sanitize_project_name(name)
    if not name:
        return {"ok": False, "error": "Invalid project name"}
    PROJECTS_DIR.mkdir(exist_ok=True)
    project_path = PROJECTS_DIR / name
    if project_path.exists() and any(project_path.iterdir()):
        return {"ok": False, "error": f"Project folder '{name}' already exists and is not empty"}
    project_path.mkdir(parents=True, exist_ok=True)
    registry = _load_registry()
    pid = f"proj_{int(time.time() * 1000)}"
    entry = {
        "id": pid,
        "name": name,
        "path": str(project_path),
        "path_relative": f"projects/{name}",
        "created": time.time(),
        "updated": time.time(),
        "description": (description or "").strip(),
        "notes": "",
    }
    registry["projects"].append(entry)
    _save_registry(registry)
    return {"ok": True, "project_id": pid, "name": name, "path": str(project_path), "project": entry}


def list_saved_projects() -> Dict[str, Any]:
    """List all saved projects (for continuing work, Agent Terminal project_path)."""
    registry = _load_registry()
    projects = registry.get("projects", [])
    return {"ok": True, "projects": projects}


def get_project(project_id: str) -> Optional[Dict[str, Any]]:
    registry = _load_registry()
    for p in registry.get("projects", []):
        if p.get("id") == project_id:
            return p
    return None


def update_project(project_id: str, **updates: Any) -> Dict[str, Any]:
    """Update project metadata (notes, description, etc.)."""
    registry = _load_registry()
    for p in registry.get("projects", []):
        if p.get("id") == project_id:
            for k, v in updates.items():
                if k in ("notes", "description", "updated"):
                    p[k] = v
            p["updated"] = time.time()
            _save_registry(registry)
            return {"ok": True, "project": p}
    return {"ok": False, "error": "Project not found"}

import joi_companion

def manage_projects(**kwargs) -> Dict[str, Any]:
    """Unified tool for managing Joi project workspaces."""
    action = kwargs.get("action")
    if not action:
        return {"ok": False, "error": "action parameter is required"}
        
    try:
        if action == "scan": return scan_projects(kwargs.get("roots"), kwargs.get("extensions"))
        elif action == "organise": return organise_into_projects(kwargs.get("categories", {}))
        elif action == "create": return create_project(kwargs.get("name", ""), kwargs.get("description", ""))
        elif action == "list_saved": return list_saved_projects()
        else: return {"ok": False, "error": f"Unknown action: {action}"}
    except Exception as exc:
        return {"ok": False, "error": f"Project action {action} failed: {exc}"}

# Register tools
joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "manage_projects",
        "description": "Unified tool to manage Joi projects (scan filesystem for files, organise them, create new projects, and list saved projects).",
        "parameters": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "description": "Action to perform",
                    "enum": ["scan", "organise", "create", "list_saved"]
                },
                "roots": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Folders to scan. Default: ['documents', 'desktop', 'downloads'] (for scan)"
                },
                "extensions": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "File extensions to scan. Default text/code formats (for scan)"
                },
                "categories": {
                    "type": "object",
                    "description": "Dict of categories and files to move (for organise)"
                },
                "name": {
                    "type": "string",
                    "description": "Project name (e.g. my_tool, weather_app) (required for create)"
                },
                "description": {
                    "type": "string",
                    "description": "Optional short description (for create)"
                }
            },
            "required": ["action"]
        }
    }},
    manage_projects,
)

# Register routes
from flask import jsonify, request as flask_req
from modules.joi_memory import require_user

def get_projects():
    require_user()
    return jsonify(list_projects())

def get_saved_projects():
    require_user()
    return jsonify(list_saved_projects())

def create_project_route():
    require_user()
    data = flask_req.get_json(force=True) or {}
    return jsonify(create_project(
        name=data.get("name", ""),
        description=data.get("description", ""),
    ))

def scan_projects_route():
    require_user()
    data = flask_req.get_json(force=True) or {}
    return jsonify(scan_projects(data.get("roots"), data.get("extensions")))

def organise_route():
    require_user()
    data = flask_req.get_json(force=True) or {}
    return jsonify(organise_into_projects(data.get("categories", {})))

joi_companion.register_route("/projects", ["GET"], get_projects, "get_projects")
joi_companion.register_route("/projects/saved", ["GET"], get_saved_projects, "get_saved_projects")
joi_companion.register_route("/projects/create", ["POST"], create_project_route, "create_project_route")
joi_companion.register_route("/projects/scan", ["POST"], scan_projects_route, "scan_projects_route")
joi_companion.register_route("/projects/organise", ["POST"], organise_route, "organise_route")
