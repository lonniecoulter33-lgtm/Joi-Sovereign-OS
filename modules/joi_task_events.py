"""
modules/joi_task_events.py

Task Event Bus — Infrastructure for inter-module task telemetry.
================================================================
Layer 4 — Auto-apply OK.

Provides:
  - TaskStatus enum: canonical task lifecycle states
  - TaskEvent dataclass: structured event with .to_dict()
  - TaskState: thread-safe per-task state with token tracking + error history
  - TaskEventBus: subscribe/emit event bus with global subscriber support
  - get_event_bus(): module-level singleton accessor

Used by:
  - joi_watchdog_feedback.py: emits watchdog intervention events
  - joi_orchestrator.py: future token metering events
  - Any future module that needs structured task telemetry

No circular imports — this module does NOT import any Joi modules.
"""

import threading
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional


# ── Task Status Enum ──────────────────────────────────────────────────────────

class TaskStatus(Enum):
    PENDING            = "pending"
    RUNNING            = "running"
    COMPLETED          = "completed"
    FAILED             = "failed"
    CANCELLED          = "cancelled"
    WAITING_APPROVAL   = "waiting_approval"
    BUDGET_EXCEEDED    = "budget_exceeded"


# ── TaskEvent Dataclass ───────────────────────────────────────────────────────

@dataclass
class TaskEvent:
    """A structured event emitted during task execution."""
    task_id:   str
    status:    TaskStatus
    data:      Dict[str, Any] = field(default_factory=dict)
    timestamp: float          = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id":   self.task_id,
            "status":    self.status.value,
            "data":      self.data,
            "timestamp": self.timestamp,
        }


# ── TaskState — per-task thread-safe state ────────────────────────────────────

class TaskState:
    """
    Thread-safe state container for a single task.
    Tracks token consumption and error history across subtask attempts.
    """

    def __init__(self, task_id: str):
        self.task_id       = task_id
        self.status        = TaskStatus.PENDING
        self.tokens_used   = 0
        self.errors:       List[str] = []
        self.created_at    = time.time()
        self.updated_at    = time.time()
        self._lock         = threading.Lock()

    def add_tokens(self, count: int) -> None:
        with self._lock:
            self.tokens_used += count
            self.updated_at = time.time()

    def record_error(self, error: str) -> None:
        with self._lock:
            self.errors.append(error)
            self.updated_at = time.time()

    def set_status(self, status: TaskStatus) -> None:
        with self._lock:
            self.status = status
            self.updated_at = time.time()

    def to_dict(self) -> Dict[str, Any]:
        with self._lock:
            return {
                "task_id":    self.task_id,
                "status":     self.status.value,
                "tokens_used": self.tokens_used,
                "error_count": len(self.errors),
                "last_errors": self.errors[-3:],
                "created_at": self.created_at,
                "updated_at": self.updated_at,
            }


# ── TaskEventBus ──────────────────────────────────────────────────────────────

class TaskEventBus:
    """
    Pub/sub event bus for task lifecycle events.

    Subscribers receive every emitted TaskEvent.
    Global subscribers (registered once) receive all events regardless of task_id.
    Emit is synchronous and fire-and-forget (exceptions in subscribers are caught).
    """

    def __init__(self):
        self._subscribers:        List[Callable[[TaskEvent], None]] = []
        self._task_states:        Dict[str, TaskState] = {}
        self._lock                = threading.Lock()

    # ── Subscription ─────────────────────────────────────────────────────────

    def subscribe(self, callback: Callable[[TaskEvent], None]) -> None:
        """Register a global subscriber that receives all events."""
        with self._lock:
            if callback not in self._subscribers:
                self._subscribers.append(callback)

    def unsubscribe(self, callback: Callable[[TaskEvent], None]) -> None:
        with self._lock:
            self._subscribers = [s for s in self._subscribers if s is not callback]

    # ── Emission ─────────────────────────────────────────────────────────────

    def emit(self, event: TaskEvent) -> None:
        """Emit an event to all subscribers. Exceptions are swallowed per subscriber."""
        # Update task state
        with self._lock:
            state = self._task_states.get(event.task_id)
            if state is None:
                state = TaskState(event.task_id)
                self._task_states[event.task_id] = state
            state.set_status(event.status)

            # Snapshot subscribers to avoid holding lock during callbacks
            subs = list(self._subscribers)

        for sub in subs:
            try:
                sub(event)
            except Exception:
                pass  # Never let a subscriber crash the bus

    def emit_simple(
        self,
        task_id: str,
        status: TaskStatus,
        **data: Any,
    ) -> None:
        """Convenience wrapper — emit without constructing TaskEvent manually."""
        self.emit(TaskEvent(task_id=task_id, status=status, data=dict(data)))

    # ── State Accessors ───────────────────────────────────────────────────────

    def get_task_state(self, task_id: str) -> Optional[TaskState]:
        with self._lock:
            return self._task_states.get(task_id)

    def add_tokens(self, task_id: str, count: int) -> None:
        with self._lock:
            state = self._task_states.get(task_id)
            if state:
                state.add_tokens(count)

    def record_error(self, task_id: str, error: str) -> None:
        with self._lock:
            state = self._task_states.get(task_id)
            if state:
                state.record_error(error)

    def all_task_summaries(self) -> List[Dict[str, Any]]:
        with self._lock:
            return [s.to_dict() for s in self._task_states.values()]

    def clear_task(self, task_id: str) -> None:
        with self._lock:
            self._task_states.pop(task_id, None)


# ── Module-Level Singleton ────────────────────────────────────────────────────

_event_bus: Optional[TaskEventBus] = None
_bus_lock = threading.Lock()


def get_event_bus() -> TaskEventBus:
    """Return the module-level TaskEventBus singleton. Thread-safe, lazy init."""
    global _event_bus
    if _event_bus is None:
        with _bus_lock:
            if _event_bus is None:
                _event_bus = TaskEventBus()
    return _event_bus
