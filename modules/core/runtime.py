"""
modules/core/runtime.py

Core runtime lifecycle and application instance.
"""
import os
import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from modules.core.config import config

# ── Logging Setup ────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler(config.LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("joi.runtime")

# Access the app through the kernel to ensure lifecycle management
from modules.core.kernel import kernel
app = kernel.app

@dataclass
class JoiContext:
    """
    Container for request-scoped state.
    Passed through the context pipeline and tool execution loop.
    """
    request_id: str
    user_message: str
    session_id: str
    recent_messages: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    brain_state: Dict[str, Any] = field(default_factory=dict)
    
    # Storage for data generated during context building
    context_data: Dict[str, Any] = field(default_factory=dict)

def get_app():
    """Return the global Flask app instance."""
    return app
