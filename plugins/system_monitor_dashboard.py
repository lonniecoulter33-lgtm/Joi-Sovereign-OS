"""
plugins/system_monitor_dashboard.py

System Monitor Dashboard
Real-time monitoring of Joi's AI activities and Claude Code tasks.

Provides:
- Flask Blueprint with /monitor routes
- Background thread collecting CPU/memory metrics via psutil
- File change detection on modules/, plugins/, config/
- Activity log for API calls, file ops, and Claude Code tasks
- Alert system for resource thresholds and conflicts
"""

import json
import time
import threading
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional
from collections import deque

try:
    import psutil
    HAVE_PSUTIL = True
except ImportError:
    HAVE_PSUTIL = False
    print("    WARNING: psutil not installed - system metrics unavailable (pip install psutil)")

from flask import Blueprint, render_template, jsonify

import joi_companion

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


# ============================================================================
# FLASK BLUEPRINT
# ============================================================================

monitor_bp = Blueprint("monitor", __name__, url_prefix="/monitor",
                       template_folder=str(BASE_DIR / "templates"))


# ============================================================================
# SYSTEM MONITOR CLASS
# ============================================================================

class SystemMonitor:
    def __init__(self):
        self.activity_log: deque = deque(maxlen=100)
        self.metrics: Dict[str, deque] = {
            "cpu_usage": deque(maxlen=60),
            "memory_usage": deque(maxlen=60),
            "api_calls": deque(maxlen=60),
            "file_operations": deque(maxlen=60),
        }
        self.file_watch: Dict[str, float] = {}
        self.monitoring = False
        self.monitor_thread: Optional[threading.Thread] = None
        self._start_time = datetime.now()

    def start_monitoring(self) -> None:
        """Start background monitoring thread"""
        if self.monitoring or not HAVE_PSUTIL:
            return
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()

        # Save uptime marker
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        (DATA_DIR / "uptime.json").write_text(
            json.dumps({"start_time": self._start_time.isoformat()}, indent=2)
        )

    def stop_monitoring(self) -> None:
        """Stop background monitoring"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2)

    def _monitor_loop(self) -> None:
        """Background loop: collect metrics every 5 seconds"""
        while self.monitoring:
            try:
                now = datetime.now().isoformat()

                self.metrics["cpu_usage"].append({
                    "timestamp": now,
                    "value": psutil.cpu_percent(interval=1)
                })

                memory = psutil.virtual_memory()
                self.metrics["memory_usage"].append({
                    "timestamp": now,
                    "value": memory.percent,
                    "used_mb": round(memory.used / (1024 * 1024), 1)
                })

                self._check_file_changes()

                time.sleep(4)  # +1s from cpu_percent(interval=1) = ~5s total
            except Exception as e:
                self.log_activity("error", f"Monitor error: {e}")
                time.sleep(5)

    def _check_file_changes(self) -> None:
        """Detect modifications in critical directories"""
        watch_dirs = ["modules", "plugins", "config"]

        for dir_name in watch_dirs:
            path = BASE_DIR / dir_name
            if not path.exists():
                continue
            for file_path in path.rglob("*.py"):
                try:
                    mtime = file_path.stat().st_mtime
                    key = str(file_path)

                    if key in self.file_watch and self.file_watch[key] != mtime:
                        self.log_activity("file_modified", str(file_path.relative_to(BASE_DIR)))
                        self.metrics["file_operations"].append({
                            "timestamp": datetime.now().isoformat(),
                            "file": str(file_path.relative_to(BASE_DIR)),
                            "action": "modified"
                        })

                    self.file_watch[key] = mtime
                except Exception:
                    pass

    def log_activity(self, activity_type: str, description: str,
                     metadata: Optional[Dict[str, Any]] = None) -> None:
        """Log a system activity event"""
        self.activity_log.append({
            "timestamp": datetime.now().isoformat(),
            "type": activity_type,
            "description": description,
            "metadata": metadata or {}
        })

    def log_api_call(self, provider: str, model: str) -> None:
        """Convenience: log an LLM API call"""
        self.metrics["api_calls"].append({
            "timestamp": datetime.now().isoformat(),
            "provider": provider,
            "model": model
        })
        self.log_activity("api_call", f"{provider} - {model}", {
            "provider": provider, "model": model
        })

    def log_file_operation(self, operation: str, filepath: str) -> None:
        """Convenience: log a file operation"""
        self.metrics["file_operations"].append({
            "timestamp": datetime.now().isoformat(),
            "file": filepath,
            "action": operation
        })
        self.log_activity("file_operation", f"{operation}: {filepath}", {
            "operation": operation, "file": filepath
        })

    def get_dashboard_data(self) -> Dict[str, Any]:
        """Assemble all data for the dashboard UI"""
        # Active AI sessions
        sessions: List[Dict[str, Any]] = []
        session_file = DATA_DIR / "active_sessions.json"
        if session_file.exists():
            try:
                sessions = json.loads(session_file.read_text(encoding="utf-8"))
            except Exception:
                pass

        return {
            "system": {
                "cpu": list(self.metrics["cpu_usage"])[-20:],
                "memory": list(self.metrics["memory_usage"])[-20:],
                "uptime": self._get_uptime()
            },
            "joi": {
                "active_sessions": sessions,
                "api_calls": list(self.metrics["api_calls"])[-20:],
                "file_operations": list(self.metrics["file_operations"])[-10:]
            },
            "activity_log": list(self.activity_log)[-30:],
            "alerts": self._get_active_alerts()
        }

    def _get_uptime(self) -> Dict[str, Any]:
        """Calculate uptime from start time"""
        uptime = datetime.now() - self._start_time
        return {
            "seconds": int(uptime.total_seconds()),
            "formatted": str(uptime).split(".")[0]
        }

    def _get_active_alerts(self) -> List[Dict[str, Any]]:
        """Generate alerts for current conditions"""
        alerts: List[Dict[str, Any]] = []
        now = datetime.now().isoformat()

        # (Claude Code removed — no longer in use)

        if not HAVE_PSUTIL:
            alerts.append({
                "level": "warning",
                "message": "psutil not installed - system metrics unavailable",
                "timestamp": now
            })
            return alerts

        # Resource alerts
        memory = psutil.virtual_memory()
        if memory.percent > 85:
            alerts.append({
                "level": "error",
                "message": f"High memory usage: {memory.percent:.1f}%",
                "timestamp": now
            })

        cpu = psutil.cpu_percent(interval=0.1)
        if cpu > 90:
            alerts.append({
                "level": "warning",
                "message": f"High CPU usage: {cpu:.1f}%",
                "timestamp": now
            })

        return alerts


# ============================================================================
# GLOBAL INSTANCE
# ============================================================================

monitor = SystemMonitor()


# ============================================================================
# FLASK ROUTES
# ============================================================================

@monitor_bp.route("/")
def dashboard():
    """Render dashboard page"""
    return render_template("monitor_dashboard.html")


@monitor_bp.route("/api/data")
def get_data():
    """API endpoint for dashboard data (polled by JS)"""
    return jsonify(monitor.get_dashboard_data())


@monitor_bp.route("/api/activity")
def get_activity():
    """Get recent activity log"""
    return jsonify(list(monitor.activity_log))


# ============================================================================
# SELF-REGISTRATION (runs on import)
# ============================================================================

# Register Blueprint on Joi's Flask app
joi_companion.app.register_blueprint(monitor_bp)

# Start background monitoring
monitor.start_monitoring()
monitor.log_activity("system", "System monitor initialized")

print("    + Monitor dashboard registered at /monitor")
