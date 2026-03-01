import os
import sys
import io
import json
import base64
from pathlib import Path
from typing import Dict, Any

import joi_companion
import requests

try:
    from PIL import Image
    HAVE_PIL = True
except ImportError:
    HAVE_PIL = False

try:
    from google import genai
    from google.genai import types
    HAVE_GEMINI = True
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
    _gemini_client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None
except ImportError:
    HAVE_GEMINI = False
    GEMINI_API_KEY = None
    _gemini_client = None


BASE_DIR = Path(__file__).resolve().parent.parent
PROJECTS_DIR = BASE_DIR / "projects"

# ── Publisher Core Functions ────────────────────────────────────────────────

def publisher_init_project(**params) -> Dict[str, Any]:
    """Initialize a new book project with the required directory structure."""
    project_name = params.get("project_name")
    if not project_name:
        return {"ok": False, "error": "project_name is required"}

    project_dir = PROJECTS_DIR / project_name
    manuscript_dir = project_dir / "manuscript" / "chapters"
    assets_dir = project_dir / "assets" / "images"
    scripts_dir = project_dir / "scripts"

    try:
        manuscript_dir.mkdir(parents=True, exist_ok=True)
        assets_dir.mkdir(parents=True, exist_ok=True)
        scripts_dir.mkdir(parents=True, exist_ok=True)

        manifest_path = project_dir / "manifest.json"
        if not manifest_path.exists():
            manifest = {
                "project_name": project_name,
                "chapters": {},
                "assets": [],
                "created_at": str(os.path.getctime(project_dir)) if project_dir.exists() else ""
            }
            manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

        return {
            "ok": True, 
            "message": f"Project '{project_name}' initialized successfully.",
            "paths": {
                "manuscript": str(manuscript_dir),
                "assets": str(assets_dir),
                "scripts": str(scripts_dir),
                "manifest": str(manifest_path)
            }
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}

def publisher_edit_chapter(**params) -> Dict[str, Any]:
    """Draft or revise a chapter in Markdown format."""
    project_name = params.get("project_name")
    chapter_num = params.get("chapter_num")
    content = params.get("content")
    operation = params.get("operation", "write") # write or append

    if not all([project_name, chapter_num, content]):
        return {"ok": False, "error": "project_name, chapter_num, and content are required."}

    project_dir = PROJECTS_DIR / project_name
    manifest_path = project_dir / "manifest.json"
    chapter_path = project_dir / "manuscript" / "chapters" / f"chapter_{chapter_num}.md"

    if not project_dir.exists() or not manifest_path.exists():
        return {"ok": False, "error": f"Project '{project_name}' not initialized. Call publisher_init_project first."}

    try:
        mode = "a" if operation == "append" else "w"
        with open(chapter_path, mode, encoding="utf-8") as f:
            if operation == "append":
                f.write("\n\n" + content)
            else:
                f.write(content)
        
        # Calculate stats
        full_text = chapter_path.read_text(encoding="utf-8")
        word_count = len(full_text.split())
        char_count = len(full_text)

        # Update Manifest
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if "chapters" not in manifest:
            manifest["chapters"] = {}
        
        manifest["chapters"][str(chapter_num)] = {
            "file": f"chapter_{chapter_num}.md",
            "word_count": word_count,
            "char_count": char_count,
            "last_edited": str(os.path.getmtime(chapter_path))
        }
        manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

        return {
            "ok": True,
            "message": f"Chapter {chapter_num} saved.",
            "stats": {"word_count": word_count, "char_count": char_count}
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}

def publisher_generate_asset(**params) -> Dict[str, Any]:
    """Generate a high-res print-ready image using Google Gemini API."""
    project_name = params.get("project_name")
    prompt = params.get("prompt")
    asset_type = params.get("asset_type", "illustration") # cover, illustration, etc
    file_name = params.get("file_name", f"{asset_type}.png")

    if not all([project_name, prompt]):
        return {"ok": False, "error": "project_name and prompt are required"}

    if not HAVE_GEMINI or not _gemini_client:
        return {"ok": False, "error": "Google Gemini API client is not configured or available."}
    
    if not HAVE_PIL:
        return {"ok": False, "error": "Pillow (PIL) is required for upscaling and DPI conversion."}

    project_dir = PROJECTS_DIR / project_name
    assets_dir = project_dir / "assets" / "images"
    manifest_path = project_dir / "manifest.json"

    if not assets_dir.exists():
        return {"ok": False, "error": f"Project '{project_name}' assets dir not found."}

    try:
        try:
            # 1. Try Gemini Image Gen
            result = _gemini_client.models.generate_images(
                model='imagen-4.0-generate-001',
                prompt=prompt,
                config=types.GenerateImagesConfig(
                    number_of_images=1,
                    output_mime_type="image/jpeg",
                    aspect_ratio="1:1" if asset_type != "cover" else "3:4" 
                )
            )
            
            if not result.generated_images:
                raise ValueError("Gemini API returned no images")

            generated_image = result.generated_images[0]
            image_bytes = generated_image.image.image_bytes
            
        except Exception as gemini_err:
            print(f"    [WARN] Gemini image gen failed, falling back to OpenAI: {gemini_err}")
            # Fallback to OpenAI DALL-E 3
            try:
                from openai import OpenAI
                openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "").strip())
                r = openai_client.images.generate(model="dall-e-3", prompt=prompt, size="1024x1024", n=1)
                img_url = r.data[0].url
                
                # Download the image
                img_r = requests.get(img_url, timeout=30)
                image_bytes = img_r.content
            except Exception as openai_err:
                 return {"ok": False, "error": f"Both Gemini and OpenAI generation failed. Gemini: {gemini_err}, OpenAI: {openai_err}"}

        # 2. Process with Pillow for Print (300 DPI upscaling/formatting)
        img = Image.open(io.BytesIO(image_bytes))
        
        # Optional: AI Upscaling placeholder. 
        # For now, we enforce a high minimum resolution and set the DPI metadata
        min_dim = 2400 # 8 inches at 300 DPI
        if img.width < min_dim or img.height < min_dim:
            # Simple lanczos resize if the raw output is smaller
            ratio = max(min_dim / img.width, min_dim / img.height)
            new_size = (int(img.width * ratio), int(img.height * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
            
        output_path = assets_dir / file_name
        
        # Save as PNG with 300 DPI 
        img.save(output_path, format="PNG", dpi=(300, 300))
        
        # 3. Update Manifest
        if manifest_path.exists():
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            if "assets" not in manifest:
                manifest["assets"] = []
            
            # Avoid duplicates
            manifest["assets"] = [a for a in manifest["assets"] if a.get("file_name") != file_name]
            
            manifest["assets"].append({
                "file_name": file_name,
                "type": asset_type,
                "prompt": prompt,
                "dpi": 300,
                "width": img.width,
                "height": img.height
            })
            manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

        return {
            "ok": True,
            "message": f"Asset '{file_name}' generated and saved at 300 DPI.",
            "path": str(output_path),
            "dimensions": f"{img.width}x{img.height}"
        }

    except Exception as e:
        return {"ok": False, "error": f"Generation failed: {str(e)}"}

# ── PDF Generators ───────────────────────────────────────────────────────────

def publisher_generate_cover_script(**params) -> Dict[str, Any]:
    """Generate and run a Python script for IngramSpark cover PDF."""
    project_name = params.get("project_name")
    specs = params.get("specs", {})
    
    if not project_name:
        return {"ok": False, "error": "project_name is required"}

    project_dir = PROJECTS_DIR / project_name
    scripts_dir = project_dir / "scripts"
    assets_dir = project_dir / "assets" / "images"
    
    # IngramSpark Required Variables
    trim_width = specs.get("trim_width", 6.0)
    trim_height = specs.get("trim_height", 9.0)
    spine_width = specs.get("spine_width", 0.5)
    bleed = 0.125
    
    total_width = (trim_width * 2) + spine_width + (bleed * 2)
    total_height = trim_height + (bleed * 2)

    script_content = f'''import sys
import os
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from PIL import Image

# Specs
total_width = {total_width} * inch
total_height = {total_height} * inch
spine_width = {spine_width} * inch
trim_width = {trim_width} * inch
bleed = {bleed} * inch

c = canvas.Canvas(r"{project_dir}\\master_cover.pdf", pagesize=(total_width, total_height))

# Setup PDF/X-1a
c.setCreator("Joi Master Publisher")
c.setTitle("{project_name} Cover")

# Front Cover Image (Right side)
front_x = (trim_width + spine_width + bleed) * inch
front_y = 0

front_img_path = r"{assets_dir}\\cover.png"
if os.path.exists(front_img_path):
    img = Image.open(front_img_path)
    if img.mode != 'CMYK':
        img = img.convert('CMYK')
        img.save(r"{assets_dir}\\cover_cmyk.jpg", "JPEG", quality=95)
        front_img_path = r"{assets_dir}\\cover_cmyk.jpg"
    c.drawImage(front_img_path, front_x, front_y, width=(trim_width + bleed)*inch, height=total_height)
else:
    c.drawString(front_x + 1*inch, 4*inch, "[Front Cover Image Missing]")

# Spine (Center)
spine_x = (trim_width + bleed) * inch
c.saveState()
c.translate(spine_x + (spine_width/2.0), total_height/2.0)
c.rotate(-90)
c.setFont("Helvetica-Bold", 14)
c.drawCentredString(0, 0, "{project_name}".upper())
c.restoreState()

# Back Cover (Left side)
back_x = 0
back_y = 0

# Draw White Barcode Box (Bottom Left of Back Cover)
barcode_x = back_x + 0.5*inch + bleed
barcode_y = back_y + 0.5*inch + bleed
c.setFillColorRGB(1,1,1)
c.rect(barcode_x, barcode_y, 1.75*inch, 1*inch, fill=1, stroke=0)

c.save()
print("Cover PDF generated successfully.")
'''
    script_path = scripts_dir / "build_cover.py"
    script_path.write_text(script_content, encoding="utf-8")
    
    # Execute the generated script
    try:
        import subprocess
        result = subprocess.run([sys.executable, str(script_path)], capture_output=True, text=True, check=True)
        return {"ok": True, "message": "Cover PDF generated.", "log": result.stdout, "script_path": str(script_path)}
    except subprocess.CalledProcessError as e:
        return {"ok": False, "error": f"Script failed: {e.stderr}"}

def publisher_format_interior_script(**params) -> Dict[str, Any]:
    """Generate and run a Python script for IngramSpark interior PDF."""
    project_name = params.get("project_name")
    
    if not project_name:
        return {"ok": False, "error": "project_name is required"}

    project_dir = PROJECTS_DIR / project_name
    scripts_dir = project_dir / "scripts"
    manuscript_dir = project_dir / "manuscript" / "chapters"

    script_content = f'''import sys
import os
import glob
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

doc = SimpleDocTemplate(r"{project_dir}\\master_interior.pdf", pagesize=(6*inch, 9*inch),
                        rightMargin=0.5*inch, leftMargin=0.75*inch, # Gutter
                        topMargin=0.5*inch, bottomMargin=0.5*inch)

styles = getSampleStyleSheet()
normal_style = styles["Normal"]
title_style = styles["Heading1"]

Story = []

# Title Page
Story.append(Spacer(1, 2*inch))
Story.append(Paragraph("<font size=24><b>{project_name}</b></font>", title_style))
Story.append(PageBreak())

# Read Chapters
chapter_files = sorted(glob.glob(r"{manuscript_dir}\\chapter_*.md"))
for f in chapter_files:
    with open(f, 'r', encoding='utf-8') as file:
        text = file.read()
        Story.append(Paragraph(os.path.basename(f).replace(".md", "").capitalize(), title_style))
        Story.append(Spacer(1, 0.2*inch))
        # Simple paragraph splitting
        for p in text.split("\\n\\n"):
            if p.strip():
                Story.append(Paragraph(p.strip().replace("\\n", "<br/>"), normal_style))
                Story.append(Spacer(1, 0.1*inch))
        Story.append(PageBreak())

doc.build(Story)
print("Interior PDF generated successfully.")
'''
    script_path = scripts_dir / "build_interior.py"
    script_path.write_text(script_content, encoding="utf-8")
    
    # Execute the generated script
    try:
        import subprocess
        result = subprocess.run([sys.executable, str(script_path)], capture_output=True, text=True, check=True)
        return {"ok": True, "message": "Interior PDF generated.", "log": result.stdout, "script_path": str(script_path)}
    except subprocess.CalledProcessError as e:
        return {"ok": False, "error": f"Script failed: {e.stderr}"}

def manage_publisher(**kwargs) -> Dict[str, Any]:
    """Unified tool for managing book publishing operations."""
    action = kwargs.get("action")
    if not action:
        return {"ok": False, "error": "action parameter is required"}
        
    try:
        if action == "init_project": return publisher_init_project(**kwargs)
        elif action == "edit_chapter": return publisher_edit_chapter(**kwargs)
        elif action == "generate_asset": return publisher_generate_asset(**kwargs)
        elif action == "generate_cover_script": return publisher_generate_cover_script(**kwargs)
        elif action == "format_interior_script": return publisher_format_interior_script(**kwargs)
        else: return {"ok": False, "error": f"Unknown action: {action}"}
    except Exception as exc:
        return {"ok": False, "error": f"Publisher action {action} failed: {exc}"}

# ── Tool Registration ────────────────────────────────────────────────────────

joi_companion.register_tool({
    "type": "function",
    "function": {
        "name": "manage_publisher",
        "description": "Unified tool to manage book publishing operations (init project, edit chapters, generate assets/covers, format interiors).",
        "parameters": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "description": "Action to perform",
                    "enum": ["init_project", "edit_chapter", "generate_asset", "generate_cover_script", "format_interior_script"]
                },
                "project_name": {
                    "type": "string",
                    "description": "The name of the book project"
                },
                "chapter_num": {
                    "type": "integer",
                    "description": "Chapter number to edit (for edit_chapter)"
                },
                "content": {
                    "type": "string",
                    "description": "Markdown content for the chapter (for edit_chapter)"
                },
                "operation": {
                    "type": "string",
                    "enum": ["write", "append"],
                    "description": "Whether to overwrite or append to the chapter (for edit_chapter)"
                },
                "prompt": {
                    "type": "string",
                    "description": "Extremely detailed image generation prompt (for generate_asset)"
                },
                "asset_type": {
                    "type": "string",
                    "description": "E.g., cover, illustration, map (for generate_asset)"
                },
                "file_name": {
                    "type": "string",
                    "description": "Target filename ending in .png (for generate_asset)"
                },
                "specs": {
                    "type": "object",
                    "description": "Optional dict. e.g. {'trim_width': 6.0, 'trim_height': 9.0, 'spine_width': 0.5} (for generate_cover_script)"
                }
            },
            "required": ["action", "project_name"]
        }
    }
}, manage_publisher)

print(f"    [OK] joi_publisher (Master Publisher & Creative Orchestrator active)")
