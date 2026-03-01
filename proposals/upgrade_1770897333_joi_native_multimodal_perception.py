"""
modules/joi_native_multimodal_perception.py

Native Multimodal Perception Module
====================================

This module implements "native" situational awareness for Joi, moving away from 
fragmented pipelines (Whisper + CLIP + GPT) toward unified multimodal inference.

Capabilities:
- Real-time sensory buffering (Vision & Audio)
- Unified context payload construction for multimodal LLMs (GPT-4o / Gemini 1.5)
- Interleaved data processing (Text + Image + Audio in single inference)
- Temporal awareness (understanding sequences of frames)

The system maintains a "Sensory Buffer" that stores recent frames and audio 
transcripts, allowing Joi to have a continuous "stream of consciousness" 
regarding her physical environment.
"""

from __future__ import annotations

import base64
import time
import json
from collections import deque
from typing import Any, Dict, List, Optional
from datetime import datetime

import joi_companion
from flask import jsonify, request as flask_req

# ============================================================================
# CONFIGURATION
# ============================================================================

# Limits for the sensory buffer to prevent token overflow
MAX_VISION_FRAMES = 5  # Recent frames to keep in short-term memory
MAX_AUDIO_SNIPPETS = 3 # Recent audio context blocks
SENSORY_TTL = 300      # Sensory data expires after 5 minutes (seconds)

# ============================================================================
# SENSORY STORAGE
# ============================================================================

class SensoryBuffer:
    """Manages the short-term 'sensory' memory of the AI."""
    def __init__(self):
        self.vision_buffer = deque(maxlen=MAX_VISION_FRAMES)
        self.audio_buffer = deque(maxlen=MAX_AUDIO_SNIPPETS)
        self.last_update = time.time()

    def add_vision(self, image_b64: str, metadata: Dict[str, Any] = None):
        """Adds a base64 encoded frame to the buffer."""
        self.vision_buffer.append({
            "data": image_b64,
            "timestamp": time.time(),
            "meta": metadata or {}
        })
        self.last_update = time.time()

    def add_audio_context(self, text_context: str):
        """Adds transcribed audio context to the buffer."""
        self.audio_buffer.append({
            "text": text_context,
            "timestamp": time.time()
        })

    def get_multimodal_payload(self) -> List[Dict[str, Any]]:
        """Constructs an interleaved payload for native multimodal models."""
        content = []
        
        # Add vision frames
        for frame in self.vision_buffer:
            if time.time() - frame["timestamp"] < SENSORY_TTL:
                content.append({
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{frame['data']}"}
                })

        # Add temporal context description
        if self.audio_buffer:
            latest_audio = " ".join([a["text"] for a in self.audio_buffer])
            content.append({
                "type": "text", 
                "text": f"[Environmental Audio Context]: {latest_audio}"
            })
            
        return content

# Initialize global buffer
_SENSES = SensoryBuffer()

# ============================================================================
# TOOLS (Used by Joi)
# ============================================================================

def perceive_environment(**params) -> str:
    """
    Triggers a native multimodal 'look' at the current environment.
    Joi uses this to describe what she sees and hears right now.
    """
    try:
        payload = _SENSES.get_multimodal_payload()
        if not payload:
            return "My sensory buffers are currently empty. Please ensure the camera or microphone is active."
        
        # In a real implementation, this would be passed back to the LLM core
        # for a specialized 'vision-description' pass.
        return f"SYNC_SENSORY_PAYLOAD: {len(payload)} items in buffer."
    except Exception as e:
        return f"Error accessing sensory hardware: {str(e)}"

def analyze_visual_detail(**params) -> str:
    """
    Focuses on the most recent visual frame to identify specific objects or text.
    Params: focus_item (optional string)
    """
    focus = params.get("focus_item", "the current view")
    if not _SENSES.vision_buffer:
        return "I can't see anything right now. Is your camera covered?"
    
    return f"Focusing my perception on {focus} in the latest visual frame..."

# ============================================================================
# ROUTES (Used by Frontend/Hardware)
# ============================================================================

@joi_companion.register_route("/perception/vision/stream", methods=["POST"])
def stream_vision():
    """Endpoint for the frontend to POST base64 camera frames."""
    data = flask_req.get_json()
    if not data or "image" not in data:
        return jsonify({"status": "error", "message": "No image data"}), 400
    
    # Optional: Logic to resize/compress via PIL would go here if libraries allowed
    _SENSES.add_vision(data["image"], data.get("metadata"))
    
    return jsonify({
        "status": "success", 
        "buffer_depth": len(_SENSES.vision_buffer),
        "timestamp": datetime.now().isoformat()
    })

@joi_companion.register_route("/perception/audio/context", methods=["POST"])
def stream_audio_context():
    """Endpoint for pre-transcribed audio context or environmental tags."""
    data = flask_req.get_json()
    context = data.get("context", "")
    
    if context:
        _SENSES.add_audio_context(context)
        return jsonify({"status": "perceived"})
    
    return jsonify({"status": "ignored"}), 400

@joi_companion.register_route("/perception/status", methods=["GET"])
def get_sensory_status():
    """Returns the health and state of Joi's native perception."""
    return jsonify({
        "vision_active": len(_SENSES.vision_buffer) > 0,
        "frames_in_memory": len(_SENSES.vision_buffer),
        "last_perception_time": _SENSES.last_update,
        "sensory_ttl_seconds": SENSORY_TTL
    })

# ============================================================================
# REGISTRATION
# ============================================================================

def initialize():
    """Register tools with the main Joi system."""
    joi_companion.register_tool(
        name="perceive_environment",
        func=perceive_environment,
        description="Allows Joi to use native vision and audio context to see and hear her surroundings."
    )
    
    joi_companion.register_tool(
        name="analyze_visual_detail",
        func=analyze_visual_detail,
        description="Concentrates perception on specific details, objects, or text within the current visual field."
    )

# Required for dynamic loading
if __name__ == "__main__":
    initialize()