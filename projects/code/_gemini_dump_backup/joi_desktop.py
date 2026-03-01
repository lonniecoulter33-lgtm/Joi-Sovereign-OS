"""
Joi Desktop Vision — Screen capture + Vision model analysis

Captures screenshots and feeds them to the Vision model so Joi can
see what's on Lonnie's screen.

REQUIRES: pip install mss pillow
Fallback: pip install pyautogui pillow
"""
from __future__ import annotations

import base64
import io
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

# Try mss first (faster, no pyautogui dependency), fall back to pyautogui
try:
    import mss
    HAVE_MSS = True
except ImportError:
    HAVE_MSS = False

try:
    import pyautogui
    HAVE_PYAUTOGUI = True
except ImportError:
    HAVE_PYAUTOGUI = False

try:
    from PIL import Image
    HAVE_PIL = True
except ImportError:
    HAVE_PIL = False

SCREENSHOT_DIR = Path(__file__).resolve().parent / "assets" / "screenshots"
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

# Keep only last N screenshots to avoid disk bloat
MAX_SCREENSHOTS = 20


def capture_screenshot(region: Optional[str] = None, save: bool = True) -> Dict[str, Any]:
    """
    Capture a screenshot of the desktop.

    Args:
        region: Optional 'x,y,width,height' for a specific area, or None for full screen
        save: Whether to save to disk (default True)

    Returns:
        Dict with ok, base64 data URL, and optional file path
    """
    if not HAVE_MSS and not HAVE_PYAUTOGUI:
        return {"ok": False, "error": "No screenshot library installed. Run: pip install mss pillow"}

    try:
        img = None

        if HAVE_MSS:
            with mss.mss() as sct:
                if region:
                    parts = [int(p.strip()) for p in region.split(',')]
                    if len(parts) != 4:
                        return {"ok": False, "error": "region must be 'x,y,width,height'"}
                    monitor = {"left": parts[0], "top": parts[1],
                               "width": parts[2], "height": parts[3]}
                else:
                    monitor = sct.monitors[0]  # full virtual screen
                raw = sct.grab(monitor)
                img = Image.frombytes("RGB", raw.size, raw.bgra, "raw", "BGRX")
        elif HAVE_PYAUTOGUI:
            if region:
                parts = [int(p.strip()) for p in region.split(',')]
                if len(parts) != 4:
                    return {"ok": False, "error": "region must be 'x,y,width,height'"}
                img = pyautogui.screenshot(region=tuple(parts))
            else:
                img = pyautogui.screenshot()

        if img is None:
            return {"ok": False, "error": "Screenshot capture returned None"}

        # Resize for Vision API (max 1920px wide to keep token cost down)
        max_w = 1920
        if img.width > max_w:
            ratio = max_w / img.width
            img = img.resize((max_w, int(img.height * ratio)), Image.LANCZOS)

        # Encode to base64
        buf = io.BytesIO()
        img.save(buf, format="PNG", optimize=True)
        b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
        data_url = f"data:image/png;base64,{b64}"

        result = {
            "ok": True,
            "message": f"Screenshot captured ({img.width}x{img.height})",
            "data": data_url,
            "width": img.width,
            "height": img.height,
        }

        # Save to disk
        if save:
            _cleanup_old_screenshots()
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = SCREENSHOT_DIR / f"screen_{ts}.png"
            img.save(str(filepath), format="PNG")
            result["path"] = str(filepath)
            result["url"] = f"/file/project/assets/screenshots/screen_{ts}.png"

        return result

    except Exception as e:
        return {"ok": False, "error": f"Screenshot failed: {type(e).__name__}: {e}"}


def analyze_screen(openai_client, vision_model: str = "gpt-4o",
                   question: str = "Describe what you see on screen.",
                   region: Optional[str] = None) -> Dict[str, Any]:
    """
    Capture a screenshot and send it to the Vision model for analysis.

    Args:
        openai_client: An initialized OpenAI client
        vision_model: Model to use for vision (default gpt-4o)
        question: What to ask about the screenshot
        region: Optional region to capture

    Returns:
        Dict with the model's analysis
    """
    if not openai_client:
        return {"ok": False, "error": "OpenAI client not available"}

    shot = capture_screenshot(region=region, save=True)
    if not shot.get("ok"):
        return shot

    try:
        response = openai_client.chat.completions.create(
            model=vision_model,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": question},
                    {"type": "image_url", "image_url": {"url": shot["data"], "detail": "low"}}
                ]
            }],
            max_tokens=500
        )
        analysis = response.choices[0].message.content or "No analysis returned."
        return {
            "ok": True,
            "analysis": analysis,
            "screenshot_url": shot.get("url", ""),
            "width": shot["width"],
            "height": shot["height"]
        }
    except Exception as e:
        return {"ok": False, "error": f"Vision analysis failed: {type(e).__name__}: {e}"}


def is_available() -> bool:
    """Check if screenshot capture is available."""
    return HAVE_MSS or HAVE_PYAUTOGUI


def _cleanup_old_screenshots():
    """Remove old screenshots beyond MAX_SCREENSHOTS."""
    try:
        shots = sorted(SCREENSHOT_DIR.glob("screen_*.png"))
        while len(shots) > MAX_SCREENSHOTS:
            shots[0].unlink(missing_ok=True)
            shots.pop(0)
    except Exception:
        pass
