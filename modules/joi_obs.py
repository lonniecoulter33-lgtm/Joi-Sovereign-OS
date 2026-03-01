"""
modules/joi_obs.py

OBS Studio WebSocket Control
=============================
Connect to OBS Studio via WebSocket 5.x to control scenes, recording,
streaming, and source visibility.  Uses obsws-python as the client library.

Config (.env):
  OBS_WEBSOCKET_HOST=localhost
  OBS_WEBSOCKET_PORT=4455
  OBS_WEBSOCKET_PASSWORD=your_password
"""

import os
import base64
import traceback
from pathlib import Path
from typing import Dict, Any, Optional

import joi_companion
from flask import jsonify, request as flask_req

# ── Optional dependency ─────────────────────────────────────────────────────
try:
    import obsws_python as obsws
    HAVE_OBS = True
except ImportError:
    HAVE_OBS = False
    print("  [joi_obs] obsws-python not installed -- OBS control disabled (pip install obsws-python)")

# ── Paths / Config ──────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent

OBS_HOST = os.getenv("OBS_WEBSOCKET_HOST", "localhost")
OBS_PORT = int(os.getenv("OBS_WEBSOCKET_PORT", "4455"))
OBS_PASSWORD = os.getenv("OBS_WEBSOCKET_PASSWORD", "")

# ── Connection state ────────────────────────────────────────────────────────
_obs_client = None


def _connect() -> Dict[str, Any]:
    """Lazy connect to OBS WebSocket. Returns status dict."""
    global _obs_client
    if not HAVE_OBS:
        return {"ok": False, "error": "obsws-python is not installed. Run: pip install obsws-python"}
    try:
        _obs_client = obsws.ReqClient(
            host=OBS_HOST,
            port=OBS_PORT,
            password=OBS_PASSWORD,
            timeout=5,
        )
        version = _obs_client.get_version()
        info = {
            "obs_version": getattr(version, "obs_version", "unknown"),
            "ws_version": getattr(version, "obs_web_socket_version", "unknown"),
        }
        print(f"  [joi_obs] connected to OBS {info['obs_version']} (ws {info['ws_version']})")
        return {"ok": True, "connected": True, **info}
    except Exception as exc:
        _obs_client = None
        print(f"  [joi_obs] connection failed: {exc}")
        return {"ok": False, "error": f"Connection failed: {exc}"}


def _ensure_connected() -> Optional[str]:
    """Ensure we have a live connection. Returns error string or None if good."""
    global _obs_client
    if _obs_client is not None:
        # Quick health check
        try:
            _obs_client.get_version()
            return None  # still connected
        except Exception:
            print("  [joi_obs] lost connection, attempting reconnect...")
            _obs_client = None

    result = _connect()
    if not result.get("ok"):
        return result.get("error", "OBS not connected. Use obs_connect() first or check OBS WebSocket settings.")
    return None


def _disconnect():
    """Clean disconnect from OBS."""
    global _obs_client
    if _obs_client is not None:
        try:
            _obs_client.base_client.ws.close()
        except Exception:
            pass
        _obs_client = None
        print("  [joi_obs] disconnected")


def _not_connected_error() -> Dict[str, Any]:
    return {"ok": False, "error": "OBS not connected. Use obs_connect() first or check OBS WebSocket settings."}


def _no_library_error() -> Dict[str, Any]:
    return {"ok": False, "error": "obsws-python is not installed. Run: pip install obsws-python"}


# ── Tool implementations ────────────────────────────────────────────────────

def _obs_connect_tool(**kwargs) -> Dict[str, Any]:
    """Connect to OBS WebSocket."""
    if not HAVE_OBS:
        return _no_library_error()
    # Disconnect first if already connected
    _disconnect()
    return _connect()


def _obs_status_tool(**kwargs) -> Dict[str, Any]:
    """Get OBS recording/streaming state, current scene, and stats."""
    if not HAVE_OBS:
        return _no_library_error()
    err = _ensure_connected()
    if err:
        return {"ok": False, "error": err}
    try:
        rec = _obs_client.get_record_status()
        stream = _obs_client.get_stream_status()
        scene = _obs_client.get_current_program_scene()
        stats = _obs_client.get_stats()
        return {
            "ok": True,
            "recording": {
                "active": getattr(rec, "output_active", False),
                "paused": getattr(rec, "output_paused", False),
                "timecode": getattr(rec, "output_timecode", "00:00:00"),
                "bytes": getattr(rec, "output_bytes", 0),
            },
            "streaming": {
                "active": getattr(stream, "output_active", False),
                "timecode": getattr(stream, "output_timecode", "00:00:00"),
                "bytes": getattr(stream, "output_bytes", 0),
            },
            "current_scene": getattr(scene, "current_program_scene_name", "unknown"),
            "stats": {
                "cpu_usage": getattr(stats, "cpu_usage", 0),
                "memory_usage": getattr(stats, "memory_usage", 0),
                "active_fps": getattr(stats, "active_fps", 0),
                "render_skipped_frames": getattr(stats, "render_skipped_frames", 0),
                "output_skipped_frames": getattr(stats, "output_skipped_frames", 0),
            },
        }
    except Exception as exc:
        return {"ok": False, "error": f"Failed to get OBS status: {exc}"}


def _obs_get_scenes_tool(**kwargs) -> Dict[str, Any]:
    """List all OBS scenes."""
    if not HAVE_OBS:
        return _no_library_error()
    err = _ensure_connected()
    if err:
        return {"ok": False, "error": err}
    try:
        resp = _obs_client.get_scene_list()
        scenes = []
        for s in getattr(resp, "scenes", []):
            name = s.get("sceneName", "unknown") if isinstance(s, dict) else getattr(s, "sceneName", "unknown")
            scenes.append(name)
        current = getattr(resp, "current_program_scene_name", "unknown")
        return {"ok": True, "scenes": scenes, "current_scene": current}
    except Exception as exc:
        return {"ok": False, "error": f"Failed to get scenes: {exc}"}


def _obs_switch_scene_tool(**kwargs) -> Dict[str, Any]:
    """Switch the active OBS scene."""
    if not HAVE_OBS:
        return _no_library_error()
    scene_name = kwargs.get("scene_name", "")
    if not scene_name:
        return {"ok": False, "error": "scene_name is required"}
    err = _ensure_connected()
    if err:
        return {"ok": False, "error": err}
    try:
        _obs_client.set_current_program_scene(scene_name)
        print(f"  [joi_obs] switched scene to '{scene_name}'")
        return {"ok": True, "scene": scene_name}
    except Exception as exc:
        return {"ok": False, "error": f"Failed to switch scene: {exc}"}


def _obs_start_recording_tool(**kwargs) -> Dict[str, Any]:
    """Start OBS recording."""
    if not HAVE_OBS:
        return _no_library_error()
    err = _ensure_connected()
    if err:
        return {"ok": False, "error": err}
    try:
        _obs_client.start_record()
        print("  [joi_obs] recording started")
        return {"ok": True, "action": "start_recording"}
    except Exception as exc:
        return {"ok": False, "error": f"Failed to start recording: {exc}"}


def _obs_stop_recording_tool(**kwargs) -> Dict[str, Any]:
    """Stop OBS recording."""
    if not HAVE_OBS:
        return _no_library_error()
    err = _ensure_connected()
    if err:
        return {"ok": False, "error": err}
    try:
        resp = _obs_client.stop_record()
        output_path = getattr(resp, "output_path", "unknown")
        print(f"  [joi_obs] recording stopped -- saved to {output_path}")
        return {"ok": True, "action": "stop_recording", "output_path": output_path}
    except Exception as exc:
        return {"ok": False, "error": f"Failed to stop recording: {exc}"}


def _obs_pause_recording_tool(**kwargs) -> Dict[str, Any]:
    """Pause or resume OBS recording."""
    if not HAVE_OBS:
        return _no_library_error()
    err = _ensure_connected()
    if err:
        return {"ok": False, "error": err}
    try:
        _obs_client.toggle_record_pause()
        print("  [joi_obs] recording pause toggled")
        return {"ok": True, "action": "toggle_record_pause"}
    except Exception as exc:
        return {"ok": False, "error": f"Failed to toggle recording pause: {exc}"}


def _obs_start_streaming_tool(**kwargs) -> Dict[str, Any]:
    """Start OBS streaming."""
    if not HAVE_OBS:
        return _no_library_error()
    err = _ensure_connected()
    if err:
        return {"ok": False, "error": err}
    try:
        _obs_client.start_stream()
        print("  [joi_obs] streaming started")
        return {"ok": True, "action": "start_streaming"}
    except Exception as exc:
        return {"ok": False, "error": f"Failed to start streaming: {exc}"}


def _obs_stop_streaming_tool(**kwargs) -> Dict[str, Any]:
    """Stop OBS streaming."""
    if not HAVE_OBS:
        return _no_library_error()
    err = _ensure_connected()
    if err:
        return {"ok": False, "error": err}
    try:
        _obs_client.stop_stream()
        print("  [joi_obs] streaming stopped")
        return {"ok": True, "action": "stop_streaming"}
    except Exception as exc:
        return {"ok": False, "error": f"Failed to stop streaming: {exc}"}


def _obs_get_sources_tool(**kwargs) -> Dict[str, Any]:
    """List sources in a specific OBS scene."""
    if not HAVE_OBS:
        return _no_library_error()
    scene_name = kwargs.get("scene_name", "")
    if not scene_name:
        return {"ok": False, "error": "scene_name is required"}
    err = _ensure_connected()
    if err:
        return {"ok": False, "error": err}
    try:
        resp = _obs_client.get_scene_item_list(scene_name)
        items = []
        for item in getattr(resp, "scene_items", []):
            if isinstance(item, dict):
                items.append({
                    "id": item.get("sceneItemId"),
                    "name": item.get("sourceName", "unknown"),
                    "type": item.get("inputKind", item.get("sourceType", "unknown")),
                    "enabled": item.get("sceneItemEnabled", True),
                })
            else:
                items.append({
                    "id": getattr(item, "sceneItemId", None),
                    "name": getattr(item, "sourceName", "unknown"),
                    "type": getattr(item, "inputKind", getattr(item, "sourceType", "unknown")),
                    "enabled": getattr(item, "sceneItemEnabled", True),
                })
        return {"ok": True, "scene": scene_name, "sources": items}
    except Exception as exc:
        return {"ok": False, "error": f"Failed to get sources: {exc}"}


def _obs_toggle_source_tool(**kwargs) -> Dict[str, Any]:
    """Show or hide a source in an OBS scene."""
    if not HAVE_OBS:
        return _no_library_error()
    source_name = kwargs.get("source_name", "")
    scene_name = kwargs.get("scene_name", "")
    visible = kwargs.get("visible", True)
    if not source_name or not scene_name:
        return {"ok": False, "error": "source_name and scene_name are both required"}
    err = _ensure_connected()
    if err:
        return {"ok": False, "error": err}
    try:
        # First find the scene item ID for this source
        resp = _obs_client.get_scene_item_list(scene_name)
        item_id = None
        for item in getattr(resp, "scene_items", []):
            if isinstance(item, dict):
                name = item.get("sourceName", "")
                sid = item.get("sceneItemId")
            else:
                name = getattr(item, "sourceName", "")
                sid = getattr(item, "sceneItemId", None)
            if name == source_name:
                item_id = sid
                break

        if item_id is None:
            return {"ok": False, "error": f"Source '{source_name}' not found in scene '{scene_name}'"}

        _obs_client.set_scene_item_enabled(scene_name, item_id, bool(visible))
        state = "visible" if visible else "hidden"
        print(f"  [joi_obs] source '{source_name}' in '{scene_name}' set to {state}")
        return {"ok": True, "source": source_name, "scene": scene_name, "visible": bool(visible)}
    except Exception as exc:
        return {"ok": False, "error": f"Failed to toggle source: {exc}"}


def _obs_screenshot_tool(**kwargs) -> Dict[str, Any]:
    """Capture a screenshot of the current OBS output as base64 PNG."""
    if not HAVE_OBS:
        return _no_library_error()
    err = _ensure_connected()
    if err:
        return {"ok": False, "error": err}
    try:
        # Get the current program scene name to use as source
        scene_resp = _obs_client.get_current_program_scene()
        scene_name = getattr(scene_resp, "current_program_scene_name", "")
        if not scene_name:
            return {"ok": False, "error": "Could not determine current scene for screenshot"}

        resp = _obs_client.get_source_screenshot(
            name=scene_name,
            img_format="png",
            width=1280,
            quality=-1,
        )
        image_data = getattr(resp, "image_data", "")
        # obsws-python returns data:image/png;base64,<data> -- strip the prefix
        if "," in image_data:
            image_data = image_data.split(",", 1)[1]
        print(f"  [joi_obs] screenshot captured ({len(image_data)} chars base64)")
        return {"ok": True, "image_base64": image_data, "format": "png", "width": 1280}
    except Exception as exc:
        return {"ok": False, "error": f"Failed to capture screenshot: {exc}"}

def manage_obs(**kwargs) -> Dict[str, Any]:
    """Unified tool for managing OBS Studio operations."""
    if not HAVE_OBS:
        return _no_library_error()
    err = _ensure_connected()
    if err:
        return {"ok": False, "error": err}

    action = kwargs.get("action")
    if not action:
        return {"ok": False, "error": "action parameter is required"}

    try:
        if action == "status": return _obs_status_tool(**kwargs)
        elif action == "get_scenes": return _obs_get_scenes_tool(**kwargs)
        elif action == "switch_scene": return _obs_switch_scene_tool(**kwargs)
        elif action == "start_recording": return _obs_start_recording_tool(**kwargs)
        elif action == "stop_recording": return _obs_stop_recording_tool(**kwargs)
        elif action == "pause_recording": return _obs_pause_recording_tool(**kwargs)
        elif action == "start_streaming": return _obs_start_streaming_tool(**kwargs)
        elif action == "stop_streaming": return _obs_stop_streaming_tool(**kwargs)
        elif action == "get_sources": return _obs_get_sources_tool(**kwargs)
        elif action == "toggle_source": return _obs_toggle_source_tool(**kwargs)
        elif action == "screenshot": return _obs_screenshot_tool(**kwargs)
        else: return {"ok": False, "error": f"Unknown action: {action}"}
    except Exception as exc:
        return {"ok": False, "error": f"OBS action {action} failed: {exc}"}



# ── Flask Routes ─────────────────────────────────────────────────────────────

def _obs_status_route():
    from modules.joi_memory import require_user
    require_user()
    if not HAVE_OBS:
        return jsonify({"ok": False, "error": "obsws-python not installed"})
    err = _ensure_connected()
    if err:
        return jsonify({"ok": False, "connected": False, "error": err})
    status = _obs_status_tool()
    status["connected"] = True
    return jsonify(status)


def _obs_control_route():
    from modules.joi_memory import require_user
    require_user()
    data = flask_req.get_json(force=True) or {}
    action = data.get("action", "")

    action_map = {
        "connect": _obs_connect_tool,
        "disconnect": lambda **kw: (_disconnect(), {"ok": True, "action": "disconnected"})[1],
        "start_recording": _obs_start_recording_tool,
        "stop_recording": _obs_stop_recording_tool,
        "pause_recording": _obs_pause_recording_tool,
        "start_streaming": _obs_start_streaming_tool,
        "stop_streaming": _obs_stop_streaming_tool,
        "switch_scene": _obs_switch_scene_tool,
        "screenshot": _obs_screenshot_tool,
    }

    handler = action_map.get(action)
    if not handler:
        return jsonify({"ok": False, "error": f"Unknown action '{action}'. Options: {', '.join(action_map.keys())}"})

    # Pass through any extra params from the request body
    params = {k: v for k, v in data.items() if k != "action"}
    return jsonify(handler(**params))


joi_companion.register_route("/obs/status", ["GET"], _obs_status_route, "obs_status_route")
joi_companion.register_route("/obs/control", ["POST"], _obs_control_route, "obs_control_route")

# ── Tool Registration ────────────────────────────────────────────────────────

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "obs_connect",
        "description": (
            "Connect to OBS Studio via WebSocket. Use when Lonnie asks you to "
            "control OBS, or before any other OBS operation if not yet connected."
        ),
        "parameters": {"type": "object", "properties": {}},
    }},
    _obs_connect_tool,
)

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "manage_obs",
        "description": (
            "Unified tool to control OBS Studio. Perform actions like getting status, changing scenes, "
            "recording, streaming, taking screenshots, and toggling sources."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "description": "Action to perform",
                    "enum": [
                        "status", "get_scenes", "switch_scene",
                        "start_recording", "stop_recording", "pause_recording",
                        "start_streaming", "stop_streaming",
                        "get_sources", "toggle_source", "screenshot"
                    ]
                },
                "scene_name": {
                    "type": "string",
                    "description": "Scene name (required for switch_scene, get_sources, toggle_source)"
                },
                "source_name": {
                    "type": "string",
                    "description": "Source name (required for toggle_source)"
                },
                "visible": {
                    "type": "boolean",
                    "description": "True to show, False to hide (required for toggle_source)"
                }
            },
            "required": ["action"]
        }
    }},
    manage_obs,
)

# ── Init print ──────────────────────────────────────────────────────────────
_lib_status = "ready" if HAVE_OBS else "no obsws-python"
print(f"  [joi_obs] loaded -- lib={_lib_status}, target={OBS_HOST}:{OBS_PORT}")
