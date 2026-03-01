"""
modules/core/scheduler.py

Background Task Scheduler for Joi's Autonomous Runtime.
Manages periodic tasks, delayed execution, and the heartbeat of the system.
"""
import time
import threading
import traceback
from typing import Dict, List, Callable, Any
from dataclasses import dataclass, field

@dataclass
class ScheduledTask:
    id: str
    name: str
    interval: float  # Seconds
    last_run: float
    func: Callable
    args: tuple = field(default_factory=tuple)
    kwargs: Dict = field(default_factory=dict)
    active: bool = True

class JoiScheduler:
    def __init__(self):
        self._tasks: Dict[str, ScheduledTask] = {}
        self._lock = threading.Lock()
        self._running = False
        self._thread = None

    def register_task(self, name: str, interval: float, func: Callable, *args, **kwargs):
        """Register a repeating background task."""
        import uuid
        task_id = str(uuid.uuid4())
        task = ScheduledTask(
            id=task_id,
            name=name,
            interval=interval,
            last_run=time.time(),
            func=func,
            args=args,
            kwargs=kwargs
        )
        with self._lock:
            self._tasks[task_id] = task
        print(f"  [SCHEDULER] Registered task: {name} (every {interval}s)")
        return task_id

    def start(self):
        """Start the scheduler loop."""
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._loop, name="joi_scheduler", daemon=True)
        self._thread.start()
        print(f"  [SCHEDULER] Started background heartbeat.")

    def stop(self):
        """Stop the scheduler."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=2.0)

    def _loop(self):
        """Main scheduler loop."""
        while self._running:
            now = time.time()
            with self._lock:
                tasks_to_run = []
                for task in self._tasks.values():
                    if task.active and (now - task.last_run) >= task.interval:
                        tasks_to_run.append(task)
            
            for task in tasks_to_run:
                try:
                    # Run task safely
                    task.func(*task.args, **task.kwargs)
                    with self._lock:
                        task.last_run = time.time()
                except Exception as e:
                    print(f"  [SCHEDULER] Task '{task.name}' failed: {e}")
                    # traceback.print_exc() # Optional: noisy logs
            
            time.sleep(1.0) # 1Hz heartbeat

# Singleton
scheduler = JoiScheduler()
