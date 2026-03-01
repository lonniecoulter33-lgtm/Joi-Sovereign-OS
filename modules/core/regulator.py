"""
modules/core/regulator.py

Layer 1 --- Core Runtime: Resource Regulator.
Monitors CPU, Memory, and Thread count to ensure Joi doesn't overload the host.
Provides feedback to the Worker Pool to scale concurrency.
"""
import psutil
import time
from typing import Dict, Any
from modules.core.registry import log_telemetry

class ResourceRegulator:
    def __init__(self):
        self.cpu_threshold = 80.0  # %
        self.memory_threshold = 75.0  # %
        self.max_agents_hard_cap = 10
        self.current_load = {"cpu": 0.0, "memory": 0.0}
        self.current_concurrency = 0

    def check_health(self) -> Dict[str, Any]:
        """Scan system resources and update telemetry."""
        self.current_load["cpu"] = psutil.cpu_percent(interval=None)
        self.current_load["memory"] = psutil.virtual_memory().percent
        
        # Sync concurrency from worker pool if available
        try:
            from modules.core.workers import pool
            self.current_concurrency = pool._active_jobs
        except ImportError: pass

        # Log to registry for observability
        log_telemetry("system_load", self.current_load)
        
        return self.current_load

    def get_concurrency_limit(self) -> int:
        """
        Calculate recommended max concurrent agents based on load.
        """
        health = self.check_health()
        
        if health["cpu"] > self.cpu_threshold or health["memory"] > self.memory_threshold:
            # Critical Load: limit to 1 agent or pause
            return 1
        
        if health["cpu"] > 60.0:
            return 3 # Moderate load
            
        return self.max_agents_hard_cap # Healthy

    def should_compress_context(self) -> bool:
        """Heuristic to decide if we should aggressively compress to save RAM/CPU."""
        return self.current_load["memory"] > 65.0

# Singleton
regulator = ResourceRegulator()
