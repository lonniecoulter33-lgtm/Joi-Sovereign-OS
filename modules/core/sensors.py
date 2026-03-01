"""
modules/core/sensors.py

Standard Joi Sensors.
Implements foundational environmental monitors.
"""
import time
import os
from typing import Dict, Any, Optional
from modules.core.interfaces import JoiSensor
from modules.core.registry import register_sensor

class TimeSensor(JoiSensor):
    """
    Monitors time-based triggers (hourly ticks, etc).
    """
    def __init__(self):
        self.name = "time_sensor"
        self.description = "Monitors system clock for scheduled events."
        self.last_hour = time.localtime().tm_hour

    def poll(self) -> Optional[Dict[str, Any]]:
        now = time.localtime()
        if now.tm_hour != self.last_hour:
            self.last_hour = now.tm_hour
            
            # Push event to Bus (Phase 7: Event-Driven)
            from modules.core.events import bus
            bus.publish("system.time.hour", {"hour": now.tm_hour}, priority=2)
            
            return {
                "event": "hour_change",
                "hour": now.tm_hour,
                "timestamp": time.time()
            }
        return None

class FileWatcherSensor(JoiSensor):
    """
    Monitors specific files for changes.
    """
    def __init__(self, watch_paths: list):
        self.name = "file_watcher"
        self.description = "Monitors files for modifications."
        self.watch_paths = watch_paths
        self.last_mtimes = {p: self._get_mtime(p) for p in watch_paths}

    def _get_mtime(self, path):
        try:
            return os.path.getmtime(path)
        except OSError:
            return 0

    def poll(self) -> Optional[Dict[str, Any]]:
        changes = []
        for path in self.watch_paths:
            current = self._get_mtime(path)
            if current > self.last_mtimes.get(path, 0):
                self.last_mtimes[path] = current
                changes.append(path)
        
        if changes:
            # Push event to Bus
            from modules.core.events import bus
            bus.publish("system.file.modified", {"paths": changes}, priority=2)
            
            return {
                "event": "files_modified",
                "paths": changes,
                "timestamp": time.time()
            }
        return None

# Register foundational sensors
register_sensor(TimeSensor())
# Pilot: Watch the main error log
from modules.core.config import config
register_sensor(FileWatcherSensor([str(config.LOG_FILE)]))
