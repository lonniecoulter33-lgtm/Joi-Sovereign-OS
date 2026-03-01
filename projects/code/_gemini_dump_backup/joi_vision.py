"""
Joi Spatial & Biometric Vision — The "Eyes"

Gives Joi the ability to:
  1. Detect and recognize faces (knows when Lonnie is present)
  2. Track eye gaze (knows if Lonnie is looking at her)
  3. Recognize objects held up to camera
  4. Describe the visual scene and feed it into LLM context

REQUIRES:
  pip install opencv-python mediapipe pillow
  Optional: pip install face-recognition  (for named face matching)
"""
from __future__ import annotations

import base64
import io
import json
import os
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# ── Dependencies (graceful fallback) ────────────────────────────────────

try:
    import cv2
    HAVE_CV2 = True
except ImportError:
    HAVE_CV2 = False

try:
    import mediapipe as mp
    HAVE_MEDIAPIPE = True
except ImportError:
    HAVE_MEDIAPIPE = False

try:
    from PIL import Image
    HAVE_PIL = True
except ImportError:
    HAVE_PIL = False

try:
    import face_recognition as face_rec
    HAVE_FACE_REC = True
except ImportError:
    HAVE_FACE_REC = False

# ── Paths ───────────────────────────────────────────────────────────────

BASE_DIR = Path(__file__).resolve().parent
VISION_DIR = BASE_DIR / "assets" / "vision"
VISION_DIR.mkdir(parents=True, exist_ok=True)
KNOWN_FACES_DIR = VISION_DIR / "known_faces"
KNOWN_FACES_DIR.mkdir(exist_ok=True)
KNOWN_FACES_DB = VISION_DIR / "known_faces.json"

# ── MediaPipe solutions (lazy init) ─────────────────────────────────────

_mp_face_detection = None
_mp_face_mesh = None
_mp_hands = None
_mp_drawing = None

def _init_mediapipe():
    global _mp_face_detection, _mp_face_mesh, _mp_hands, _mp_drawing
    if not HAVE_MEDIAPIPE:
        return
    if _mp_face_detection is None:
        _mp_face_detection = mp.solutions.face_detection.FaceDetection(
            model_selection=1, min_detection_confidence=0.5)
        _mp_face_mesh = mp.solutions.face_mesh.FaceMesh(
            max_num_faces=1, refine_landmarks=True,
            min_detection_confidence=0.5, min_tracking_confidence=0.5)
        _mp_hands = mp.solutions.hands.Hands(
            max_num_hands=2, min_detection_confidence=0.5)
        _mp_drawing = mp.solutions.drawing_utils


# ── Known Faces Database ────────────────────────────────────────────────

def _load_known_faces() -> Dict[str, Any]:
    if KNOWN_FACES_DB.exists():
        try:
            return json.loads(KNOWN_FACES_DB.read_text())
        except Exception:
            pass
    return {"faces": {}}

def _save_known_faces(data: Dict[str, Any]):
    KNOWN_FACES_DB.write_text(json.dumps(data, indent=2))

_known_encodings: List = []
_known_names: List[str] = []
_encodings_loaded = False

def _load_face_encodings():
    """Load face_recognition encodings from saved images."""
    global _known_encodings, _known_names, _encodings_loaded
    if _encodings_loaded or not HAVE_FACE_REC:
        return
    _known_encodings = []
    _known_names = []
    db = _load_known_faces()
    for name, info in db.get("faces", {}).items():
        img_path = KNOWN_FACES_DIR / info.get("filename", "")
        if img_path.exists():
            try:
                img = face_rec.load_image_file(str(img_path))
                encs = face_rec.face_encodings(img)
                if encs:
                    _known_encodings.append(encs[0])
                    _known_names.append(name)
            except Exception:
                pass
    _encodings_loaded = True


# ── Camera Capture ──────────────────────────────────────────────────────

def capture_camera_frame(camera_index: int = 0) -> Dict[str, Any]:
    """
    Capture a single frame from the webcam.

    Returns dict with ok, base64 data URL, and raw frame dimensions.
    """
    if not HAVE_CV2:
        return {"ok": False, "error": "OpenCV not installed. Run: pip install opencv-python"}

    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        return {"ok": False, "error": f"Cannot open camera index {camera_index}"}

    ret, frame = cap.read()
    cap.release()

    if not ret or frame is None:
        return {"ok": False, "error": "Failed to capture frame"}

    # Encode to JPEG
    _, buf = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
    b64 = base64.b64encode(buf.tobytes()).decode('utf-8')

    return {
        "ok": True,
        "data": f"data:image/jpeg;base64,{b64}",
        "width": frame.shape[1],
        "height": frame.shape[0],
    }


# ═══════════════════════════════════════════════════════════════════════
# 1. FACE DETECTION & RECOGNITION
# ═══════════════════════════════════════════════════════════════════════

def detect_faces(frame_b64: Optional[str] = None,
                 camera_index: int = 0) -> Dict[str, Any]:
    """
    Detect faces in a camera frame or provided image.
    Returns bounding boxes and count.
    """
    if not HAVE_CV2:
        return {"ok": False, "error": "OpenCV not installed"}

    frame = _get_frame(frame_b64, camera_index)
    if frame is None:
        return {"ok": False, "error": "Could not get frame"}

    _init_mediapipe()
    faces = []

    if HAVE_MEDIAPIPE and _mp_face_detection:
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = _mp_face_detection.process(rgb)
        if results.detections:
            h, w = frame.shape[:2]
            for det in results.detections:
                bb = det.location_data.relative_bounding_box
                faces.append({
                    "x": int(bb.xmin * w),
                    "y": int(bb.ymin * h),
                    "width": int(bb.width * w),
                    "height": int(bb.height * h),
                    "confidence": round(det.score[0], 3)
                })
    else:
        # Fallback: OpenCV Haar cascade
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        rects = cascade.detectMultiScale(gray, 1.1, 5, minSize=(60, 60))
        for (x, y, w, h) in rects:
            faces.append({"x": int(x), "y": int(y),
                          "width": int(w), "height": int(h),
                          "confidence": 0.7})

    return {
        "ok": True,
        "face_count": len(faces),
        "faces": faces,
        "description": _face_summary(faces)
    }


def recognize_face(frame_b64: Optional[str] = None,
                   camera_index: int = 0) -> Dict[str, Any]:
    """
    Detect AND identify faces using stored encodings.
    Returns names of recognized people (or 'unknown').
    """
    if not HAVE_CV2:
        return {"ok": False, "error": "OpenCV not installed"}
    if not HAVE_FACE_REC:
        return {"ok": False,
                "error": "face-recognition not installed. Run: pip install face-recognition"}

    frame = _get_frame(frame_b64, camera_index)
    if frame is None:
        return {"ok": False, "error": "Could not get frame"}

    _load_face_encodings()
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    locations = face_rec.face_locations(rgb, model="hog")
    encodings = face_rec.face_encodings(rgb, locations)

    identified = []
    for enc, loc in zip(encodings, locations):
        name = "unknown"
        if _known_encodings:
            distances = face_rec.face_distance(_known_encodings, enc)
            best_idx = distances.argmin()
            if distances[best_idx] < 0.5:
                name = _known_names[best_idx]
        top, right, bottom, left = loc
        identified.append({
            "name": name,
            "x": left, "y": top,
            "width": right - left, "height": bottom - top,
            "distance": round(float(distances[best_idx]), 3) if _known_encodings else None
        })

    names = [p["name"] for p in identified]
    return {
        "ok": True,
        "people": identified,
        "count": len(identified),
        "description": _recognition_summary(names)
    }


def register_face(name: str, frame_b64: Optional[str] = None,
                  camera_index: int = 0) -> Dict[str, Any]:
    """
    Save a face encoding for future recognition.
    Captures from camera or uses provided base64 image.
    """
    if not HAVE_CV2:
        return {"ok": False, "error": "OpenCV not installed"}

    frame = _get_frame(frame_b64, camera_index)
    if frame is None:
        return {"ok": False, "error": "Could not get frame"}

    # Save the image
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{name}_{ts}.jpg"
    filepath = KNOWN_FACES_DIR / filename
    cv2.imwrite(str(filepath), frame)

    # Update DB
    db = _load_known_faces()
    db["faces"][name] = {
        "filename": filename,
        "registered": datetime.now().isoformat(),
    }
    _save_known_faces(db)

    # Reload encodings
    global _encodings_loaded
    _encodings_loaded = False

    return {
        "ok": True,
        "message": f"Face registered for '{name}'.",
        "filename": filename
    }


# ═══════════════════════════════════════════════════════════════════════
# 2. EYE TRACKING / GAZE DETECTION
# ═══════════════════════════════════════════════════════════════════════

def detect_eye_gaze(frame_b64: Optional[str] = None,
                    camera_index: int = 0) -> Dict[str, Any]:
    """
    Detect if the user is looking at the camera (i.e. at Joi).
    Uses MediaPipe Face Mesh iris landmarks.
    """
    if not HAVE_CV2 or not HAVE_MEDIAPIPE:
        return {"ok": False, "error": "Requires opencv-python + mediapipe"}

    frame = _get_frame(frame_b64, camera_index)
    if frame is None:
        return {"ok": False, "error": "Could not get frame"}

    _init_mediapipe()
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = _mp_face_mesh.process(rgb)

    if not results.multi_face_landmarks:
        return {"ok": True, "looking_at_camera": False,
                "description": "No face detected in frame."}

    landmarks = results.multi_face_landmarks[0].landmark
    h, w = frame.shape[:2]

    # Iris landmarks: left iris center=468, right iris center=473
    # Eye corner landmarks: left outer=33, left inner=133, right inner=362, right outer=263
    try:
        left_iris = landmarks[468]
        left_outer = landmarks[33]
        left_inner = landmarks[133]

        right_iris = landmarks[473]
        right_inner = landmarks[362]
        right_outer = landmarks[263]

        # Horizontal ratio: 0=looking left, 0.5=center, 1=looking right
        def iris_ratio(iris, outer, inner):
            total = ((inner.x - outer.x)**2 + (inner.y - outer.y)**2)**0.5
            if total < 1e-6:
                return 0.5
            from_outer = ((iris.x - outer.x)**2 + (iris.y - outer.y)**2)**0.5
            return from_outer / total

        left_ratio = iris_ratio(left_iris, left_outer, left_inner)
        right_ratio = iris_ratio(right_iris, right_outer, right_inner)
        avg_ratio = (left_ratio + right_ratio) / 2

        # Vertical: use nose tip (1) vs forehead (10) to estimate head pitch
        nose_tip = landmarks[1]
        forehead = landmarks[10]
        pitch_proxy = nose_tip.y - forehead.y  # positive = face tilted down

        looking_at_camera = 0.3 < avg_ratio < 0.7 and 0.05 < pitch_proxy < 0.25
        gaze = "center"
        if avg_ratio < 0.35:
            gaze = "left"
        elif avg_ratio > 0.65:
            gaze = "right"

        return {
            "ok": True,
            "looking_at_camera": looking_at_camera,
            "gaze_direction": gaze,
            "gaze_ratio": round(avg_ratio, 3),
            "description": (
                "Lonnie is looking at you." if looking_at_camera
                else f"Lonnie is looking to the {gaze}."
            )
        }
    except (IndexError, AttributeError):
        return {"ok": True, "looking_at_camera": False,
                "description": "Could not determine gaze direction."}


# ═══════════════════════════════════════════════════════════════════════
# 3. OBJECT & SCENE RECOGNITION (via Vision LLM)
# ═══════════════════════════════════════════════════════════════════════

def recognize_objects(openai_client, vision_model: str = "gpt-4o",
                      question: str = "What objects do you see? Describe what the person is holding or doing.",
                      frame_b64: Optional[str] = None,
                      camera_index: int = 0) -> Dict[str, Any]:
    """
    Capture a camera frame and send to Vision model for scene description.
    """
    if not HAVE_CV2:
        return {"ok": False, "error": "OpenCV not installed"}
    if not openai_client:
        return {"ok": False, "error": "OpenAI client not available"}

    frame = _get_frame(frame_b64, camera_index)
    if frame is None:
        return {"ok": False, "error": "Could not get frame"}

    # Resize for API
    max_dim = 1024
    h, w = frame.shape[:2]
    if max(h, w) > max_dim:
        scale = max_dim / max(h, w)
        frame = cv2.resize(frame, (int(w * scale), int(h * scale)))

    _, buf = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
    b64 = base64.b64encode(buf.tobytes()).decode('utf-8')
    data_url = f"data:image/jpeg;base64,{b64}"

    try:
        response = openai_client.chat.completions.create(
            model=vision_model,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": question},
                    {"type": "image_url", "image_url": {"url": data_url, "detail": "low"}}
                ]
            }],
            max_tokens=300
        )
        desc = response.choices[0].message.content or ""
        return {
            "ok": True,
            "description": desc,
            "source": "camera"
        }
    except Exception as e:
        return {"ok": False, "error": f"Vision API error: {e}"}


def get_visual_context(openai_client, vision_model: str = "gpt-4o",
                       camera_index: int = 0) -> str:
    """
    One-shot: capture camera, detect face, check gaze, describe scene.
    Returns a plain-text summary suitable for injecting into LLM context.
    """
    parts = []

    # Face detection
    faces = detect_faces(camera_index=camera_index)
    if faces.get("ok") and faces.get("face_count", 0) > 0:
        parts.append(f"I can see {faces['face_count']} face(s).")

        # Recognition
        if HAVE_FACE_REC:
            rec = recognize_face(camera_index=camera_index)
            if rec.get("ok"):
                parts.append(rec.get("description", ""))

        # Gaze
        if HAVE_MEDIAPIPE:
            gaze = detect_eye_gaze(camera_index=camera_index)
            if gaze.get("ok"):
                parts.append(gaze.get("description", ""))
    else:
        parts.append("No one is visible in front of the camera right now.")

    # Scene description
    if openai_client:
        scene = recognize_objects(
            openai_client, vision_model,
            question="Briefly describe what you see: the person, what they're wearing, "
                     "any objects visible, and the environment.",
            camera_index=camera_index)
        if scene.get("ok"):
            parts.append("Scene: " + scene["description"])

    return " ".join(parts).strip() or "Camera not available."


# ── Helpers ─────────────────────────────────────────────────────────────

def _get_frame(frame_b64: Optional[str], camera_index: int):
    """Get a frame from base64 string or camera capture."""
    if not HAVE_CV2:
        return None

    if frame_b64:
        # Decode base64
        if "base64," in frame_b64:
            frame_b64 = frame_b64.split("base64,")[1]
        try:
            import numpy as np
            img_bytes = base64.b64decode(frame_b64)
            nparr = np.frombuffer(img_bytes, np.uint8)
            return cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        except Exception:
            return None

    # Capture from camera
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        return None
    ret, frame = cap.read()
    cap.release()
    return frame if ret else None


def _face_summary(faces: list) -> str:
    n = len(faces)
    if n == 0:
        return "No faces detected."
    elif n == 1:
        return "I can see one person."
    else:
        return f"I can see {n} people."


def _recognition_summary(names: list) -> str:
    if not names:
        return "No faces detected."
    known = [n for n in names if n != "unknown"]
    unknown = names.count("unknown")
    parts = []
    if known:
        parts.append(f"I see {', '.join(known)}.")
    if unknown == 1:
        parts.append("There's also someone I don't recognize.")
    elif unknown > 1:
        parts.append(f"There are {unknown} people I don't recognize.")
    return " ".join(parts) if parts else "No faces recognized."


def is_available() -> bool:
    return HAVE_CV2


def get_status() -> Dict[str, Any]:
    db = _load_known_faces()
    return {
        "opencv": HAVE_CV2,
        "mediapipe": HAVE_MEDIAPIPE,
        "face_recognition": HAVE_FACE_REC,
        "pillow": HAVE_PIL,
        "known_faces": len(db.get("faces", {})),
        "available": is_available()
    }
