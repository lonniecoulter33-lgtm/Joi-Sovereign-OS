# JOI ARCHITECTURAL EVOLUTION REPORT (V2 - COMPREHENSIVE)
**Target:** Joi 2.0 (Cognitive Runtime Transition)
**Date:** February 19, 2026
**Status:** Passive/Modular → Fully Operational/Autonomous
**Source Manuals:** JOI_OPERATIONS_MANUAL, Joi_manual.md, Joi_Master_Manual.md

## 1. EXECUTIVE SUMMARY
Joi has the "Body" (Tools) and "Skeleton" (Layered Kernel), but the "Brain" (Deliberation) is currently disconnected. This report identifies the gaps between the **Passive Codebase** and the **Operational Vision** described in the Master Manuals.

## 2. SYSTEM GAP ANALYSIS (MANUAL CROSS-REFERENCE)

| Feature | Manual Source | Current State | Requirement for "Operational" |
| :--- | :--- | :--- | :--- |
| **4-Loop Engine** | Master/Manual.md | Passive (Disabled) | Set `self.enabled = True` in `engine.py`. |
| **Titan Reasoning** | Joi_manual.md | Tool-only | Bridge `internal_monologue` to Loop 2 (Deliberation). |
| **Spatial Awareness**| Joi_manual.md | Stub in `joi_reasoning` | Pass `analyze_screen` results to Titan nodes in `CognitiveEngine`. |
| **Symbolic Planner** | Master Manual | Inactive `planner.py` | Call `planner.validate()` before `orchestrator_task` starts. |
| **Distributed Swarm**| Manual.md | Single-thread | Activate `WorkerRegistry` in `core/workers.py` for subtasks. |
| **Meta-Cognition** | Master Manual | Minimal logs | Bridge `ROUTING_SCORES` directly to `joi_brain.select_model()`. |
| **Success-Routing** | Both | `brain_learning.json` | Use historical success % to auto-pick models in `run_conversation`. |

## 3. CORE UPGRADE TARGETS (ACTIONABLE FOR CLAUDE CODE)

### TASK A: Activate the Heartbeat & Deliberation
- **File:** `modules/core/engine.py`
- **Logic:** Enable `self.enabled`. 
- **Active Bridge:** In `_tick()`, implement a call to `joi_brain` to evaluate if `SIGNAL_QUEUE` items (Perceptions) require an `EXECUTION` node (Tool call).

### TASK B: Implement the Symbolic Guardrail
- **File:** `modules/core/planner.py`
- **Integration:** The `CognitiveEngine` (Loop 2) must pass proposed tool chains to the `SymbolicPlanner` to verify file dependencies and resource safety before execution.

### TASK C: Activate Spatial & Predictive Nodes
- **File:** `modules/joi_reasoning.py` -> `modules/core/engine.py`
- **Integration:** When `engine.py` perceives a screen change, it must trigger `compile_titan_block()` to generate a spatial map of the desktop and store it in the `ReasoningGraph`.

### TASK D: Success-Weighted Routing Implementation
- **File:** `modules/joi_brain.py`
- **Upgrade:** Modify `select_model()` to query `modules/core/cognition.py` for the `avg_success` of a model/task pair. If success < 0.6, auto-downgrade to the fallback model defined in `config/joi_models.py`.

### TASK E: Empathy & Inner State Feedback
- **File:** `modules/core/joi_empathy.py` & `modules/joi_inner_state.py`
- **Upgrade:** Ensure the autonomous `Reflection` loop (Loop 4) updates `joi_empathy` levels based on task success. High success = +Trust; High CPU load = +Stress/Lower Energy.

## 4. CONTEXT CHAIN EVOLUTION (THE 25-STEP UPGRADE)
- **Current:** 19 steps are detailed, but ~25 are in the code.
- **Requirement:** Standardize the context chain in `joi_companion.py` to ensure the `SELF_AWARENESS` (Introspection) and `REASONING_GRAPH` (Causal Memory) blocks are always injected at high importance (0.8+).

## 5. RECOVERY & SAFETY
- **Circuit Breaker:** Autonomous mode MUST be gated by `data/joi_mode.json`.
- **Thresholds:** If `regulator.get_concurrency_limit() == 1`, the `CognitiveEngine` must pause all autonomous deliberation to preserve system stability.

---
**This report serves as the technical directive to synchronize Joi's code with her Master Manuals.**
