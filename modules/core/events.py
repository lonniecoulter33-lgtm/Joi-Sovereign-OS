"""
modules/core/events.py

Layer 1 --- Core Runtime: Event Bus.
Asynchronous message passing for the Event-Driven Cognition Loop.
Decouples producers (Sensors, API) from consumers (Cognitive Engine).
"""
import queue
import time
import threading
from typing import Dict, Any, Callable, List
from dataclasses import dataclass, field

@dataclass
class JoiEvent:
    topic: str
    payload: Dict[str, Any]
    priority: int = 1  # 0=Critical, 1=High, 2=Normal, 3=Background
    timestamp: float = field(default_factory=time.time)
    source: str = "system"

class EventBus:
    def __init__(self):
        # PriorityQueue stores items as (priority, timestamp, event)
        self._queue = queue.PriorityQueue()
        self._subscribers: Dict[str, List[Callable]] = {}
        self._lock = threading.Lock()
        self._running = False
        self._worker_thread = None

    def publish(self, topic: str, payload: Dict[str, Any], priority: int = 2, source: str = "system"):
        """Push an event to the bus."""
        event = JoiEvent(topic, payload, priority, source=source)
        # Priority tuple: lower number = higher priority
        self._queue.put((priority, event.timestamp, event))
        # print(f"  [BUS] Published: {topic} (pri={priority})")

    def subscribe(self, topic_pattern: str, handler: Callable):
        """Subscribe a handler function to a topic (supports exact match only for now)."""
        with self._lock:
            if topic_pattern not in self._subscribers:
                self._subscribers[topic_pattern] = []
            self._subscribers[topic_pattern].append(handler)

    def start(self):
        """Start the event dispatcher thread."""
        if self._running: return
        self._running = True
        self._worker_thread = threading.Thread(target=self._dispatch_loop, name="joi_event_bus", daemon=True)
        self._worker_thread.start()
        print("  [BUS] Event Bus Online.")

    def stop(self):
        self._running = False
        if self._worker_thread:
            self._worker_thread.join(timeout=1.0)

    def _dispatch_loop(self):
        while self._running:
            try:
                # Blocking get with timeout allows checking _running flag
                _, _, event = self._queue.get(timeout=0.5)
                self._dispatch(event)
                self._queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                print(f"  [BUS] Dispatch error: {e}")

    def _dispatch(self, event: JoiEvent):
        """Route event to subscribers."""
        # Exact match
        handlers = []
        with self._lock:
            handlers.extend(self._subscribers.get(event.topic, []))
            handlers.extend(self._subscribers.get("*", [])) # Wildcard
        
        for handler in handlers:
            try:
                handler(event)
            except Exception as e:
                print(f"  [BUS] Handler failed for {event.topic}: {e}")

# Singleton Bus
bus = EventBus()
