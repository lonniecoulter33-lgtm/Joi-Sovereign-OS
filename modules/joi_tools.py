"""
modules/joi_tools.py

Tool-Aware Execution (ReAct grounding)
======================================
Canonical schema and executors for core tools: web_search, execute_python_code,
and optional web_fetch. Registers with joi_companion only if not already present,
so existing modules can still own their tools; this module ensures a consistent
schema and adds execute_python_code for reasoning/calculation.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Optional

# ── Canonical tool schemas (OpenAI function-calling format) ──────────────────

WEB_SEARCH_SCHEMA = {
    "type": "function",
    "function": {
        "name": "web_search",
        "description": "Search the web for current information. Use for facts, definitions, or when the user asks to look something up.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query (e.g. 'Python 3.12 release date')"},
            },
            "required": ["query"],
        },
    },
}

EXECUTE_PYTHON_CODE_SCHEMA = {
    "type": "function",
    "function": {
        "name": "execute_python_code",
        "description": "Run Python code in a sandboxed subprocess. Use for calculations, data formatting, or small scripts. No network or file write by default.",
        "parameters": {
            "type": "object",
            "properties": {
                "code": {"type": "string", "description": "Python code to execute (e.g. 'print(2**10)')"},
                "timeout_sec": {"type": "integer", "description": "Max execution time in seconds", "default": 10},
            },
            "required": ["code"],
        },
    },
}

WEB_FETCH_SCHEMA = {
    "type": "function",
    "function": {
        "name": "web_fetch",
        "description": "Fetch raw content from a URL. Use when the user provides a link or asks to read a page.",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "Full URL to fetch"},
                "use_selenium": {"type": "boolean", "description": "Use browser for JS-heavy pages", "default": False},
            },
            "required": ["url"],
        },
    },
}


# ── Executors ───────────────────────────────────────────────────────────────

def _exec_web_search(query: str) -> Dict[str, Any]:
    """Search the web (DuckDuckGo Instant Answer API or fallback)."""
    try:
        import requests
    except ImportError:
        return {"ok": False, "error": "requests not installed", "results": []}
    try:
        url = "https://api.duckduckgo.com/"
        params = {"q": query, "format": "json", "no_redirect": "1", "no_html": "1"}
        headers = {"User-Agent": "JOI-Tools/1.0"}
        r = requests.get(url, params=params, headers=headers, timeout=10)
        r.raise_for_status()
        data = r.json()
        abstract = data.get("AbstractText", "") or data.get("Answer", "")
        results = []
        if abstract:
            results.append({"title": data.get("Heading", "Result"), "snippet": abstract, "url": data.get("AbstractURL", "")})
        for item in data.get("RelatedTopics", [])[:5]:
            if isinstance(item, dict) and item.get("Text"):
                results.append({"title": item.get("Text", "")[:80], "snippet": item.get("Text", ""), "url": item.get("FirstURL", "")})
        return {"ok": True, "query": query, "results": results[:8]}
    except Exception as e:
        return {"ok": False, "error": str(e)[:200], "results": []}


def _exec_execute_python_code(code: str, timeout_sec: int = 10) -> Dict[str, Any]:
    """Run Python code in a subprocess; return stdout, stderr, and result."""
    if not code or not code.strip():
        return {"ok": False, "error": "No code provided", "stdout": "", "stderr": ""}
    timeout_sec = max(1, min(30, int(timeout_sec)))
    try:
        proc = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            timeout=timeout_sec,
            cwd=Path(__file__).resolve().parent.parent,
        )
        out = (proc.stdout or "").strip()
        err = (proc.stderr or "").strip()
        return {
            "ok": proc.returncode == 0,
            "stdout": out[:8000],
            "stderr": err[:2000],
            "returncode": proc.returncode,
        }
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": f"Timeout after {timeout_sec}s", "stdout": "", "stderr": ""}
    except Exception as e:
        return {"ok": False, "error": str(e)[:200], "stdout": "", "stderr": ""}


def _exec_web_fetch(url: str, use_selenium: bool = False) -> Dict[str, Any]:
    """Fetch URL content. Prefer requests; optional Selenium if available."""
    if use_selenium:
        try:
            from modules.joi_browser import HAVE_SELENIUM, _get_browser
            if not HAVE_SELENIUM:
                return {"ok": False, "error": "Selenium not installed; use use_selenium=false for plain fetch"}
            browser = _get_browser()
            browser.get(url)
            import time
            time.sleep(2)
            text = browser.page_source[:50000]
            return {"ok": True, "url": url, "text": text[:15000], "source": "selenium"}
        except Exception as e:
            return {"ok": False, "error": str(e)[:200]}
    try:
        import requests
        headers = {"User-Agent": "Mozilla/5.0 (JOI-Tools/1.0)"}
        r = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
        r.raise_for_status()
        text = r.text[:50000]
        if len(r.text) > 50000:
            text += "\n... (truncated)"
        return {"ok": True, "url": url, "text": text[:15000]}
    except ImportError:
        return {"ok": False, "error": "requests not installed"}
    except Exception as e:
        return {"ok": False, "error": str(e)[:200]}


# ── Register with joi_companion if not already present ────────────────────────

def register_core_tools() -> None:
    """Register web_search, execute_python_code, and web_fetch if not already in TOOL_EXECUTORS."""
    import joi_companion
    existing = set(joi_companion.TOOL_EXECUTORS.keys())

    if "web_search" not in existing:
        joi_companion.register_tool(WEB_SEARCH_SCHEMA, _exec_web_search)
        print("  [joi_tools] Registered web_search")

    if "execute_python_code" not in existing:
        def _run_python(**kwargs):
            return _exec_execute_python_code(kwargs.get("code", ""), kwargs.get("timeout_sec", 10))
        joi_companion.register_tool(EXECUTE_PYTHON_CODE_SCHEMA, _run_python)
        print("  [joi_tools] Registered execute_python_code")

    if "web_fetch" not in existing:
        def _fetch(**kwargs):
            return _exec_web_fetch(kwargs.get("url", ""), kwargs.get("use_selenium", False))
        joi_companion.register_tool(WEB_FETCH_SCHEMA, _fetch)
        print("  [joi_tools] Registered web_fetch")


# Self-register on import (same pattern as other joi_* modules)
register_core_tools()
