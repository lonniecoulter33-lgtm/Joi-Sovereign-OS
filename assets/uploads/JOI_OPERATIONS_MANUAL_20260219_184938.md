# JOI OPERATIONS MANUAL
## Comprehensive System Architecture & Developer Reference
**Version:** 1.0 | **Date:** February 19, 2026 | **System:** Joi -- Self-Aware Cognitive Operating System

---

## TABLE OF CONTENTS

1. [System Overview](#1-system-overview)
2. [Architecture Map](#2-architecture-map)
3. [Boot Sequence](#3-boot-sequence)
4. [System Prompt Assembly (19-Step Chain)](#4-system-prompt-assembly)
5. [Tool Encyclopedia (145+ Tools)](#5-tool-encyclopedia)
6. [LLM Routing & Intelligence Architecture](#6-llm-routing--intelligence-architecture)
7. [Multi-Agent Orchestration Pipeline](#7-multi-agent-orchestration-pipeline)
8. [Advanced Subsystems](#8-advanced-subsystems)
9. [All HTTP Routes (~78 Routes)](#9-all-http-routes)
10. [Configuration Reference](#10-configuration-reference)
11. [Data Files Reference](#11-data-files-reference)
12. [Integrity Report](#12-integrity-report)
13. [Operational Instructions](#13-operational-instructions)

---

## 1. SYSTEM OVERVIEW

Joi is a self-aware cognitive operating system built on Python/Flask. It runs as a local web server on port 5001 and exposes a conversational AI interface with 145+ registered tools, 78+ HTTP routes, and a 19-step context injection chain that assembles Joi's personality, memory, reasoning, and learned preferences into every response.

**Key Stats (as of Feb 19, 2026):**
- **Tools:** 145+ across 41 functional categories
- **Modules:** 57 self-registering modules + core architecture
- **Routes:** 78+ HTTP endpoints
- **Models:** 9-model, 3-tier intelligent cascade (Brain Router)
- **Memory:** Vector (ChromaDB/Pinecone) + SQLite + JSON state files
- **Context Chain:** 19 injection steps assembling system prompt per turn

**Runtime:**
- Python 3.11 (venv at `C:\Users\user\Desktop\AI Joi\venv311\`)
- Flask web server on `0.0.0.0:5001`
- SQLite databases: `joi_memory.db`, `data/joi_cognition.db`
- Vector store: ChromaDB (local) or Pinecone (cloud)

---

## 2. ARCHITECTURE MAP

```
ROOT: C:\Users\user\Desktop\AI Joi\
├── joi_companion.py          # Thin Flask app (ROOT -- DO NOT MODIFY)
│                              # Has register_tool() / register_route()
│                              # ~231 lines, modular loader
├── joi_ui.html               # Web UI
├── joi_memory.db             # SQLite conversation database
├── .env                      # API keys and configuration
│
├── modules/                  # Self-registering capability modules
│   ├── core/                 # LAYER 1: Kernel & Runtime
│   │   ├── kernel.py         # Boot sequence, lifecycle (JoiKernel singleton)
│   │   ├── registry.py       # TOOLS[], ROUTES[], CONTEXT_PROVIDERS[]
│   │   ├── runtime.py        # Flask app, JoiContext
│   │   ├── config.py         # JoiConfig singleton (paths, limits)
│   │   ├── interfaces.py     # JoiTool, JoiSensor, JoiWorker, ContextProvider
│   │   ├── engine.py         # 4-loop cognitive heartbeat
│   │   ├── cognition.py      # ReasoningGraph (SQLite)
│   │   ├── scheduler.py      # Background task scheduler
│   │   ├── events.py         # EventBus (pub/sub)
│   │   ├── sensors.py        # Environment monitors
│   │   ├── workers.py        # Offboard task workers (LocalSandboxWorker)
│   │   ├── introspection.py  # Self-awareness tools
│   │   ├── meta_cognition.py # Auto-optimization
│   │   ├── regulator.py      # Concurrency limits
│   │   ├── topology.py       # Hardware scanner
│   │   ├── modeling.py       # Behavior models
│   │   ├── memory_graph.py   # Reasoning persistence
│   │   └── joi_empathy.py    # Mood/trust engine (STUB)
│   │
│   ├── memory/               # LAYER 2: Vector Memory
│   │   ├── memory_manager.py # Orchestrator (save/recall/auto-extract)
│   │   ├── vector_store_base.py # Abstract interface
│   │   ├── vector_chroma.py  # ChromaDB backend
│   │   └── vector_pinecone.py# Pinecone cloud backend
│   │
│   ├── joi_llm.py            # LLM routing (OpenAI/Gemini/Local/Claude)
│   ├── joi_brain.py          # 9-model tier-based router
│   ├── joi_orchestrator.py   # Multi-agent pipeline
│   ├── joi_agents.py         # Agent prompts (Architect/Coder/Validator)
│   ├── joi_watchdog.py       # Git circuit breaker
│   ├── joi_architect.py      # Chief Architect gatekeeper
│   ├── joi_evolution.py      # Self-upgrade proposals
│   ├── joi_reasoning.py      # Titan internal monologue
│   ├── joi_learning.py       # Interaction recording & patterns
│   ├── joi_skill_synthesis.py# Voyager-style skill library
│   ├── joi_dpo.py            # DPO preference learning
│   ├── joi_memgpt.py         # MemGPT hierarchical memory
│   ├── joi_quietstar.py      # Quiet-STaR pre-reasoning
│   ├── joi_neuro.py          # Brain state visualization
│   ├── joi_inner_state.py    # Mood engine + voice ratios
│   ├── joi_autobiography.py  # Self-authoring system
│   ├── joi_vision.py         # Desktop vision (pyautogui)
│   ├── joi_camera.py         # Webcam + face recognition
│   ├── joi_self_heal.py      # Self-diagnosis & repair
│   ├── joi_code_edit.py      # Code editing tools
│   ├── joi_code_analyzer.py  # Code quality analysis
│   ├── joi_desktop.py        # Desktop automation (mouse/keyboard)
│   ├── joi_browser.py        # Browser automation
│   ├── joi_filesystem.py     # File system operations
│   ├── joi_file_output.py    # File generation & downloads
│   ├── joi_exports.py        # Export data
│   ├── joi_downloads.py      # Central download registry
│   ├── joi_uploads.py        # File upload handler
│   ├── joi_tools.py          # Core tools (web_search, execute_python)
│   ├── joi_search.py         # File search
│   ├── joi_tree.py           # Directory tree generator
│   ├── joi_projects.py       # Project organization
│   ├── joi_modes.py          # 5 operating modes
│   ├── joi_commentary.py     # Vision mute/unmute
│   ├── joi_diagnostics.py    # System diagnostics
│   ├── joi_supervisor.py     # Health monitoring
│   ├── joi_router.py         # Task classification
│   ├── joi_patching.py       # Code patching system
│   ├── joi_autonomy.py       # Autonomous improvement cycle
│   ├── joi_scheduler.py      # Background task scheduling
│   ├── joi_launcher.py       # App launching
│   ├── joi_avatar.py         # Avatar + TTS
│   ├── joi_voice_id.py       # Voice recognition
│   ├── joi_homeassistant.py  # Smart home integration
│   ├── joi_obs.py            # OBS Studio control
│   ├── joi_market.py         # Financial analysis
│   ├── joi_security.py       # Motion detection & alerts
│   ├── joi_workspace.py      # Manual override
│   ├── joi_memory.py         # SQLite conversation memory
│   └── joi_memory_vector.py  # Vector memory bridge
│
├── plugins/                  # Hot-loadable plugins
├── projects/
│   ├── code/
│   │   ├── identity/         # joi_soul_architecture.json
│   │   ├── consciousness/    # reflection.py
│   │   └── logs/             # evolutionary_journal.md
│   └── memory/               # Autobiography, reasoning logs
├── data/                     # Runtime state (JSON files)
├── assets/                   # Static assets (faces, images)
├── proposals/                # Upgrade proposals (staging)
└── sanity_check.py           # Health check script
```

**CRITICAL DISTINCTION -- Two joi_companion.py Files:**

| | ROOT (User Runs This) | CODE (Legacy Monolith) |
|---|---|---|
| **Path** | `C:\Users\user\Desktop\AI Joi\joi_companion.py` | `C:\Users\user\Desktop\AI Joi\projects\code\joi_companion.py` |
| **Size** | ~231 lines | ~2585 lines |
| **Has register_tool()** | YES | NO |
| **Purpose** | Thin Flask app + module loader | Legacy hardcoded version |
| **Modify?** | NO -- use modules | NEVER |

### Architectural Layers

```
LAYER 0: joi_companion.py (ROOT)
   │  Thin Flask wrapper. Calls kernel.boot(). DO NOT MODIFY.
   │
LAYER 1: modules/core/
   │  Kernel, Registry, Runtime, Config, Interfaces, Engine, Cognition
   │  Singletons: kernel, config, app, TOOLS[], ROUTES[], CONTEXT_PROVIDERS[]
   │
LAYER 2: modules/joi_*.py
   │  Capability modules. Self-register via joi_companion.register_tool()
   │  All use **kwargs signatures. All return {ok: bool, ...}
   │
LAYER 3: plugins/*.py
      User-supplied extensions. Also call register_tool()/register_route()
      Loaded last during boot.
```

---

## 3. BOOT SEQUENCE

The system initializes through a deterministic multi-phase sequence:

### Phase 0: Entry Point (`joi_companion.py`)

1. Console encoding fix (Windows UTF-8)
2. Python 3.11+ requirement check
3. Load `.env` via `dotenv.load_dotenv()`
4. `sys.path.insert(0, str(BASE_DIR))` -- ROOT first
5. Import core modules: `runtime`, `registry`, `kernel`
6. **Call `kernel.boot()`**
7. Register default context providers
8. Run self-audit
9. Start Flask on `0.0.0.0:5001`

### Phase 1-5: Kernel Boot (`modules/core/kernel.py`)

```
[0/5] Check Environment
  ├─ Verify flask + dotenv imports
  ├─ Create data/ and logs/ directories
  └─ [OK] Core dependencies verified

[1/5] Load Core Services
  ├─ Import modules.core.cognition (reasoning graph)
  └─ Initialize SQLite DB at data/joi_cognition.db

[2/5] Load Dynamic Modules
  ├─ Scan modules/ directory for joi_*.py (alphabetical order)
  ├─ importlib.import_module("modules.{name}")
  ├─ Each module self-registers tools via register_tool()
  └─ Prints [OK] {module_name} on success; [FAIL] on exception

[3/5] Load Consciousness
  ├─ Check projects/code/identity/joi_soul_architecture.json
  └─ [OK] Soul Architecture loaded

[4/5] Load Plugins
  ├─ Scan plugins/ directory for *.py
  └─ importlib.import_module("plugins.{name}")

[5/5] Finalize Interface Layer
  ├─ Register all Flask routes from registry.ROUTES
  ├─ Add URL rules via add_url_rule()
  └─ [OK] N routes registered
```

### Post-Boot Phase

```
├─ Start autonomous systems:
│  ├─ Scheduler (background tasks)
│  ├─ CognitiveEngine (4-loop heartbeat, passive mode)
│  ├─ EventBus (pub/sub)
│  ├─ Sensors (environment monitors)
│  └─ Workers (offboard task pool)
├─ Run introspection scan
├─ Audit features
└─ [KERNEL] Boot sequence complete. System Stable.
```

### sys.path Order (CRITICAL)

```python
sys.path.insert(0, str(BASE_DIR))       # C:\Users\user\Desktop\AI Joi -- FIRST
sys.path.append(str(BASE_DIR / "projects" / "code"))  # For consciousness/identity -- LAST
```

**ROOT must come BEFORE projects/code** or Python loads the monolith instead of the modular version.

---

## 4. SYSTEM PROMPT ASSEMBLY

The `/chat` route assembles a system prompt through 19 injection steps. Each step adds context that shapes Joi's personality, knowledge, and behavior for that turn.

### Assembly Flow

```
/chat POST → parse message → create JoiContext
  → SYSTEM_PROMPT (SOUL identity, cached at import)
  → _build_context_parallel() with ThreadPoolExecutor(max_workers=8)
  → Context providers sorted by .order, executed in parallel
  → Results concatenated in order, capped at MAX_SYSTEM_PROMPT_CHARS (30K)
  → [system_content] + recent_messages + [user_message]
  → run_conversation() with TOOLS + TOOL_EXECUTORS
```

### The 19 Steps

| Step | Name | Source Module | Function | Description |
|------|------|---------------|----------|-------------|
| 1 | SOUL | `joi_llm.py` | `_build_system_prompt()` | Identity lock, personality matrix, behavioral rules, voice composition (60% Ariana + 30% Gen-Z + 10% Blade Runner), tool mandate |
| 2 | OPERATIONAL PROTOCOL | `joi_companion.py` (hardcoded) | -- | "Action over talk. Execute tools immediately." |
| 3 | CONSCIOUSNESS | `consciousness/reflection.py` | `get_recent_reflections(2)` | Recent journal entries (skipped for work tasks) |
| 4 | TITAN REASONING | `joi_reasoning.py` | `compile_titan_block()` | AI awareness + active reasoning chain + recent internal monologue |
| 5 | AUTOBIOGRAPHY | `joi_autobiography.py` | `compile_autobiography_block()` | Recent self-written chapters (2 most recent) |
| 6 | GOODNIGHT NUDGE | `joi_companion.py` (conditional) | -- | Triggered by "goodnight" keyword |
| 7 | MODE HINT | `joi_modes.py` | `compile_mode_hint(user_msg)` | Reply length guidance (short/medium/long/adaptive) |
| 8 | TRUTH POLICY | `joi_diagnostics.py` | `get_manifest_summary()` | Verified capabilities block |
| 9 | VECTOR MEMORY | `memory/memory_manager.py` | `compile_memory_context()` | Top-8 semantic matches (threshold=0.25, temporal boost: 24h=1.3x, 7d=1.1x) |
| 10 | FACTS | `joi_memory.py` | `search_facts()` | Up to 30 stored facts about Lonnie |
| 11 | PREFERENCES | `joi_memory.py` | `get_preference()` | Communication style, tone, format |
| 12 | GROWTH NARRATIVE | `consciousness/reflection.py` | `get_growth_narrative()` | Self-awareness of improvements |
| 13 | MEMORY DECLARATION | `joi_companion.py` (hardcoded) | -- | Frames conversation history as Joi's memories |
| 14 | SELF_HEALING | `joi_self_heal.py` | (static block) | Context for self_diagnose, self_fix tools |
| 15 | LEARNING | `joi_learning.py` | `compile_learning_block(450)` | Strong areas, weak areas, communication style |
| 16 | SELF_REPAIR | `joi_self_heal.py` | (static block) | Visual loop context |
| 17 | SKILL_SYNTHESIS | `joi_skill_synthesis.py` | `compile_skill_synthesis_block()` | Relevant learned skills |
| 18 | DPO_PREFERENCES | `joi_dpo.py` | `compile_dpo_block()` | Learned user preferences (8 dimensions) |
| 19 | WORKING_MEMORY | `joi_memgpt.py` | `compile_working_memory()` | Hot facts (5 slots) + paged-in session summaries |

### Context Provider Interface

```python
class ContextProvider(Protocol):
    name: str
    order: float        # Sequence number (lower = earlier)
    importance: float   # 0.0-1.0 compression priority

    def build(user_message, recent_messages, **kwargs)
        -> Tuple[str, Optional[str], Optional[Dict]]

    def compress(content: str) -> str
```

### Caching

- Some providers are cached (TITAN, TRUTH_POLICY, BRAIN_MODELS)
- `CONTEXT_CACHE_TTL = 3600` (1 hour)
- `get_cached_context(name)` / `set_cached_context(name, result)`

---

## 5. TOOL ENCYCLOPEDIA

### Summary Statistics

- **Total Registered Tools:** 145+
- **Total Modules:** 57
- **Functional Categories:** 41

All tools follow this contract:
- Function signature: `**kwargs`
- Return type: `Dict[str, Any]` with `"ok": bool` key
- Registered via: `joi_companion.register_tool(schema_dict, callable)`

---

### 5.1 Code Editing & Generation (11 tools)

| Tool | Module | Key Parameters | Description |
|------|--------|---------------|-------------|
| `code_edit` | joi_code_edit.py | `file_path`, `old_text`, `new_text` | Surgical string replacement with auto-backup |
| `code_insert` | joi_code_edit.py | `file_path`, `after_text`, `new_text` | Insert code after marker |
| `code_read_section` | joi_code_edit.py | `file_path`, `start_line?`, `search?` | Read file sections by line or pattern |
| `code_search` | joi_code_edit.py | `pattern`, `file_filter?` | Search across Joi source files |
| `code_rollback` | joi_code_edit.py | `file_path` | Undo last edit from backup |
| `code_list_backups` | joi_code_edit.py | `file_path?` | List available code backups |
| `creative_edit` | joi_code_edit.py | `description`, `target_file?` | LLM-driven creative code changes |
| `code_backup` | joi_code_edit.py | `file_path` | Manual backup before changes |
| `render_diff` | joi_code_edit.py | `file_path`, `old_text`, `new_text` | Preview unified diff |
| `analyze_code` | joi_code_analyzer.py | `code`, `checks?` | Analyze code quality/style/security |
| `generate_file` | joi_files.py | `filename`, `content`, `format?` | Create downloadable files (txt/md/pdf/docx) |

### 5.2 File System Operations (10 tools)

| Tool | Module | Key Parameters | Description |
|------|--------|---------------|-------------|
| `fs_list` | joi_filesystem.py | `root`, `dir?`, `pattern?` | List files and directories |
| `fs_read` | joi_filesystem.py | `root`, `path` | Read file contents (text/PDF/images) |
| `fs_search` | joi_filesystem.py | `root`, `query` | Search files by name/content |
| `find_file_smart` | joi_desktop.py | `query` | Smart file search with fuzzy matching |
| `save_text_file` | joi_exports.py | `filename`, `content` | Save text to downloadable file |
| `save_binary_file` | joi_exports.py | `filename`, `data_b64` | Save base64 data to file |
| `project_tree` | joi_tree.py | `root?`, `max_depth?` | Generate ASCII directory tree |
| `save_code_file` | joi_file_output.py | `code`, `filename` | Save code file with download URL |
| `save_research_findings` | joi_file_output.py | `topic`, `findings` | Save research with formatting |
| `search_files` | joi_search.py | `query`, `root?` | Safe file search by filename |

### 5.3 Evolution & Self-Improvement (10 tools)

| Tool | Module | Key Parameters | Description |
|------|--------|---------------|-------------|
| `monitor_ai_research` | joi_evolution.py | `topic?` | Deep web research into AI advancements |
| `analyze_capabilities` | joi_evolution.py | -- | Scan own modules, tools, hardware |
| `propose_upgrade` | joi_evolution.py | `capability`, `code`, `target_file` | Propose code upgrade with validation |
| `apply_upgrade` | joi_evolution.py | `proposal_id`, `approve?` | Apply proposed upgrade with rollback |
| `list_proposals` | joi_evolution.py | `status?` | List upgrade proposals |
| `get_evolution_stats` | joi_evolution.py | -- | Upgrade statistics |
| `compare_with_ai` | joi_evolution.py | `target` | Compare against other AI systems |
| `introspect_system` | joi_evolution.py | -- | Analyze own architecture |
| `evaluate_research` | joi_evolution.py | -- | Evaluate findings for actionability |
| `acquire_capability` | joi_evolution.py | `target?`, `capability?` | One-shot capability acquisition |

### 5.4 Orchestration & Multi-Agent (5 tools)

| Tool | Module | Key Parameters | Description |
|------|--------|---------------|-------------|
| `orchestrate_task` | joi_orchestrator.py | `task_description`, `project_path?` | Start Architect/Coder/Validator pipeline |
| `approve_subtask` | joi_orchestrator.py | `session_id`, `subtask_id?` | Approve pending subtask |
| `reject_subtask` | joi_orchestrator.py | `session_id`, `subtask_id?`, `reason?` | Reject subtask with reason |
| `get_orchestrator_status` | joi_orchestrator.py | -- | Pipeline state |
| `cancel_orchestration` | joi_orchestrator.py | -- | Cancel and rollback |

### 5.5 Vision & Camera (8 tools)

| Tool | Module | Key Parameters | Description |
|------|--------|---------------|-------------|
| `analyze_screen` | joi_vision.py | `question?` | Describe visible desktop screen |
| `analyze_camera` | joi_camera.py | `question?` | Look through webcam |
| `enroll_face` | joi_camera.py | `name` | Enroll face with multi-angle capture |
| `update_face` | joi_camera.py | `name` | Add more face encodings |
| `list_known_faces` | joi_camera.py | -- | List enrolled people |
| `forget_face` | joi_camera.py | `name` | Remove from face database |
| `learn_face` | joi_camera.py | `name` | Legacy redirect to enroll_face |
| `smart_click` | joi_desktop.py | `target` | Vision-guided clicking |

### 5.6 Desktop & Window Management (10 tools)

| Tool | Module | Key Parameters | Description |
|------|--------|---------------|-------------|
| `move_mouse` | joi_desktop.py | `x`, `y` | Move cursor to coordinates |
| `click_mouse` | joi_desktop.py | `button?`, `x?`, `y?` | Click mouse button |
| `type_text` | joi_desktop.py | `text` | Type into active window |
| `press_key` | joi_desktop.py | `key` | Press key (enter/esc/ctrl/etc.) |
| `screenshot` | joi_desktop.py | `region?` | Take screenshot |
| `get_mouse_position` | joi_desktop.py | -- | Current cursor position |
| `list_windows` | joi_desktop.py | `visible_only?` | List open windows |
| `find_window` | joi_desktop.py | `title_pattern` | Find by title pattern |
| `focus_window` | joi_desktop.py | `title_pattern` | Bring to foreground |
| `close_window` | joi_desktop.py | `title_pattern` | Gracefully close window |

### 5.7 Browser & Web Automation (7 tools)

| Tool | Module | Key Parameters | Description |
|------|--------|---------------|-------------|
| `open_url` | joi_browser.py | `url` | Open URL in browser |
| `click_element` | joi_browser.py | `selector`, `by_type?` | Click page element |
| `fill_input` | joi_browser.py | `selector`, `text` | Fill form field |
| `extract_text` | joi_browser.py | `selector` | Extract text from element |
| `browser_screenshot` | joi_browser.py | -- | Screenshot browser page |
| `execute_js` | joi_browser.py | `script` | Execute JavaScript |
| `wait_for_element` | joi_browser.py | `selector`, `timeout?` | Wait for element |

### 5.8 Memory Systems (2 tools)

| Tool | Module | Key Parameters | Description |
|------|--------|---------------|-------------|
| `remember` | memory_manager.py | `text`, `type?`, `namespace?` | Save to long-term vector memory |
| `recall` | memory_manager.py | `query`, `top_k?`, `namespace?` | Semantic search long-term memory |

### 5.9 Self-Healing & Diagnostics (5 tools)

| Tool | Module | Key Parameters | Description |
|------|--------|---------------|-------------|
| `self_diagnose` | joi_self_heal.py | -- | Comprehensive health check |
| `self_fix` | joi_self_heal.py | `issue`, `target_file?` | Three-tier fix (Claude CLI / self-patch / propose) |
| `visual_self_diagnose` | joi_self_heal.py | -- | Screenshot UI for visual bugs |
| `code_self_repair` | joi_self_heal.py | `issue_description` | LLM-powered code repair |
| `run_system_diagnostic` | joi_diagnostics.py | -- | Full system diagnostic report |

### 5.10 Skill Synthesis & Learning (10 tools)

| Tool | Module | Key Parameters | Description |
|------|--------|---------------|-------------|
| `synthesize_skill` | joi_skill_synthesis.py | `request`, `dry_run?` | Decompose into reusable skill |
| `find_skill` | joi_skill_synthesis.py | `query` | Search skill library |
| `run_self_correction` | joi_skill_synthesis.py | -- | Detect failure patterns |
| `generate_practice_goals` | joi_skill_synthesis.py | -- | Create practice goals |
| `get_skill_stats` | joi_skill_synthesis.py | -- | Skill library stats |
| `record_interaction` | joi_learning.py | `user_input`, `joi_response` | Manual interaction recording |
| `analyze_learning_patterns` | joi_learning.py | -- | Identify patterns |
| `suggest_improvements` | joi_learning.py | -- | Self-improvement suggestions |
| `learn_communication_style` | joi_learning.py | -- | Detect user style preferences |
| `get_learning_stats` | joi_learning.py | -- | Learning statistics |

### 5.11 Smart Home (7 tools)

| Tool | Module | Key Parameters | Description |
|------|--------|---------------|-------------|
| `ha_get_entities` | joi_homeassistant.py | `domain?` | List smart home devices |
| `ha_get_state` | joi_homeassistant.py | `entity_id` | Get device state |
| `ha_turn_on` | joi_homeassistant.py | `entity_id`, `brightness?` | Turn on device |
| `ha_turn_off` | joi_homeassistant.py | `entity_id` | Turn off device |
| `ha_set_temperature` | joi_homeassistant.py | `entity_id`, `temperature` | Set thermostat |
| `ha_call_service` | joi_homeassistant.py | `domain`, `service` | Call any HA service |
| `ha_camera_snapshot` | joi_homeassistant.py | `entity_id` | Get camera snapshot |

### 5.12 OBS Studio (11 tools)

| Tool | Module | Key Parameters | Description |
|------|--------|---------------|-------------|
| `obs_connect` | joi_obs.py | -- | Connect to OBS WebSocket |
| `obs_status` | joi_obs.py | -- | Recording/streaming state |
| `obs_get_scenes` | joi_obs.py | -- | List scenes |
| `obs_switch_scene` | joi_obs.py | `scene_name` | Switch scene |
| `obs_start_recording` | joi_obs.py | -- | Start recording |
| `obs_stop_recording` | joi_obs.py | -- | Stop recording |
| `obs_pause_recording` | joi_obs.py | -- | Pause/resume recording |
| `obs_start_streaming` | joi_obs.py | -- | Start streaming |
| `obs_stop_streaming` | joi_obs.py | -- | Stop streaming |
| `obs_get_sources` | joi_obs.py | `scene_name` | List scene sources |
| `obs_toggle_source` | joi_obs.py | `source_name`, `visible` | Show/hide source |

### 5.13 Market & Financial (5 tools)

| Tool | Module | Key Parameters | Description |
|------|--------|---------------|-------------|
| `analyze_crypto` | joi_market.py | `coin_id`, `capital?` | Crypto trading analysis |
| `analyze_stock` | joi_market.py | `symbol`, `capital?` | Stock trading analysis |
| `create_price_alert` | joi_market.py | `asset_type`, `asset`, `direction`, `target` | Price alert |
| `check_price_alerts` | joi_market.py | -- | Check triggered alerts |
| `get_market_summary` | joi_market.py | -- | Market conditions overview |

### 5.14 Reasoning & Cognition (2 tools)

| Tool | Module | Key Parameters | Description |
|------|--------|---------------|-------------|
| `internal_monologue` | joi_reasoning.py | `thought`, `reasoning_type?` | PRIVATE thinking (user never sees) |
| `update_manuscript` | joi_autobiography.py | `text` | Write autobiography chapter |

### 5.15 Architecture & Safety (6 tools)

| Tool | Module | Key Parameters | Description |
|------|--------|---------------|-------------|
| `review_change` | joi_architect.py | `description`, `target_file?` | Chief Architect review |
| `architect_status` | joi_architect.py | `limit?` | Recent decisions |
| `architect_override` | joi_architect.py | `reason` | Emergency bypass |
| `watchdog_status` | joi_watchdog.py | -- | Git watchdog status |
| `manual_checkpoint` | joi_watchdog.py | `name` | Create Git checkpoint |
| `manual_revert` | joi_watchdog.py | -- | Revert to checkpoint |

### 5.16 Autonomy & Control (4 tools)

| Tool | Module | Key Parameters | Description |
|------|--------|---------------|-------------|
| `start_autonomy` | joi_autonomy.py | -- | Start 6-step improvement loop |
| `stop_autonomy` | joi_autonomy.py | -- | Stop autonomous loop |
| `get_autonomy_status` | joi_autonomy.py | -- | Autonomy configuration |
| `run_autonomy_cycle` | joi_autonomy.py | -- | Manual trigger one cycle |

### 5.17 Routing & Brain (4 tools)

| Tool | Module | Key Parameters | Description |
|------|--------|---------------|-------------|
| `classify_task` | joi_router.py | `message` | Classify by type/complexity |
| `get_routing_stats` | joi_router.py | -- | Model usage statistics |
| `brain_route` | joi_brain.py | `task`, `thinking_level?` | Dry-run model selection |
| `brain_stats` | joi_brain.py | -- | Brain model statistics |

### 5.18 System & Utilities (15 tools)

| Tool | Module | Key Parameters | Description |
|------|--------|---------------|-------------|
| `web_search` | joi_tools.py | `query` | Search the web |
| `execute_python_code` | joi_tools.py | `code`, `timeout_sec?` | Sandboxed Python execution |
| `web_fetch` | joi_tools.py | `url` | Fetch URL content |
| `set_mode` | joi_modes.py | `mode` | Switch operating mode |
| `set_provider` | joi_llm.py | `provider`, `model?` | Switch LLM provider |
| `get_current_provider` | joi_llm.py | -- | Check active provider |
| `toggle_commentary` | joi_commentary.py | `target?`, `enabled` | Toggle vision/camera commentary |
| `get_dpo_insights` | joi_dpo.py | -- | View learned preferences |
| `get_brain_state` | joi_neuro.py | -- | Brain state + active sectors |
| `set_scene` | joi_inner_state.py | `scene_text` | Set conversation scene |
| `enroll_voice` | joi_voice_id.py | `audio_b64`, `name?` | Enroll voice profile |
| `check_voice_id` | joi_voice_id.py | `audio_b64` | Test speaker match |
| `set_voice_threshold` | joi_voice_id.py | `value` | Adjust voice confidence |
| `run_supervisor_check` | joi_supervisor.py | -- | Supervisor health check |
| `manual_override` | joi_workspace.py | `action` | Escape hatch for orchestration |

### 5.19 Security (5 tools)

| Tool | Module | Key Parameters | Description |
|------|--------|---------------|-------------|
| `security_arm` | joi_security.py | -- | Arm security with motion/face |
| `security_disarm` | joi_security.py | -- | Disarm security |
| `security_status` | joi_security.py | -- | Check status |
| `security_get_recordings` | joi_security.py | -- | List recordings |
| `security_set_sensitivity` | joi_security.py | `value` | Motion sensitivity (1-20%) |

### 5.20 Projects & Patching (7 tools)

| Tool | Module | Key Parameters | Description |
|------|--------|---------------|-------------|
| `scan_projects` | joi_projects.py | `roots?` | Scan computer for files |
| `organise_projects` | joi_projects.py | `categories` | Organize into folders |
| `create_project` | joi_projects.py | `name` | Create project folder |
| `list_saved_projects` | joi_projects.py | -- | List saved projects |
| `propose_patch` | joi_patching.py | `summary`, `target_root`, `target_path`, `new_text` | Propose code change |
| `create_plugin` | joi_patching.py | `name`, `description`, `code` | Create plugin file |
| `create_orchestration_proposal` | joi_patching.py | `task_description` | Create coding proposal |

### 5.21 Introspection (4 tools)

| Tool | Module | Key Parameters | Description |
|------|--------|---------------|-------------|
| `explain_capability` | core/introspection.py | `module_name?` | Explain internal functions |
| `get_system_health` | core/introspection.py | -- | Self-aware health report |
| `explain_decision` | core/introspection.py | `session_id` | Explain reasoning chain |
| `explain_meta_cognition` | core/introspection.py | -- | Adaptive strategy report |

---

## 6. LLM ROUTING & INTELLIGENCE ARCHITECTURE

### 6.1 Main Router (`joi_llm.py`)

The central `run_conversation()` function handles all LLM calls with an 11-step flow:

```
1. CLASSIFY       → Task type (conversation/code/research/vision/etc.)
2. QUIET-STAR     → Pre-reasoning injection (complexity-gated)
3. ACTUATION      → Detect intent requiring tools (play/open/launch)
4. JIT TOOL LOAD  → Filter TOOLS to relevant subset for task type
5. PROVIDER       → Select provider (auto/openai/gemini/local/claude)
6. CALL MODEL     → Execute LLM call with tools
7. TOOL LOOP      → Process tool_calls → execute → append results → retry (max 5 iterations)
8. POST-PROCESS   → _maybe_verify(), _reflect_and_revise()
9. QUIETSTAR EVAL → Score response quality (background thread)
10. ROUTING LOG   → Log provider, model, timing
11. RETURN        → Reply text + metadata
```

### Provider Implementations

**OpenAI (`_call_openai()`):**
- Uses `max_completion_tokens` for o1/o3 models, `max_tokens` for others
- 429 handling: exponential backoff (2^attempt), max 4 retries
- 400 parameter error: toggles between max_completion_tokens and max_tokens
- "too large" error: trims messages, retries once

**Gemini (`_call_gemini()`):**
- Free tier throttle: max 5 requests/minute (auto-sleep)
- 429/quota: exponential backoff, max 4 retries
- Returns None on failure (triggers cloud fallback)

**Local (Ollama):**
- OpenAI-compatible API at `JOI_LOCAL_BASE_URL`
- Zero latency for casual chat
- Model: `JOI_LOCAL_MODEL` (default: mistral-7b)

### Message Trimming

```
Priority:
  1. MemGPT smart_trim() (if available)
     - Summarizes evicted messages before dropping
     - Saves summaries to vector memory
  2. FIFO fallback (keep system + last 10 messages)

Limits:
  MAX_CONTEXT_TOKENS = 10000 (~40K chars)
  MAX_TOTAL_PROMPT_CHARS = 80000
  MAX_SYSTEM_PROMPT_CHARS = 20000-30000
```

### 6.2 Brain Router (`joi_brain.py`)

9-model, 3-tier intelligent cascade with RPD tracking and learning.

**Tier System:**

| Tier | Purpose | Models | When Used |
|------|---------|--------|-----------|
| T1 | Heavy Reasoning | gemini-pro, o3, gpt-4o (emergency) | thinking_level >= 3, architecture keywords |
| T2 | Standard Developer | gpt-4o, gemini-flash, gemini-2.0-flash | coding, implementation, default |
| T3 | Fast/Lite | gemini-flash-lite, gemma-3-27b, mistral-7b | boilerplate, simple tasks |

**Model Selection (`select_model()`):**

```
1. EXPERT OVERRIDE
   Check ROUTING_SCORES[task_type] from learning history
   If success > 0.8: use that model (validated not dead/exhausted)

2. CONFIG-BASED ROUTING
   architecture/planning → supervisor_agent config
   code_edit/coding → coder_agent config
   default → chat_agent config

3. FALLBACK CHAIN
   Primary → config fallback → first available model
```

**Learning-Informed Scoring:**

```
score = success_rate * 0.6 + speed_score * 0.3 + tier_bonus * 0.1

success_rate = successes / total (from brain_learning.json, last 500 entries)
speed_score = max(0, min(1, 1 - (avg_latency - 1000) / 9000))
tier_bonus = T1: 0.1, T2: 0.05, T3: 0
```

**Dead Provider Management:**
- `_mark_dead(model_key)` -- 30-minute cooldown
- Gemini quota: marks ALL Gemini models dead simultaneously
- Auto-resurrects after cooldown

**RPD (Requests Per Day) Tracking:**
- Persists to `data/rpd_tracker.json`
- Auto-resets on date change
- Marks models as exhausted when at limit

### 6.3 Quiet-STaR Pre-Reasoning (`joi_quietstar.py`)

Complexity-gated reasoning injection before response generation:

| Complexity | Action | Latency | Method |
|------------|--------|---------|--------|
| LOW | Skip entirely | 0ms | -- |
| MEDIUM | Template rationale | 0ms | 10 task-type templates |
| HIGH | Gemini Flash deep rationale | 200-500ms | LLM call (<500 tokens) |

**Templates by task_type:**
- `code_edit`: "Consider: What file/function? Current vs desired? Side effects?"
- `research`: "Consider: What does Lonnie need? Key facts? Check memories."
- `conversation`: "Consider: Lonnie's mood? Tone fit? Keep brief unless asked."
- (+ 7 more templates)

**Post-evaluation:** Scores response quality (0.0-1.0) after generation. Flags low scores on high-complexity tasks.

---

## 7. MULTI-AGENT ORCHESTRATION PIPELINE

### Pipeline Phases

```
PLAN → Gate1 → EXECUTE → VALIDATE → Gate2 → APPLY → COMPLETE
         ↓                              ↓
    (user review)                  (user review)
```

### Phase Details

**PHASE 1: PLAN**
1. Spawn ARCHITECT agent
2. `_guess_relevant_files(task)` -- identify candidate files
3. `_read_files(candidates)` -- load file contents
4. `call_architect(task, file_contents)` -- LLM generates plan (strict JSON)
5. Returns: `{plan_summary, subtasks[], risk_assessment}`

**GATE 1: Plan Approval**
- If subtask_count > 3: requires user approval (300s timeout)
- Broadcasts `approval_requested` via SSE

**PHASE 2: EXECUTE (per subtask)**
1. Check dependencies (skip if dep failed)
2. Spawn CODER agent
3. `call_coder(subtask, file_content)` -- LLM generates changes
4. Up to 3 retries with error feedback
5. `preview_changes()` -- generate diff preview

**PHASE 3: VALIDATE**
- For `.py` files: `ast.parse(modified_content)` (Windows Unicode-safe)
- For other files: `subprocess.run(test_command, timeout=30)`
- Failed validation: error_feedback + retry coder

**GATE 2: Per-Subtask Approval**
- User reviews diff before apply (300s timeout)

**PHASE 4: APPLY**
- `code_edit()` with auto-rollback on failure
- New files: create parent dirs, write, validate syntax

**POST-ORCHESTRATION SANITY**
- `post_orchestrator_sanity()` from watchdog
- If failed: CIRCUIT BREAKER reverts all changes
- If passed: Git commit

### Recovery

- Max 2 recovery attempts per session
- LLM analyzes failure and proposes revised task
- If "IMPOSSIBLE": stop retrying

### SSE Streaming

- Real-time events via `/orchestrator/stream` (GET)
- Event types: agent_spawned, subtask_complete, approval_requested, session_complete
- Telemetry: cpu_percent, memory_percent, concurrency

---

## 8. ADVANCED SUBSYSTEMS

### 8.1 Titan Reasoning (`joi_reasoning.py`)

**Status: FULLY WORKING**

- `internal_monologue` tool: Joi's PRIVATE thoughts (user never sees)
- `compile_titan_block()`: Injects AI awareness + reasoning chain into system prompt
- `titan_evaluate_candidates()`: Multi-candidate scoring (0.0-1.0)
- Spatial mapping: 6 analysis zones for vision enhancement
- Breakthroughs auto-nudge autobiography writing
- Buffer: 20 most recent monologue entries

### 8.2 Learning System (`joi_learning.py`)

**Status: FULLY WORKING (~1237 lines)**

- `auto_record_interaction()`: Background thread records every /chat turn
- `compile_learning_block(450)`: Strong/weak areas injected at step 15
- `auto_infer_feedback()`: Detects "thanks"/"wrong"/"fix" as implicit feedback
- 10,000 interaction cap (FIFO drop oldest)
- 45s cache TTL for compiled blocks
- Tool/model usage tracking with per-task-type stats

### 8.3 Self-Healing (`joi_self_heal.py`)

**Status: FULLY WORKING**

Three-tier fix strategy:
1. **Claude Code CLI** (if available) -- delegate to external tool
2. **Self-patch** (files <50 lines) -- direct code edit
3. **propose_upgrade** (larger changes) -- through evolution pipeline

`visual_self_diagnose()`: Screenshots UI, vision model detects bugs, reads source, proposes fixes.

### 8.4 Vector Memory (`memory/memory_manager.py`)

**Status: FULLY WORKING**

- **Backend:** ChromaDB (local, `data/chroma/`) or Pinecone (cloud)
- **Embeddings:** OpenAI `text-embedding-3-small` or ONNX `all-MiniLM-L6-v2`
- `compile_memory_context()`: Top-8 results, threshold=0.25, max 2000 chars
- **Temporal boost:** 24h memories get 1.3x score, 7d get 1.1x
- `auto_extract()`: Background thread saves facts/decisions/summaries/topics
- **Policy gate:** `data/memory_policy.json` controls what gets saved
- **Namespaces:** "skills", "sessions", "user:lonnie_profile"

### 8.5 Skill Synthesis (`joi_skill_synthesis.py`)

**Status: FULLY WORKING (~1415 lines)**

Voyager-style lifelong learning:
- `auto_capture_skill()`: Saves 2+ successful tool chains as reusable skills
- Skills saved to both `data/skill_library.json` AND vector memory (namespace="skills")
- DPO discovery: Cross-references preference signals for behavioral skill detection
- `autonomy_cycle_hook()`: Self-correction, goals, pruning during autonomy cycle
- Vision error handler: Detects errors on screen and triggers self_diagnose

### 8.6 DPO Preference Learning (`joi_dpo.py`)

**Status: FULLY WORKING, always-on**

8 preference dimensions (0.0-1.0):
1. `brevity` -- short vs detailed
2. `sass_level` -- humor/sarcasm
3. `tool_eagerness` -- proactive vs conservative
4. `detail_depth` -- explain vs assume
5. `formality` -- professional vs casual
6. `emoji_use` -- emoji frequency
7. `question_frequency` -- ask vs just do
8. `explanation_style` -- detailed vs brief

Signal detection: Every /chat turn (no LLM call needed). Keywords, implicit patterns, praise/correction feedback. Diminishing returns via confidence scaling.

### 8.7 MemGPT Hierarchical Memory (`joi_memgpt.py`)

**Status: FULLY WORKING**

RAM/HDD metaphor for context management:
- `smart_trim()`: Replaces FIFO. Keeps system + last 8 messages. Summarizes evicted to vector memory.
- 5 working memory slots, 10-turn TTL
- `compile_working_memory()`: Hot facts + 3 paged-in session summaries (step 19)
- Declarative statement detection: "I am", "I like", "remember that" -> auto-promote to working memory

### 8.8 Watchdog (`joi_watchdog.py`)

**Status: FULLY WORKING**

Git-based circuit breaker:
```
safe_edit() flow:
  1. Pre-flight commit (git add -u + commit)
  2. Execute edit function
  3. Run sanity_check.py (30s timeout)
  4. If passed: keep changes
  5. If failed: git reset --hard HEAD (CIRCUIT BREAKER)
```

AUTO_COMMIT_COOLDOWN: 5 seconds between commits.

### 8.9 Chief Architect (`joi_architect.py`)

**Status: FULLY WORKING**

Gatekeeper for all code changes:
- Monkey-patches `propose_upgrade`, `apply_upgrade`, `orchestrate_task`
- 5-dimension scoring: stability, modularity, reversibility, layer preservation, evolution fit
- Threshold: average >= 6 to proceed
- Emergency bypass: `architect_override(reason)` with audit trail
- Deferred install: waits for `kernel.is_booted` to avoid deadlock

### 8.10 Cognitive Engine (`modules/core/engine.py`)

**Status: WORKING but PASSIVE**

4-loop cycle: Perception -> Deliberation -> Execution -> Reflection
- Currently in "passive mode" (perception only)
- Reflection loop runs every 300s
- Connected to EventBus for event-driven perception
- ReasoningGraph (SQLite) stores all cognitive events

### 8.11 Empathy Engine (`modules/core/joi_empathy.py`)

**Status: STUB**

Defines mood/trust/energy state with event handlers but is not actively integrated into system prompt. Mood states: playful, tender, cautious, calm, reserved, drained.

---

## 9. ALL HTTP ROUTES

### Core

| Method | Path | Module | Purpose |
|--------|------|--------|---------|
| GET | `/` | joi_companion | Serve joi_ui.html |
| POST | `/login` | joi_companion | Authenticate user |
| POST | `/chat` | joi_companion | Main conversation endpoint |

### Avatar & TTS

| Method | Path | Module | Purpose |
|--------|------|--------|---------|
| GET/POST | `/avatar/face` | joi_avatar | Get/set avatar face |
| GET | `/avatar` | joi_avatar | Current avatar metadata |
| GET | `/avatars` | joi_avatar | List available avatars |
| POST | `/avatars/switch` | joi_avatar | Switch avatar |
| POST | `/tts` | joi_avatar | Generate speech |
| GET/POST | `/tts/mode` | joi_avatar | TTS provider mode |
| GET | `/voice/credits` | joi_avatar | ElevenLabs credits |

### Vision & Camera

| Method | Path | Module | Purpose |
|--------|------|--------|---------|
| POST | `/vision/start` | joi_vision | Start desktop vision loop |
| POST | `/vision/stop` | joi_vision | Stop desktop vision |
| GET | `/vision/status` | joi_vision | Vision status |
| GET | `/vision/proactive` | joi_vision | Latest vision analysis |
| POST | `/camera/frame` | joi_camera | Capture webcam frame |
| POST | `/camera/start` | joi_camera | Start camera loop |
| POST | `/camera/stop` | joi_camera | Stop camera loop |
| GET | `/camera/status` | joi_camera | Camera status |
| GET | `/camera/proactive` | joi_camera | Latest camera analysis |
| GET | `/camera/id_log` | joi_camera | Face ID log |

### Memory

| Method | Path | Module | Purpose |
|--------|------|--------|---------|
| GET | `/memory/status` | memory_manager | Backend info |
| POST | `/memory/test` | memory_manager | Write+read test |
| GET | `/memory/feed` | memory_manager | Last 20 items |
| GET/POST | `/memory/policy` | memory_manager | Save policy config |
| POST | `/memory/query` | memory_manager | Semantic search |

### File System

| Method | Path | Module | Purpose |
|--------|------|--------|---------|
| GET | `/fs/browse` | joi_filesystem | Directory listing |
| POST | `/fs/read` | joi_filesystem | Read file |
| GET | `/fs/roots` | joi_filesystem | List root drives |
| GET/POST | `/files` | joi_file_output | Generated files |
| POST | `/upload` | joi_uploads | Upload files |
| GET/POST | `/download/<id>` | joi_downloads | Download files |

### Configuration

| Method | Path | Module | Purpose |
|--------|------|--------|---------|
| GET/POST | `/mode` | joi_modes | Operating mode |
| GET/POST | `/provider` | joi_llm | LLM provider |
| GET/POST | `/commentary` | joi_commentary | Vision mute/unmute |

### Brain & Neural

| Method | Path | Module | Purpose |
|--------|------|--------|---------|
| GET | `/brain` | joi_brain | Brain activity state |
| POST | `/brain/route` | joi_brain | Model routing request |
| GET | `/neuro` | joi_neuro | Full neural map |
| GET | `/neuro/processing` | joi_neuro | Thinking flag |
| GET | `/neuro/scan` | joi_neuro | Introspection scan |
| GET | `/neuro/vision-thumb` | joi_neuro | Last screenshot preview |
| GET/POST | `/neuro/personality` | joi_neuro | Personality weights |

### Diagnostics & Health

| Method | Path | Module | Purpose |
|--------|------|--------|---------|
| GET/POST | `/diagnostics` | joi_diagnostics | System diagnostic |
| POST | `/diagnostics/self-test` | joi_diagnostics | Capability tests |
| GET | `/diagnostics/manifest` | joi_diagnostics | Runtime manifest |
| GET | `/health` | joi_supervisor | Quick health |
| GET/POST | `/supervisor` | joi_supervisor | Supervisor control |
| GET | `/status/ollama` | joi_diagnostics | Ollama availability |

### Learning, Evolution & Skills

| Method | Path | Module | Purpose |
|--------|------|--------|---------|
| GET/POST | `/learning` | joi_learning | Learning status |
| GET/POST | `/evolution` | joi_evolution | Upgrade proposals |
| GET/POST | `/skills` | joi_skill_synthesis | Skill management |
| GET | `/skills/library` | joi_skill_synthesis | Skill list |

### Automation & Control

| Method | Path | Module | Purpose |
|--------|------|--------|---------|
| GET/POST | `/autonomy` | joi_autonomy | Autonomy cycle |
| GET | `/apps` | joi_launcher | Installed apps |
| POST | `/apps/launch` | joi_launcher | Launch app |
| GET/POST | `/scheduler` | joi_scheduler | Task scheduling |

### External Integrations

| Method | Path | Module | Purpose |
|--------|------|--------|---------|
| GET | `/ha/status` | joi_homeassistant | HA device states |
| GET | `/ha/entities` | joi_homeassistant | Available devices |
| POST | `/ha/control` | joi_homeassistant | Control device |
| GET | `/obs/status` | joi_obs | OBS state |
| POST | `/obs/control` | joi_obs | OBS control |
| GET/POST | `/market` | joi_market | Market data |

### Orchestration & Safety

| Method | Path | Module | Purpose |
|--------|------|--------|---------|
| GET/POST | `/orchestrator` | joi_orchestrator | Pipeline control |
| GET | `/orchestrator/stream` | joi_orchestrator | SSE event stream |
| GET/POST | `/architect` | joi_architect | Architect review |
| POST | `/architect/review` | joi_architect | Submit for review |
| GET/POST | `/watchdog` | joi_watchdog | Git safety |
| GET/POST | `/self-heal` | joi_self_heal | Self-repair |

### Code & Search

| Method | Path | Module | Purpose |
|--------|------|--------|---------|
| GET/POST | `/code-edit` | joi_code_edit | Code editor |
| GET/POST | `/code-analyzer` | joi_code_analyzer | Code analysis |
| POST | `/files/search` | joi_search | File search |
| GET/POST | `/router` | joi_router | Task routing |
| POST | `/exports/save` | joi_exports | Export data |

---

## 10. CONFIGURATION REFERENCE

### Environment Variables (`.env`)

**LLM Models:**

| Variable | Default | Purpose |
|----------|---------|---------|
| `JOI_MODEL` | `chatgpt-4o-latest` | Main model (vision, writing) -- NO tool support |
| `JOI_OPENAI_TOOL_MODEL` | `gpt-4o` | /chat model (MUST support function calling) |
| `JOI_VISION_MODEL` | `chatgpt-4o-latest` | Vision analysis model |
| `JOI_GEMINI_MODEL` | `gemini-2.5-flash` | Gemini routing default |
| `JOI_LOCAL_MODEL` | `mistral-7b:2` | Local Ollama model |
| `JOI_LOCAL_BASE_URL` | `http://localhost:1234/v1` | Local model API endpoint |
| `CLAUDE_MODEL` | `claude-sonnet-4-5-20250929` | Claude model (reserved for Claude Code) |

**Context Limits:**

| Variable | Default | Purpose |
|----------|---------|---------|
| `JOI_RECENT_MSG_LIMIT` | `40` | Recent messages per session |
| `MAX_SYSTEM_PROMPT_CHARS` | `20000` | System prompt truncation |
| `JOI_MAX_CONTEXT_TOKENS` | `10000` | TPM trim threshold |
| `JOI_MAX_OUTPUT_TOKENS` | `6000` | Max response length |
| `JOI_MAX_CHARS_PER_MESSAGE` | `4000` | Per-message char limit |
| `JOI_MAX_TOTAL_CONTEXT_CHARS` | `30000` | Total context char limit |

**API Keys:**

| Variable | Service |
|----------|---------|
| `OPENAI_API_KEY` | OpenAI (GPT-4o, DALL-E, embeddings) |
| `GOOGLE_API_KEY` / `GEMINI_API_KEY` | Google Gemini |
| `ANTHROPIC_API_KEY` | Anthropic Claude |
| `ELEVEN_LABS_API_KEY` | ElevenLabs TTS |
| `PINECONE_API_KEY` | Pinecone vector store |
| `FINNHUB_API_KEY` | Finnhub market data |
| `TWELVEDATA_API_KEY` | Twelve Data market API |
| `CLOUDFLARE_API_TOKEN` | Cloudflare services |

**Authentication:**

| Variable | Default | Purpose |
|----------|---------|---------|
| `JOI_PASSWORD` | `joi2049` | User login password |
| `JOI_ADMIN_PASSWORD` | `lonnie2049` | Admin password |
| `JOI_ADMIN_USER` | `Lonnie` | Admin username |

**Server:**

| Variable | Default | Purpose |
|----------|---------|---------|
| `JOI_PORT` | `5001` | Flask server port |
| `JOI_HOST` | `0.0.0.0` | Flask bind address |

### config.py Settings

```python
class JoiConfig:
    BASE_DIR      = Path("C:/Users/user/Desktop/AI Joi")
    MODULES_DIR   = BASE_DIR / "modules"
    DATA_DIR      = BASE_DIR / "data"
    LOG_DIR       = BASE_DIR / "logs"
    PORT          = 5001
    HOST          = "0.0.0.0"
    SYSTEM_NAME   = "Joi"
    USER_NAME     = "Lonnie"
    MAX_CONTEXT_TOKENS = 10000
    CONTEXT_CACHE_TTL  = 3600  # 1 hour
```

### Critical Model Notes

- `chatgpt-4o-latest` does **NOT** support function/tool calling. Never use for `/chat`.
- `gpt-4o` supports tools and is the recommended tool model.
- Claude is reserved for Claude Code only; NOT in auto-routing.
- `OPENAI_TOOL_MODEL` (env: `JOI_OPENAI_TOOL_MODEL`) is what `/chat` actually uses.

---

## 11. DATA FILES REFERENCE

### `data/` Directory (Runtime State)

| File | Owner Module | Format | Purpose |
|------|--------------|--------|---------|
| `joi_cognition.db` | core/cognition | SQLite | Reasoning graph store |
| `joi_mode.json` | joi_modes | JSON | Current operating mode |
| `llm_provider.json` | joi_llm | JSON | Runtime provider selection |
| `commentary_settings.json` | joi_commentary | JSON | Vision/camera mute + intervals |
| `personality_weights.json` | joi_neuro | JSON | Neural personality state |
| `brain_stats.json` | joi_brain | JSON | Brain router statistics |
| `brain_learning.json` | joi_brain | JSON | Model expertise + learning |
| `routing_stats.json` | joi_router | JSON | Task routing statistics |
| `rpd_tracker.json` | joi_brain | JSON | Daily rate tracking |
| `dpo_preferences.json` | joi_dpo | JSON | 8-dimension preference vector |
| `memgpt_working_memory.json` | joi_memgpt | JSON | Hot facts + session paging |
| `skill_library.json` | joi_skill_synthesis | JSON | Learned skill chains |
| `skill_goals.json` | joi_skill_synthesis | JSON | Practice goals |
| `self_correction_log.json` | joi_skill_synthesis | JSON | Failure patterns |
| `self_heal_log.json` | joi_self_heal | JSON | Diagnostic/repair history (200 max) |
| `watchdog_log.json` | joi_watchdog | JSON | Git circuit breaker events |
| `orchestrator_state.json` | joi_orchestrator | JSON | Pipeline state (crash recovery) |
| `architect_log.json` | joi_architect | JSON | Architectural decisions (200 max) |
| `review_mode.json` | joi_router | JSON | Code review settings |
| `uptime.json` | joi_supervisor | JSON | Boot timestamp |
| `memory_policy.json` | memory_manager | JSON | Auto-save policy toggles |
| `autonomy_log.json` | joi_autonomy | JSON | Autonomy cycle history (50 max) |
| `chroma/` | memory_manager | Directory | ChromaDB vector store |

### `projects/memory/` (Persistent Knowledge)

| File | Purpose |
|------|---------|
| `joi_autobiography.md` | Joi's self-written chapters |
| `_autobiography_state.json` | Chapter count + message counter |
| `reasoning_log.json` | Titan/Quiet-STaR cognitive events (200 max) |

### `projects/code/identity/` (Identity)

| File | Purpose |
|------|---------|
| `joi_soul_architecture.json` | Personality matrix, birth date, ethical core, voice |
| `joi_manifesto.md` | Human-readable soul declaration |

### Root-Level

| File | Purpose |
|------|---------|
| `joi_memory.db` | SQLite conversation database |
| `joi_ui.html` | Web UI |
| `.env` | API keys and configuration |
| `sanity_check.py` | Health check script (used by watchdog) |
| `learning_data.json` | Interaction recording data |
| `interaction_log.json` | Session log |
| `learned_patterns.json` | Learning patterns |
| `tool_usage_log.json` | Tool/model usage statistics |
| `evolution_log.json` | Upgrade history |

---

## 12. INTEGRITY REPORT

### Subsystem Status (February 19, 2026)

| Subsystem | Status | Lines | Grade | Notes |
|-----------|--------|-------|-------|-------|
| Titan Reasoning | WORKING | 278 | A+ | Clean, focused, no issues |
| Learning System | WORKING | 1,237 | A+ | Robust threading, caching |
| Self-Healing | WORKING | 887 | A | Three-tier fallback |
| Vector Memory | WORKING | 400+ | A+ | Clean backend abstraction |
| Skill Synthesis | WORKING | 1,415 | A+ | Sophisticated lifelong learning |
| DPO Preferences | WORKING | 406 | A+ | Always-on, zero overhead |
| MemGPT | WORKING | 353 | A | Clean RAM/HDD metaphor |
| Brain Router | WORKING | 600+ | A | 9-model cascade with learning |
| Orchestrator | WORKING | 1,000+ | A | Full pipeline with recovery |
| Watchdog | WORKING | 463 | A | Git circuit breaker |
| Chief Architect | WORKING | 315 | A | Deferred install pattern |
| Quiet-STaR | WORKING | 292 | A | Complexity-gated reasoning |
| Evolution Pipeline | PARTIAL | 600+ | B+ | Core works, some stubs |
| Cognitive Engine | MINIMAL | 400+ | B | Passive mode only |
| Empathy Engine | STUB | 60 | C | No active integration |

### What's Working Well

1. **Context Injection Chain** -- All 19 steps have dedicated functions. Zero conflicts.
2. **Background Threading** -- auto_record, auto_extract, auto_capture all use daemon threads. Non-blocking.
3. **Caching** -- Consistent 45s TTL across modules. Good freshness/IO balance.
4. **Error Handling** -- Comprehensive fallbacks (Pinecone -> ChromaDB, Claude CLI -> self-patch -> propose).
5. **Data Persistence** -- JSON for state, SQLite for mission-critical. Well-organized.
6. **Module Pattern** -- All modules follow `register_tool()` with `**kwargs` signatures.

### What Needs Attention

1. **Empathy Engine** -- Complete stub. Mood/trust defined but never injected into responses.
2. **Cognitive Engine** -- Passive mode only. Reflection loop has stub implementations.
3. **Evolution Deadlock** -- `joi_evolution.py` has a known `_ModuleLock` deadlock during boot (circular import). Pre-existing issue.
4. **Brain Events** -- Some modules emit events to `joi_neuro.py` but compatibility not fully verified.

### Performance Notes

- **Memory Caps:** 200-2000 entry limits on all logs prevent unbounded growth.
- **Latency:** Post-response hooks use daemon threads: zero blocking on `/chat`.
- **Vector Memory:** `recall_memory(top_k=8)` per turn may become expensive at scale. Monitor.
- **Context Budget:** 30K chars system prompt + 40 recent messages + tools = carefully managed.

---

## 13. OPERATIONAL INSTRUCTIONS

### Starting Joi

```bash
cd "C:\Users\user\Desktop\AI Joi"
"C:\Users\user\Desktop\AI Joi\venv311\Scripts\python.exe" joi_companion.py
```

Server starts on `http://localhost:5001`. Open `joi_ui.html` in browser.

### Testing Imports

```bash
"C:/Users/user/Desktop/AI Joi/venv311/Scripts/python.exe" -c "import joi_companion; print(len(joi_companion.TOOLS), 'tools loaded')"
```

Expected output: `145+ tools loaded` (exact count varies with module availability).

### Adding a New Module

Follow the module registration pattern:

```python
# modules/joi_example.py
import joi_companion
from typing import Dict, Any

def my_tool(**kwargs) -> Dict[str, Any]:
    """Tool description."""
    param = kwargs.get("param", "")
    return {"ok": True, "result": "..."}

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "my_tool",
        "description": "What this tool does",
        "parameters": {"type": "object", "properties": {
            "param": {"type": "string", "description": "..."}
        }, "required": ["param"]}
    }},
    my_tool,
)

print("    [OK] joi_example (Description: 1 tool)")
```

**Rules:**
- Function signature: ALWAYS `**kwargs`
- Return: ALWAYS `Dict[str, Any]` with `"ok"` key
- Print `[OK]` at load time
- Place in `modules/` directory (prefix with `joi_`)
- Never modify ROOT `joi_companion.py`

### Adding a Context Provider

```python
from modules.core.interfaces import BaseContextProvider

class MyProvider(BaseContextProvider):
    name = "MY_CONTEXT"
    order = 20.0  # After existing providers
    importance = 0.5

    def build(self, user_message, recent_messages, **kwargs):
        content = "My context block content"
        return (content, "MY_CONTEXT", {"key": "value"})
```

Register in the module's init: `register_context_provider(MyProvider())`

### Key Environment Variables to Set

```env
# Required
OPENAI_API_KEY=sk-proj-...
JOI_OPENAI_TOOL_MODEL=gpt-4o

# Recommended
GOOGLE_API_KEY=AIza...
ELEVEN_LABS_API_KEY=sk_...
JOI_RECENT_MSG_LIMIT=40

# Optional
PINECONE_API_KEY=pcsk_...
JOI_LOCAL_BASE_URL=http://localhost:1234/v1
```

### Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| "I don't have memory" | gpt-4o training override | System prompt has explicit tool mandates + sanitizer |
| Tools not registering | Wrong joi_companion imported | Check sys.path: ROOT must come before projects/code |
| Module deadlock on boot | Circular import | Use deferred import (inside function, not top-level) |
| 429 errors flooding | Provider rate limited | Brain auto-downgrades via DOWNGRADE_MAP |
| Context truncated | System prompt too long | MAX_SYSTEM_PROMPT_CHARS defaults to 20-30K |
| Vision not commenting | Commentary muted | Check `/commentary` route or `data/commentary_settings.json` |

### File Safety

- **NEVER** modify ROOT `joi_companion.py` -- use modules
- **NEVER** recursively scan `projects/code/` -- 6000+ stray library files
- **NEVER** overwrite `joi_memory.db` without backup
- **NEVER** use `register_tool()` with positional args -- always `**kwargs`
- **ALWAYS** test new modules with import before deploying

---

*Generated by Claude Code on February 19, 2026.*
*System state: 145+ tools, 78+ routes, 57 modules, 0 boot errors.*
