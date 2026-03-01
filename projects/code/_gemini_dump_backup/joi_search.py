from __future__ import annotations
import os
import re
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

# ---- helpers ---------------------------------------------------------

def _safe_err(msg: str, hint: str = "") -> Dict[str, Any]:
    out = {"ok": False, "error": msg}
    if hint:
        out["hint"] = hint
    return out

def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip().lower())

def _looks_like_glob(q: str) -> bool:
    return any(ch in q for ch in ["*", "?", "["])

def _iter_files(root: Path, max_files: int, exts: Optional[List[str]]) -> Tuple[List[Path], Optional[str]]:
    """
    Walk root safely. Returns (paths, warning).
    """
    results: List[Path] = []
    warning = None

    try:
        for dirpath, dirnames, filenames in os.walk(root):
            # Skip very heavy folders
            dn_lower = {d.lower() for d in dirnames}
            # You can tune these:
            skip = {"node_modules", ".git", "__pycache__", ".venv", "venv", "dist", "build"}
            dirnames[:] = [d for d in dirnames if d.lower() not in skip]

            for fn in filenames:
                p = Path(dirpath) / fn
                if exts:
                    if p.suffix.lower().lstrip(".") not in exts:
                        continue
                results.append(p)
                if len(results) >= max_files:
                    warning = f"Stopped early at {max_files} files for speed."
                    return results, warning
    except PermissionError:
        warning = "Some folders were skipped due to permissions."
    except Exception as e:
        warning = f"Search hit an unexpected issue: {type(e).__name__}"
    return results, warning

def _score(path: Path, q: str) -> int:
    """
    Simple scoring:
    - exact filename match high
    - substring in filename medium
    - substring in full path low
    """
    qn = _norm(q)
    name = _norm(path.name)
    full = _norm(str(path))
    if name == qn:
        return 100
    if qn in name:
        return 70
    if qn in full:
        return 40
    return 0

# ---- module registration --------------------------------------------

def register(joi_companion, require_user, BASE_DIR: Path, resolve_path):
    """
    resolve_path should be your existing modules.joi_filesystem.resolve_path(root, relpath)
    We will also use it to constrain searches to allowed roots.
    """

    # Allowed roots (match your /file/<root>/<relpath> design)
    # Add/adjust names to match your existing filesystem module.
    ALLOWED_ROOTS = ["project", "downloads", "documents", "desktop"]

    def search_files(**params) -> Dict[str, Any]:
        require_user()

        query = (params.get("query") or "").strip()
        root_name = (params.get("root") or "project").strip().lower()
        max_results = int(params.get("max_results") or 20)
        max_files = int(params.get("max_files_scanned") or 25000)
        exts = params.get("extensions")  # like ["pdf","docx","txt"]
        contains = (params.get("contains_text") or "").strip()  # optional file content search (text only)

        if not query:
            return _safe_err("No query provided.", "Provide a filename (or part of it).")
        if root_name not in ALLOWED_ROOTS:
            return _safe_err("Root not allowed.", f"Allowed roots: {', '.join(ALLOWED_ROOTS)}")
        if max_results < 1:
            max_results = 10
        if max_results > 50:
            max_results = 50

        # Resolve the base folder safely using your existing resolver
        base = resolve_path(root_name, "")
        if not base or not base.exists():
            return _safe_err("Search root not found.", f"Root '{root_name}' does not resolve to a folder.")
        if not base.is_dir():
            return _safe_err("Search root is not a folder.", f"Resolved path: {base}")

        if exts and isinstance(exts, list):
            exts = [str(x).lower().lstrip(".") for x in exts if str(x).strip()]
        else:
            exts = None

        # Walk files
        files, warning = _iter_files(base, max_files=max_files, exts=exts)

        # Glob search (fast path)
        matches: List[Path] = []
        q = query
        if _looks_like_glob(q):
            try:
                matches = list(base.rglob(q))
            except Exception:
                matches = []
        else:
            # Fuzzy filename/path scoring
            scored = [(p, _score(p, q)) for p in files]
            scored = [sp for sp in scored if sp[1] > 0]
            scored.sort(key=lambda x: x[1], reverse=True)
            matches = [p for p, s in scored[:max_results * 5]]

        # Optional text content search (very limited + safe)
        if contains:
            ct = _norm(contains)
            filtered = []
            for p in matches:
                # only small-ish text files
                if p.suffix.lower() not in [".txt", ".md", ".py", ".json", ".csv", ".log"]:
                    continue
                try:
                    if p.stat().st_size > 2_000_000:  # 2MB cap
                        continue
                    text = p.read_text(errors="ignore").lower()
                    if ct in text:
                        filtered.append(p)
                except Exception:
                    continue
            matches = filtered

        # Limit final results
        matches = matches[:max_results]

        # Return safe, UI-friendly links using your /file route
        items = []
        for p in matches:
            try:
                rel = p.relative_to(base).as_posix()
            except Exception:
                rel = p.name
            items.append({
                "name": p.name,
                "path": str(p),
                "url": f"/file/{root_name}/{rel}"
            })

        out = {"ok": True, "query": query, "root": root_name, "results": items}
        if warning:
            out["warning"] = warning
        return out

    # Register as a tool callable by the LLM
    joi_companion.register_tool(
        {"type": "function", "function": {
            "name": "search_files",
            "description": "Search for files on the computer by filename/path (safe). Returns download/open URLs. Use when user asks 'find my X file'.",
            "parameters": {"type": "object", "properties": {
                "query": {"type":"string", "description":"Filename or partial name. Supports wildcards like *.pdf"},
                "root": {"type":"string", "description":"Where to search: project, downloads, documents, desktop", "default":"project"},
                "max_results": {"type":"integer", "default": 20},
                "extensions": {"type":"array", "items":{"type":"string"}, "description":"Optional list like ['pdf','docx']"},
                "contains_text": {"type":"string", "description":"Optional: only return files that contain this text (text files only)"},
                "max_files_scanned": {"type":"integer", "default": 25000}
            }, "required":["query"]}
        }},
        search_files
    )

    # Also provide a route for the UI if you want to test it directly
    from flask import jsonify, request
    def search_files_route():
        require_user()
        data = request.get_json(force=True) or {}
        return jsonify(search_files(**data))
    joi_companion.register_route("/files/search", ["POST"], search_files_route, "search_files_route")
