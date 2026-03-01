"""
modules/core/config.py

Centralized configuration management for Joi.
Handles environment variables, defaults, and runtime constants.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

class JoiConfig:
    def __init__(self):
        # Paths
        self.BASE_DIR = Path(__file__).resolve().parent.parent.parent
        self.MODULES_DIR = self.BASE_DIR / "modules"
        self.DATA_DIR = self.BASE_DIR / "data"
        self.LOG_DIR = self.BASE_DIR / "logs"
        
        # Ensure directories exist
        self.DATA_DIR.mkdir(exist_ok=True)
        self.LOG_DIR.mkdir(exist_ok=True)

        # Server Settings
        self.APP_SECRET = os.getenv("JOI_APP_SECRET", "joi-secret-change-me")
        self.PORT = int(os.getenv("JOI_PORT", "5001"))
        self.HOST = os.getenv("JOI_HOST", "0.0.0.0")
        self.DEBUG = os.getenv("JOI_DEBUG", "False").lower() in ("true", "1", "t")

        # Identity
        self.SYSTEM_NAME = "Joi"
        self.USER_NAME = os.getenv("JOI_ADMIN_USER", "Lonnie")

        # Passwords
        self.PASSWORD = os.getenv("JOI_PASSWORD", "joi2049")
        self.ADMIN_PASSWORD = os.getenv("JOI_ADMIN_PASSWORD", "lonnie2049")

        # Limits
        self.MAX_CONTEXT_TOKENS = int(os.getenv("JOI_MAX_CONTEXT_TOKENS", "32000"))
        self.CONTEXT_CACHE_TTL = 3600

        # Logging
        self.LOG_FILE = self.LOG_DIR / "joi_runtime.log"
        self.ERROR_LOG = self.BASE_DIR / "error_log.txt"

    def get(self, key, default=None):
        return getattr(self, key, default)

def is_work_task(user_message: str) -> bool:
    """Classify if a task is work-related (coding, research, etc)."""
    try:
        from modules.joi_router import classify_task
        tt = classify_task(user_message or "").get("task_type", "conversation")
        work_tasks = ("research", "writing", "code_edit", "code_review", "orchestration", "architecture", "math")
        return tt in work_tasks
    except Exception: return False

# Singleton config instance
config = JoiConfig()
