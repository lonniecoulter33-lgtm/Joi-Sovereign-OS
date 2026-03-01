"""
modules/joi_homeassistant.py

Home Assistant Integration
==========================
Control smart home devices through the Home Assistant REST API.
Supports lights, switches, climate, cameras, media players, sensors,
automations, and generic service calls.

Config (.env):
  HA_URL=http://homeassistant.local:8123
  HA_TOKEN=your_long_lived_access_token
"""

import os
import base64
import json
from pathlib import Path
from typing import Any, Dict, Optional

import joi_companion
from flask import jsonify, request as flask_req

try:
    import requests
    HAVE_REQUESTS = True
except ImportError:
    HAVE_REQUESTS = False

# -- Paths / Config -----------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

HA_URL   = os.getenv("HA_URL", "").strip().rstrip("/")
HA_TOKEN = os.getenv("HA_TOKEN", "").strip()

_NOT_CONFIGURED_MSG = (
    "Home Assistant not configured. Set HA_URL and HA_TOKEN in .env"
)


# -- Helpers -------------------------------------------------------------------

def _ha_configured() -> bool:
    """Return True if both HA_URL and HA_TOKEN are set."""
    return bool(HA_URL and HA_TOKEN)


def _domain_from_entity(entity_id: str) -> str:
    """Extract the domain prefix from an entity_id (e.g. 'light' from 'light.living_room')."""
    return entity_id.split(".")[0] if "." in entity_id else "homeassistant"


def _ha_request(method: str, path: str, data: Optional[dict] = None) -> Dict[str, Any]:
    """
    Authenticated request to the Home Assistant REST API.
    Returns parsed JSON on success or an error dict on failure.
    """
    if not HAVE_REQUESTS:
        return {"ok": False, "error": "Python 'requests' library is not installed."}
    if not _ha_configured():
        return {"ok": False, "error": _NOT_CONFIGURED_MSG}

    url = f"{HA_URL}/api/{path}"
    headers = {
        "Authorization": f"Bearer {HA_TOKEN}",
        "Content-Type": "application/json",
    }

    try:
        resp = requests.request(method, url, headers=headers, json=data, timeout=10)
        resp.raise_for_status()
        # Some HA endpoints return empty body on success
        if resp.status_code == 204 or not resp.text.strip():
            return {"ok": True}
        return resp.json()
    except requests.exceptions.ConnectionError:
        return {"ok": False, "error": f"Cannot connect to Home Assistant at {HA_URL}"}
    except requests.exceptions.Timeout:
        return {"ok": False, "error": "Home Assistant request timed out (10s)"}
    except requests.exceptions.HTTPError as e:
        return {"ok": False, "error": f"HTTP {e.response.status_code}: {e.response.text[:300]}"}
    except Exception as e:
        return {"ok": False, "error": f"{type(e).__name__}: {str(e)[:300]}"}


def _ha_request_raw(method: str, path: str) -> Any:
    """
    Raw authenticated request -- returns the Response object (for binary data).
    Returns None on failure.
    """
    if not HAVE_REQUESTS or not _ha_configured():
        return None

    url = f"{HA_URL}/api/{path}"
    headers = {
        "Authorization": f"Bearer {HA_TOKEN}",
    }

    try:
        resp = requests.request(method, url, headers=headers, timeout=15)
        resp.raise_for_status()
        return resp
    except Exception:
        return None


# ==============================================================================
# TOOL FUNCTIONS
# ==============================================================================

def ha_get_entities(**kwargs) -> Dict[str, Any]:
    """List entities filtered by domain."""
    if not _ha_configured():
        return {"ok": False, "error": _NOT_CONFIGURED_MSG}

    domain = kwargs.get("domain", "").strip().lower()
    result = _ha_request("GET", "states")

    if isinstance(result, dict) and not result.get("ok", True):
        return result  # error dict

    if not isinstance(result, list):
        return {"ok": False, "error": "Unexpected response from Home Assistant"}

    entities = []
    for entity in result:
        eid = entity.get("entity_id", "")
        if domain and not eid.startswith(f"{domain}."):
            continue
        entities.append({
            "entity_id": eid,
            "state": entity.get("state"),
            "friendly_name": entity.get("attributes", {}).get("friendly_name", eid),
        })

    return {
        "ok": True,
        "domain": domain or "all",
        "count": len(entities),
        "entities": entities,
    }


def ha_get_state(**kwargs) -> Dict[str, Any]:
    """Get current state + attributes of a single entity."""
    if not _ha_configured():
        return {"ok": False, "error": _NOT_CONFIGURED_MSG}

    entity_id = kwargs.get("entity_id", "").strip()
    if not entity_id:
        return {"ok": False, "error": "Provide an entity_id (e.g. 'light.living_room')"}

    result = _ha_request("GET", f"states/{entity_id}")

    if isinstance(result, dict) and "entity_id" in result:
        return {
            "ok": True,
            "entity_id": result["entity_id"],
            "state": result.get("state"),
            "attributes": result.get("attributes", {}),
            "last_changed": result.get("last_changed"),
            "last_updated": result.get("last_updated"),
        }

    # Error or not found
    if isinstance(result, dict) and result.get("error"):
        return result
    return {"ok": False, "error": f"Entity '{entity_id}' not found"}


def ha_turn_on(**kwargs) -> Dict[str, Any]:
    """Turn on an entity with optional attributes (brightness, color, etc)."""
    if not _ha_configured():
        return {"ok": False, "error": _NOT_CONFIGURED_MSG}

    entity_id = kwargs.get("entity_id", "").strip()
    if not entity_id:
        return {"ok": False, "error": "Provide an entity_id"}

    domain = _domain_from_entity(entity_id)
    service_data: Dict[str, Any] = {"entity_id": entity_id}

    # Optional light attributes
    if "brightness" in kwargs:
        service_data["brightness"] = int(kwargs["brightness"])
    if "color_temp" in kwargs:
        service_data["color_temp"] = int(kwargs["color_temp"])
    if "rgb_color" in kwargs:
        rgb = kwargs["rgb_color"]
        if isinstance(rgb, list) and len(rgb) == 3:
            service_data["rgb_color"] = [int(c) for c in rgb]

    result = _ha_request("POST", f"services/{domain}/turn_on", service_data)

    if isinstance(result, list):
        # HA returns a list of changed states on service calls
        return {"ok": True, "entity_id": entity_id, "action": "turn_on", "changed": len(result)}
    if isinstance(result, dict) and result.get("ok") is False:
        return result
    return {"ok": True, "entity_id": entity_id, "action": "turn_on"}


def ha_turn_off(**kwargs) -> Dict[str, Any]:
    """Turn off an entity."""
    if not _ha_configured():
        return {"ok": False, "error": _NOT_CONFIGURED_MSG}

    entity_id = kwargs.get("entity_id", "").strip()
    if not entity_id:
        return {"ok": False, "error": "Provide an entity_id"}

    domain = _domain_from_entity(entity_id)
    service_data = {"entity_id": entity_id}

    result = _ha_request("POST", f"services/{domain}/turn_off", service_data)

    if isinstance(result, list):
        return {"ok": True, "entity_id": entity_id, "action": "turn_off", "changed": len(result)}
    if isinstance(result, dict) and result.get("ok") is False:
        return result
    return {"ok": True, "entity_id": entity_id, "action": "turn_off"}


def ha_set_temperature(**kwargs) -> Dict[str, Any]:
    """Set target temperature on a climate entity."""
    if not _ha_configured():
        return {"ok": False, "error": _NOT_CONFIGURED_MSG}

    entity_id = kwargs.get("entity_id", "").strip()
    temperature = kwargs.get("temperature")

    if not entity_id:
        return {"ok": False, "error": "Provide an entity_id (e.g. 'climate.thermostat')"}
    if temperature is None:
        return {"ok": False, "error": "Provide a target temperature"}

    service_data = {
        "entity_id": entity_id,
        "temperature": float(temperature),
    }

    result = _ha_request("POST", "services/climate/set_temperature", service_data)

    if isinstance(result, list):
        return {"ok": True, "entity_id": entity_id, "temperature": float(temperature), "changed": len(result)}
    if isinstance(result, dict) and result.get("ok") is False:
        return result
    return {"ok": True, "entity_id": entity_id, "temperature": float(temperature)}


def ha_call_service(**kwargs) -> Dict[str, Any]:
    """Generic Home Assistant service caller."""
    if not _ha_configured():
        return {"ok": False, "error": _NOT_CONFIGURED_MSG}

    domain = kwargs.get("domain", "").strip()
    service = kwargs.get("service", "").strip()
    entity_id = kwargs.get("entity_id", "").strip()
    data = kwargs.get("data", {})

    if not domain or not service:
        return {"ok": False, "error": "Provide both 'domain' and 'service' (e.g. domain='light', service='toggle')"}

    service_data = dict(data) if isinstance(data, dict) else {}
    if entity_id:
        service_data["entity_id"] = entity_id

    result = _ha_request("POST", f"services/{domain}/{service}", service_data)

    if isinstance(result, list):
        return {"ok": True, "domain": domain, "service": service, "changed": len(result)}
    if isinstance(result, dict) and result.get("ok") is False:
        return result
    return {"ok": True, "domain": domain, "service": service}


def ha_camera_snapshot(**kwargs) -> Dict[str, Any]:
    """Get a camera snapshot as base64-encoded image."""
    if not _ha_configured():
        return {"ok": False, "error": _NOT_CONFIGURED_MSG}

    entity_id = kwargs.get("entity_id", "").strip()
    if not entity_id:
        return {"ok": False, "error": "Provide a camera entity_id (e.g. 'camera.front_door')"}

    resp = _ha_request_raw("GET", f"camera_proxy/{entity_id}")
    if resp is None:
        return {"ok": False, "error": f"Could not fetch snapshot for '{entity_id}'"}

    content_type = resp.headers.get("Content-Type", "image/jpeg")
    img_b64 = base64.b64encode(resp.content).decode("utf-8")

    return {
        "ok": True,
        "entity_id": entity_id,
        "content_type": content_type,
        "image_base64": img_b64,
        "size_bytes": len(resp.content),
    }


def manage_home_assistant(**kwargs) -> Dict[str, Any]:
    """Unified tool for managing Home Assistant operations."""
    action = kwargs.get("action")
    if not action:
        return {"ok": False, "error": "action parameter is required"}
        
    try:
        if action == "get_entities": return ha_get_entities(**kwargs)
        elif action == "get_state": return ha_get_state(**kwargs)
        elif action == "turn_on": return ha_turn_on(**kwargs)
        elif action == "turn_off": return ha_turn_off(**kwargs)
        elif action == "set_temperature": return ha_set_temperature(**kwargs)
        elif action == "call_service": return ha_call_service(**kwargs)
        elif action == "camera_snapshot": return ha_camera_snapshot(**kwargs)
        else: return {"ok": False, "error": f"Unknown action: {action}"}
    except Exception as exc:
        return {"ok": False, "error": f"Home Assistant action {action} failed: {exc}"}

# ==============================================================================
# TOOL REGISTRATION
# ==============================================================================

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "manage_home_assistant",
        "description": (
            "Unified tool to control Home Assistant devices. Perform actions like getting states, "
            "listing entities, turning devices on/off, changing temperatures, grabbing camera snapshots, or calling services."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "description": "Action to perform",
                    "enum": [
                        "get_entities", "get_state", "turn_on",
                        "turn_off", "set_temperature", "call_service", "camera_snapshot"
                    ]
                },
                "entity_id": {
                    "type": "string",
                    "description": "Target entity ID (required for get_state, turn_on, turn_off, set_temperature, camera_snapshot)"
                },
                "domain": {
                    "type": "string",
                    "description": "Device domain to filter by or service domain (required for call_service)"
                },
                "service": {
                    "type": "string",
                    "description": "Service name (required for call_service)"
                },
                "temperature": {
                    "type": "number",
                    "description": "Target temperature value (required for set_temperature)"
                },
                "brightness": {
                    "type": "integer",
                    "description": "Brightness level 0-255 (lights only)"
                },
                "color_temp": {
                    "type": "integer",
                    "description": "Color temperature in mireds (lights only)"
                },
                "rgb_color": {
                    "type": "array",
                    "items": {"type": "integer"},
                    "description": "RGB color as [r, g, b] array (lights only)"
                },
                "data": {
                    "type": "object",
                    "description": "Additional service data as key/value pairs (for call_service)"
                }
            },
            "required": ["action"]
        }
    }},
    manage_home_assistant,
)


# ==============================================================================
# FLASK ROUTES
# ==============================================================================

def _ha_status_route():
    """GET /ha/status -- connection status + entity count."""
    from modules.joi_memory import require_user
    require_user()

    if not _ha_configured():
        return jsonify({
            "ok": True,
            "configured": False,
            "url": None,
            "connected": False,
            "entity_count": 0,
        })

    # Test connectivity
    connected = False
    entity_count = 0
    try:
        result = _ha_request("GET", "states")
        if isinstance(result, list):
            connected = True
            entity_count = len(result)
    except Exception:
        pass

    return jsonify({
        "ok": True,
        "configured": True,
        "url": HA_URL,
        "connected": connected,
        "entity_count": entity_count,
    })


def _ha_entities_route():
    """GET /ha/entities?domain=light -- list entities."""
    from modules.joi_memory import require_user
    require_user()

    domain = flask_req.args.get("domain", "").strip().lower()
    result = ha_get_entities(domain=domain)
    return jsonify(result)


def _ha_control_route():
    """POST /ha/control -- unified control endpoint."""
    from modules.joi_memory import require_user
    require_user()

    data = flask_req.get_json(force=True) or {}
    action = data.get("action", "").strip().lower()
    entity_id = data.get("entity_id", "")

    if action == "turn_on":
        return jsonify(ha_turn_on(**data))
    elif action == "turn_off":
        return jsonify(ha_turn_off(entity_id=entity_id))
    elif action == "set_temp":
        return jsonify(ha_set_temperature(
            entity_id=entity_id,
            temperature=data.get("temperature"),
        ))
    elif action == "call_service":
        return jsonify(ha_call_service(**data))
    else:
        return jsonify({
            "ok": False,
            "error": f"Unknown action '{action}'. Use: turn_on, turn_off, set_temp, call_service",
        })


joi_companion.register_route("/ha/status", ["GET"], _ha_status_route, "ha_status_route")
joi_companion.register_route("/ha/entities", ["GET"], _ha_entities_route, "ha_entities_route")
joi_companion.register_route("/ha/control", ["POST"], _ha_control_route, "ha_control_route")


# ==============================================================================
# INIT
# ==============================================================================

if _ha_configured():
    print(f"  [joi_homeassistant] loaded -- HA_URL={HA_URL}")
else:
    print("  [joi_homeassistant] loaded -- NOT CONFIGURED (set HA_URL + HA_TOKEN in .env)")
