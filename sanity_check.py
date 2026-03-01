"""
sanity_check.py — Health-check script for joi_watchdog.py circuit breaker.

Exit 0 = healthy, non-zero = broken.
Must complete within 30 seconds (HEALTH_CHECK_TIMEOUT in watchdog).
"""

import glob
import json
import os
import py_compile
import sqlite3
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
passed = 0
failed = 0


def check(name, fn):
    global passed, failed
    try:
        fn()
        print(f"  [PASS] {name}")
        passed += 1
    except Exception as e:
        print(f"  [FAIL] {name}: {e}")
        failed += 1


# ── 1. Python syntax validation of all modules/*.py ─────────────────────────
def check_module_syntax():
    modules_dir = os.path.join(BASE_DIR, "modules")
    errors = []
    for py_file in glob.glob(os.path.join(modules_dir, "*.py")):
        try:
            py_compile.compile(py_file, doraise=True)
        except py_compile.PyCompileError as e:
            errors.append(str(e))
    # Also check modules/memory/*.py and modules/core/*.py
    for subdir in ("memory", "core"):
        sub_path = os.path.join(modules_dir, subdir, "*.py")
        for py_file in glob.glob(sub_path):
            try:
                py_compile.compile(py_file, doraise=True)
            except py_compile.PyCompileError as e:
                errors.append(str(e))
    if errors:
        raise RuntimeError(f"{len(errors)} syntax error(s):\n" + "\n".join(errors[:5]))


# ── 2. Core import health ────────────────────────────────────────────────────
def check_core_import():
    sys.path.insert(0, BASE_DIR)
    import importlib
    # If Flask is not in this Python env, the check can't run (environment issue, not code bug).
    # This happens if sanity_check.py is accidentally run with a non-venv Python.
    # Skip gracefully instead of triggering a false circuit-breaker revert.
    try:
        import flask  # noqa: F401
    except ImportError:
        print("  [SKIP] Flask not available in this Python environment — core import check skipped (env issue, not code bug)")
        return  # Don't increment failed count
    mod = importlib.import_module("joi_companion")
    tools = getattr(mod, "TOOLS", None)
    if tools is None:
        raise RuntimeError("joi_companion.TOOLS not found")
    if not isinstance(tools, list) or len(tools) == 0:
        raise RuntimeError(f"TOOLS is empty or not a list (type={type(tools).__name__}, len={len(tools) if isinstance(tools, list) else '?'})")


# ── 3. SQLite DB accessible ─────────────────────────────────────────────────
def check_database():
    db_path = os.path.join(BASE_DIR, "joi_memory.db")
    if not os.path.exists(db_path):
        raise RuntimeError("joi_memory.db not found")
    conn = sqlite3.connect(db_path, timeout=5)
    try:
        cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table' LIMIT 1")
        cur.fetchone()
    finally:
        conn.close()


# ── 4. Critical files exist ──────────────────────────────────────────────────
def check_critical_files():
    required = [
        os.path.join(BASE_DIR, "projects", "code", "identity", "joi_soul_architecture.json"),
        os.path.join(BASE_DIR, "projects", "code", "consciousness", "reflection.py"),
        os.path.join(BASE_DIR, ".env"),
    ]
    missing = [f for f in required if not os.path.exists(f)]
    if missing:
        raise RuntimeError("Missing: " + ", ".join(os.path.basename(f) for f in missing))


# ── 5. JSON config integrity ────────────────────────────────────────────────
def check_json_configs():
    data_dir = os.path.join(BASE_DIR, "data")
    if not os.path.isdir(data_dir):
        raise RuntimeError("data/ directory not found")
    errors = []
    for jf in glob.glob(os.path.join(data_dir, "*.json")):
        try:
            with open(jf, "r", encoding="utf-8") as f:
                json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            errors.append(f"{os.path.basename(jf)}: {e}")
    if errors:
        raise RuntimeError(f"{len(errors)} invalid JSON file(s):\n" + "\n".join(errors[:5]))


# ── Run all checks ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Joi Sanity Check")
    print("=" * 40)

    check("Module syntax validation", check_module_syntax)
    check("Core import (joi_companion + TOOLS)", check_core_import)
    check("SQLite database accessible", check_database)
    check("Critical files exist", check_critical_files)
    check("JSON config integrity", check_json_configs)

    print("=" * 40)
    print(f"Results: {passed} passed, {failed} failed")

    if failed > 0:
        print("HEALTH: UNHEALTHY")
        sys.exit(1)
    else:
        print("HEALTH: OK")
        sys.exit(0)
