"""
modules/joi_scheduler.py

Background Task Scheduler for Joi
==================================

Runs periodic tasks in the background:
- AI research monitoring (every 6 hours)
- Market data updates (every 3 hour)
- Investment opportunity scanning (continuous)
- Notification triggers

Uses threading to avoid blocking the main Flask app.
Safe restart/shutdown handling.
"""

from __future__ import annotations

import os
import time
import json
import threading
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Callable
from pathlib import Path

import joi_companion
from flask import jsonify, request as flask_req
from modules.joi_memory import require_user

# ============================================================================
# CONFIGURATION
# ============================================================================

SCHEDULER_CONFIG_FILE = Path("scheduler_config.json")
SCHEDULER_LOG_FILE = Path("scheduler_log.json")
# Default intervals (in seconds)

DEFAULT_INTERVALS = {
    "ai_research": 6 * 3600,        # 6 hours
    "market_update": 2 * 3600,     # 2 hours
    "crypto_scan": 2 * 3600,       # 2 hours
    "stock_scan": 2 * 3600,        # 2 hours
    "notification_check": 1 * 3600 # 1 hour
}

# ============================================================================
# GLOBAL STATE
# ============================================================================

_scheduler_thread: Optional[threading.Thread] = None
_scheduler_running = False
_scheduler_lock = threading.Lock()
_task_registry: Dict[str, Dict[str, Any]] = {}
_last_run_times: Dict[str, float] = {}


# ============================================================================
# CONFIGURATION MANAGEMENT
# ============================================================================

def _load_config() -> Dict[str, Any]:
    """Load scheduler configuration"""
    if not SCHEDULER_CONFIG_FILE.exists():
        default_config = {
            "enabled": True,
            "intervals": DEFAULT_INTERVALS.copy(),
            "tasks_enabled": {
                "ai_research": True,
                "market_update": True,
                "crypto_scan": True,
                "stock_scan": True,
                "notification_check": True,
            }
        }
        _save_config(default_config)
        return default_config
    
    try:
        return json.loads(SCHEDULER_CONFIG_FILE.read_text())
    except:
        return {
            "enabled": True,
            "intervals": DEFAULT_INTERVALS.copy(),
            "tasks_enabled": {}
        }


def _save_config(config: Dict[str, Any]):
    """Save scheduler configuration"""
    SCHEDULER_CONFIG_FILE.write_text(json.dumps(config, indent=2))


def _load_log() -> Dict[str, Any]:
    """Load scheduler execution log"""
    if not SCHEDULER_LOG_FILE.exists():
        default_log = {
            "started_at": time.time(),
            "task_history": [],
            "errors": []
        }
        _save_log(default_log)
        return default_log
    
    try:
        return json.loads(SCHEDULER_LOG_FILE.read_text())
    except:
        return {"started_at": time.time(), "task_history": [], "errors": []}


def _save_log(log: Dict[str, Any]):
    """Save scheduler log"""
    # Keep only last 1000 entries
    if len(log.get("task_history", [])) > 1000:
        log["task_history"] = log["task_history"][-1000:]
    if len(log.get("errors", [])) > 100:
        log["errors"] = log["errors"][-100:]
    
    SCHEDULER_LOG_FILE.write_text(json.dumps(log, indent=2))


def _log_task_run(task_name: str, success: bool, duration: float, result: Any = None, error: Any = None):
    """Log a task execution"""
    log = _load_log()
    
    entry = {
        "task": task_name,
        "timestamp": time.time(),
        "datetime": datetime.now().isoformat(),
        "success": success,
        "duration_seconds": round(duration, 3)
    }
    
    if result is not None:
        entry["result_summary"] = str(result)[:200]
    
    if error is not None:
        entry["error"] = str(error)[:500]
        log["errors"].append(entry)
    
    log["task_history"].append(entry)
    _save_log(log)


# ============================================================================
# TASK REGISTRY
# ============================================================================

def register_scheduled_task(
    task_name: str,
    task_function: Callable,
    interval_seconds: int,
    enabled: bool = True,
    description: str = ""
):
    """
    Register a task to be run on schedule
    
    Args:
        task_name: Unique task identifier
        task_function: Function to call (should accept no args)
        interval_seconds: How often to run (in seconds)
        enabled: Whether task is active
        description: Human-readable description
    """
    with _scheduler_lock:
        _task_registry[task_name] = {
            "function": task_function,
            "interval": interval_seconds,
            "enabled": enabled,
            "description": description,
            "last_run": 0,
            "run_count": 0,
            "error_count": 0
        }


def unregister_task(task_name: str):
    """Remove a task from the schedule"""
    with _scheduler_lock:
        if task_name in _task_registry:
            del _task_registry[task_name]


def enable_task(task_name: str):
    """Enable a scheduled task"""
    with _scheduler_lock:
        if task_name in _task_registry:
            _task_registry[task_name]["enabled"] = True


def disable_task(task_name: str):
    """Disable a scheduled task"""
    with _scheduler_lock:
        if task_name in _task_registry:
            _task_registry[task_name]["enabled"] = False


# ============================================================================
# SCHEDULER CORE
# ============================================================================

def _scheduler_loop():
    """Main scheduler loop - runs in background thread"""
    global _scheduler_running
    
    print("🕐 Scheduler started")
    
    while _scheduler_running:
        try:
            config = _load_config()
            
            if not config.get("enabled", True):
                time.sleep(60)  # Check again in 1 minute
                continue
            
            current_time = time.time()
            
            with _scheduler_lock:
                tasks_to_run = []
                
                for task_name, task_info in _task_registry.items():
                    if not task_info.get("enabled", True):
                        continue
                    
                    last_run = task_info.get("last_run", 0)
                    interval = task_info.get("interval", 3600)
                    
                    if current_time - last_run >= interval:
                        tasks_to_run.append((task_name, task_info))
            
            # Execute tasks outside the lock
            for task_name, task_info in tasks_to_run:
                try:
                    start_time = time.time()
                    result = task_info["function"]()
                    duration = time.time() - start_time
                    
                    with _scheduler_lock:
                        _task_registry[task_name]["last_run"] = start_time
                        _task_registry[task_name]["run_count"] += 1
                    
                    _log_task_run(task_name, True, duration, result)
                    print(f"✅ Scheduler: {task_name} completed in {duration:.2f}s")
                    
                except Exception as e:
                    duration = time.time() - start_time
                    
                    with _scheduler_lock:
                        _task_registry[task_name]["error_count"] += 1
                    
                    _log_task_run(task_name, False, duration, error=str(e))
                    print(f"❌ Scheduler: {task_name} failed: {e}")
            
            # Sleep for a bit before next check
            time.sleep(30)  # Check every 30 seconds
            
        except Exception as e:
            print(f"❌ Scheduler error: {e}")
            time.sleep(60)
    
    print("🕐 Scheduler stopped")


def start_scheduler():
    """Start the background scheduler"""
    global _scheduler_thread, _scheduler_running
    
    if _scheduler_running:
        return {"ok": False, "error": "Scheduler already running"}
    
    _scheduler_running = True
    _scheduler_thread = threading.Thread(target=_scheduler_loop, daemon=True)
    _scheduler_thread.start()
    
    return {"ok": True, "message": "Scheduler started"}


def stop_scheduler():
    """Stop the background scheduler"""
    global _scheduler_running
    
    if not _scheduler_running:
        return {"ok": False, "error": "Scheduler not running"}
    
    _scheduler_running = False
    
    # Wait for thread to finish (with timeout)
    if _scheduler_thread:
        _scheduler_thread.join(timeout=5.0)
    
    return {"ok": True, "message": "Scheduler stopped"}


def get_scheduler_status() -> Dict[str, Any]:
    """Get current scheduler status"""
    config = _load_config()
    log = _load_log()
    
    with _scheduler_lock:
        tasks_status = []
        for task_name, task_info in _task_registry.items():
            tasks_status.append({
                "name": task_name,
                "description": task_info.get("description", ""),
                "enabled": task_info.get("enabled", True),
                "interval_seconds": task_info.get("interval", 0),
                "last_run": task_info.get("last_run", 0),
                "last_run_datetime": datetime.fromtimestamp(task_info.get("last_run", 0)).isoformat() if task_info.get("last_run", 0) > 0 else None,
                "next_run": task_info.get("last_run", 0) + task_info.get("interval", 0),
                "next_run_datetime": datetime.fromtimestamp(task_info.get("last_run", 0) + task_info.get("interval", 0)).isoformat() if task_info.get("last_run", 0) > 0 else None,
                "run_count": task_info.get("run_count", 0),
                "error_count": task_info.get("error_count", 0)
            })
    
    return {
        "ok": True,
        "running": _scheduler_running,
        "config": config,
        "uptime_seconds": time.time() - log.get("started_at", time.time()),
        "tasks": tasks_status,
        "recent_errors": log.get("errors", [])[-10:],
        "recent_runs": log.get("task_history", [])[-20:]
    }


# ============================================================================
# SCHEDULED TASK IMPLEMENTATIONS
# ============================================================================

def _task_ai_research():
    """Scheduled: Check for AI research updates"""
    try:
        from modules import joi_evolution
        result = joi_evolution.monitor_ai_research({"force": False})
        return f"AI research check: {result.get('status', 'unknown')}"
    except Exception as e:
        return f"AI research check failed: {e}"


def _task_market_update():
    """Scheduled: Update market data"""
    try:
        from modules import joi_market
        result = joi_market.update_all_market_data()
        return f"Market update: {result.get('status', 'unknown')}"
    except Exception as e:
        return f"Market update failed: {e}"


def _task_crypto_scan():
    """Scheduled: Scan for crypto opportunities"""
    try:
        from modules import joi_market
        result = joi_market.scan_crypto_opportunities()
        return f"Crypto scan: {result.get('opportunities_found', 0)} opportunities"
    except Exception as e:
        return f"Crypto scan failed: {e}"


def _task_stock_scan():
    """Scheduled: Scan for stock opportunities"""
    try:
        from modules import joi_market
        result = joi_market.scan_stock_opportunities()
        return f"Stock scan: {result.get('opportunities_found', 0)} opportunities"
    except Exception as e:
        return f"Stock scan failed: {e}"


def _task_notification_check():
    """Scheduled: Check for notification triggers"""
    try:
        from modules import joi_market
        result = joi_market.check_notification_triggers()
        return f"Notifications: {result.get('sent', 0)} sent"
    except Exception as e:
        return f"Notification check failed: {e}"


# ============================================================================
# TOOLS FOR LLM
# ============================================================================

def scheduler_control(**params) -> Dict[str, Any]:
    """
    Tool: Control the scheduler
    
    Actions: start, stop, status, enable_task, disable_task
    """
    require_user()
    
    action = params.get("action")
    
    if action == "start":
        return start_scheduler()
    elif action == "stop":
        return stop_scheduler()
    elif action == "status":
        return get_scheduler_status()
    elif action == "enable_task":
        task_name = params.get("task_name")
        if not task_name:
            return {"ok": False, "error": "task_name required"}
        enable_task(task_name)
        return {"ok": True, "message": f"Task {task_name} enabled"}
    elif action == "disable_task":
        task_name = params.get("task_name")
        if not task_name:
            return {"ok": False, "error": "task_name required"}
        disable_task(task_name)
        return {"ok": True, "message": f"Task {task_name} disabled"}
    else:
        return {"ok": False, "error": f"Unknown action: {action}"}


def configure_scheduler(**params) -> Dict[str, Any]:
    """
    Tool: Configure scheduler intervals and settings
    """
    require_user()
    
    config = _load_config()
    
    if "intervals" in params:
        config["intervals"].update(params["intervals"])
    
    if "tasks_enabled" in params:
        config["tasks_enabled"].update(params["tasks_enabled"])
    
    _save_config(config)
    
    return {
        "ok": True,
        "message": "Scheduler configuration updated",
        "config": config
    }


# ============================================================================
# TOOL REGISTRATION
# ============================================================================

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "scheduler_control",
        "description": "Control the background scheduler: start, stop, check status, enable/disable tasks",
        "parameters": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["start", "stop", "status", "enable_task", "disable_task"],
                    "description": "Action to perform"
                },
                "task_name": {
                    "type": "string",
                    "description": "Task name (required for enable_task/disable_task)"
                }
            },
            "required": ["action"]
        }
    }},
    scheduler_control
)

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "configure_scheduler",
        "description": "Configure scheduler task intervals and settings",
        "parameters": {
            "type": "object",
            "properties": {
                "intervals": {
                    "type": "object",
                    "description": "Task intervals in seconds: ai_research, market_update, crypto_scan, stock_scan, notification_check"
                },
                "tasks_enabled": {
                    "type": "object",
                    "description": "Enable/disable specific tasks"
                }
            }
        }
    }},
    configure_scheduler
)


# ============================================================================
# FLASK ROUTES
# ============================================================================

def scheduler_route():
    """GET scheduler status or POST control action"""
    require_user()
    
    if flask_req.method == "GET":
        return jsonify(get_scheduler_status())
    
    data = flask_req.get_json(silent=True) or {}
    
    if "action" in data:
        return jsonify(scheduler_control(data))
    else:
        return jsonify(configure_scheduler(data))


joi_companion.register_route("/scheduler", ["GET", "POST"], scheduler_route, "scheduler_route")


# ============================================================================
# AUTO-START & TASK REGISTRATION
# ============================================================================

def _initialize_scheduler():
    """Initialize scheduler with default tasks"""
    config = _load_config()
    intervals = config.get("intervals", DEFAULT_INTERVALS)
    tasks_enabled = config.get("tasks_enabled", {})
    
    # Register all tasks
    register_scheduled_task(
        "ai_research",
        _task_ai_research,
        intervals.get("ai_research", DEFAULT_INTERVALS["ai_research"]),
        tasks_enabled.get("ai_research", True),
        "Monitor AI research and advancements"
    )
    
    register_scheduled_task(
        "market_update",
        _task_market_update,
        intervals.get("market_update", DEFAULT_INTERVALS["market_update"]),
        tasks_enabled.get("market_update", True),
        "Update crypto and stock market data"
    )
    
    register_scheduled_task(
        "crypto_scan",
        _task_crypto_scan,
        intervals.get("crypto_scan", DEFAULT_INTERVALS["crypto_scan"]),
        tasks_enabled.get("crypto_scan", True),
        "Scan for cryptocurrency trading opportunities"
    )
    
    register_scheduled_task(
        "stock_scan",
        _task_stock_scan,
        intervals.get("stock_scan", DEFAULT_INTERVALS["stock_scan"]),
        tasks_enabled.get("stock_scan", True),
        "Scan for stock trading opportunities"
    )
    
    register_scheduled_task(
        "notification_check",
        _task_notification_check,
        intervals.get("notification_check", DEFAULT_INTERVALS["notification_check"]),
        tasks_enabled.get("notification_check", True),
        "Check for price alerts and send notifications"
    )
    
    # Auto-start if enabled
    if config.get("enabled", True):
        start_scheduler()


# Initialize on module load
_initialize_scheduler()
