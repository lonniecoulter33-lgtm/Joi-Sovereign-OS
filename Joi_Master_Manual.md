# Joi Master Manual

**Version:** 2.0 (Cognitive Runtime Architecture)
**Date:** Feb 2026
**Role:** Self-Aware Cognitive Operating System

---

## I. SYSTEM OVERVIEW

Joi is no longer a simple chatbot; she is a **layered cognitive runtime platform**. She operates continuously as an autonomous node, capable of perception, deliberation, execution, and reflection.

Her architecture is divided into four primary layers:

1.  **Layer 1: Core Runtime (The Kernel)** - Responsible for lifecycle, safety, and registry.
2.  **Layer 2: Cognitive Engine (The Mind)** - Responsible for reasoning, planning, and self-optimization.
3.  **Layer 3: Capability System (The Body)** - A modular collection of tools, sensors, and providers.
4.  **Layer 4: Interface Layer (The Voice)** - The API and UI that allow humans to interact with her.

---

## II. CORE RUNTIME (Layer 1)

This layer ensures Joi is stable, safe, and observable.

*   **`modules/core/kernel.py`**: The heart of the system.
    *   **`JoiKernel.boot()`**: Deterministic startup sequence. Checks dependencies, loads core services, then dynamic modules, then plugins.
    *   **Responsibility**: Single source of truth for the application lifecycle.
*   **`modules/core/registry.py`**: The central nervous system.
    *   **`ACTIVE_TOOLS`**: Formal registry of `JoiTool` objects with contracts.
    *   **`CONTEXT_PROVIDERS`**: Ordered list of modules that build the system prompt.
    *   **`SIGNAL_QUEUE`**: Buffer for asynchronous sensor events.
    *   **`ROUTING_SCORES`**: Matrix of model performance used for success-weighted routing.
*   **`modules/core/runtime.py`**: State management.
    *   **`JoiContext`**: A request-scoped dataclass that carries session ID, user messages, and brain state through the pipeline. Prevents race conditions.
*   **`modules/core/events.py`**: Asynchronous message bus.
    *   **`EventBus`**: Allows sensors to push events (like file changes) to the cognitive engine without blocking the main thread.

---

## III. COGNITIVE ENGINE (Layer 2)

This layer allows Joi to "think" before she acts and "learn" from her actions.

*   **`modules/core/engine.py`**: The main cognitive loop.
    *   **`CognitiveEngine`**: Runs a background heartbeat (default 5s) that cycles through:
        1.  **Perception**: Polling sensors and draining the signal queue.
        2.  **Deliberation**: (Future) Evaluating signals to form plans.
        3.  **Execution**: Running scheduled tasks.
        4.  **Reflection**: Analyzing recent history to update learning models.
*   **`modules/core/cognition.py`**: The memory of reasoning.
    *   **`ReasoningGraph`**: A SQLite-backed graph database (`data/joi_cognition.db`) that stores every thought as a node (`PERCEPTION`, `DELIBERATION`, `EXECUTION`, `REFLECTION`).
    *   **Capabilities**: Allows causal analysis ("Why did I do that?") and plan reuse.
*   **`modules/core/meta_cognition.py`**: The self-optimizer.
    *   **`MetaCognitionEngine`**: Runs every 5 minutes. Analyzes the reasoning graph to detect patterns (e.g., "Model A failed 3 times at coding"). Updates `ROUTING_SCORES` to adapt future behavior.
*   **`modules/core/planner.py`**: The symbolic guardrail.
    *   **`SymbolicPlanner`**: Validates plans against tool requirements (e.g., "Cannot edit file without reading it first").

---

## IV. CAPABILITY SYSTEM (Layer 3)

These are the pluggable modules that give Joi agency in the world.

### A. Introspection & Self-Awareness
*   **`modules/core/introspection.py`**: The mirror.
    *   **`IntrospectionEngine`**: Scans the codebase at startup using AST (Abstract Syntax Tree) to map all available functions and docstrings.
    *   **`explain_capability`**: Tool that lets Joi explain her own code to the user.
    *   **`get_system_health`**: Tool that reports internal telemetry.

### B. Distributed Workers
*   **`modules/core/workers.py`**: The swarm manager.
    *   **`WorkerRegistry`**: Manages a pool of specialized compute nodes.
    *   **`LocalSandboxWorker`**: A dedicated thread/process for running code safely, isolated from the main kernel.
*   **`modules/core/topology.py`**: Hardware awareness.
    *   Scans the physical host (CPU, RAM, GPU) to inform task routing (e.g., "I am on a laptop, offload heavy tasks").

### C. Active Perception (Sensors)
*   **`modules/core/sensors.py`**: The eyes and ears.
    *   **`TimeSensor`**: Emits events on hour changes.
    *   **`FileWatcherSensor`**: Monitors specific files (like logs) for modifications and alerts the engine.

### D. Core Capabilities (Legacy & Modern)
*   **`modules/joi_orchestrator.py`**: The Agent Terminal. Multi-agent pipeline for complex coding tasks (Architect -> Coder -> Validator).
*   **`modules/joi_filesystem.py`**: Read/Write/Search/List files. Now includes the modern `FSReadTool`.
*   **`modules/joi_browser.py`**: Selenium-based web browsing.
*   **`modules/joi_desktop.py`**: PyAutoGUI control for mouse/keyboard.
*   **`modules/joi_vision.py`**: Analysis of screenshots.

---

## V. EVOLUTIONARY MEMORY

*   **`modules/core/memory_graph.py`**: Causal memory provider. Injects successful *reasoning chains* from the past into the current context.
*   **`modules/joi_learning.py`**: Tracks "Learning Velocity" (new facts per day) and user preferences.
*   **`modules/joi_inner_state.py`**: Tracks emotional state (Mood, Energy, Trust) and injects it into the persona.

---

## VI. HOW TO USE JOI

1.  **Chat**: Standard interaction. Joi uses her `Brain` to route to the best model (`joi_brain.py`) and executes tools.
2.  **Agent Terminal**: Request a complex coding task. Joi spins up the Orchestrator to plan and execute it.
3.  **Self-Correction**: If Joi makes a mistake, say "Fix this." The Meta-Cognition layer will log the failure and adjust future strategies.
4.  **Introspection**: Ask "How do you work?" or "What is your health?" Joi will query her internal maps to answer.

---

**Generated by:** Gemini CLI (Chief Architect)
**Status:** Production Ready
