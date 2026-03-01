"""
Joi VTube Studio Bridge — Embodied Avatar

Connects to VTube Studio via pyvts to control a Live2D/VRM avatar.
Lip-sync is driven by TTS audio analysis.

REQUIRES: pip install pyvts
VTube Studio must be running with API enabled (port 8001 default).

Usage:
  bridge = VTubeBridge()
  await bridge.connect()
  await bridge.set_mouth_open(0.8)   # 0.0 = closed, 1.0 = fully open
  await bridge.set_expression("happy")
"""
from __future__ import annotations

import asyncio
import json
import time
from typing import Any, Dict, Optional

try:
    import pyvts
    HAVE_PYVTS = True
except ImportError:
    HAVE_PYVTS = False


class VTubeBridge:
    """Bridge between Joi and VTube Studio for avatar control."""

    def __init__(self, port: int = 8001):
        self.port = port
        self.vts: Optional[pyvts.vts] = None
        self.connected = False
        self.plugin_info = {
            "plugin_name": "Joi Companion",
            "developer": "Lonnie",
            "plugin_icon": ""
        }

    async def connect(self) -> Dict[str, Any]:
        """Connect to VTube Studio and authenticate."""
        if not HAVE_PYVTS:
            return {"ok": False, "error": "pyvts not installed. Run: pip install pyvts"}
        try:
            self.vts = pyvts.vts(plugin_info=self.plugin_info)
            await self.vts.connect()
            await self.vts.request_authenticate_token()
            await self.vts.request_authenticate()
            self.connected = True
            return {"ok": True, "message": "Connected to VTube Studio."}
        except Exception as e:
            self.connected = False
            return {"ok": False, "error": f"VTube Studio connection failed: {e}"}

    async def disconnect(self):
        """Disconnect from VTube Studio."""
        if self.vts:
            try:
                await self.vts.close()
            except Exception:
                pass
        self.connected = False

    async def set_mouth_open(self, value: float) -> Dict[str, Any]:
        """
        Set mouth open amount (0.0 = closed, 1.0 = fully open).
        Drives the MouthOpen parameter in the Live2D model.
        """
        if not self.connected or not self.vts:
            return {"ok": False, "error": "Not connected to VTube Studio"}
        try:
            value = max(0.0, min(1.0, value))
            await self.vts.request(
                self.vts.vts_request.requestSetParameterValue(
                    parameter="MouthOpen", value=value))
            return {"ok": True, "mouth_open": value}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    async def set_expression(self, emotion: str) -> Dict[str, Any]:
        """
        Trigger a VTube Studio expression/hotkey by name.
        Common: happy, sad, angry, surprised, thinking
        """
        if not self.connected or not self.vts:
            return {"ok": False, "error": "Not connected to VTube Studio"}
        try:
            # Get available hotkeys
            response = await self.vts.request(
                self.vts.vts_request.requestHotKeyList())
            hotkeys = response.get("data", {}).get("availableHotkeys", [])

            # Find matching hotkey
            emotion_lower = emotion.lower()
            for hk in hotkeys:
                if emotion_lower in hk.get("name", "").lower():
                    await self.vts.request(
                        self.vts.vts_request.requestTriggerHotKey(
                            hotkeyID=hk["hotkeyID"]))
                    return {"ok": True, "expression": emotion,
                            "hotkey": hk["name"]}

            return {"ok": False, "error": f"No hotkey matching '{emotion}' found.",
                    "available": [h["name"] for h in hotkeys]}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    async def lip_sync_from_audio_data(self, audio_samples: list,
                                        sample_rate: int = 44100,
                                        chunk_ms: int = 50):
        """
        Drive lip-sync from raw audio amplitude data.
        audio_samples: list of float amplitude values (0.0-1.0)
        """
        if not self.connected:
            return
        chunk_size = int(sample_rate * chunk_ms / 1000)
        for i in range(0, len(audio_samples), chunk_size):
            chunk = audio_samples[i:i + chunk_size]
            if chunk:
                amplitude = sum(abs(s) for s in chunk) / len(chunk)
                mouth_val = min(1.0, amplitude * 3.0)  # amplify
                await self.set_mouth_open(mouth_val)
                await asyncio.sleep(chunk_ms / 1000)
        await self.set_mouth_open(0.0)


def is_available() -> bool:
    return HAVE_PYVTS


def get_status() -> Dict[str, Any]:
    return {
        "pyvts_installed": HAVE_PYVTS,
        "available": is_available()
    }
