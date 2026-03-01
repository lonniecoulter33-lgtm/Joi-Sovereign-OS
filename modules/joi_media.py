"""
modules/joi_media.py

Unified Senses & Media Module
==============================
Combines Desktop Vision, Webcam Camera, and Avatar/TTS systems.
"""

import os
import io
import time
import json
import base64
import threading
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Union

import joi_companion
import requests
from flask import jsonify, request as flask_req
from modules.joi_memory import get_preference, set_preference

# ── Optional Imports ─────────────────────────────────────────────────────────
try:
    import pyautogui
    HAVE_PYAUTOGUI = True
except ImportError: HAVE_PYAUTOGUI = False

try:
    from PIL import Image
    HAVE_PIL = True
except ImportError: HAVE_PIL = False

try:
    import face_recognition
    import numpy as np
    HAVE_FACE_REC = True
except (ImportError, RuntimeError): HAVE_FACE_REC = False

try:
    import edge_tts
    HAVE_EDGE_TTS = True
except ImportError: HAVE_EDGE_TTS = False

try:
    from openai import OpenAI
    HAVE_OPENAI = True
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
    client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None
except ImportError:
    HAVE_OPENAI = False
    OPENAI_API_KEY = None
    client = None

# Kokoro TTS
try:
    from modules.joi_tts_kokoro import generate_speech_kokoro, kokoro_available
    HAVE_KOKORO = True
except ImportError:
    HAVE_KOKORO = False
    def kokoro_available(): return False
    def generate_speech_kokoro(*a, **kw): return None

# ── Configuration & Paths ────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
AVATAR_DIR = BASE_DIR / "assets" / "avatars"
AUDIO_DIR = BASE_DIR / "assets" / "audio"
FACES_DIR = BASE_DIR / "assets" / "faces"
DATA_DIR = BASE_DIR / "data"

for d in [AVATAR_DIR, AUDIO_DIR, FACES_DIR, DATA_DIR]: d.mkdir(parents=True, exist_ok=True)

FACE_DB_PATH = FACES_DIR / "face_db.json"
AVATAR_FACE_DB_PATH = DATA_DIR / "avatar_faces.json"

VISION_MODEL = os.getenv("JOI_VISION_MODEL", "gpt-4o").strip()
CAPTURE_INTERVAL = float(os.getenv("JOI_VISION_CAPTURE_INTERVAL", "2"))
PROACTIVE_INTERVAL = float(os.getenv("JOI_VISION_PROACTIVE_INTERVAL", "25"))
CAMERA_PROACTIVE_INTERVAL = float(os.getenv("JOI_CAMERA_PROACTIVE_INTERVAL", "15"))

# ── Shared State ─────────────────────────────────────────────────────────────
_media_lock = threading.Lock()

# Vision
_latest_frame_b64: Optional[str] = None
_latest_frame_ts: float = 0.0
_vision_active = False
_proactive_queue: List[str] = []

# Camera
_latest_camera_b64: Optional[str] = None
_latest_camera_ts: float = 0.0
_camera_active = False
_camera_proactive_queue: List[str] = []
_face_db: Dict[str, Any] = {"people": {}}

# Avatar
DEFAULT_FACE = {"mx": 0.50, "my": 0.50, "mw": 0.20, "mh": 0.09, "ex": 0.55, "ey": 0.32, "ew": 0.28, "eh": 0.08}

# ── Utils ────────────────────────────────────────────────────────────────────
def _img_to_b64_jpeg(img, quality=70) -> str:
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=quality)
    return base64.b64encode(buf.getvalue()).decode("utf-8")

def _call_vision_api(frame_b64: str, prompt: str, system_msg: str = "You are Joi.", max_tokens: int = 500) -> Optional[str]:
    if not client: return None
    resp = client.chat.completions.create(
        model=VISION_MODEL,
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{frame_b64}", "detail": "low"}}
            ]}
        ],
        max_tokens=max_tokens
    )
    return resp.choices[0].message.content

# ── Desktop Vision ───────────────────────────────────────────────────────────
def _capture_loop():
    global _latest_frame_b64, _latest_frame_ts
    while _vision_active:
        try:
            if HAVE_PYAUTOGUI:
                img = pyautogui.screenshot()
                b64 = _img_to_b64_jpeg(img)
                with _media_lock:
                    _latest_frame_b64 = b64
                    _latest_frame_ts = time.time()
                # Update Neuro HUD
                try:
                    from modules.joi_neuro import update_vision_thumbnail
                    thumb = img.copy()
                    thumb.thumbnail((160, 160))
                    update_vision_thumbnail(_img_to_b64_jpeg(thumb, quality=40))
                except: pass
        except: pass
        time.sleep(CAPTURE_INTERVAL)

def start_vision():
    global _vision_active
    if not _vision_active:
        _vision_active = True
        threading.Thread(target=_capture_loop, daemon=True).start()
    return {"ok": True, "message": "Vision active"}

def stop_vision():
    global _vision_active
    _vision_active = False
    return {"ok": True, "message": "Vision stopped"}

def analyze_screen(**params) -> Dict[str, Any]:
    from modules.joi_auth import require_user
    require_user()
    with _media_lock: frame = _latest_frame_b64
    if not frame and HAVE_PYAUTOGUI:
        frame = _img_to_b64_jpeg(pyautogui.screenshot())
    if not frame: return {"ok": False, "error": "No frame"}
    q = params.get("question", "Describe the screen.")
    desc = _call_vision_api(frame, q)
    return {"ok": True, "description": desc}

# ── Camera & Face ID ─────────────────────────────────────────────────────────
def _load_face_db():
    global _face_db
    if FACE_DB_PATH.exists():
        try: _face_db = json.loads(FACE_DB_PATH.read_text(encoding="utf-8"))
        except: pass

def _save_face_db():
    FACE_DB_PATH.write_text(json.dumps(_face_db, indent=2), encoding="utf-8")

def enroll_face(**params) -> Dict[str, Any]:
    from modules.joi_auth import require_user
    require_user()
    name = params.get("name")
    if not name: return {"ok": False, "error": "Name required"}
    # Simplified enrollment: use latest frame
    with _media_lock: frame = _latest_camera_b64
    if not frame: return {"ok": False, "error": "No camera frame"}
    
    encs = []
    if HAVE_FACE_REC:
        img = face_recognition.load_image_file(io.BytesIO(base64.b64decode(frame)))
        encs = [e.tolist() for e in face_recognition.face_encodings(img)]
    
    _face_db["people"][name] = {"encodings": encs, "last_seen": time.time()}
    _save_face_db()
    return {"ok": True, "message": f"Enrolled {name}"}

def _identify_faces_encoding(frame_b64: str) -> List[str]:
    """Identify faces in a base64 frame against the face database."""
    if not HAVE_FACE_REC:
        return []
    try:
        img_data = base64.b64decode(frame_b64)
        img = face_recognition.load_image_file(io.BytesIO(img_data))
        encodings = face_recognition.face_encodings(img)
        if not encodings:
            return []
            
        known_encodings = []
        known_names = []
        for name, data in _face_db.get("people", {}).items():
            for enc in data.get("encodings", []):
                known_encodings.append(np.array(enc))
                known_names.append(name)
        
        if not known_encodings:
            return ["unknown"] * len(encodings)
            
        results = []
        for face_enc in encodings:
            matches = face_recognition.compare_faces(known_encodings, face_enc, tolerance=0.6)
            name = "unknown"
            if True in matches:
                first_match_index = matches.index(True)
                name = known_names[first_match_index]
            results.append(name)
        return results
    except Exception as e:
        print(f"  [joi_media] face identification error: {e}")
        return []

def analyze_camera(**params) -> Dict[str, Any]:
    from modules.joi_auth import require_user
    require_user()
    with _media_lock: frame = _latest_camera_b64
    if not frame: return {"ok": False, "error": "No frame"}
    q = params.get("question", "What do you see?")
    desc = _call_vision_api(frame, q)
    return {"ok": True, "description": desc}

# ── Avatar & TTS ─────────────────────────────────────────────────────────────
def _load_avatar_face_db():
    if AVATAR_FACE_DB_PATH.exists():
        try: return json.loads(AVATAR_FACE_DB_PATH.read_text(encoding="utf-8"))
        except: pass
    return {}

def get_face_coords(name): return _load_avatar_face_db().get(name, dict(DEFAULT_FACE))

def generate_avatar_image(**params):
    from modules.joi_auth import require_user
    require_user()
    desc = params.get("description")
    name = params.get("name", "custom")
    if not client: return {"ok": False, "error": "No OpenAI"}
    r = client.images.generate(model="dall-e-3", prompt=desc, size="1024x1024", n=1)
    img_url = r.data[0].url
    img_r = requests.get(img_url, timeout=30)
    path = AVATAR_DIR / f"{name}.png"
    path.write_bytes(img_r.content)
    set_preference("avatar_image", str(path))
    set_preference("avatar_name", name)
    return {"ok": True, "url": f"/file/project/assets/avatars/{name}.png"}

def generate_speech(text: str):
    engine = get_preference("tts_engine", "kokoro")
    if engine == "kokoro" and HAVE_KOKORO:
        res = generate_speech_kokoro(text)
        if res: return res
    
    if HAVE_EDGE_TTS:
        voice = get_preference("tts_voice", "en-US-AriaNeural")
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        out = AUDIO_DIR / f"tts_{ts}.mp3"
        async def _run():
            c = edge_tts.Communicate(text, voice)
            await c.save(str(out))
        asyncio.run(_run())
        return out
    return None

def list_avatars() -> Dict[str, Any]:
    try:
        avatars = []
        current_avatar = get_preference("avatar_name")
        for avatar_file in AVATAR_DIR.glob("*"):
            if avatar_file.suffix.lower() in ['.png', '.jpg', '.jpeg', '.gif', '.webp']:
                stat = avatar_file.stat()
                avatars.append({
                    "name": avatar_file.stem,
                    "filename": avatar_file.name,
                    "path": str(avatar_file),
                    "url": f"/file/project/assets/avatars/{avatar_file.name}",
                    "size": stat.st_size,
                    "is_current": avatar_file.stem == current_avatar
                })
        return {"ok": True, "avatars": avatars, "count": len(avatars)}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def avatars_route():
    from modules.joi_auth import require_user
    require_user()
    return jsonify(list_avatars())

def avatars_switch_route():
    from modules.joi_auth import require_user
    require_user()
    data = flask_req.get_json(force=True) or {}
    name = data.get("name", "")
    avatar_path = AVATAR_DIR / f"{name}.png"
    if not avatar_path.exists():
        for ext in ['.png', '.jpg', '.jpeg', '.gif', '.webp']:
            candidate = AVATAR_DIR / f"{name}{ext}"
            if candidate.exists():
                avatar_path = candidate
                break
    if avatar_path.exists():
        set_preference("avatar_image", str(avatar_path))
        set_preference("avatar_name", name)
        return jsonify({"ok": True, "message": f"Switched to {name}",
                        "url": f"/file/project/assets/avatars/{avatar_path.name}"})
    return jsonify({"ok": False, "error": f"Avatar '{name}' not found"}), 404

# ── Routes ───────────────────────────────────────────────────────────────────
def vision_start_route(): return jsonify(start_vision())
def vision_stop_route(): return jsonify(stop_vision())

def camera_start_route():
    global _camera_active
    _camera_active = True
    return jsonify({"ok": True, "message": "Camera backend active"})

def camera_stop_route():
    global _camera_active
    _camera_active = False
    return jsonify({"ok": True, "message": "Camera backend stopped"})

def camera_frame_route():
    global _latest_camera_b64, _latest_camera_ts
    data = flask_req.get_json() or {}
    b64 = data.get("image_b64")
    if b64:
        with _media_lock:
            _latest_camera_b64 = b64
            _latest_camera_ts = time.time()
    return jsonify({"ok": True})

def camera_proactive_route():
    global _camera_proactive_queue
    with _media_lock:
        msgs = list(_camera_proactive_queue)
        _camera_proactive_queue.clear()
    return jsonify({"ok": True, "messages": msgs})

def tts_route():
    data = flask_req.get_json() or {}
    text = data.get("text")
    audio = generate_speech(text)
    if audio and audio.exists():
        rel = audio.relative_to(BASE_DIR)
        return jsonify({"ok": True, "url": f"/file/project/{rel}"})
    return jsonify({"ok": False})

# ── Registration ─────────────────────────────────────────────────────────────
_load_face_db()

joi_companion.register_tool({"type": "function", "function": {"name": "analyze_screen", "description": "Describe the desktop."}}, analyze_screen)
joi_companion.register_tool({"type": "function", "function": {"name": "analyze_camera", "description": "Describe the camera view."}}, analyze_camera)
joi_companion.register_tool({"type": "function", "function": {"name": "enroll_face", "description": "Enroll a person's face."}}, enroll_face)

joi_companion.register_route("/vision/start", ["POST"], vision_start_route, "vision_start")
joi_companion.register_route("/vision/stop", ["POST"], vision_stop_route, "vision_stop")
joi_companion.register_route("/camera/start", ["POST"], camera_start_route, "camera_start")
joi_companion.register_route("/camera/stop", ["POST"], camera_stop_route, "camera_stop")
joi_companion.register_route("/camera/proactive", ["GET"], camera_proactive_route, "camera_proactive")
def get_current_avatar_route():
    avatar_path = get_preference("avatar_image")
    avatar_name = get_preference("avatar_name", "default")
    if avatar_path and Path(avatar_path).exists():
        try:
            rel = Path(avatar_path).relative_to(BASE_DIR)
            return jsonify({"ok": True, "url": f"/file/project/{rel}", "name": avatar_name})
        except ValueError:
            return jsonify({"ok": True, "url": f"/file/project/assets/avatars/{Path(avatar_path).name}", "name": avatar_name})
    return jsonify({"ok": False, "message": "No custom avatar set"})

joi_companion.register_route("/camera/frame", ["POST"], camera_frame_route, "camera_frame")
joi_companion.register_route("/tts", ["POST"], tts_route, "generate_tts")
joi_companion.register_route("/avatar", ["GET"], get_current_avatar_route, "get_avatar")
joi_companion.register_route("/avatars", ["GET"], avatars_route, "list_avatars")
joi_companion.register_route("/avatars/switch", ["POST"], avatars_switch_route, "switch_avatar")

# ── Commentary Settings ──────────────────────────────────────────────────────
SETTINGS_PATH = DATA_DIR / "commentary_settings.json"

_DEFAULT_SETTINGS = {
    "vision_commentary": True,
    "camera_commentary": True,
    "global_mute": False,
    "vision_min_interval": 45,
    "camera_min_interval": 30,
}

def _load_settings() -> Dict[str, Any]:
    if SETTINGS_PATH.exists():
        try:
            s = json.loads(SETTINGS_PATH.read_text(encoding="utf-8"))
            for k, v in _DEFAULT_SETTINGS.items():
                if k not in s: s[k] = v
            return s
        except: pass
    return dict(_DEFAULT_SETTINGS)

def _save_settings(settings: Dict[str, Any]):
    SETTINGS_PATH.write_text(json.dumps(settings, indent=2), encoding="utf-8")

def is_muted() -> bool: return _load_settings().get("global_mute", False)

def set_mute(muted: bool):
    s = _load_settings()
    s["global_mute"] = bool(muted)
    _save_settings(s)

def is_vision_commentary_on() -> bool:
    s = _load_settings()
    return not s.get("global_mute", False) and s.get("vision_commentary", True)

def is_camera_commentary_on() -> bool:
    s = _load_settings()
    return not s.get("global_mute", False) and s.get("camera_commentary", True)

def get_vision_interval() -> float: return float(_load_settings().get("vision_min_interval", 45))
def get_camera_interval() -> float: return float(_load_settings().get("camera_min_interval", 30))

def check_mute_trigger(message: str):
    """Check if message is a mute/unmute trigger. Returns (is_trigger, muted, response)."""
    lower = message.strip().lower().rstrip(".!?")
    mutes = ["shut up joi", "quiet joi", "mute joi", "be quiet", "shh", "shut up", "hush joi", "silence joi", "stfu joi"]
    unmutes = ["ok joi you can talk", "unmute joi", "talk now joi", "you can talk", "ok talk", "speak joi", "unmute"]
    for t in mutes:
        if t in lower:
            set_mute(True)
            return (True, True, "Say less. I'm quiet.")
    for t in unmutes:
        if t in lower:
            set_mute(False)
            return (True, False, "I'm back, baby.")
    return (False, None, None)

def toggle_commentary(**params):
    target = params.get("target", "all")
    enabled = params.get("enabled", True)
    if target == "all":
        set_mute(not enabled)
        return {"ok": True, "global_mute": not enabled}
    # (Simplified update logic)
    s = _load_settings()
    if target == "vision": s["vision_commentary"] = enabled
    if target == "camera": s["camera_commentary"] = enabled
    _save_settings(s)
    return {"ok": True, "settings": s}

# Registration
joi_companion.register_tool({"type": "function", "function": {"name": "toggle_commentary", "description": "Toggle vision/camera commentary.", "parameters": {"type": "object", "properties": {"target": {"type": "string", "enum": ["all", "vision", "camera"]}, "enabled": {"type": "boolean"}}, "required": ["enabled"]}}}, toggle_commentary)
joi_companion.register_route("/commentary", ["GET", "POST"], lambda: jsonify({"ok": True, "settings": _load_settings()}), "commentary_route")

print(f"    [OK] joi_media (Senses consolidated, commentary control active)")
