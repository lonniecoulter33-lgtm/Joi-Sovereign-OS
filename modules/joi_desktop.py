"""
Desktop Automation -- mouse, keyboard, screenshots, window management

REQUIRES: pip install pyautogui pillow
OPTIONAL: pip install pywinauto  (for window management)
"""
import os
import re
import time
import fnmatch
from pathlib import Path
from typing import Dict, Any, List, Optional

try:
    import pyautogui
    import io
    import base64
    from PIL import Image
    HAVE_PYAUTOGUI = True
except ImportError:
    HAVE_PYAUTOGUI = False
    print("  WARNING: pyautogui not installed. Run: pip install pyautogui pillow")

try:
    import pywinauto
    from pywinauto import Desktop as PwaDesktop
    HAVE_PYWINAUTO = True
except ImportError:
    HAVE_PYWINAUTO = False
    print("  [joi_desktop] pywinauto not installed -- window management unavailable. Run: pip install pywinauto")

BASE_DIR = Path(__file__).resolve().parent.parent

# ── Directory cache for find_file_smart ──────────────────────────────────────
_dir_cache: Dict[str, tuple] = {}  # path -> (entries_list, cache_ts)
_DIR_CACHE_TTL = 60.0


# ── Core mouse/keyboard tools ───────────────────────────────────────────────

def move_mouse(**kwargs):
    x = kwargs.get("x")
    y = kwargs.get("y")
    duration = kwargs.get("duration", 0.5)
    if not HAVE_PYAUTOGUI:
        return {"ok": False, "error": "pyautogui not installed"}
    try:
        pyautogui.moveTo(int(x), int(y), duration=float(duration))
        return {"ok": True, "message": f"Mouse moved to ({x}, {y})"}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def click_mouse(**kwargs):
    button = kwargs.get("button", "left")
    x = kwargs.get("x")
    y = kwargs.get("y")
    if not HAVE_PYAUTOGUI:
        return {"ok": False, "error": "pyautogui not installed"}
    try:
        if x is not None and y is not None:
            pyautogui.click(int(x), int(y), button=button)
        else:
            pyautogui.click(button=button)
        return {"ok": True, "message": f"Clicked {button} button"}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def type_text(**kwargs):
    text = kwargs.get("text", "")
    interval = kwargs.get("interval", 0.05)
    if not HAVE_PYAUTOGUI:
        return {"ok": False, "error": "pyautogui not installed"}
    try:
        pyautogui.typewrite(text, interval=float(interval))
        return {"ok": True, "message": f"Typed: {text[:50]}..."}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def press_key(**kwargs):
    key = kwargs.get("key", "")
    if not HAVE_PYAUTOGUI:
        return {"ok": False, "error": "pyautogui not installed"}
    try:
        pyautogui.press(key)
        return {"ok": True, "message": f"Pressed: {key}"}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def screenshot(**kwargs):
    """Take screenshot. region format: 'x,y,width,height' or None for full screen."""
    region = kwargs.get("region")
    if not HAVE_PYAUTOGUI:
        return {"ok": False, "error": "pyautogui not installed"}
    try:
        if region:
            parts = [int(p) for p in region.split(',')]
            if len(parts) != 4:
                return {"ok": False, "error": "region must be 'x,y,w,h'"}
            img = pyautogui.screenshot(region=parts)
        else:
            img = pyautogui.screenshot()

        buf = io.BytesIO()
        img.save(buf, format='PNG')
        b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        return {"ok": True, "message": "Screenshot taken", "data": f"data:image/png;base64,{b64}"}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def get_mouse_position(**kwargs):
    if not HAVE_PYAUTOGUI:
        return {"ok": False, "error": "pyautogui not installed"}
    try:
        x, y = pyautogui.position()
        return {"ok": True, "x": x, "y": y}
    except Exception as e:
        return {"ok": False, "error": str(e)}


# ── Window management (pywinauto) ───────────────────────────────────────────

def list_windows(**kwargs) -> Dict[str, Any]:
    """List all visible windows with title, handle, process, and rect."""
    if not HAVE_PYWINAUTO:
        return {"ok": False, "error": "pywinauto not installed. Run: pip install pywinauto"}
    visible_only = kwargs.get("visible_only", True)
    try:
        desktop = PwaDesktop(backend="uia")
        windows = desktop.windows()
        result = []
        for w in windows:
            try:
                title = w.window_text()
                if not title:
                    continue
                if visible_only and not w.is_visible():
                    continue
                rect = w.rectangle()
                result.append({
                    "title": title,
                    "handle": w.handle,
                    "pid": w.process_id(),
                    "visible": w.is_visible(),
                    "rect": {
                        "left": rect.left,
                        "top": rect.top,
                        "right": rect.right,
                        "bottom": rect.bottom
                    }
                })
            except Exception:
                continue
        return {"ok": True, "windows": result, "count": len(result)}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def find_window(**kwargs) -> Dict[str, Any]:
    """Find windows matching a title pattern (case-insensitive substring or regex)."""
    if not HAVE_PYWINAUTO:
        return {"ok": False, "error": "pywinauto not installed. Run: pip install pywinauto"}
    title_pattern = kwargs.get("title_pattern", "").strip()
    if not title_pattern:
        return {"ok": False, "error": "Provide a 'title_pattern' to search for."}
    try:
        desktop = PwaDesktop(backend="uia")
        windows = desktop.windows()
        pattern_lower = title_pattern.lower()
        matches = []
        for w in windows:
            try:
                title = w.window_text()
                if not title:
                    continue
                # Case-insensitive substring match, or regex
                if pattern_lower in title.lower() or re.search(title_pattern, title, re.IGNORECASE):
                    rect = w.rectangle()
                    matches.append({
                        "title": title,
                        "handle": w.handle,
                        "pid": w.process_id(),
                        "visible": w.is_visible(),
                        "rect": {
                            "left": rect.left,
                            "top": rect.top,
                            "right": rect.right,
                            "bottom": rect.bottom
                        }
                    })
            except Exception:
                continue
        return {"ok": True, "matches": matches, "count": len(matches)}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def focus_window(**kwargs) -> Dict[str, Any]:
    """Find a window by title pattern and bring it to the foreground."""
    if not HAVE_PYWINAUTO:
        return {"ok": False, "error": "pywinauto not installed. Run: pip install pywinauto"}
    title_pattern = kwargs.get("title_pattern", "").strip()
    if not title_pattern:
        return {"ok": False, "error": "Provide a 'title_pattern' to focus."}
    try:
        desktop = PwaDesktop(backend="uia")
        windows = desktop.windows()
        pattern_lower = title_pattern.lower()
        target = None
        for w in windows:
            try:
                title = w.window_text()
                if title and (pattern_lower in title.lower() or re.search(title_pattern, title, re.IGNORECASE)):
                    target = w
                    break
            except Exception:
                continue

        if not target:
            return {"ok": False, "error": f"No window matching '{title_pattern}' found."}

        # Restore if minimized, then focus
        if target.is_minimized():
            target.restore()
            time.sleep(0.3)
        target.set_focus()

        rect = target.rectangle()
        return {
            "ok": True,
            "message": f"Focused: {target.window_text()}",
            "title": target.window_text(),
            "rect": {"left": rect.left, "top": rect.top, "right": rect.right, "bottom": rect.bottom}
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


def close_window(**kwargs) -> Dict[str, Any]:
    """Gracefully close a window by title pattern."""
    if not HAVE_PYWINAUTO:
        return {"ok": False, "error": "pywinauto not installed. Run: pip install pywinauto"}
    title_pattern = kwargs.get("title_pattern", "").strip()
    if not title_pattern:
        return {"ok": False, "error": "Provide a 'title_pattern' to close."}
    try:
        desktop = PwaDesktop(backend="uia")
        windows = desktop.windows()
        pattern_lower = title_pattern.lower()
        closed = []
        for w in windows:
            try:
                title = w.window_text()
                if title and (pattern_lower in title.lower() or re.search(title_pattern, title, re.IGNORECASE)):
                    w.close()
                    closed.append(title)
            except Exception:
                continue

        if not closed:
            return {"ok": False, "error": f"No window matching '{title_pattern}' found."}
        return {"ok": True, "message": f"Closed {len(closed)} window(s)", "closed": closed}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def smart_click(**kwargs) -> Dict[str, Any]:
    """
    Vision-guided clicking: describe what to click and Joi finds it on screen.
    Takes a screenshot, sends to vision model to find coordinates, then clicks.
    """
    if not HAVE_PYAUTOGUI:
        return {"ok": False, "error": "pyautogui not installed"}

    target = kwargs.get("target", "").strip()
    if not target:
        return {"ok": False, "error": "Provide a 'target' description (e.g., 'the play button', 'File menu')."}

    try:
        # Step 1: Take screenshot
        img = pyautogui.screenshot()
        buf = io.BytesIO()
        img.save(buf, format='JPEG', quality=70)
        frame_b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        screen_w, screen_h = img.size

        # Step 2: Send to vision model
        try:
            from openai import OpenAI
            api_key = os.getenv("OPENAI_API_KEY", "").strip()
            vision_model = os.getenv("JOI_VISION_MODEL", "gpt-4o").strip()
            if not api_key:
                return {"ok": False, "error": "OpenAI API key required for smart_click."}

            client = OpenAI(api_key=api_key)
            resp = client.chat.completions.create(
                model=vision_model,
                messages=[
                    {"role": "system", "content": (
                        f"You are a precise UI element locator. The screen resolution is {screen_w}x{screen_h}. "
                        "When asked to find a UI element, respond with ONLY the x,y pixel coordinates in format: x,y "
                        "No other text. Just the coordinates."
                    )},
                    {"role": "user", "content": [
                        {"type": "text", "text": f"Find the exact pixel coordinates of: {target}"},
                        {"type": "image_url", "image_url": {
                            "url": f"data:image/jpeg;base64,{frame_b64}",
                            "detail": "high"
                        }}
                    ]}
                ],
                max_tokens=50
            )
            coord_text = resp.choices[0].message.content.strip()
        except ImportError:
            return {"ok": False, "error": "OpenAI package required for smart_click."}

        # Step 3: Parse coordinates
        coord_match = re.search(r'(\d+)\s*,\s*(\d+)', coord_text)
        if not coord_match:
            return {"ok": False, "error": f"Could not parse coordinates from vision response: {coord_text}"}

        click_x = int(coord_match.group(1))
        click_y = int(coord_match.group(2))

        # Sanity check
        if click_x < 0 or click_x > screen_w or click_y < 0 or click_y > screen_h:
            return {"ok": False, "error": f"Coordinates ({click_x}, {click_y}) out of screen bounds ({screen_w}x{screen_h})."}

        # Step 4: Click
        pyautogui.click(click_x, click_y)

        return {
            "ok": True,
            "message": f"Clicked '{target}' at ({click_x}, {click_y})",
            "target": target,
            "coordinates": {"x": click_x, "y": click_y},
            "screen_size": {"width": screen_w, "height": screen_h}
        }
    except Exception as e:
        return {"ok": False, "error": f"smart_click failed: {type(e).__name__}: {str(e)[:300]}"}


def find_file_smart(**kwargs) -> Dict[str, Any]:
    """
    Smart file search across common directories with fuzzy matching.
    Searches: Desktop, Documents, Downloads, Music, Videos, and project dirs.
    """
    query = kwargs.get("query", "").strip()
    if not query:
        return {"ok": False, "error": "Provide a 'query' (filename or glob pattern)."}

    max_results = kwargs.get("max_results", 10)
    home = Path.home()

    # Directories to search
    search_dirs = [
        home / "Desktop",
        home / "Documents",
        home / "Downloads",
        home / "Music",
        home / "Videos",
        BASE_DIR,  # Joi project root
        BASE_DIR / "projects",
    ]

    matches = []
    query_lower = query.lower()
    is_glob = any(c in query for c in "*?[")

    for search_dir in search_dirs:
        if not search_dir.exists():
            continue

        # Use cache
        cache_key = str(search_dir)
        now = time.time()
        if cache_key in _dir_cache and (now - _dir_cache[cache_key][1]) < _DIR_CACHE_TTL:
            entries = _dir_cache[cache_key][0]
        else:
            try:
                entries = []
                for item in search_dir.rglob("*"):
                    if item.is_file():
                        entries.append(item)
                    if len(entries) > 5000:  # Safety limit
                        break
                _dir_cache[cache_key] = (entries, now)
            except PermissionError:
                continue

        for filepath in entries:
            name = filepath.name.lower()
            if is_glob:
                if fnmatch.fnmatch(name, query_lower):
                    matches.append(filepath)
            else:
                # Fuzzy: substring match in filename
                if query_lower in name:
                    matches.append(filepath)

            if len(matches) >= max_results * 3:  # Collect extra for sorting
                break

    # Sort by relevance: exact match first, then by modification time
    def sort_key(p: Path):
        name = p.name.lower()
        exact = 0 if name == query_lower else 1
        try:
            mtime = -p.stat().st_mtime
        except Exception:
            mtime = 0
        return (exact, mtime)

    matches.sort(key=sort_key)
    matches = matches[:max_results]

    results = []
    for m in matches:
        try:
            stat = m.stat()
            results.append({
                "path": str(m),
                "name": m.name,
                "size_bytes": stat.st_size,
                "modified": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(stat.st_mtime))
            })
        except Exception:
            results.append({"path": str(m), "name": m.name})

    return {"ok": True, "results": results, "count": len(results), "query": query}


# ── Register tools ──────────────────────────────────────────────────────────
import joi_companion

if HAVE_PYAUTOGUI:
    joi_companion.register_tool(
        {"type": "function", "function": {
            "name": "move_mouse",
            "description": "Move mouse cursor to coordinates",
            "parameters": {"type": "object", "properties": {
                "x": {"type": "integer"},
                "y": {"type": "integer"},
                "duration": {"type": "number", "default": 0.5}
            }, "required": ["x", "y"]}
        }},
        move_mouse
    )

    joi_companion.register_tool(
        {"type": "function", "function": {
            "name": "click_mouse",
            "description": "Click mouse button (optionally at coordinates)",
            "parameters": {"type": "object", "properties": {
                "button": {"type": "string", "enum": ["left", "right", "middle"], "default": "left"},
                "x": {"type": "integer"},
                "y": {"type": "integer"}
            }}
        }},
        click_mouse
    )

    joi_companion.register_tool(
        {"type": "function", "function": {
            "name": "type_text",
            "description": "Type text into active window",
            "parameters": {"type": "object", "properties": {
                "text": {"type": "string"},
                "interval": {"type": "number", "default": 0.05}
            }, "required": ["text"]}
        }},
        type_text
    )

    joi_companion.register_tool(
        {"type": "function", "function": {
            "name": "press_key",
            "description": "Press a key (enter, esc, tab, ctrl, etc)",
            "parameters": {"type": "object", "properties": {
                "key": {"type": "string"}
            }, "required": ["key"]}
        }},
        press_key
    )

    joi_companion.register_tool(
        {"type": "function", "function": {
            "name": "screenshot",
            "description": "Take a screenshot (full screen or region)",
            "parameters": {"type": "object", "properties": {
                "region": {"type": "string", "description": "Optional 'x,y,width,height'"}
            }}
        }},
        screenshot
    )

    joi_companion.register_tool(
        {"type": "function", "function": {
            "name": "get_mouse_position",
            "description": "Get current mouse cursor position",
            "parameters": {"type": "object", "properties": {}}
        }},
        get_mouse_position
    )

    joi_companion.register_tool(
        {"type": "function", "function": {
            "name": "smart_click",
            "description": (
                "Vision-guided clicking: describe what to click and Joi finds it on screen. "
                "Takes a screenshot, uses vision AI to locate the target element, then clicks it. "
                "Use when you need to click a specific button, menu item, or UI element but don't know coordinates. "
                "Example: smart_click(target='the play button') or smart_click(target='File menu')"
            ),
            "parameters": {"type": "object", "properties": {
                "target": {"type": "string", "description": "Description of what to click (e.g., 'the Save button', 'File menu', 'the X close button')"}
            }, "required": ["target"]}
        }},
        smart_click
    )

    joi_companion.register_tool(
        {"type": "function", "function": {
            "name": "find_file_smart",
            "description": (
                "Smart file search across Desktop, Documents, Downloads, Music, Videos, and project directories. "
                "Supports glob patterns (*.mp3, report*.pdf) and fuzzy substring matching. "
                "Use when Lonnie asks to find a file or when you need to locate a specific file."
            ),
            "parameters": {"type": "object", "properties": {
                "query": {"type": "string", "description": "Filename, substring, or glob pattern (e.g., '*.mp3', 'report', 'budget*.xlsx')"},
                "max_results": {"type": "integer", "description": "Maximum results to return (default 10)"}
            }, "required": ["query"]}
        }},
        find_file_smart
    )

# Window management tools (require pywinauto)
if HAVE_PYWINAUTO:
    joi_companion.register_tool(
        {"type": "function", "function": {
            "name": "list_windows",
            "description": (
                "List all open windows with their titles, handles, process IDs, and screen positions. "
                "Use to see what programs are running or find a specific window."
            ),
            "parameters": {"type": "object", "properties": {
                "visible_only": {"type": "boolean", "description": "Only show visible windows (default true)"}
            }}
        }},
        list_windows
    )

    joi_companion.register_tool(
        {"type": "function", "function": {
            "name": "find_window",
            "description": (
                "Find windows matching a title pattern. Case-insensitive substring or regex match. "
                "Use to locate a specific application window. Example: find_window(title_pattern='Notepad')"
            ),
            "parameters": {"type": "object", "properties": {
                "title_pattern": {"type": "string", "description": "Substring or regex to match window titles"}
            }, "required": ["title_pattern"]}
        }},
        find_window
    )

    joi_companion.register_tool(
        {"type": "function", "function": {
            "name": "focus_window",
            "description": (
                "Bring a window to the foreground by title pattern. Restores minimized windows. "
                "Use when you need to interact with a specific application. "
                "Example: focus_window(title_pattern='Chrome')"
            ),
            "parameters": {"type": "object", "properties": {
                "title_pattern": {"type": "string", "description": "Substring or regex to match the window title"}
            }, "required": ["title_pattern"]}
        }},
        focus_window
    )

    joi_companion.register_tool(
        {"type": "function", "function": {
            "name": "close_window",
            "description": (
                "Gracefully close a window by title pattern. "
                "Use when asked to close a program or clean up windows."
            ),
            "parameters": {"type": "object", "properties": {
                "title_pattern": {"type": "string", "description": "Substring or regex to match the window title"}
            }, "required": ["title_pattern"]}
        }},
        close_window
    )

    print("  [joi_desktop] window management tools registered (list_windows, find_window, focus_window, close_window)")

if HAVE_PYAUTOGUI:
    print("  [joi_desktop] desktop tools registered (move_mouse, click_mouse, type_text, press_key, screenshot, get_mouse_position, smart_click, find_file_smart)")
