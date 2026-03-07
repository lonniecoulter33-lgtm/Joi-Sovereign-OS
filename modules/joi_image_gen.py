"""
modules/joi_image_gen.py

Dedicated open-ended Image Generation Tool for Joi.
Uses OpenAI DALL-E 3 (or Gemini fallback if configured) to generate an image based on any prompt.
Requires no project name or book structure.
"""

import os
import requests
from pathlib import Path
from typing import Dict, Any
import joi_companion

try:
    from openai import OpenAI
    HAVE_OPENAI = True
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
    client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None
except ImportError:
    HAVE_OPENAI = False
    OPENAI_API_KEY = None
    client = None

BASE_DIR = Path(__file__).resolve().parent.parent
GALLERY_DIR = BASE_DIR / "data" / "gallery"

# Ensure the gallery directory exists
GALLERY_DIR.mkdir(parents=True, exist_ok=True)

def generate_image(**params) -> Dict[str, Any]:
    """Generates an image from a prompt and returns the result."""
    from modules.joi_auth import require_user
    require_user()
    
    prompt = params.get("prompt")
    if not prompt:
        return {"ok": False, "error": "prompt is required"}
        
    if not HAVE_OPENAI or not client:
        return {"ok": False, "error": "OpenAI client is not configured."}

    try:
        # We use standard DALL-E 3 config
        r = client.images.generate(model="dall-e-3", prompt=prompt, size="1024x1024", n=1)
        img_url = r.data[0].url
        
        # Download it
        img_r = requests.get(img_url, timeout=30)
        
        # Create a nice snake_case filename from the first few words of the prompt
        safe_prompt = "".join(c if c.isalnum() else "_" for c in prompt)[:30].strip("_")
        import time
        timestamp = int(time.time())
        filename = f"{safe_prompt}_{timestamp}.png"
        
        path = GALLERY_DIR / filename
        path.write_bytes(img_r.content)
        
        relative_path = f"/file/data/gallery/{filename}"
        
        # Return the markdown so Joi can render it directly
        return {
            "ok": True,
            "message": f"Image successfully generated.",
            "path": str(path),
            "url": relative_path,
            "markdown": f"![{prompt}]({relative_path})"
        }
    except Exception as e:
        return {"ok": False, "error": f"Image generation failed: {str(e)}"}

# Register the standalone tool
tool_schema = {
    "type": "function",
    "function": {
        "name": "generate_image",
        "description": "Call this tool ANY TIME the user asks you to create, generate, draw, or make an image, picture, photo, or art. This is a standalone tool that DOES NOT require a project name.",
        "parameters": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "An extremely detailed image generation prompt describing what you want to draw."
                }
            },
            "required": ["prompt"]
        }
    }
}

joi_companion.register_tool(tool_schema, generate_image)
print(f"    [OK] joi_image_gen (Standalone Image Generation active)")
