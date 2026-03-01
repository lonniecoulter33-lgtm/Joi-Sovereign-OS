"""
modules/joi_tester.py

Adversarial Tester — Sandboxed execution for true self-healing.
=============================================================
Runs Python code in a restricted sandbox with timeout. Captures stdout/stderr.
If the code fails (non-zero exit, SyntaxError, ImportError), returns a
Correction Prompt for the Implementer so the loop can fix without user intervention.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, Optional

BASE_DIR = Path(__file__).resolve().parent.parent
# Restricted sandbox under data/ so it's writable and contained
SANDBOX_DIR = BASE_DIR / "data" / "sandbox"
SANDBOX_DIR.mkdir(parents=True, exist_ok=True)

TIMEOUT_SEC = 5


def run_code_sandbox(
    code_text: str,
    file_name: str = "temp_test.py",
    timeout_sec: int = TIMEOUT_SEC,
) -> Dict[str, Any]:
    """
    Run Python code in a sandboxed subprocess with strict timeout.

    - Writes code to a temp file under data/sandbox/
    - Uses subprocess.run with timeout_sec (default 5)
    - Captures stdout and stderr
    - Returns: {"success": bool, "output": str, "error": str, "exit_code": int}
    - If stderr contains SyntaxError or ImportError, also returns "correction_prompt"
      for the Implementer (high-priority self-correction).
    """
    if not code_text or not code_text.strip():
        return {"success": False, "output": "", "error": "No code provided", "exit_code": -1}

    safe_name = re.sub(r"[^\w\-.]", "_", file_name)[:64]
    if not safe_name.endswith(".py"):
        safe_name += ".py"
    path = SANDBOX_DIR / safe_name

    try:
        path.write_text(code_text, encoding="utf-8")
    except Exception as e:
        return {"success": False, "output": "", "error": f"Write failed: {e}", "exit_code": -1}

    try:
        proc = subprocess.run(
            [sys.executable, str(path)],
            capture_output=True,
            text=True,
            timeout=max(1, min(30, timeout_sec)),
            cwd=str(SANDBOX_DIR),
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        )
        stdout = (proc.stdout or "").strip()
        stderr = (proc.stderr or "").strip()
        success = proc.returncode == 0
        out = {
            "success": success,
            "output": stdout[:8000],
            "error": stderr[:4000],
            "exit_code": proc.returncode,
        }
        # Build correction prompt for Implementer when run failed
        if not success and stderr:
            out["correction_prompt"] = _build_correction_prompt(stderr, code_text)
        return out
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "output": "",
            "error": f"Timeout after {timeout_sec}s",
            "exit_code": -2,
            "correction_prompt": f"The previous code timed out after {timeout_sec} seconds. Simplify or fix infinite loops.",
        }
    except Exception as e:
        return {
            "success": False,
            "output": "",
            "error": str(e)[:500],
            "exit_code": -1,
            "correction_prompt": f"The execution failed: {e}. Fix the code and try again.",
        }
    finally:
        try:
            if path.exists():
                path.unlink()
        except Exception:
            pass


def _build_correction_prompt(stderr: str, code_preview: str) -> str:
    """
    Wrap stderr in a high-priority Self-Correction prompt for the Implementer.
    Emphasize SyntaxError and ImportError so the model can pinpoint the fix.
    """
    stderr_snippet = stderr[:2000].strip()
    return (
        "[SELF-CORRECTION — High Priority] The previous code failed when run. "
        "Fix the code and output only the corrected version.\n\n"
        "Error from interpreter:\n"
        "```\n" + stderr_snippet + "\n```\n\n"
        "Do not repeat the error; fix the code and try again."
    )


def extract_python_blocks(text: str) -> list[str]:
    """Extract ```python ... ``` blocks from assistant output."""
    if not text:
        return []
    pattern = r"```(?:python|py)\s*\n([\s\S]*?)```"
    blocks = re.findall(pattern, text, re.IGNORECASE)
    return [b.strip() for b in blocks if b.strip()]


def should_run_sandbox_for_step(step_description: str, step_output: str) -> bool:
    """True if this step likely produced runnable Python (write/fix/implement + code block)."""
    desc_lower = (step_description or "").lower()
    code_indicators = ("write", "implement", "fix", "code", "function", "script", "run", "def ", "import ")
    if not any(x in desc_lower for x in code_indicators):
        return False
    return bool(extract_python_blocks(step_output))
