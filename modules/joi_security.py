"""
modules/joi_security.py

Security Assistant -- motion detection, face-gated alerts, recording.

Features:
- Motion detection via camera frame differencing (PIL-based, no OpenCV)
- Face-gated alerts: known faces suppress alerts, unknown faces trigger them
- Ring buffer recording: always keeps last 30 frames, dumps to disk on motion
- ffmpeg MP4 conversion of recorded frame sequences
- Arm/disarm via tool or route, adjustable sensitivity
"""

import os
import io
import json
import base64
import time
import subprocess
import threading
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple

import joi_companion
from flask import jsonify, request as flask_req

# ── Lazy imports (joi_camera / joi_memory may not be loaded yet) ─────────────
def _require_user():
    from modules.joi_memory import require_user
    return require_user()


# ── Optional imports ─────────────────────────────────────────────────────────
try:
    from PIL import Image
    HAVE_PIL = True
except ImportError:
    HAVE_PIL = False
    print("  [joi_security] PIL not available -- motion detection disabled")

# ── Paths & config ──────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
SENSITIVITY = int(os.getenv("SECURITY_SENSITIVITY", "5"))       # percent pixel change threshold
RECORD_DURATION = int(os.getenv("SECURITY_RECORD_DURATION", "60"))  # seconds
RECORDINGS_DIR = BASE_DIR / "data" / "security_recordings"
RECORDINGS_DIR.mkdir(parents=True, exist_ok=True)

# ── State globals ────────────────────────────────────────────────────────────
_lock = threading.Lock()
_armed = False
_monitoring_thread: Optional[threading.Thread] = None
_last_frame: Optional[Any] = None          # Previous PIL Image for comparison
_motion_events: List[Dict[str, Any]] = []  # {timestamp, type, faces, confidence}
_recording_active = False
_record_start_ts: float = 0.0
_frame_buffer: List[Tuple[float, bytes]] = []  # Ring buffer: (timestamp, jpeg_bytes), max 30
_current_recording_dir: Optional[Path] = None
_frame_counter: int = 0                     # Sequential frame number within a recording


# ═════════════════════════════════════════════════════════════════════════════
#  Motion Detection Engine
# ═════════════════════════════════════════════════════════════════════════════

def _detect_motion(current_frame_b64: str) -> Tuple[bool, float]:
    """
    Compare current camera frame to the previous one.
    Returns (motion_detected: bool, change_percent: float).
    Uses PIL only -- no OpenCV dependency.
    """
    global _last_frame, SENSITIVITY

    if not HAVE_PIL:
        return (False, 0.0)

    try:
        # Decode base64 -> PIL Image
        img_data = base64.b64decode(current_frame_b64)
        current_img = Image.open(io.BytesIO(img_data))
    except Exception as e:
        print(f"  [joi_security] frame decode error: {e}")
        return (False, 0.0)

    # First frame -- store and return
    if _last_frame is None:
        _last_frame = current_img
        return (False, 0.0)

    try:
        # Convert both to grayscale and resize to 320x240 for speed
        size = (320, 240)
        prev_gray = _last_frame.convert("L").resize(size, Image.LANCZOS)
        curr_gray = current_img.convert("L").resize(size, Image.LANCZOS)

        # Per-pixel absolute difference
        prev_pixels = prev_gray.load()
        curr_pixels = curr_gray.load()
        total_pixels = size[0] * size[1]
        changed_pixels = 0
        noise_threshold = 30

        for y in range(size[1]):
            for x in range(size[0]):
                diff = abs(prev_pixels[x, y] - curr_pixels[x, y])
                if diff > noise_threshold:
                    changed_pixels += 1

        change_pct = (changed_pixels / total_pixels) * 100.0

        # Update previous frame
        _last_frame = current_img

        if change_pct > SENSITIVITY:
            return (True, round(change_pct, 2))
        return (False, round(change_pct, 2))

    except Exception as e:
        print(f"  [joi_security] motion calc error: {e}")
        _last_frame = current_img
        return (False, 0.0)


# ═════════════════════════════════════════════════════════════════════════════
#  Face-Gated Alert Logic
# ═════════════════════════════════════════════════════════════════════════════

def _process_motion(frame_b64: str):
    """
    Called when motion is detected.
    Runs face identification -- if a known (enrolled) person is recognized
    with confidence > 65%, log but suppress alert. Otherwise, trigger alert.
    """
    global _motion_events

    faces_identified: List[str] = []
    owner_present = False

    # Lazy import from joi_camera
    try:
        from modules.joi_camera import _identify_faces_encoding, _face_db
        faces_identified = _identify_faces_encoding(frame_b64)
    except ImportError:
        pass  # face recognition unavailable
    except Exception as e:
        print(f"  [joi_security] face ID error: {e}")

    # Check if any recognized face is a known (enrolled) person
    # face_recognition returns names for matches, "unknown" otherwise
    for face in faces_identified:
        if face != "unknown":
            owner_present = True
            break

    ts = time.time()
    event = {
        "timestamp": ts,
        "iso": time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(ts)),
        "type": "motion",
        "faces": faces_identified,
        "confidence": 0.0,
    }

    if owner_present:
        # Known person -- log quietly, no alert
        event["type"] = "motion_owner"
        event["alert"] = False
        with _lock:
            _motion_events.append(event)
            if len(_motion_events) > 500:
                _motion_events = _motion_events[-500:]
        print(f"  [joi_security] motion detected -- owner present ({faces_identified}), no alert")
        return

    # Unknown face or no face -> ALERT
    event["type"] = "motion_alert"
    event["alert"] = True
    with _lock:
        _motion_events.append(event)
        if len(_motion_events) > 500:
            _motion_events = _motion_events[-500:]

    print(f"  [joi_security] ALERT -- motion with unknown/no face: {faces_identified}")

    # Start recording if not already active
    if not _recording_active:
        _start_recording()

    # Push alert to camera proactive queue so the frontend gets notified
    alert_msg = (
        f"[SECURITY ALERT] Motion detected at {event['iso']}. "
        f"Faces: {faces_identified if faces_identified else 'none detected'}. "
        f"Recording started."
    )
    try:
        from modules.joi_camera import _camera_proactive_queue, _lock as _cam_lock
        with _cam_lock:
            _camera_proactive_queue.append(alert_msg)
            if len(_camera_proactive_queue) > 10:
                _camera_proactive_queue.pop(0)
    except ImportError:
        pass  # camera module not loaded
    except Exception as e:
        print(f"  [joi_security] proactive push error: {e}")


# ═════════════════════════════════════════════════════════════════════════════
#  Recording Pipeline
# ═════════════════════════════════════════════════════════════════════════════

def _add_to_frame_buffer(frame_b64: str):
    """Append frame to the ring buffer (max 30 entries)."""
    global _frame_buffer
    try:
        jpeg_bytes = base64.b64decode(frame_b64)
        ts = time.time()
        with _lock:
            _frame_buffer.append((ts, jpeg_bytes))
            if len(_frame_buffer) > 30:
                _frame_buffer = _frame_buffer[-30:]
    except Exception as e:
        print(f"  [joi_security] buffer append error: {e}")


def _start_recording():
    """Dump the ring buffer to disk and begin recording new frames."""
    global _recording_active, _record_start_ts, _current_recording_dir, _frame_counter

    ts = int(time.time())
    rec_dir = RECORDINGS_DIR / str(ts)
    rec_dir.mkdir(parents=True, exist_ok=True)

    _current_recording_dir = rec_dir
    _frame_counter = 0

    # Dump existing buffer frames
    with _lock:
        buffer_copy = list(_frame_buffer)

    for _, jpeg_bytes in buffer_copy:
        frame_path = rec_dir / f"frame_{_frame_counter:03d}.jpg"
        try:
            frame_path.write_bytes(jpeg_bytes)
            _frame_counter += 1
        except Exception as e:
            print(f"  [joi_security] buffer dump error: {e}")

    _recording_active = True
    _record_start_ts = time.time()
    print(f"  [joi_security] recording started -- {rec_dir}")


def _save_recording_frame(frame_b64: str):
    """Save a single frame to the active recording directory."""
    global _frame_counter

    if not _recording_active or _current_recording_dir is None:
        return

    try:
        jpeg_bytes = base64.b64decode(frame_b64)
        frame_path = _current_recording_dir / f"frame_{_frame_counter:03d}.jpg"
        frame_path.write_bytes(jpeg_bytes)
        _frame_counter += 1
    except Exception as e:
        print(f"  [joi_security] save frame error: {e}")


def _stop_recording():
    """Stop recording, attempt ffmpeg MP4 conversion."""
    global _recording_active, _current_recording_dir, _frame_counter

    _recording_active = False
    rec_dir = _current_recording_dir

    if rec_dir is None:
        return

    print(f"  [joi_security] recording stopped -- {_frame_counter} frames in {rec_dir}")

    # Try ffmpeg conversion in background
    def _convert():
        try:
            input_pattern = str(rec_dir / "frame_%03d.jpg")
            output_path = str(rec_dir / "recording.mp4")
            result = subprocess.run(
                [
                    "ffmpeg", "-y",
                    "-framerate", "1",
                    "-i", input_pattern,
                    "-c:v", "libx264",
                    "-pix_fmt", "yuv420p",
                    output_path,
                ],
                capture_output=True,
                timeout=60,
            )
            if result.returncode == 0:
                print(f"  [joi_security] MP4 saved -- {output_path}")
            else:
                print(f"  [joi_security] ffmpeg error: {result.stderr.decode('utf-8', errors='replace')[:300]}")
        except FileNotFoundError:
            print("  [joi_security] ffmpeg not found -- frames saved as JPEGs only")
        except subprocess.TimeoutExpired:
            print("  [joi_security] ffmpeg timed out (60s)")
        except Exception as e:
            print(f"  [joi_security] ffmpeg error: {e}")

    threading.Thread(target=_convert, daemon=True).start()

    # Log event
    with _lock:
        _motion_events.append({
            "timestamp": time.time(),
            "iso": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "type": "recording_saved",
            "path": str(rec_dir),
            "frames": _frame_counter,
        })

    _current_recording_dir = None
    _frame_counter = 0


# ═════════════════════════════════════════════════════════════════════════════
#  Monitoring Thread
# ═════════════════════════════════════════════════════════════════════════════

def _security_monitor_loop():
    """Main monitoring loop -- runs while _armed is True."""
    global _armed, _recording_active

    print("  [joi_security] monitoring thread started")
    while _armed:
        try:
            # Grab latest frame from joi_camera
            frame_b64 = None
            try:
                from modules.joi_camera import _latest_camera_b64
                frame_b64 = _latest_camera_b64
            except ImportError:
                pass

            if frame_b64 is None:
                time.sleep(1)
                continue

            # Add to ring buffer
            _add_to_frame_buffer(frame_b64)

            # Save to active recording if running
            if _recording_active:
                _save_recording_frame(frame_b64)

            # Motion detection
            motion, change_pct = _detect_motion(frame_b64)
            if motion:
                _process_motion(frame_b64)

            # Check recording duration
            if _recording_active and (time.time() - _record_start_ts) > RECORD_DURATION:
                _stop_recording()

        except Exception as e:
            print(f"  [joi_security] monitor loop error: {e}")

        time.sleep(1)

    print("  [joi_security] monitoring thread stopped")


# ═════════════════════════════════════════════════════════════════════════════
#  Tool Functions
# ═════════════════════════════════════════════════════════════════════════════

def security_arm(**kwargs) -> Dict[str, Any]:
    """Arm the security system -- start monitoring the camera for motion."""
    global _armed, _monitoring_thread, _last_frame

    if _armed:
        return {"ok": True, "armed": True, "sensitivity": SENSITIVITY, "message": "Already armed."}

    _armed = True
    _last_frame = None  # Reset so first frame is baseline

    _monitoring_thread = threading.Thread(target=_security_monitor_loop, daemon=True)
    _monitoring_thread.start()

    print("  [joi_security] ARMED")
    return {"ok": True, "armed": True, "sensitivity": SENSITIVITY}


def security_disarm(**kwargs) -> Dict[str, Any]:
    """Disarm the security system -- stop monitoring."""
    global _armed, _monitoring_thread, _last_frame

    if not _armed:
        return {"ok": True, "armed": False, "message": "Already disarmed."}

    _armed = False

    # Stop recording if active
    if _recording_active:
        _stop_recording()

    # Thread will exit on its own (checks _armed flag)
    _monitoring_thread = None
    _last_frame = None

    print("  [joi_security] DISARMED")
    return {"ok": True, "armed": False}


def security_status(**kwargs) -> Dict[str, Any]:
    """Return current security system status."""
    with _lock:
        events_count = len(_motion_events)
        last_event = _motion_events[-1] if _motion_events else None

    return {
        "ok": True,
        "armed": _armed,
        "sensitivity": SENSITIVITY,
        "events_count": events_count,
        "last_event": last_event,
        "recording_active": _recording_active,
        "buffer_frames": len(_frame_buffer),
    }


def security_get_recordings(**kwargs) -> Dict[str, Any]:
    """List saved recordings with timestamps."""
    recordings = []
    if RECORDINGS_DIR.exists():
        for d in sorted(RECORDINGS_DIR.iterdir(), reverse=True):
            if d.is_dir():
                mp4 = d / "recording.mp4"
                frame_count = len(list(d.glob("frame_*.jpg")))
                recordings.append({
                    "directory": d.name,
                    "timestamp": int(d.name) if d.name.isdigit() else 0,
                    "iso": time.strftime(
                        "%Y-%m-%dT%H:%M:%S",
                        time.localtime(int(d.name))
                    ) if d.name.isdigit() else d.name,
                    "has_mp4": mp4.exists(),
                    "frames": frame_count,
                })
    return {"ok": True, "recordings": recordings}


def security_set_sensitivity(**kwargs) -> Dict[str, Any]:
    """Adjust motion detection sensitivity (1-20%, default 5%)."""
    global SENSITIVITY

    value = kwargs.get("value")
    if value is None:
        return {"ok": False, "error": "Missing 'value' parameter (1-20)."}

    try:
        value = int(value)
    except (TypeError, ValueError):
        return {"ok": False, "error": "'value' must be an integer (1-20)."}

    if value < 1 or value > 20:
        return {"ok": False, "error": "Sensitivity must be between 1 and 20."}

    SENSITIVITY = value
    print(f"  [joi_security] sensitivity set to {SENSITIVITY}%")
    return {"ok": True, "sensitivity": SENSITIVITY}


# ═════════════════════════════════════════════════════════════════════════════
#  Routes
# ═════════════════════════════════════════════════════════════════════════════

def _security_status_route():
    _require_user()
    return jsonify(security_status())


def _security_control_route():
    _require_user()
    body = flask_req.get_json(silent=True) or {}
    action = body.get("action", "").lower()

    if action == "arm":
        return jsonify(security_arm())
    elif action == "disarm":
        return jsonify(security_disarm())
    elif action == "set_sensitivity":
        val = body.get("value")
        return jsonify(security_set_sensitivity(value=val))
    else:
        return jsonify({"ok": False, "error": f"Unknown action: {action}. Use arm/disarm/set_sensitivity."})


def manage_security(**kwargs) -> Dict[str, Any]:
    """Unified tool for managing security system operations."""
    action = kwargs.get("action")
    if not action:
        return {"ok": False, "error": "action parameter is required"}
        
    try:
        if action == "arm": return security_arm(**kwargs)
        elif action == "disarm": return security_disarm(**kwargs)
        elif action == "status": return security_status(**kwargs)
        elif action == "get_recordings": return security_get_recordings(**kwargs)
        elif action == "set_sensitivity": return security_set_sensitivity(**kwargs)
        else: return {"ok": False, "error": f"Unknown action: {action}"}
    except Exception as exc:
        return {"ok": False, "error": f"Security action {action} failed: {exc}"}

# ═════════════════════════════════════════════════════════════════════════════
#  Registration
# ═════════════════════════════════════════════════════════════════════════════

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "manage_security",
        "description": "Unified tool to control the security system (arm, disarm, check status, get recordings, set sensitivity).",
        "parameters": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "description": "Action to perform",
                    "enum": ["arm", "disarm", "status", "get_recordings", "set_sensitivity"]
                },
                "value": {
                    "type": "integer",
                    "description": "Sensitivity threshold as a percentage 1-20 (required for set_sensitivity)"
                }
            },
            "required": ["action"],
        },
    }},
    manage_security,
)

# Routes
joi_companion.register_route("/security/status", ["GET"], _security_status_route, "security_status")
joi_companion.register_route("/security/control", ["POST"], _security_control_route, "security_control")

print("  [joi_security] loaded -- 5 tools, 2 routes")
