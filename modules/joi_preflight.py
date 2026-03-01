"""
modules/joi_preflight.py

Pre-Flight Validator for Agent Terminal
=======================================
Validates code changes BEFORE they are written to disk.
Three validation stages:
  1. AST syntax check (ast.parse)
  2. Import graph resolution (verify imports exist)
  3. Compile check in isolated namespace

Called by:
  - joi_orchestrator._apply_changes_direct() before writing
  - joi_watchdog.safe_edit_incremental() as pre-apply gate
"""

import ast
import importlib
import importlib.util
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

BASE_DIR = Path(__file__).resolve().parent.parent

# ── Module registry cache (loaded once from file_registry.json) ──────────────
_source_modules: Optional[Dict[str, str]] = None


def _load_source_registry() -> Dict[str, str]:
    """Load source_modules map from file_registry.json (cached)."""
    global _source_modules
    if _source_modules is not None:
        return _source_modules

    registry_path = BASE_DIR / "file_registry.json"
    try:
        if registry_path.exists():
            with open(registry_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            _source_modules = data.get("source_modules", {})
        else:
            _source_modules = {}
    except Exception:
        _source_modules = {}
    return _source_modules


def reload_registry():
    """Force reload of source module registry (call after registry changes)."""
    global _source_modules
    _source_modules = None
    _load_source_registry()


# ══════════════════════════════════════════════════════════════════════════════
# STAGE 1: AST SYNTAX VALIDATION
# ══════════════════════════════════════════════════════════════════════════════

def _check_syntax(source: str, file_path: str = "<string>") -> Dict[str, Any]:
    """Parse source with ast.parse. Returns {passed, errors}."""
    try:
        ast.parse(source, filename=file_path)
        return {"passed": True, "errors": []}
    except SyntaxError as e:
        return {
            "passed": False,
            "errors": [
                f"SyntaxError at line {e.lineno}, col {e.offset}: {e.msg}"
            ],
        }


# ══════════════════════════════════════════════════════════════════════════════
# STAGE 2: IMPORT GRAPH RESOLUTION
# ══════════════════════════════════════════════════════════════════════════════

# Modules that are known to exist but may not be findable via importlib.util
_KNOWN_INTERNAL_PREFIXES = (
    "modules.", "consciousness.", "identity.", "config.",
    "plugins.", "core.",
)

# Stdlib modules that importlib.util.find_spec can resolve
_STDLIB_SKIP = {
    "sys", "os", "re", "json", "time", "datetime", "pathlib", "math",
    "hashlib", "threading", "subprocess", "importlib", "collections",
    "functools", "itertools", "typing", "io", "traceback", "ast",
    "glob", "shutil", "copy", "abc", "enum", "dataclasses", "textwrap",
    "difflib", "sqlite3", "base64", "uuid", "secrets", "logging",
    "socket", "http", "urllib", "email", "tempfile", "signal",
    "contextlib", "inspect", "struct", "queue", "concurrent",
    "multiprocessing", "asyncio", "ssl", "csv", "xml", "html",
    "unittest", "py_compile", "compileall", "pdb", "profile",
    "string", "random", "statistics", "decimal", "fractions",
}


def _extract_imports(source: str) -> List[Dict[str, str]]:
    """Extract all import statements from source code."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []

    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append({
                    "type": "import",
                    "module": alias.name,
                    "line": node.lineno,
                })
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append({
                    "type": "from",
                    "module": node.module,
                    "line": node.lineno,
                })
    return imports


def _check_imports(source: str, file_path: str = "") -> Dict[str, Any]:
    """
    Check that all imported modules can be resolved.
    Returns {passed, errors, warnings}.
    """
    imports = _extract_imports(source)
    errors = []
    warnings = []
    registry = _load_source_registry()

    for imp in imports:
        module_name = imp["module"]
        top_level = module_name.split(".")[0]

        # Skip stdlib
        if top_level in _STDLIB_SKIP:
            continue

        # Skip known internal prefixes (they're loaded dynamically)
        if any(module_name.startswith(p) for p in _KNOWN_INTERNAL_PREFIXES):
            # Check if it's in the source registry
            stem = module_name.split(".")[-1]
            if stem in registry:
                continue  # Verified in registry
            # Still allow — these are dynamically loaded
            continue

        # Try importlib.util.find_spec for installed packages
        try:
            spec = importlib.util.find_spec(top_level)
            if spec is None:
                warnings.append(
                    f"Line {imp['line']}: '{module_name}' - top-level '{top_level}' "
                    f"not found in current environment (may be optional)"
                )
        except (ModuleNotFoundError, ValueError):
            warnings.append(
                f"Line {imp['line']}: '{module_name}' - could not resolve "
                f"'{top_level}' (may need to install or may be a local import)"
            )

    return {
        "passed": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
    }


# ══════════════════════════════════════════════════════════════════════════════
# STAGE 3: COMPILE CHECK
# ══════════════════════════════════════════════════════════════════════════════

def _check_compile(source: str, file_path: str = "<string>") -> Dict[str, Any]:
    """Attempt compile() in an isolated namespace. Returns {passed, errors}."""
    try:
        compile(source, file_path, "exec")
        return {"passed": True, "errors": []}
    except SyntaxError as e:
        return {
            "passed": False,
            "errors": [f"CompileError at line {e.lineno}: {e.msg}"],
        }
    except Exception as e:
        return {
            "passed": False,
            "errors": [f"CompileError: {type(e).__name__}: {e}"],
        }


# ══════════════════════════════════════════════════════════════════════════════
# MAIN ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

def preflight_validate(
    file_path: str,
    original_content: str,
    modified_content: str,
) -> Dict[str, Any]:
    """
    Run all pre-flight validation stages on modified content.

    Args:
        file_path: Path to the file being modified
        original_content: Original file content (for reference)
        modified_content: Proposed new content to validate

    Returns:
        {
            "passed": bool,
            "errors": [...],
            "warnings": [...],
            "stages": {
                "syntax": {passed, errors},
                "imports": {passed, errors, warnings},
                "compile": {passed, errors},
            }
        }
    """
    result = {
        "passed": True,
        "errors": [],
        "warnings": [],
        "stages": {},
    }

    # Only validate Python files
    if not file_path.endswith(".py"):
        result["stages"]["skipped"] = {"passed": True, "message": "Non-Python file"}
        return result

    # Stage 1: AST Syntax
    syntax = _check_syntax(modified_content, file_path)
    result["stages"]["syntax"] = syntax
    if not syntax["passed"]:
        result["passed"] = False
        result["errors"].extend(syntax["errors"])
        # Early return — no point checking imports/compile if syntax is broken
        return result

    # Stage 2: Import Resolution
    imports = _check_imports(modified_content, file_path)
    result["stages"]["imports"] = imports
    if not imports["passed"]:
        result["passed"] = False
        result["errors"].extend(imports["errors"])
    result["warnings"].extend(imports.get("warnings", []))

    # Stage 3: Compile Check
    comp = _check_compile(modified_content, file_path)
    result["stages"]["compile"] = comp
    if not comp["passed"]:
        result["passed"] = False
        result["errors"].extend(comp["errors"])

    return result


def preflight_validate_content(content: str, file_path: str = "<string>") -> Dict[str, Any]:
    """Convenience wrapper — validate content without original (for new files)."""
    return preflight_validate(file_path, "", content)


# ── Self-register as a tool so Joi can call it directly ──────────────────────
try:
    import joi_companion
    joi_companion.register_tool(
        {
            "type": "function",
            "function": {
                "name": "preflight_check",
                "description": (
                    "Run pre-flight validation on Python source code before applying changes. "
                    "Returns syntax errors, import issues, and compilation problems. "
                    "Use this BEFORE code_edit or creative_edit to catch errors early."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "Path to the Python file to validate",
                        },
                        "content": {
                            "type": "string",
                            "description": "The modified source code to validate",
                        },
                    },
                    "required": ["file_path", "content"],
                },
            },
        },
        lambda **kwargs: preflight_validate_content(
            kwargs.get("content", ""),
            kwargs.get("file_path", "<string>"),
        ),
    )
    print("    [OK] joi_preflight (Pre-Flight Validator: 1 tool)")
except Exception:
    pass
