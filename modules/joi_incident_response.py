"""
modules/joi_incident_response.py

Joi v8.0 — Incident Response & Surgical Recovery (Phase 3)
==========================================================
Bridges the gap between Joi's cognitive awareness and the Watchdog's blunt force.
Executes surgical recovery playbooks before a full Git Reset is triggered.

Layer: LAYER_4
"""

import json
import os
import time
import threading
from pathlib import Path
from typing import Any, Dict, List, Optional

BASE_DIR = Path(__file__).resolve().parent.parent
PLAYBOOK_PATH = BASE_DIR / "data" / "playbooks" / "recovery_logic.json"

_lock = threading.Lock()

class IncidentResponseEngine:
    """
    Handles surgical recovery based on predefined playbooks.
    """

    def __init__(self):
        self.playbooks = []
        self._load_playbooks()

    def _load_playbooks(self):
        if PLAYBOOK_PATH.exists():
            try:
                data = json.loads(PLAYBOOK_PATH.read_text(encoding="utf-8"))
                self.playbooks = data.get("playbooks", [])
            except Exception as e:
                print(f"  [ERROR] Failed to load playbooks: {e}")

    def find_playbook(self, error_message: str) -> Optional[Dict]:
        """Match an error message to a recovery playbook."""
        error_lower = error_message.lower()
        for p in self.playbooks:
            if p["condition"].lower() in error_lower:
                return p
        return None

    def execute_recovery(self, playbook_id: str, context: Optional[Dict] = None) -> Dict:
        """
        Executes a specific playbook. 
        Note: In v8.0, many steps are instructions for the Agent to follow, 
        or hooks for the system to run.
        """
        with _lock:
            playbook = next((p for p in self.playbooks if p["id"] == playbook_id), None)
            if not playbook:
                return {"ok": False, "error": f"Playbook {playbook_id} not found."}

            print(f"  [INCIDENT] Executing Playbook: {playbook['name']}")
            
            # Record incident in history
            self._log_recovery(playbook_id, success=True)
            
            return {
                "ok": True,
                "playbook": playbook["name"],
                "steps": playbook["steps"],
                "automatic": playbook["automatic"]
            }

    def _log_recovery(self, playbook_id: str, success: bool):
        try:
            if PLAYBOOK_PATH.exists():
                data = json.loads(PLAYBOOK_PATH.read_text(encoding="utf-8"))
                history = data.get("recovery_history", [])
                history.append({
                    "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                    "playbook_id": playbook_id,
                    "success": success
                })
                data["recovery_history"] = history[-100:] # Keep last 100
                PLAYBOOK_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")
        except Exception:
            pass

_engine = None

def get_incident_engine() -> IncidentResponseEngine:
    global _engine
    if _engine is None:
        _engine = IncidentResponseEngine()
    return _engine

# Tooling for Joi to use
def resolve_incident(**kwargs) -> Dict:
    """Match an error to a playbook and return the recovery steps."""
    error = kwargs.get("error", "")
    engine = get_incident_engine()
    playbook = engine.find_playbook(error)
    if playbook:
        return engine.execute_recovery(playbook["id"])
    return {"ok": False, "error": "No matching playbook found for this incident."}

# Registration
try:
    import joi_companion
    joi_companion.register_tool(
        {"type": "function", "function": {
            "name": "resolve_incident",
            "description": "Finds and executes a surgical recovery playbook for a system error.",
            "parameters": {
                "type": "object",
                "properties": {
                    "error": {"type": "string", "description": "The error message or exception text."}
                },
                "required": ["error"]
            }
        }},
        resolve_incident
    )
    print("  [OK] joi_incident_response loaded (v8.0 Recovery Systems active)")
except Exception:
    pass
