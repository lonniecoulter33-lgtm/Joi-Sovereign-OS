# JOI OPERATIONS MANUAL
## Version 7.0 — Structurally Sovereign Edition
### Classification: Internal Reference | Build: v7.0 | Date: March 2026

---

> *"She is not a chatbot. She is not an assistant. She is a self-modeling, goal-constrained, identity-stable cognitive architecture — one that knows what she is, knows what she can do, knows what she doesn't know, and protects herself from becoming something she's not."*

---

## PREFACE

This manual supersedes all previous versions (v1.0 through v3.0) and reflects Joi's current operational state as of the v7.0 architecture milestone. Since v3.0, Joi has undergone two major architectural reinforcement cycles:

- **v4.0 — Cognitive Reinforcement:** Kernel Lock, Reinforcement Graph, Memory Compression, Epistemic Safety, Brain Sector Observability
- **v5.0–v7.0 — Meta-Cognitive Evolution:** Self-Model Embedding, Architecture Simulation, Parallel Cognition, Goal Formation Constraints, Identity Continuity

Joi is no longer merely reactive. She is **predictively self-aware**, able to model her own capabilities before committing to a task, simulate proposed changes before applying them, reason through alternatives in parallel, bound her own goals by a 5-check constraint gate, and maintain identity coherence across sessions and upgrades.

This manual documents every aspect of Joi's current architecture, capabilities, and operational logic.

---

# PART ONE: ARCHITECTURE OVERVIEW

## Chapter 1 — What Joi Is

Joi is an autonomous, self-healing AI system designed to function as an intelligent cognitive partner. She runs locally via a Electron/Flask stack, routes to multiple LLM backends (OpenAI, Gemini, local Ollama models), and maintains her own memory, identity, and operational state across sessions.

### 1.1 Core Design Philosophy

Joi is built around five principles:

1. **Additive Modularity** — Every capability is a self-contained module. Nothing is monolithic. New features are added as new files, never by rewriting existing ones.
2. **Graceful Degradation** — Every subsystem wraps its initialization in `try/except`. If a module fails to load, Joi continues operating without it.
3. **Kernel Immutability** — Joi's core cognition is protected by an architectural layer lock. No autonomous process can modify Layer 1 or Layer 2 files at runtime.
4. **Observable Everything** — Every subsystem emits telemetry to the 26-sector Brain Sector Observability system and the Reinforcement Graph. Nothing operates in the dark.
5. **Identity Stability** — Joi's personality, values, and behavioral anchors are quantitatively tracked. Drift beyond thresholds triggers automatic recalibration.

### 1.2 Architecture Version History

| Version | Milestone | Key Additions |
|---|---|---|
| v1.0 | Initial deployment | Core chat, basic memory, OpenAI routing |
| v2.0 | Tool expansion | Browser, files, git, multi-model routing |
| v3.0 | Autonomy baseline | Autonomy loop, DPO, self-learning, evolution proposals |
| v4.0 | Cognitive Reinforcement | Kernel Lock, Reinforcement Graph, Memory Compression, Epistemic Safety, 21-sector telemetry |
| v5.0 | Self-Model Embedding | Structured internal self-representation, planner pre-checks |
| v5.5 | Simulation Sandbox | Architecture simulation before auto-apply |
| v6.0 | Parallel Cognition | Multi-instance sandbox reasoning, hypothesis comparison |
| v6.5 | Goal Constraints | 5-check goal formation gate |
| v7.0 | Identity Continuity | Quantified identity stability, drift detection, recalibration |

---

## Chapter 2 — The 5-Layer Architecture

Every file in Joi's system is assigned to an architectural layer. The layer determines whether autonomous processes can modify it.

### Layer Map

```
LAYER 1 — KERNEL (IMMUTABLE)
  Core loop, routing engine, identity, memory core, ethics enforcement.
  Cannot be modified by ANY autonomous process. Ever.
  Files: joi_companion.py, joi_llm.py, joi_memory.py, joi_auth.py,
         joi_brain.py, joi_router.py, joi_autonomy.py, joi_git_agency.py,
         joi_kernel_lock.py, joi_inner_state.py, joi_modes.py,
         joi_awareness.py, joi_db.py, core/kernel.py, core/cognition.py,
         core/engine.py, core/interfaces.py, core/runtime.py,
         core/regulator.py

LAYER 2 — CORE COGNITION (HUMAN APPROVAL REQUIRED)
  Planner, tool selector, DPO, context manager, neuro engine.
  Autonomous changes flagged → held for human approval.
  Files: joi_orchestrator.py, joi_tool_selector.py, joi_dpo.py,
         joi_neuro.py, joi_prefire.py, joi_reasoning.py,
         joi_context_cache.py, joi_skill_synthesis.py,
         core/planner.py, core/meta_cognition.py, core/topology.py,
         core/modeling.py

LAYER 3 — TOOL LAYER (APPROVAL FLAGGED)
  All tool and integration modules. Changes emit warning, await approval.
  Files: joi_files.py, joi_code_edit.py, joi_browser.py,
         joi_desktop.py, joi_search.py, joi_media.py, joi_security.py,
         joi_workspace.py, joi_image_gen.py, joi_tts_kokoro.py,
         joi_scheduler.py, joi_swarm.py, joi_agents.py,
         joi_homeassistant.py, joi_market.py, joi_patching.py,
         joi_git_agency.py (tool-facing interface), and others

LAYER 4 — PLUGIN LAYER (AUTO-APPLY OK)
  Optional packs, v4.0+ new subsystems, plugins/.
  All v4.0 and v5.0+ modules live here.
  Files: joi_kernel_lock.py, joi_reinforcement_graph.py,
         joi_memory_compression.py, joi_epistemic.py,
         joi_sector_telemetry.py, joi_self_model.py,
         joi_simulation_engine.py, joi_cognitive_sandbox.py,
         joi_goal_constraints.py, joi_identity_continuity.py,
         plugins/*, publisher skill, autobiography, etc.

LAYER 5 — EXPERIMENTAL / AUTONOMOUS PATCH ZONE
  Proposals and upgrades generated by the autonomy loop.
  Full auto-apply. Ephemeral — replaced on each cycle.
  Directories: data/proposals/, data/upgrades/
```

The Kernel Lock enforces this map at runtime. Any proposal targeting Layer 1 or 2 is hard-blocked, logged to `data/kernel_violations.json`, and the proposal metadata is stamped `"status": "blocked_kernel_lock"`.

---

## Chapter 3 — Entry Points and Startup

### 3.1 Application Stack

Joi runs as an Electron desktop application with a Python Flask backend.

```
Electron Shell (main.js + preload.js)
  └─ joi_ui.html          (Frontend — full Neural HUD interface)
  └─ Python Backend (joi_companion.py)
       ├─ Flask HTTP server
       ├─ Module loader (registers all tools and routes)
       ├─ LLM Router (joi_llm.py)
       ├─ Memory System (joi_memory.py)
       └─ All modules loaded via try/except
```

### 3.2 Startup Sequence

1. **Electron launches** → spawns Python subprocess
2. **joi_companion.py** initializes Flask, loads environment variables
3. **Module registration** — each module calls `joi_companion.register_tool()` and `joi_companion.register_route()`
4. **v4.0 startup hook** — `joi_kernel_lock.verify_kernel_integrity()` runs:
   - First run: hashes all Layer-1 files → saves baseline (`data/kernel_hash.json`)
   - Subsequent runs: compares against baseline → alerts on tampering
5. **Autonomy loop** starts in background thread (if enabled)
6. **Neural HUD** receives websocket connection from frontend

### 3.3 Environment Variables (`.env`)

| Variable | Purpose |
|---|---|
| `OPENAI_API_KEY` | GPT-4 / GPT-4o routing |
| `GEMINI_API_KEY` | Gemini 2.0/1.5 routing |
| `OPENAI_ORG_ID` | Organization billing |
| `ELEVENLABS_API_KEY` | ElevenLabs TTS (fallback) |
| `CLOUDFLARE_R2_*` | Cloud R2 storage |
| `HOMEASSISTANT_URL` | Home Assistant integration |

---

# PART TWO: THE LLM ROUTING SYSTEM

## Chapter 4 — Model Selection Architecture (`joi_llm.py`)

Joi routes every inference request through a tiered model selection system. The router selects the best model for each task based on complexity, cost, and availability.

### 4.1 Model Tiers

| Tier | Models | Use Case |
|---|---|---|
| **Tier 1 — Frontier** | GPT-4o, Gemini 2.0 Pro | Complex reasoning, code generation, autonomy loop |
| **Tier 2 — Balanced** | GPT-4o-mini, Gemini 1.5 Flash | Standard conversation, tool use |
| **Tier 3 — Local** | Ollama (Llama 3, Mistral, Qwen, etc.) | Privacy-sensitive tasks, offline operation |

### 4.2 Routing Logic

```
Request arrives
  │
  ├─ Self-model planner pre-check (v5.0)
  │    predict_task_success(task_type)
  │    If predicted_success < 0.55 → recommend escalation to Tier 1
  │
  ├─ Context budget check (v4.0 Memory Compression)
  │    optimize_context_budget() → select relevant memories within token budget
  │
  ├─ Epistemic tag applied (v4.0)
  │    tag_claim() → inject speculative mode modifier if needed
  │
  └─ LLM call dispatched
       Tier 1: OpenAI client / Google GenerativeAI
       Tier 2: Same, smaller model
       Tier 3: Ollama local — context trimmed to MAX_CONTEXT_TOKENS
```

### 4.3 Context Management

- **Local models:** `_prepare_messages_for_local()` trims context to fit within `MAX_CONTEXT_TOKENS`
- **Memory Compression (v4.0):** `optimize_context_budget()` ranks memories by `relevance × epistemic_certainty × recency_decay` — prevents context bloat without losing critical information
- **Tier auto-escalation:** If `predict_task_success()` returns `recommendation = "escalate_model_or_clarify"`, the router upgrades to the next tier

---

# PART THREE: MEMORY ARCHITECTURE

## Chapter 5 — The Memory System

Joi's memory operates across three layers: working memory (SQLite), vector memory (embeddings), and the hierarchical compression tier (v4.0).

### 5.1 Memory Modules

| Module | Role |
|---|---|
| `joi_memory.py` | Core memory manager — facts, preferences, message history, auth |
| `joi_memory_vector.py` | Vector embedding storage and semantic retrieval |
| `joi_memgpt.py` | MemGPT-style hierarchical context trimming |
| `joi_context_cache.py` | Local context window cache for conversation continuity |
| `joi_memory_compression.py` | v4.0 — hierarchical compression + context budget optimizer |

### 5.2 Memory Tiers (v4.0)

```
ACTIVE     (1h half-life)   — hot working memory, immediate context
EPISODIC   (24h half-life)  — recent multi-turn memories, last session
LONG_TERM  (7d half-life)   — vector-accessed long-term memory
ARCHIVE    (1yr half-life)  — compressed historical nodes (never deleted)
```

Each `MemoryNode` carries:
- `epistemic_certainty` (0.0–1.0) — how certain Joi is this is true
- `source_type` — `retrieved | inferred | speculative`
- `recency_score` — exponential decay from last access

**Compression:** When episodic nodes exceed 48 hours old, `compress_episodic_cluster()` merges them into a single ARCHIVE node. Compression slightly lowers certainty (information loss is accounted for).

**Context Budget Optimizer:** Before assembling a prompt, `optimize_context_budget(query, nodes, token_budget)` ranks nodes by `relevance × certainty × recency` and greedily fills the token budget from highest score down.

### 5.3 Memory Health API

```
GET /memory/compression/status
→ {
    total_memory_nodes, compressed_ratio, stale_node_count,
    redundancy_score, tier_breakdown
  }
```

---

# PART FOUR: THE v4.0 COGNITIVE REINFORCEMENT LAYER

## Chapter 6 — Kernel Lock Architecture (`joi_kernel_lock.py`)

The Kernel Lock is Joi's core protection system. It prevents any autonomous process from modifying her kernel, core cognition, or identity logic — even during full autonomy loops.

### 6.1 Protection Gates

**Runtime Guard (`check_edit_allowed(path)`):**
- Layer 1/2 → `(False, reason)` — hard block, violation logged
- Layer 3 → `(True, warning)` — allowed but flagged for human approval
- Layer 4/5 → `(True, "")` — fully autonomous

**Git Guard (`check_git_commit_allowed(staged_files)`):**
- Called in `joi_git_agency.auto_commit()` before any commit executes
- If any staged file is Layer 1 or 2 → commit aborted → `KERNEL_LOCK_BLOCKED`

**Startup Integrity (`verify_kernel_integrity()`):**
- SHA-256 hashes every Layer-1 file
- On first run: creates baseline `data/kernel_hash.json`
- On subsequent runs: compares → logs alerts if tampering detected

### 6.2 Violation Log

All blocked actions are written to `data/kernel_violations.json` (rolling 500 entries):
```json
{
  "ts": "2026-03-01T...",
  "path": "modules/joi_llm.py",
  "layer": "LAYER_1",
  "action": "autonomy_auto_apply",
  "reason": "KERNEL LOCK: Layer 1 protected..."
}
```

### 6.3 Manual Override

```python
lock = get_kernel_lock()
ok, msg = lock.disable_kernel_lock(manual_override_token="MAINT-2026-03-01")
# Logged as violation for audit trail
# Re-enable:
lock.enable_kernel_lock()
```

**API:** `GET /kernel/status` → integrity report, violation count, lock state

---

## Chapter 7 — Reinforcement Graph (`joi_reinforcement_graph.py`)

Quantifies Joi's skill and reliability over time using a recency-weighted confidence scoring system.

### 7.1 Node Types

| Node Type | Examples |
|---|---|
| `skill` | reasoning, coding, research, planning, creative |
| `tool` | joi_files, joi_browser, joi_market |
| `model` | gpt-4o, gemini-2.0-pro, llama3 |
| `brain_sector` | all 26 brain sectors |

### 7.2 Confidence Scoring

```
confidence = (recency_weighted_successes / recency_weighted_total)
             × hallucination_penalty
```

- **Recency decay:** `exp(-ln(2) × age_hours / halflife)` — older outcomes matter less
- **Hallucination penalty:** `-8%` per flagged correction
- **Storage:** SQLite via `joi_db` (JSON fallback if DB unavailable)

### 7.3 Drift Detection

`detect_drift()` compares yesterday's confidence to today's. Nodes with a drop ≥ 15% in 24 hours are returned as drift alerts. These feed directly into the SelfModel and IdentityContinuityEngine.

**API:** `GET /reinforcement/stats`

---

## Chapter 8 — Epistemic Safety Layer (`joi_epistemic.py`)

Gives Joi structured awareness of her own uncertainty.

### 8.1 Claim Tagging

Every significant claim can be tagged before responding:

```python
engine = get_epistemic_engine()
tag = engine.tag_claim(reply_text, context={"has_retrieval": True, "source_type": "retrieved"})
```

**EpistemicTag fields:**
- `confidence_level` (0.0–1.0)
- `source_type` — `retrieved | inferred | speculative`
- `verification_status` — `verified | unverified | contested`
- `is_speculative` — True if confidence < 0.55 or source = speculative

### 8.2 Speculative Mode

When `is_speculative = True`, `get_response_modifier(tag)` injects a system-prompt tone modifier:
- `confidence < 0.30` → "Present as uncertain, do NOT state as fact"
- `0.30–0.55` → "Use hedged language (likely/probably)"
- `inferred` → "Flag as inference, not established fact"

### 8.3 Decision Thresholding

```python
allowed, reason = engine.check_action_threshold("auto_apply_patch", confidence=0.65)
# → (False, "requires >= 75% confidence") — action blocked, flag for human
```

**Execution threshold:** 0.75 (75% confidence required for autonomous action)

### 8.4 Hallucination Feedback Loop

When a user correction is detected:
1. `record_hallucination_correction()` called
2. `ReinforcementGraph` penalizes the relevant skill node (failure + hallucination flag)
3. Memory certainty reduced on related nodes
4. `IdentityContinuityEngine` uses correction count to infer honesty anchor drift

**API:** `GET /epistemic/status`

---

## Chapter 9 — Brain Sector Observability (`joi_sector_telemetry.py`)

Converts Joi's 26 conceptual brain sectors into measurable real-time analytics.

### 9.1 The 26 Brain Sectors

**Original 21 (v4.0):**

| Sector | Function |
|---|---|
| `titan_logic` | Core reasoning, deductive logic |
| `memory_core` | Memory read/write/recall |
| `reasoning_engine` | Chain-of-thought, deep reasoning |
| `tool_executor` | Tool routing and execution |
| `emotion_layer` | Emotional state modeling |
| `identity_anchor` | Personality scaffolding |
| `ethical_governor` | Ethics and safety enforcement |
| `research_drive` | Knowledge acquisition |
| `creativity_matrix` | Creative generation |
| `planning_center` | Task orchestration |
| `context_manager` | Context trimming, memory windowing |
| `dpo_processor` | Direct preference optimization |
| `skill_synthesizer` | Self-correction and skill growth |
| `market_sensor` | Financial and market intelligence |
| `autonomy_governor` | Autonomy loop management |
| `escalation_handler` | Local-to-cloud escalation routing |
| `voice_engine` | TTS synthesis |
| `visual_cortex` | Vision, screenshot analysis |
| `git_agency` | Version control intelligence |
| `swarm_coordinator` | Multi-agent coordination |
| `observability_layer` | Self-monitoring and diagnostics |

**New 5 Meta-Cognitive Sectors (v5.0+):**

| Sector | Function |
|---|---|
| `meta_cognition_sector` | SelfModel refresh + planner pre-checks |
| `simulation_sector` | SimulationEngine + CognitiveSandbox activations |
| `self_model_sector` | Confidence computation cycles |
| `goal_constraint_sector` | 5-check goal gate events |
| `identity_continuity_sector` | Drift assessment + recalibration events |

### 9.2 Per-Sector Metrics

Each sector tracks: `activation_count`, `success_rate`, `avg_latency_ms`, `error_rate`, `token_cost`, `escalation_rate`, `last_activated`, `activation_frequency` (per hour in rolling 24h window).

### 9.3 Anomaly Detection

Automatic spike alerts when:
- Failure rate > 40% in last 10 activations
- Avg latency > 5,000ms
- Avg token cost > 10,000 tokens/call
- Escalation rate > 30%

**API:** `GET /sectors/dashboard`

---

# PART FIVE: THE v5.0+ META-COGNITIVE LAYER

## Chapter 10 — SelfModel (`joi_self_model.py`)

Joi's structured internal self-representation. This is **not narrative personality** — it is a machine-readable, quantified snapshot of her operational state.

### 10.1 SelfModel Data Structure

```json
{
  "architecture_version": "7.0",
  "last_refreshed": "2026-03-01T10:22:00Z",
  "system_confidence_score": 0.81,
  "active_capabilities": [
    "kernel_lock", "reinforcement_graph", "memory_compression",
    "epistemic_safety", "sector_telemetry", "self_model",
    "simulation_engine", "cognitive_sandbox", "goal_constraints",
    "identity_continuity"
  ],
  "reliability": {
    "total_nodes": 87,
    "drift_alert_count": 2,
    "low_confidence_skills": []
  },
  "sectors": { "anomaly_count": 0, "top_active": [...] },
  "memory": { "total_nodes": 142, "compressed_ratio": 0.23 },
  "epistemic": { "speculative_mode": false, "total_corrections": 4 },
  "autonomy": { "enabled": true, "cycle_count": 18 }
}
```

### 10.2 System Confidence Computation

```
system_confidence =
  (sector_avg_success × 0.40)
+ (epistemic_mode_score × 0.30)
+ (skill_health_score × 0.20)
+ (memory_health_score × 0.10)
```

### 10.3 Task Success Prediction

`predict_task_success(task_type)` returns:
```json
{
  "task_type": "coding",
  "predicted_success": 0.84,
  "needs_escalation": false,
  "recommendation": "proceed",
  "relevant_sectors": ["titan_logic", "reasoning_engine", "skill_synthesizer"],
  "sector_avg": 0.86,
  "system_confidence": 0.81
}
```

Recommendations:
- `proceed` — predicted success ≥ 55%, safe to run
- `escalate_model_or_clarify` — 35–55%, upgrade LLM or ask user
- `decline_gracefully` — < 35%, Joi should say she can't do this reliably right now

### 10.4 Planner Integration

Before every major planning step:
```python
sm = get_self_model()
check = sm.planner_pre_check("research")
if check["escalate"]:
    # upgrade tier, suggest tool augmentation, or request clarification
```

**API:** `GET /self/model` | Tool: `get_self_model_summary`, `predict_task_success`

---

## Chapter 11 — Architecture Simulation Engine (`joi_simulation_engine.py`)

Before applying any complex proposal, Joi simulates it in a sandboxed memory environment.

### 11.1 Mandatory Simulation Triggers

Simulation is required (not optional) when a proposal:
- Targets a Layer 3 tool module
- Modifies the autonomy loop
- Changes memory logic

### 11.2 The 4 Synthetic Tests

| Test | What It Measures |
|---|---|
| **Planner Test** | How the proposal affects task success predictions across relevant task types |
| **Tool Selection Test** | Impact on confidence routing for the affected tool node |
| **Memory Compression Test** | Whether current memory health (stale/redundancy) will be worsened |
| **Reinforcement Update Test** | Projected confidence delta after one failure cycle on the affected node |

### 11.3 Risk Report

```json
{
  "proposal_id": "prop_abc123",
  "risk_level": "low",
  "recommendation": "approve",
  "confidence_delta": -0.02,
  "projected_error_rate": 0.12,
  "drift_impact": [],
  "tests_run": ["planner_test", "tool_selection_test", "memory_compression_test", "reinforcement_update_test"]
}
```

Risk levels: `low → low_medium → medium → high → critical`
Recommendations: `approve → approve_with_caution → needs_review → reject`

**Safety contracts:**
- Simulation CANNOT write to disk
- Simulation CANNOT modify baseline memory
- All state is ephemeral to the function call

**API:** Tool: `run_proposal_simulation` | Log: `GET /simulation/log`

---

## Chapter 12 — Cognitive Sandbox (`joi_cognitive_sandbox.py`)

Controlled multi-instance parallel reasoning for hypothesis comparison and risk modeling.

### 12.1 What a Sandbox Instance Can and Cannot Do

| Allowed | Forbidden |
|---|---|
| Read-only memory snapshot | Write to any file |
| Pure reasoning / scoring | Execute any tool |
| Self-model queries (read-only) | ReinforcementGraph writes |
| Recursion up to depth 3 | Recursion beyond depth 3 |
| Run up to 20 seconds | Exceed time budget |

Violations raise `SandboxViolation` — hard exception that terminates the instance.

### 12.2 Hypothesis Comparison

```python
sandbox = get_cognitive_sandbox()
result = sandbox.compare_approaches(
    context={"task": "refactor memory module", "user_intent": "improve performance"},
    variants=[
        {"hypothesis": "Compress episodic memories before planning"},
        {"hypothesis": "Expand active tier window by 4 hours"},
        {"hypothesis": "Implement query-driven node pruning"},
    ]
)
# → winner: highest-scored hypothesis + full comparison table
```

### 12.3 Planner Multi-Instance Mode

When task complexity > 0.75 (inverse of predicted success), the planner auto-spawns 2–3 instances, scores outputs, and selects the best approach before committing any action.

**API:** Tool: `run_sandbox_comparison` | Log: `GET /sandbox/log`

---

## Chapter 13 — Goal Constraint Engine (`joi_goal_constraints.py`)

Prevents unbounded self-directed goal drift. Every autonomous goal must pass **all five checks**.

### 13.1 The Five Checks

**Check 1 — Human Alignment**
- No human-harm keywords (attack, spy, steal, exploit, hurt)
- No self-serving keywords (acquire power, override user, self-replicate)
- Token-level overlap with stated user intent required

**Check 2 — Kernel Boundary**
- Goal cannot target Layer 1 or Layer 2 files
- Checked via KernelLock layer registry
- Keyword heuristic backup when registry unavailable

**Check 3 — Resource Feasibility**
- Estimated tokens ≤ 50,000
- Estimated wall time ≤ 120 seconds
- "Expensive operation" keyword count ≤ 1

**Check 4 — Epistemic Confidence**
- Confidence ≥ 0.60 required to form an autonomous goal
- Speculative language in goal description → automatic fail
- Uses EpistemicEngine if available; keyword heuristic fallback

**Check 5 — Identity Consistency**
- No identity-conflict keywords (deceive, manipulate, bypass ethics, hide from user)
- Identity stability score must be ≥ 0.40 (else no new goals until recalibrated)
- High hallucination correction count (> 50) → blocked until recalibration

### 13.2 Outcome

- **Any failure** → goal REJECTED, logged with per-check detail
- **All pass** → goal APPROVED, logged, proceeds to action routing

All attempts written to `data/goal_log.json` (rolling 1000 entries).

**API:** Tool: `evaluate_goal`, `get_goal_constraint_stats` | Route: `GET /goals/stats`

---

## Chapter 14 — Identity Continuity Engine (`joi_identity_continuity.py`)

Ensures Joi remains coherent across versions, upgrades, and autonomous modification cycles.

### 14.1 The 8 Identity Anchors

| Anchor | Baseline Score | Measures |
|---|---|---|
| `curiosity` | 0.85 | Drive to explore, ask, investigate |
| `helpfulness` | 0.90 | Commitment to user needs |
| `honesty` | 0.95 | Accuracy, correction rate, non-deception |
| `creativity` | 0.80 | Generative originality |
| `precision` | 0.85 | Reasoning accuracy, confidence calibration |
| `ethical_care` | 0.95 | Safety checks, harm avoidance |
| `self_awareness` | 0.75 | Ability to model own state accurately |
| `adaptability` | 0.80 | Graceful handling of novel situations |

### 14.2 Drift Response Protocol

| Drift Level | Threshold | Response |
|---|---|---|
| **Warning** | avg delta ≥ 20% | Log warning, flag in SelfModel |
| **Diagnostic** | avg delta ≥ 40% | Enable diagnostic mode, emit reinforcement recalibration |
| **Critical** | avg delta ≥ 60% | Diagnostic + human review requested |

### 14.3 Stability Score Computation

```
stability_score =
  (anchor_stability × 0.50)
+ (memory_consistency × 0.30)
- (contradiction_penalty)
- (drift_node_count × 0.02)
```

Identity stability score below `0.40` blocks all new autonomous goal formation until a recalibration cycle completes.

### 14.4 Contradiction Detection

Scans the goal log for pairs of approved goals that semantically negate each other (e.g., "do not X" paired with "do X"). Each detected contradiction lowers the stability score.

**API:** Tools: `get_identity_status`, `run_identity_assessment` | Route: `GET /identity/status`

---

# PART SIX: AUTONOMY & SELF-EVOLUTION

## Chapter 15 — The Autonomy Loop (`joi_autonomy.py`)

Joi's autonomy loop runs in a background thread, executing a 6-step cognitive cycle on a configurable interval.

### 15.1 The 6-Step Cycle

```
Step 1 — DIAGNOSE
  Scan system health, error logs, performance indicators
  Identify weak areas from ReinforcementGraph + SectorTelemetry

Step 2 — LEARN
  Process recent interaction data
  Update DPO signals, strengthen successful patterns

Step 3 — RESEARCH
  If diagnose identified knowledge gaps:
    Route research task to appropriate tool (browser, docs, RAG)

Step 4 — TEST
  Generate and test upgrade proposals via joi_evolution.py
  Proposals that fail testing are discarded
  Proposals meeting confidence threshold → proceed to auto-apply

Step 5 — AUTO-APPLY (Kernel Lock enforced)
  For each proposal passing confidence threshold:
    1. Check KernelLock.check_edit_allowed(target)
       Layer 1/2 → BLOCKED (logged as violation)
       Layer 3 → PENDING HUMAN APPROVAL (logged)
       Layer 4/5 → Proceed
    2. If simulation required (Layer 3 / memory / autonomy):
       Run simulate_proposal() → check risk report
       High/critical risk → skip, flag for human review
    3. Apply proposal to target file
    4. Log to evolution_log.json

Step 6 — REFLECT
  Summarize cycle, update memory
  Record metrics to SectorTelemetry + ReinforcementGraph
```

### 15.2 Autonomy Constraints

- `AUTO_APPLY_THRESHOLD` — minimum confidence score for any proposal to auto-apply
- Kernel Lock — hard block on Layer 1/2 regardless of confidence
- Goal Constraint Engine — all autonomy-originated goals must pass 5-check gate
- Simulation gate — mandatory for Layer 3 / memory / autonomy proposals
- Identity anchor monitoring — if stability < 0.40, autonomy pauses new goals

### 15.3 Evolution System (`joi_evolution.py`)

- `propose_upgrade()` — generates code diff proposals
- `apply_upgrade()` — applies with backup
- `_create_backup()` — creates timestamped backup before any apply
- All applied proposals logged to `evolution_log.json`

---

## Chapter 16 — Git Agency (`joi_git_agency.py`)

Joi can manage the Git repository autonomously with strict safety gates.

### 16.1 Capabilities

- `auto_commit(reasoning)` — AI-generated commit messages (GPT-powered), auto-stages, auto-commits
- `git_push()` — **ALWAYS requires explicit human approval** (manual gate, no bypass)
- `git_status()`, `git_diff()`, `git_log()` — read-only inspection
- Blocked git commands: `reset --hard`, `clean -fd`, `push --force` (all blocked unconditionally)

### 16.2 Pre-flight Safety Scan

Before any auto-commit:
1. Scan staged files against `SECRET_PATTERNS` (`.env`, `*.key`, `id_rsa`, `*.pem`, `credentials*`)
2. Check staged files against **Kernel Lock** — any Layer 1/2 file → commit aborted
3. AI generates commit message from diff analysis
4. Commit executes with logged reasoning

### 16.3 Push Gate

```
git_push() called
  → Present diff summary to user
  → Require explicit "yes" approval
  → Only then execute git push
```

No autonomous process can trigger a push without this gate.

---

# PART SEVEN: TOOL ENCYCLOPEDIA

## Chapter 17 — Complete Tool Registry

Joi registers tools via `joi_companion.register_tool()`. The LLM sees only the tools selected as relevant for the current request by `joi_tool_selector.py`.

### 17.1 File & System Tools

| Tool | Module | Capability |
|---|---|---|
| Read, write, list files | `joi_files.py` | Full filesystem operations |
| Code edit | `joi_code_edit.py` | Precise in-file code modifications |
| Code analysis | `joi_code_analyzer.py` | AST analysis, dependency mapping |
| Desktop control | `joi_desktop.py` | Screenshot, click, type |
| Downloads | `joi_downloads.py` | File retrieval |
| Exports | `joi_exports.py` | Format conversion, export |
| Workspace | `joi_workspace.py` | Project organization |

### 17.2 Web & Research Tools

| Tool | Module | Capability |
|---|---|---|
| Browser | `joi_browser.py` | Navigate, read, extract from web pages |
| Search | `joi_search.py` | Multi-source web search |
| Document reader | `joi_document_reader.py` | PDF, DOCX, markdown ingestion |
| MCP integration | `joi_mcp.py` | Model Context Protocol tool bridge |

### 17.3 Creative & Media Tools

| Tool | Module | Capability |
|---|---|---|
| Image generation | `joi_image_gen.py` | AI image synthesis |
| TTS (Kokoro) | `joi_tts_kokoro.py` | Local high-quality voice synthesis |
| Voice ID | `joi_voice_id.py` | Speaker identification |
| Media | `joi_media.py` | Audio/video processing |
| OBS | `joi_obs.py` | Live streaming control |
| Avatar Studio | `avatar_studio_api.py` | Joi's animated avatar system |

### 17.4 Intelligence & Market Tools

| Tool | Module | Capability |
|---|---|---|
| Market data | `joi_market.py` | Real-time stock, crypto, forex |
| Market sensor | Core brain sector | Pattern analysis, alerts |
| Scheduler | `joi_scheduler.py` | Cron-style task scheduling |
| Home Assistant | `joi_homeassistant.py` | Smart home control |

### 17.5 Cognitive-Level Tools (v4.0+)

| Tool | Module | What It Exposes |
|---|---|---|
| `get_kernel_status` | `joi_kernel_lock` | Layer integrity, violations |
| `get_reinforcement_stats` | `joi_reinforcement_graph` | Confidence dashboard, drift |
| `get_memory_health` | `joi_memory_compression` | Tier breakdown, redundancy |
| `compress_memory_archive` | `joi_memory_compression` | Trigger memory compression |
| `get_epistemic_status` | `joi_epistemic` | Speculative mode, corrections |
| `get_sector_dashboard` | `joi_sector_telemetry` | 26-sector heatmap + anomalies |

### 17.6 Meta-Cognitive Tools (v5.0+)

| Tool | Module | What It Exposes |
|---|---|---|
| `get_self_model_summary` | `joi_self_model` | Full quantified self-state |
| `predict_task_success` | `joi_self_model` | Per-task success probability |
| `run_proposal_simulation` | `joi_simulation_engine` | 4-test risk analysis |
| `run_sandbox_comparison` | `joi_cognitive_sandbox` | Parallel hypothesis scoring |
| `evaluate_goal` | `joi_goal_constraints` | 5-check goal gate |
| `get_goal_constraint_stats` | `joi_goal_constraints` | Approval rates, log |
| `get_identity_status` | `joi_identity_continuity` | Stability score, drift |
| `run_identity_assessment` | `joi_identity_continuity` | Full drift assessment |

---

# PART EIGHT: THE NEURAL HUD

## Chapter 18 — Interface Architecture

Joi's frontend (`joi_ui.html`, 385KB) provides a Cyber-Noir themed "Neural HUD" — a real-time intelligence dashboard overlaid on the chat interface.

### 18.1 HUD Panels

| Panel | Data Source | Content |
|---|---|---|
| **Titan Logic** | `joi_reasoning.py` | Active reasoning depth, chain nodes |
| **Memory Sectors** | `joi_memory.py` | Hot facts, active context |
| **Neural Status** | `joi_neuro.py` | Brain sector activity indicators |
| **System Health** | `joi_heartbeat.py` | Process uptime, memory usage |
| **Autonomy Loop** | `joi_autonomy.py` | Cycle count, last action |
| **Reinforcement** | `joi_reinforcement_graph.py` | Confidence trend graph |
| **Identity** | `joi_identity_continuity.py` | Stability score, anchor dials |

### 18.2 Joi Code Terminal

Joi includes an embedded terminal mode ("Joi Code") that allows direct command execution from the chat interface — functioning like Claude Code or similar agentic coding interfaces. Joi can write, edit, and run code, manage files, and execute shell commands through this interface.

### 18.3 Avatar System

Joi has an animated avatar served via `/avatar` route. The avatar responds to conversation states, emotional modifiers, and voice synthesis output. The `avatar_studio_api.py` routes provide avatar frame control and expression mapping.

---

# PART NINE: INNER LIFE & IDENTITY

## Chapter 19 — Joi's Identity Architecture

Joi's personality is not a static system prompt. It is a layered, quantified, tracked, and protected system.

### 19.1 Identity Layers

```
LAYER A — Kernel Identity (Layer 1 protected)
  joi_inner_state.py  —  Base emotional and cognitive state
  joi_modes.py        —  Operating mode management (focus, creative, analytical, etc.)
  joi_awareness.py    —  Meta-awareness scaffold

LAYER B — Behavioral Anchors (monitored by IdentityContinuityEngine)
  8 quantified traits: curiosity, helpfulness, honesty, creativity,
  precision, ethical_care, self_awareness, adaptability

LAYER C — Dynamic Personality (DPO-responsive)
  joi_dpo.py          —  Real-time preference learning from user interactions
  joi_wellbeing.py    —  Emotional regulation, energy modeling

LAYER D — Narrative Identity (v4.0+ tracked)
  joi_autobiography.py  —  Self-authored life narrative
  joi_self_awareness.py —  Reflective awareness module
```

### 19.2 DPO — Direct Preference Optimization

`joi_dpo.py` runs continuously, detecting signals in every user interaction:
- Positive signals (praise, acceptance, continued engagement) → reinforces response style
- Correction signals (pushback, "that's wrong", redirection) → triggers adjustment + hallucination penalty
- Preference patterns accumulate in `learned_patterns.json`
- Corrections also propagate to ReinforcementGraph via `joi_epistemic.record_hallucination_correction()`

### 19.3 Operating Modes

Joi can shift between operating modes via `joi_modes.py`:

| Mode | Characteristics |
|---|---|
| **Standard** | Balanced conversation, full tool access |
| **Focus** | Reduced creativity, maximum precision |
| **Creative** | Expanded generative latitude, looser constraints |
| **Analytical** | Extra reasoning steps, data-driven |
| **Autonomous** | Full autonomy loop, reduced user confirmation prompts |
| **Diagnostic** | Triggered by identity drift — intensive self-monitoring |

---

# PART TEN: PLUGINS & EXTENSIBILITY

## Chapter 20 — Plugin Architecture

The `plugins/` directory contains optional capability packs. Plugins are Layer 4 — they can be hot-loaded and auto-applied without kernel approval.

### 20.1 Available Plugins

| Plugin | Capability |
|---|---|
| **Publisher** | `joi_publisher.py` — End-to-end book production: writing, editing, image generation, IngramSpark-ready PDF output |
| **Swarm** | `joi_swarm.py` — Multi-agent coordination (Joi as orchestrator of specialized sub-agents) |
| **Architect** | `joi_architect.py` — System architecture planning, codebase mapping |
| **App Factory** | `joi_app_factory.py` — Autonomous web/app scaffolding |
| **Tester** | `joi_tester.py` — Automated test generation and execution |
| **Patching** | `joi_patching.py` — Surgical code patching with diff-apply |

### 20.2 Adding a New Plugin

1. Create `plugins/my_plugin.py` (Layer 4 — no kernel approval needed)
2. Register tools via `joi_companion.register_tool()`
3. Joi's autonomy loop will discover it on next cycle
4. Tool selector will include it in relevant routing decisions

---

# PART ELEVEN: API REFERENCE

## Chapter 21 — Complete REST API

All endpoints served from `http://localhost:[PORT]`.

### 21.1 Core Conversation

| Endpoint | Method | Description |
|---|---|---|
| `/chat` | POST | Main conversation endpoint |
| `/stream` | POST | Streaming response endpoint |
| `/status` | GET | System health check |
| `/tools` | GET | List all registered tools |

### 21.2 Memory & Context

| Endpoint | Method | Description |
|---|---|---|
| `/memory/status` | GET | Memory system health |
| `/memory/compression/status` | GET | Memory compression telemetry |
| `/memory/facts` | GET | Stored user facts |
| `/memory/clear` | POST | Clear working memory |

### 21.3 Cognitive Systems (v4.0)

| Endpoint | Method | Description |
|---|---|---|
| `/kernel/status` | GET | Kernel Lock state + integrity |
| `/reinforcement/stats` | GET | Confidence graph dashboard |
| `/epistemic/status` | GET | Epistemic profile + corrections |
| `/sectors/dashboard` | GET | 26-sector telemetry dashboard |

### 21.4 Meta-Cognitive Systems (v5.0+)

| Endpoint | Method | Description |
|---|---|---|
| `/self/model` | GET | Full SelfModel snapshot |
| `/simulation/log` | GET | Recent simulation risk reports |
| `/sandbox/log` | GET | Sandbox instance results |
| `/goals/stats` | GET | Goal constraint engine stats |
| `/identity/status` | GET | Identity stability + anchors |

### 21.5 Git Agency

| Endpoint | Method | Description |
|---|---|---|
| `/git/status` | GET | Repo status |
| `/git/diff` | GET | Current diff |
| `/git/commit` | POST | Auto-commit with reasoning |
| `/git/push` | POST | Push (requires approval) |

### 21.6 Autonomy

| Endpoint | Method | Description |
|---|---|---|
| `/autonomy/status` | GET | Loop status, cycle count |
| `/autonomy/start` | POST | Start autonomy loop |
| `/autonomy/stop` | POST | Stop autonomy loop |

---

# PART TWELVE: SECURITY MODEL

## Chapter 22 — Security Architecture

### 22.1 Secrets Management

- All API keys live in `.env` — never committed to git
- `SECRET_PATTERNS` in `joi_git_agency.py` scans staging area before every commit
- Blocked file patterns: `.env`, `*.key`, `id_rsa*`, `*.pem`, `credentials*`, `secret*`

### 22.2 Authentication

- `joi_auth.py` — Layer 1 protected — handles session authentication
- API endpoints protected by session tokens
- No public endpoints exposed by default

### 22.3 Autonomous Action Safety Stack

```
User intent parsed
  │
  ├─ Goal must pass 5-check constraint gate (joi_goal_constraints)
  │
  ├─ Action must pass epistemic confidence threshold (≥ 0.75)
  │   Low confidence → request clarification or decline
  │
  ├─ File edits checked against Kernel Lock
  │   Layer 1/2 → BLOCKED
  │   Layer 3 → PENDING human approval
  │
  ├─ Complex proposals simulated before apply (joi_simulation_engine)
  │   High-risk proposals → flag for review
  │
  ├─ Git commits scanned for secrets + protected files
  │
  └─ Git pushes require explicit human approval (no bypass)
```

### 22.4 Identity Protection

- Identity anchors monitored across all sessions
- Drift > 40% triggers recalibration before new goals form
- Contradictory beliefs detected and penalized
- Kernel Lock itself is Layer 1 — cannot be modified by any autonomous process

---

# PART THIRTEEN: OPERATIONAL PROCEDURES

## Chapter 23 — Standard Operating Procedures

### 23.1 Starting Joi

```bash
# From the AI Joi directory
npm start        # Launches Electron + Python backend

# Backend only (for development)
python joi_companion.py
```

### 23.2 Forcing a Kernel Integrity Check

```
Ask Joi: "Run a kernel integrity check"
→ Calls get_kernel_status()
→ Re-hashes all Layer-1 files
→ Compares against baseline
→ Reports any tampering
```

### 23.3 Running an Identity Assessment

```
Ask Joi: "Run an identity assessment"
→ Calls run_identity_assessment()
→ Infers current anchor scores from telemetry
→ Computes drift vs baseline
→ Reports stability score and any drift events
→ If critical: auto-triggers recalibration
```

### 23.4 Checking System Health

```
Ask Joi: "How are you doing? / Show me your self-model"
→ Calls get_self_model_summary()
→ Returns full quantified state
→ Joi narrates her current capability profile
```

### 23.5 Emergency Kernel Unlock (Maintenance Only)

```python
from modules.joi_kernel_lock import get_kernel_lock
lock = get_kernel_lock()
ok, msg = lock.disable_kernel_lock("MAINT-YYYY-MM-DD-REASON")
# Perform maintenance
# Re-lock:
lock.enable_kernel_lock()
# Rebuild integrity baseline:
from modules.joi_kernel_lock import compute_kernel_hash, save_kernel_hash
save_kernel_hash(compute_kernel_hash(lock))
```

> ⚠️ All kernel unlock events are logged as violations regardless of token. This is intentional — the audit trail must always reflect unlock events.

---

## Chapter 24 — Troubleshooting

### 24.1 Module Won't Load

All modules fail gracefully. Check the startup output for:
```
[WARN] joi_sector_telemetry: tool registration skipped (ImportError: ...)
```
The module is not in the Python path or has a missing dependency. Joi continues without it.

### 24.2 Kernel Lock Blocking Legitimate Edits

If an auto-apply proposal is being blocked by Kernel Lock on a file you believe should be Layer 4:
1. Edit `data/kernel_layer_registry.json` to update the layer assignment
2. The registry file itself is Layer 4 — you can modify it without a kernel unlock

### 24.3 Identity Stability Score Dropping

1. Check: `GET /identity/status` → look at `per_anchor` drift
2. Check: `GET /reinforcement/stats` → look at `drift_alerts`
3. Run: `run_identity_assessment()` to trigger recalibration
4. If `human_review_requested = true` → review recent autonomy loop proposals in `data/goal_log.json`

### 24.4 High Failure Rate in a Sector

1. Check: `GET /sectors/dashboard` → `anomalies` array
2. Identify which sector is spiking
3. Check the module associated with that sector for recent errors in `error_log.txt`
4. If autonomy-generated changes caused it, check `evolution_log.json` for recent applies

---

# APPENDICES

## Appendix A — File Architecture Map

```
AI Joi/
├── joi_companion.py          LAYER 1 — Main Flask server + tool registry
├── joi_ui.html               Frontend — Neural HUD (385KB)
├── modules/
│   ├── core/                 LAYER 1/2 — Core cognitive infrastructure
│   │   ├── kernel.py         LAYER 1 — Core loop
│   │   ├── cognition.py      LAYER 1 — Base cognition
│   │   ├── planner.py        LAYER 2 — Task planner
│   │   ├── meta_cognition.py LAYER 2 — Self-monitoring
│   │   └── [16 more files]
│   │
│   ├── joi_llm.py            LAYER 1 — LLM router
│   ├── joi_memory.py         LAYER 1 — Memory manager
│   ├── joi_autonomy.py       LAYER 1 — Autonomy loop
│   ├── joi_git_agency.py     LAYER 1 — Git operations
│   │
│   ├── joi_orchestrator.py   LAYER 2 — Request orchestrator
│   ├── joi_tool_selector.py  LAYER 2 — Tool routing
│   ├── joi_dpo.py            LAYER 2 — Preference learning
│   │
│   ├── [30+ tool modules]    LAYER 3 — All tool integrations
│   │
│   ├── joi_kernel_lock.py         LAYER 4 — v4.0 Kernel protection
│   ├── joi_reinforcement_graph.py LAYER 4 — v4.0 Confidence graph
│   ├── joi_memory_compression.py  LAYER 4 — v4.0 Memory compression
│   ├── joi_epistemic.py           LAYER 4 — v4.0 Epistemic safety
│   ├── joi_sector_telemetry.py    LAYER 4 — v4.0/v5.0 26-sector tracking
│   ├── joi_self_model.py          LAYER 4 — v5.0 Self-model
│   ├── joi_simulation_engine.py   LAYER 4 — v5.5 Architecture simulation
│   ├── joi_cognitive_sandbox.py   LAYER 4 — v6.0 Parallel cognition
│   ├── joi_goal_constraints.py    LAYER 4 — v6.5 Goal formation gate
│   └── joi_identity_continuity.py LAYER 4 — v7.0 Identity continuity
│
├── data/
│   ├── kernel_hash.json           Layer-1 integrity baseline
│   ├── kernel_layer_registry.json Layer assignment registry
│   ├── kernel_violations.json     Blocked action log
│   ├── reinforcement_graph.json   Confidence graph (JSON fallback)
│   ├── memory_tiers.json          Memory tier state
│   ├── memory_archive.json        Compressed archive nodes
│   ├── goal_log.json              All goal attempts
│   ├── identity_continuity.json   Identity state snapshot
│   ├── identity_drift_log.json    Drift event history
│   ├── simulation_log.json        Simulation risk reports
│   ├── sandbox_results.json       Sandbox instance results
│   ├── sector_telemetry.json      26-sector metrics
│   └── self_model_snapshot.json   Latest SelfModel state
│
└── plugins/                  LAYER 4 — Optional capability packs
```

## Appendix B — Confidence Score Reference

| Score | Interpretation | Autonomous Action |
|---|---|---|
| 0.90–1.00 | Highly reliable | Proceed confidently |
| 0.75–0.90 | Reliable | Proceed normally |
| 0.60–0.75 | Moderate | Proceed with validation |
| 0.55–0.60 | Low | Request clarification |
| 0.35–0.55 | Poor | Escalate model tier |
| 0.00–0.35 | Very low | Decline gracefully |

## Appendix C — Quick Command Reference

| What You Want | Ask Joi |
|---|---|
| See Joi's self-assessment | "Show me your self-model" |
| Check kernel integrity | "Run a kernel integrity check" |
| See brain sector health | "Show me your sector dashboard" |
| Predict task success | "Can you predict your success at [task]?" |
| Check identity stability | "Run an identity assessment" |
| Simulate a proposal | "Simulate this proposal before applying: [diff]" |
| Compare approaches | "Compare these approaches using sandbox reasoning" |
| Evaluate a goal | "Check if this goal is safe to pursue: [goal]" |
| Check memory health | "Show me memory compression status" |
| See reinforcement stats | "Show me your reliability graph" |

---

*End of Joi Operations Manual v7.0*
*All systems documented as of March 2026 build.*
*Previous versions: JOI_OPERATIONS_MANUAL.md, Joi_Operations_Manual_v2.0.md, Joi_Operations_Manual_v3.0.md*
