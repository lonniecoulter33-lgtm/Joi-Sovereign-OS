"""
modules/core/engine.py

Layer 2 --- Cognitive Engine: The "Main Loop" of Joi's Mind.
Orchestrates the 4-loop cognition cycle: Perception -> Deliberation -> Execution -> Reflection.
"""
import time
import threading
from modules.core.config import config
from modules.core.cognition import graph, CognitiveNode

class CognitiveEngine:
    def __init__(self):
        self.enabled = False  # Start disabled (Passive Mode)
        self.cycle_interval = 5.0 # Seconds between cognitive ticks
        self._thread = None
        self._running = False

    def enable(self):
        """Enable active cognitive processing."""
        self.enabled = True
        print("  [ENGINE] Cognitive Engine: ENABLED")

    def disable(self):
        """Disable active cognitive processing (Passive Mode)."""
        self.enabled = False
        print("  [ENGINE] Cognitive Engine: DISABLED")

    def start(self):
        """Start the engine thread."""
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._run_loop, name="joi_cognition", daemon=True)
        self._thread.start()
        
        # Register the Reflection Job (Loop 4)
        from modules.core.scheduler import scheduler
        scheduler.register_task("reflection_loop", 300.0, self.reflect_on_recent_logic)
        
        # Subscribe to Event Bus (Phase 7: Event-Driven)
        from modules.core.events import bus
        bus.subscribe("*", self._on_event)

        # Auto-enable after boot completes (all modules need time to register)
        def _delayed_enable():
            time.sleep(10)
            self.enable()
            print("  [ENGINE] Heartbeat auto-enabled (full 4-loop cycle active)")
        threading.Thread(target=_delayed_enable, daemon=True).start()

        print("  [ENGINE] Started Cognitive Loop.")

    def _on_event(self, event):
        """Handle incoming events from the bus (Loop 1: Perception)."""
        if not self.enabled: return

        try:
            graph.add_node(
                "PERCEPTION",
                {"topic": event.topic, "payload": event.payload, "source": event.source},
                session_id=f"evt_{int(event.timestamp)}"
            )

            # Spatial mapping for vision events
            if event.topic in ("vision_update", "screen_change", "desktop_vision"):
                self._process_spatial_event(event)

            # Trigger immediate deliberation for high-priority events
            if event.priority <= 1:
                self._tick()
        except Exception: pass

    def _execute_tool(self, tool_name, tool_args, session_id):
        """Execute a tool via the registry, recording results to graph."""
        try:
            from modules.core.registry import TOOL_EXECUTORS
            executor = TOOL_EXECUTORS.get(tool_name)
            if not executor:
                return {"ok": False, "error": f"Unknown tool: {tool_name}"}
            return executor(**tool_args)
        except Exception as e:
            return {"ok": False, "error": str(e), "source": "engine"}

    def _process_spatial_event(self, event):
        """Extract spatial data from vision events and store in reasoning graph."""
        try:
            payload = event.payload or {}
            description = payload.get("description", "")
            if not description or description == "UNCHANGED":
                return
            graph.add_node(
                "PERCEPTION",
                {"type": "spatial_map", "description": description[:500],
                 "source": event.source, "focus_app": payload.get("focus_app", "unknown")},
                session_id=f"spatial_{int(event.timestamp)}",
                capability_id="spatial_awareness",
                tags=["spatial", "vision"],
            )
        except Exception as e:
            print(f"  [ENGINE] Spatial error: {e}")

    def reflect_on_recent_logic(self):
        """
        LOOP 4 --- REFLECTION: Analyze the Reasoning Graph.
        Called periodically by the scheduler.
        """
        # Phase 8: Meta-Cognitive Auto-Optimization
        try:
            from modules.core.meta_cognition import meta
            meta.run_analysis_cycle()
        except Exception as e:
            print(f"  [ENGINE] Meta-cognition error: {e}")
            
        # 2. Perform Capability Audit (Phase 3: Self-Awareness)
        # (This is now partially subsumed by meta_cognition but kept for redundancy during migration)
        from modules.core.cognition import graph
        from modules.core.registry import log_telemetry
        cap_stats = graph.get_capability_stats()
        for cap in cap_stats:
            if cap['success_rate'] < 0.5:
                # print(f"  [ENGINE] Capability Warning: {cap['capability_id']} has low success rate.")
                log_telemetry("errors", 1)
        
        # 3. Track Learning Velocity (Phase 5: Optimization)
        try:
            from modules.joi_learning import calculate_learning_velocity
            velocity = calculate_learning_velocity()
        except Exception: pass
        
        pass

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=2.0)

    def _run_loop(self):
        """The 4-Loop Cognition Cycle."""
        while self._running:
            if not self.enabled:
                # Still run perception in passive mode to build the graph
                try:
                    self._tick_perception()
                except Exception as e:
                    print(f"  [ENGINE] Perception Fault: {e}")
                
                time.sleep(self.cycle_interval)
                continue

            try:
                self._tick()
            except Exception as e:
                print(f"  [ENGINE] Cognitive Fault: {e}")
            
            time.sleep(self.cycle_interval)

    def _tick_perception(self):
        """LOOP 1: Perception. Poll sensors and record to graph."""
        from modules.core.registry import ACTIVE_SENSORS, SIGNAL_QUEUE
        
        # 1. Gather raw signals from sensors
        for name, sensor in ACTIVE_SENSORS.items():
            try:
                signal = sensor.poll()
                if signal:
                    # Note: sensor.poll should already call push_signal or return data
                    # We handle both patterns for robustness
                    if isinstance(signal, dict):
                        from modules.core.registry import push_signal
                        push_signal(name, signal)
            except Exception as e:
                print(f"  [ENGINE] Sensor '{name}' poll failed: {e}")

        # 2. Drain Signal Queue and record nodes
        while SIGNAL_QUEUE:
            sig = SIGNAL_QUEUE.pop(0)
            graph.add_node(
                "PERCEPTION", 
                {"source": sig["source"], "data": sig["data"]},
                session_id=f"sensory_{int(sig['timestamp'])}"
            )

    def _tick(self):
        """One cognitive cycle: Perception -> Deliberation -> Execution -> Reflection."""
        self._tick_perception()

        session_id = f"auto_{int(time.time())}"

        # 2. DELIBERATION — check if any high-priority signals need action
        from modules.core.registry import SIGNAL_QUEUE
        pending_signals = len(SIGNAL_QUEUE)
        has_work = pending_signals > 0

        if has_work:
            delib_content = {
                "decision": "process_signals",
                "reason": f"{pending_signals} pending signals",
            }
        else:
            delib_content = {"decision": "idle", "reason": "No pending work"}

        d_node = graph.add_node("DELIBERATION", delib_content, session_id=session_id)

        # 3. EXECUTION — route actionable signals through tool system
        exec_results = []
        if has_work:
            while SIGNAL_QUEUE:
                sig = SIGNAL_QUEUE.pop(0)
                source = sig.get("source", "unknown")
                data = sig.get("data", {})
                action_type = data.get("action_type", "info")

                if action_type == "tool_call":
                    result = self._execute_tool(
                        data.get("tool_name", ""),
                        data.get("tool_args", {}),
                        session_id,
                    )
                else:
                    result = {"source": source, "processed": True, "passive": True}

                exec_results.append(result)
                graph.add_node(
                    "EXECUTION",
                    {"action": "process_signal", "source": source, "result": result},
                    parent_id=d_node,
                    session_id=session_id,
                    capability_id=data.get("tool_name"),
                    success_score=1.0 if result.get("ok", result.get("processed")) else 0.0,
                )

        # 4. REFLECTION — evaluate cycle quality
        quality = 1.0 if not exec_results else (0.8 + 0.2 * min(len(exec_results), 5) / 5)
        reflect_content = {
            "cycle_quality": quality,
            "signals_processed": len(exec_results),
            "notes": f"Processed {len(exec_results)} signals" if exec_results else "Idle cycle",
        }
        graph.add_node("REFLECTION", reflect_content, parent_id=d_node, session_id=session_id)

# Singleton
engine = CognitiveEngine()
