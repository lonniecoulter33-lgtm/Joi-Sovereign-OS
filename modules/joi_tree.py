"""
modules/joi_tree.py

Project Tree Generator — Spatial awareness for the 3-Tier workflow.
===============================================================
Produces an ASCII directory tree so Architect/Implementer/Reviewer can
re-orient, verify created files, and suggest pruning. Optional JOI_MAP.md
persists the layout at end of coding sessions.

Usage:
  - Architect: call at start of task to see existing structure before adding files.
  - Implementer: call after creating files to confirm they're in the right place.
  - Reviewer: compare tree to plan to audit missing/extra files.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Set

BASE_DIR = Path(__file__).resolve().parent.parent

# Directories to skip so the tree stays readable and token-lean
DEFAULT_IGNORE: Set[str] = {
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "node_modules",
    ".env",
    ".tox",
    "dist",
    "build",
    "*.egg-info",
    "sandbox",  # e.g. data/sandbox
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
}
# For matching we only care about directory names (no glob in pathlib.walk for dirs)
_IGNORE_DIR_NAMES = {d for d in DEFAULT_IGNORE if "*" not in d}


def generate_project_tree(
    root_dir: Optional[Path | str] = None,
    max_depth: int = 10,
    ignore_dirs: Optional[Set[str]] = None,
    max_children: int = 50,
) -> str:
    """
    Return an ASCII tree of the directory structure using ├── and └──.

    Ignores .git, __pycache__, .venv, node_modules, data/sandbox, etc.
    Truncates per-folder listing to max_children to avoid huge output.
    """
    root = Path(root_dir) if root_dir else BASE_DIR
    root = root.resolve()
    if not root.is_dir():
        return f"[Not a directory: {root}]"
    ignore = set(ignore_dirs) if ignore_dirs else _IGNORE_DIR_NAMES
    lines: list[str] = [root.name + "/"]
    _walk(root, prefix="", lines=lines, depth=0, max_depth=max_depth, ignore=ignore, max_children=max_children)
    return "\n".join(lines)


def _walk(
    dir_path: Path,
    prefix: str,
    lines: list[str],
    depth: int,
    max_depth: int,
    ignore: Set[str],
    max_children: int,
) -> None:
    if depth >= max_depth:
        return
    try:
        entries = sorted(dir_path.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
    except OSError:
        return
    # Filter and cap
    filtered: list[Path] = []
    for p in entries:
        if p.name in ignore:
            continue
        filtered.append(p)
    if len(filtered) > max_children:
        filtered = filtered[:max_children]
        truncated = True
    else:
        truncated = False
    for i, p in enumerate(filtered):
        is_last = i == len(filtered) - 1 and not truncated
        branch = "└── " if is_last else "├── "
        name = p.name + ("/" if p.is_dir() else "")
        lines.append(prefix + branch + name)
        if p.is_dir():
            extension = "    " if is_last else "│   "
            _walk(
                p,
                prefix + extension,
                lines,
                depth + 1,
                max_depth,
                ignore,
                max_children,
            )
    if truncated:
        lines.append(prefix + "└── ... (%d more)" % (len(entries) - max_children))


def update_joi_map(root_dir: Optional[Path | str] = None) -> str:
    """
    Generate the project tree and write it to JOI_MAP.md in the project root.
    Call at end of a coding session to give Joi a persistent layout memory.
    Returns the path to JOI_MAP.md and a short confirmation message.
    """
    root = Path(root_dir) if root_dir else BASE_DIR
    root = root.resolve()
    tree = generate_project_tree(root_dir=root)
    map_path = root / "JOI_MAP.md"
    header = "# JOI_MAP.md — Project layout (auto-generated)\n\n"
    body = "```\n" + tree + "\n```\n"
    try:
        map_path.write_text(header + body, encoding="utf-8")
        return f"Updated {map_path}. Use this file for context on project structure."
    except OSError as e:
        return f"Could not write JOI_MAP.md: {e}"


# ── Tool registration ─────────────────────────────────────────────────────
try:
    import joi_companion
except ImportError:
    joi_companion = None

PROJECT_TREE_SCHEMA = {
    "type": "function",
    "function": {
        "name": "project_tree",
        "description": (
            "Generate an ASCII directory tree of the project (spatial awareness). "
            "Use at the START of a coding task to re-orient (e.g. see if helpers/ or utils already exist), "
            "or after creating files to verify they are in the right place. "
            "Optionally save the tree to JOI_MAP.md for persistent layout memory. "
            "Ignores .git, __pycache__, .venv, node_modules, sandbox."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "root": {
                    "type": "string",
                    "description": "Root to list: 'project' (default, Joi workspace root) or a path relative to project.",
                    "default": "project",
                },
                "save_to_joi_map": {
                    "type": "boolean",
                    "description": "If true, write the tree to JOI_MAP.md in the project root for persistent layout memory.",
                    "default": False,
                },
                "max_depth": {
                    "type": "integer",
                    "description": "Maximum directory depth (default 10).",
                    "default": 10,
                },
            },
            "required": [],
        },
    },
}


def _exec_project_tree(
    root: str = "project",
    save_to_joi_map: bool = False,
    max_depth: int = 10,
) -> str:
    if root == "project" or not root.strip():
        root_path = BASE_DIR
    else:
        root_path = BASE_DIR / root.strip().lstrip("/")
    root_path = root_path.resolve()
    try:
        root_path.relative_to(BASE_DIR)
    except ValueError:
        return f"Path must be under project root. Got: {root_path}"
    if not root_path.is_dir():
        return f"Not a directory: {root_path}"
    tree = generate_project_tree(root_dir=root_path, max_depth=max(1, min(20, max_depth)))
    if save_to_joi_map:
        update_joi_map(BASE_DIR)
    return tree


if joi_companion is not None:
    joi_companion.register_tool(PROJECT_TREE_SCHEMA, _exec_project_tree)

print("  [OK] joi_tree (project_tree) loaded")
