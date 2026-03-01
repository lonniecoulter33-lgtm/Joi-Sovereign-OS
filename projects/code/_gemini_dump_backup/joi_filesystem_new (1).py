"""
Filesystem tools — read, write, search files (with "did you mean" suggestions)

This module is designed to be *safe-by-default*:
- By default, file access is limited to known roots (project/home/Desktop/etc).
- To allow searching outside your home folder (e.g., all of C:\), set:
    JOI_FS_ALLOW_ALL=1
Optionally, you can also set:
    JOI_FS_EXTRA_ROOTS=C:\SomeFolder;D:\OtherFolder
to add additional allowed roots.

Note: searching an entire drive can be slow. The search functions below include
caps to keep Joi responsive.
"""
from __future__ import annotations

import os
import re
import base64
import fnmatch
import difflib
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, Optional, List, Iterable, Tuple

try:
    from pypdf import PdfReader
    HAVE_PYPDF = True
except Exception:
    HAVE_PYPDF = False

BASE_DIR = Path(__file__).resolve().parent.parent

# ----------------------------
# Roots / access control
# ----------------------------

def _parse_extra_roots() -> Dict[str, str]:
    extra = os.getenv("JOI_FS_EXTRA_ROOTS", "").strip()
    out: Dict[str, str] = {}
    if not extra:
        return out
    parts = [p.strip().strip('"') for p in extra.split(";") if p.strip()]
    for i, p in enumerate(parts, start=1):
        try:
            rp = str(Path(p).expanduser().resolve())
            out[f"extra{i}"] = rp
        except Exception:
            continue
    return out

ALLOW_ALL = os.getenv("JOI_FS_ALLOW_ALL", "0").strip() == "1"

FILE_ROOTS: Dict[str, str] = {
    "project": str(BASE_DIR),
    "home": str(Path.home()),
    "desktop": str(Path.home() / "Desktop"),
    "documents": str(Path.home() / "Documents"),
    "downloads": str(Path.home() / "Downloads"),
    "pictures": str(Path.home() / "Pictures"),
    "music": str(Path.home() / "Music"),
    "videos": str(Path.home() / "Videos"),
}
FILE_ROOTS.update(_parse_extra_roots())

# Optional: enable full-drive access
if ALLOW_ALL:
    # Common Windows drive roots
    FILE_ROOTS.setdefault("c", r"C:\\")

# ----------------------------
# File type helpers
# ----------------------------

TEXT_EXTS = {
    ".txt", ".md", ".py", ".js", ".html", ".css", ".json", ".xml", ".yaml", ".yml",
    ".ini", ".cfg", ".log", ".csv", ".ts", ".tsx", ".jsx", ".sh", ".bat", ".ps1",
}
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".svg"}
PDF_EXTS = {".pdf"}
CODE_EXTS = {".py", ".js", ".ts", ".java", ".cpp", ".c", ".cs", ".go", ".rs", ".rb", ".php", ".html", ".css"}

MAX_READ = 5_000_000  # bytes

# Keep searches responsive on machines without a strong GPU/CPU
SEARCH_MAX_FILES_DEFAULT = int(os.getenv("JOI_FS_SEARCH_MAX_FILES", "25000"))
SEARCH_MAX_RESULTS_DEFAULT = int(os.getenv("JOI_FS_SEARCH_MAX_RESULTS", "50"))
SEARCH_MAX_FILESIZE_FOR_CONTENT = int(os.getenv("JOI_FS_SEARCH_MAX_FILESIZE", str(MAX_READ)))

# Skip very noisy / huge folders when allow_all is enabled
DEFAULT_SKIP_DIRS = {
    "$recycle.bin", "system volume information",
    "windows", "program files", "program files (x86)",
    "programdata",
    # node/python caches
    "node_modules", ".git", ".hg", ".svn",
    "__pycache__", ".venv", "venv",
}
# also skip these patterns anywhere
DEFAULT_SKIP_PATTERNS = [
    "*\\AppData\\Local\\Temp\\*",
    "*\\AppData\\Local\\Microsoft\\Windows\\INetCache\\*",
]

def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s or "").strip().lower()

def _root_path(root: str) -> Optional[Path]:
    if root not in FILE_ROOTS:
        return None
    try:
        rp = Path(FILE_ROOTS[root]).expanduser().resolve()
        return rp if rp.exists() else None
    except Exception:
        return None

def _suggest_root(bad_root: str) -> Optional[str]:
    keys = list(FILE_ROOTS.keys())
    m = difflib.get_close_matches(bad_root, keys, n=1, cutoff=0.55)
    return m[0] if m else None

def resolve_path(root: str, relpath: str) -> Tuple[Optional[Path], Optional[str]]:
    """
    Resolve root + relative path safely.
    Returns: (Path|None, error|None)
    """
    if root not in FILE_ROOTS:
        suggestion = _suggest_root(root)
        if suggestion:
            return None, f"Unknown root '{root}'. Did you mean '{suggestion}'?"
        return None, f"Unknown root '{root}'. Valid roots: {', '.join(sorted(FILE_ROOTS.keys()))}"

    root_path = _root_path(root)
    if not root_path:
        return None, f"Root '{root}' does not exist on disk."

    relpath = relpath or ""
    try:
        target = (root_path / relpath).expanduser().resolve()
        # prevent path traversal
        target.relative_to(root_path)
    except Exception:
        return None, f"Invalid path '{relpath}' for root '{root}'."
    return target, None

# ----------------------------
# Listing / reading / writing
# ----------------------------

def fs_list(root: str, dir: str = "", pattern: str = "*") -> Dict[str, Any]:
    try:
        base, err = resolve_path(root, dir)
        if err or not base or not base.is_dir():
            return {"ok": False, "error": err or f"Not a directory: {root}/{dir}"}

        items: List[Dict[str, Any]] = []
        for item in base.glob(pattern):
            try:
                rel = item.relative_to(Path(FILE_ROOTS[root]))
                st = item.stat()
                items.append({
                    "name": item.name,
                    "path": str(rel),
                    "type": "dir" if item.is_dir() else "file",
                    "size": st.st_size if item.is_file() else 0,
                    "modified": datetime.fromtimestamp(st.st_mtime).isoformat(),
                })
            except Exception:
                continue
        items.sort(key=lambda x: (x["type"] != "dir", x["name"].lower()))
        return {"ok": True, "root": root, "dir": dir, "items": items, "count": len(items)}
    except Exception as e:
        return {"ok": False, "error": f"{type(e).__name__}: {e}"}

def fs_read(root: str, path: str) -> Dict[str, Any]:
    try:
        fp, err = resolve_path(root, path)
        if err or not fp or not fp.is_file():
            return {"ok": False, "error": err or f"Not found: {root}/{path}"}

        size = fp.stat().st_size
        if size > MAX_READ:
            return {"ok": False, "error": f"File too large ({size} bytes). Limit is {MAX_READ} bytes."}

        ext = fp.suffix.lower()
        if ext in TEXT_EXTS or ext in CODE_EXTS or ext == "":
            return {"ok": True, "type": "text", "text": fp.read_text(encoding="utf-8", errors="replace"), "size": size}

        if ext in PDF_EXTS and HAVE_PYPDF:
            reader = PdfReader(str(fp))
            text = "\n\n".join((p.extract_text() or "") for p in reader.pages)
            return {"ok": True, "type": "pdf", "text": text, "pages": len(reader.pages), "size": size}

        if ext in IMAGE_EXTS:
            data = base64.b64encode(fp.read_bytes()).decode("utf-8")
            return {"ok": True, "type": "image", "data": f"data:image/{ext[1:]};base64,{data}", "size": size}

        return {"ok": False, "error": f"Unsupported file type: {ext}"}
    except Exception as e:
        return {"ok": False, "error": f"{type(e).__name__}: {e}"}

def fs_write(root: str, path: str, text: str, overwrite: bool = False) -> Dict[str, Any]:
    """
    Write a UTF-8 text file. Creates parent directories if needed.
    """
    try:
        fp, err = resolve_path(root, path)
        if err or not fp:
            return {"ok": False, "error": err or "Invalid path."}

        if fp.exists() and not overwrite:
            return {"ok": False, "error": "File exists. Set overwrite=true to replace it."}

        fp.parent.mkdir(parents=True, exist_ok=True)
        data = text if isinstance(text, str) else str(text)
        fp.write_text(data, encoding="utf-8", errors="replace")
        return {"ok": True, "path": path, "bytes": len(data.encode("utf-8", errors="replace"))}
    except Exception as e:
        return {"ok": False, "error": f"{type(e).__name__}: {e}"}

def fs_delete(root: str, path: str) -> Dict[str, Any]:
    """
    Delete a file (not a directory).
    """
    try:
        fp, err = resolve_path(root, path)
        if err or not fp:
            return {"ok": False, "error": err or "Invalid path."}
        if not fp.exists():
            return {"ok": False, "error": "Not found."}
        if fp.is_dir():
            return {"ok": False, "error": "Refusing to delete a directory. Delete files only."}
        fp.unlink()
        return {"ok": True, "path": path}
    except Exception as e:
        return {"ok": False, "error": f"{type(e).__name__}: {e}"}

# ----------------------------
# Smart search
# ----------------------------

def _should_skip_dir(dir_name: str) -> bool:
    return _norm(dir_name) in DEFAULT_SKIP_DIRS

def _matches_skip_patterns(p: str) -> bool:
    # simple fnmatch on Windows-like paths
    for pat in DEFAULT_SKIP_PATTERNS:
        if fnmatch.fnmatch(p, pat):
            return True
    return False

def _walk_files(base: Path, *, max_files: int, allow_all_mode: bool) -> Iterable[Path]:
    """
    Yield files under base with guardrails.
    """
    seen = 0
    for root, dirs, files in os.walk(base):
        if seen >= max_files:
            break

        # prune noisy folders, mostly relevant when allow_all scans a big tree
        if allow_all_mode:
            dirs[:] = [d for d in dirs if not _should_skip_dir(d)]
        # skip some noisy patterns
        if allow_all_mode and _matches_skip_patterns(root):
            dirs[:] = []
            continue

        for f in files:
            if seen >= max_files:
                break
            seen += 1
            yield Path(root) / f

def _did_you_mean(query: str, candidates: List[str]) -> List[str]:
    if not candidates:
        return []
    # Prefer close matches; keep short list
    matches = difflib.get_close_matches(query, candidates, n=5, cutoff=0.55)
    # Also try token-based contains matches
    qn = _norm(query)
    contains = [c for c in candidates if qn and qn in _norm(c)]
    out = []
    for x in matches + contains:
        if x not in out:
            out.append(x)
    return out[:5]

def fs_search(
    root: str,
    dir: str = "",
    query: str = "",
    *,
    mode: str = "auto",
    max_results: int = SEARCH_MAX_RESULTS_DEFAULT,
    max_files: int = SEARCH_MAX_FILES_DEFAULT,
) -> Dict[str, Any]:
    """
    Search for files by name and (optionally) by content.

    mode:
      - "name": filename only
      - "content": search text file contents too (slower)
      - "auto": name first; content only if query is >= 3 chars
    """
    try:
        query = (query or "").strip()
        if not query:
            return {"ok": False, "error": "query is required"}

        base, err = resolve_path(root, dir)
        if err or not base:
            return {"ok": False, "error": err or "Invalid base path."}
        if not base.exists():
            return {"ok": False, "error": "Base path does not exist."}

        allow_all_mode = (root == "c") and ALLOW_ALL

        q = query.lower()
        do_content = (mode == "content") or (mode == "auto" and len(q) >= 3)

        results: List[Dict[str, Any]] = []
        name_candidates: List[str] = []

        scanned = 0
        for item in _walk_files(base, max_files=max_files, allow_all_mode=allow_all_mode):
            scanned += 1
            if len(results) >= max_results:
                break

            name_candidates.append(item.name)

            # filename match
            if q in item.name.lower():
                results.append({
                    "path": str(item.relative_to(Path(FILE_ROOTS[root]))),
                    "name": item.name,
                    "match": "filename",
                    "size": item.stat().st_size if item.exists() else 0,
                })
                continue

            # content match (text-ish only, reasonably sized)
            if do_content and item.suffix.lower() in TEXT_EXTS:
                try:
                    st = item.stat()
                    if st.st_size > SEARCH_MAX_FILESIZE_FOR_CONTENT:
                        continue
                    content = item.read_text(encoding="utf-8", errors="ignore")
                    if q in content.lower():
                        snippet = ""
                        for line in content.splitlines():
                            if q in line.lower():
                                snippet = line.strip()[:200]
                                break
                        results.append({
                            "path": str(item.relative_to(Path(FILE_ROOTS[root]))),
                            "name": item.name,
                            "match": "content",
                            "snippet": snippet,
                            "size": st.st_size,
                        })
                except Exception:
                    pass

        # did-you-mean suggestions if zero matches
        suggestions: List[str] = []
        if not results:
            suggestions = _did_you_mean(query, list(dict.fromkeys(name_candidates))[:5000])

        return {
            "ok": True,
            "root": root,
            "dir": dir,
            "query": query,
            "mode": mode,
            "results": results,
            "count": len(results),
            "scanned_files": scanned,
            "truncated": scanned >= max_files or len(results) >= max_results,
            "did_you_mean": suggestions,
            "note": (
                "Tip: searching an entire drive can be slow; narrow the dir or use mode='name'."
                if allow_all_mode else None
            ),
        }
    except Exception as e:
        return {"ok": False, "error": f"{type(e).__name__}: {e}"}

def fs_search_all(
    query: str,
    *,
    roots: Optional[List[str]] = None,
    mode: str = "name",
    max_results: int = SEARCH_MAX_RESULTS_DEFAULT,
    max_files_per_root: int = 8000,
) -> Dict[str, Any]:
    """
    Convenience: search across multiple roots.
    Defaults to: project, home, desktop, documents, downloads
    """
    try:
        query = (query or "").strip()
        if not query:
            return {"ok": False, "error": "query is required"}

        roots = roots or ["project", "home", "desktop", "documents", "downloads"]
        out_results: List[Dict[str, Any]] = []
        root_summaries: List[Dict[str, Any]] = []

        for r in roots:
            if len(out_results) >= max_results:
                break
            resp = fs_search(r, "", query, mode=mode, max_results=max_results - len(out_results), max_files=max_files_per_root)
            if not resp.get("ok"):
                root_summaries.append({"root": r, "ok": False, "error": resp.get("error")})
                continue
            root_summaries.append({
                "root": r,
                "ok": True,
                "count": resp.get("count", 0),
                "scanned_files": resp.get("scanned_files", 0),
                "truncated": resp.get("truncated", False),
            })
            out_results.extend([dict(x, root=r) for x in resp.get("results", [])])

        return {"ok": True, "query": query, "mode": mode, "results": out_results, "count": len(out_results), "roots": root_summaries}
    except Exception as e:
        return {"ok": False, "error": f"{type(e).__name__}: {e}"}

# ----------------------------
# Register tools
# ----------------------------

import joi_companion

def _roots_enum() -> List[str]:
    return list(FILE_ROOTS.keys())

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "fs_list",
        "description": "List files and directories under an allowed root.",
        "parameters": {"type": "object", "properties": {
            "root": {"type": "string", "enum": _roots_enum()},
            "dir": {"type": "string", "default": ""},
            "pattern": {"type": "string", "default": "*"},
        }, "required": ["root"]}
    }},
    fs_list
)

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "fs_read",
        "description": "Read a file's contents (text/pdf/image) under an allowed root.",
        "parameters": {"type": "object", "properties": {
            "root": {"type": "string", "enum": _roots_enum()},
            "path": {"type": "string"},
        }, "required": ["root", "path"]}
    }},
    fs_read
)

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "fs_write",
        "description": "Write a UTF-8 text file under an allowed root.",
        "parameters": {"type": "object", "properties": {
            "root": {"type": "string", "enum": _roots_enum()},
            "path": {"type": "string"},
            "text": {"type": "string"},
            "overwrite": {"type": "boolean", "default": False},
        }, "required": ["root", "path", "text"]}
    }},
    fs_write
)

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "fs_delete",
        "description": "Delete a file under an allowed root (files only).",
        "parameters": {"type": "object", "properties": {
            "root": {"type": "string", "enum": _roots_enum()},
            "path": {"type": "string"},
        }, "required": ["root", "path"]}
    }},
    fs_delete
)

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "fs_search",
        "description": "Smart search for files by name and optionally by text content. Returns 'did_you_mean' suggestions when no results.",
        "parameters": {"type": "object", "properties": {
            "root": {"type": "string", "enum": _roots_enum()},
            "dir": {"type": "string", "default": ""},
            "query": {"type": "string"},
            "mode": {"type": "string", "enum": ["auto", "name", "content"], "default": "auto"},
            "max_results": {"type": "integer", "default": SEARCH_MAX_RESULTS_DEFAULT},
            "max_files": {"type": "integer", "default": SEARCH_MAX_FILES_DEFAULT},
        }, "required": ["root", "query"]}
    }},
    fs_search
)

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "fs_search_all",
        "description": "Search across multiple roots at once (project/home/desktop/documents/downloads by default).",
        "parameters": {"type": "object", "properties": {
            "query": {"type": "string"},
            "roots": {"type": "array", "items": {"type": "string", "enum": _roots_enum()}},
            "mode": {"type": "string", "enum": ["auto", "name", "content"], "default": "name"},
            "max_results": {"type": "integer", "default": SEARCH_MAX_RESULTS_DEFAULT},
            "max_files_per_root": {"type": "integer", "default": 8000},
        }, "required": ["query"]}
    }},
    fs_search_all
)
