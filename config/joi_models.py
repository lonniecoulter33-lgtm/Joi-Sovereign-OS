"""
JOI CENTRAL MODEL CONFIGURATION
Single source of truth for all LLM usage.

Do not hardcode models anywhere else.
All routing must reference this file.

Model Tiers (updated Feb 21, 2026):
  PRIMARY BRAIN  -- Gemini 2.5 Flash    : Best available on free tier, 1M context
  EMERGENCY      -- Gemini 2.5 Flash Lite: Rate-limit emergency only (~1000 RPD free tier)
  SPECIALIST     -- OpenAI models        : Tool calling, vision, code editing, reasoning chains
  LOCAL          -- Ollama               : Offline / private/sensitive use only (not cloud)

NOTE: gemini-2.5-pro requires a paid API tier (limit: 0 on free tier).
      Do NOT add it back until billing is enabled in Google AI Studio.
"""

# -----------------------------
# ALLOWED MODELS (enforced everywhere)
# -----------------------------
ALLOWED_GEMINI = (
    "gemini-2.5-flash",       # T1: Primary brain — best available on free tier, 1M context
    "gemini-2.5-flash-lite",  # T2: Emergency only — ~1000 RPD free tier hard cap
)

ALLOWED_OPENAI = (
    "gpt-5", "gpt-5-mini", "gpt-5-nano",
    "o3-mini", "o4-mini",
    "gpt-4.1-mini", "gpt-4o", "gpt-4o-mini",
    # "gpt-5-codex-mini",  # Returns 404 — removed until OpenAI makes it available
)

# Legacy model names -> modern replacement
# NOTE: all pro/old names route to gemini-2.5-flash (Pro requires paid tier — limit: 0 on free)
GEMINI_MODEL_ALIASES = {
    "gemini-2.5-flash":         "gemini-2.5-flash",     # canonical
    "gemini-2.5-flash-lite":    "gemini-2.5-flash-lite",# canonical
    # Pro aliases -> Flash (Pro is inaccessible on free tier)
    "gemini-2.5-pro":           "gemini-2.5-flash",
    "gemini-2.5-pro-preview":   "gemini-2.5-flash",
    "gemini-3-pro-preview":     "gemini-2.5-flash",
    "gemini-1.5-pro":           "gemini-2.5-flash",
    # Legacy flash names
    "gemini-1.5-flash":         "gemini-2.5-flash",
    "gemini-2-flash":           "gemini-2.5-flash",
    "gemini-2.0-flash":         "gemini-2.5-flash",
    "gemini-2.0-flash-001":     "gemini-2.5-flash",
    "gemini-3-flash":           "gemini-2.5-flash",
    "gemini-3-flash-preview":   "gemini-2.5-flash",
    "gemini-2.5-flash-preview": "gemini-2.5-flash",
    # Old lite aliases
    "gemini-2.5-flash-lite-preview": "gemini-2.5-flash-lite",
}

OPENAI_MODEL_ALIASES = {
    "chatgpt-4o-latest": "gpt-4o",
    "gpt-4o-latest":     "gpt-4o",
    "o3":                "o4-mini",   # full o3 -> o4-mini fallback
    "gpt-4":             "gpt-5-mini",
    "gpt-4-turbo":       "gpt-5-mini",
}

# Thinking level tokens per model (Gemini 2.5 thinking models)
GEMINI_THINKING_BUDGETS = {
    "gemini-2.5-flash":       {"low": 256, "medium": 1024, "high": 4000},
    "gemini-2.5-flash-lite":  {"low": 0,   "medium": 0,    "high": 512},
    # Pro is inaccessible on free tier — alias to Flash budgets just in case
    "gemini-2.5-pro":         {"low": 256, "medium": 1024, "high": 4000},
}

# Legacy thinking level strings (used by some callers)
GEMINI_DEFAULT_THINKING_LEVEL = "low"
GEMINI_COMPLEX_THINKING_LEVEL  = "medium"
GEMINI_HEAVY_THINKING_LEVEL    = "high"


def sanitize_gemini_model(name: str) -> str:
    """Return an allowed Gemini model id. Defaults to gemini-2.5-flash (primary on free tier)."""
    if not name or not name.strip():
        return "gemini-2.5-flash"
    n = name.strip().lower()
    if n in ALLOWED_GEMINI:
        return n
    if n in GEMINI_MODEL_ALIASES:
        mapped = GEMINI_MODEL_ALIASES[n]
        if mapped in ALLOWED_GEMINI:
            return mapped
    # Default to primary brain
    return "gemini-2.5-flash"


def sanitize_openai_model(name: str) -> str:
    """Return an allowed OpenAI model id."""
    if not name or not name.strip():
        return "gpt-5-mini"
    n = name.strip().lower()
    if n in ALLOWED_OPENAI:
        return n
    if n in OPENAI_MODEL_ALIASES:
        return OPENAI_MODEL_ALIASES[n]
    return "gpt-5-mini"


def get_thinking_level(task_type: str = "", complexity: str = "") -> str:
    """Return the appropriate Gemini thinking level for a task."""
    if complexity == "high" or task_type in ("planning", "supervisor", "architecture", "research"):
        return GEMINI_HEAVY_THINKING_LEVEL
    if complexity == "medium" or task_type in ("coding", "code_edit", "validation"):
        return GEMINI_COMPLEX_THINKING_LEVEL
    return GEMINI_DEFAULT_THINKING_LEVEL


def get_thinking_budget(model_id: str, level: str) -> int:
    """Return thinking token budget for a specific Gemini model + level combo."""
    budgets = GEMINI_THINKING_BUDGETS.get(model_id, GEMINI_THINKING_BUDGETS["gemini-2.5-flash-lite"])
    return budgets.get(level, 0)


# -----------------------------
# MODEL PROVIDERS
# -----------------------------

# Gemini model roles
# primary  = T1 : best available on free tier, 1M context, primary brain
# emergency= T2 : last resort for rate limits (~1000 RPD free tier hard cap)
# standard/general/fallback = backward-compat aliases -> primary
# NOTE: gemini-2.5-pro has limit: 0 on free tier — do not use until billing enabled
GEMINI_MODELS = {
    "primary":   "gemini-2.5-flash",      # T1: Primary brain (best on free tier, 1M context)
    "standard":  "gemini-2.5-flash",      # T1: Compat alias -> primary
    "emergency": "gemini-2.5-flash-lite", # T2: Emergency only (~1000 RPD)
    # Backward-compat aliases (used by agents, orchestrator, etc.)
    "general":   "gemini-2.5-flash",      # -> primary
    "fallback":  "gemini-2.5-flash-lite", # -> emergency
}

OPENAI_MODELS = {
    "architect":    "gpt-5",        # T1: Planning, complex architecture — best quality
    "reasoning":    "o4-mini",      # T1: Orchestration logic, validation, reasoning chains
    "coding":       "gpt-4o",       # T2: Code edits, Joi codebase (gpt-5-codex-mini = 404)
    "worker":       "gpt-5-mini",   # T2: Swarm workers — 500k TPM, never rate-limits
    "fast":         "gpt-5-nano",   # T3: Simple tasks, data cleanup — cheapest
    "long_context": "gpt-4.1-mini", # Special: 1M token window, reading full files
    "vision":       "gpt-4o",       # Special: image/screenshot analysis
    "vision_fast":  "gpt-4o-mini",  # Special: cheaper multimodal
    "fallback":     "gpt-5-mini",   # Default fallback for any OpenAI role
}

# -----------------------------
# LOCAL MODEL ROLES (Ollama)
# Used when: offline, private/sensitive mode, or explicit set_provider("ollama")
# Never auto-inserted before cloud models.
# -----------------------------
OLLAMA_ROLE_KEYS = {
    "private":   "OLLAMA_PRIVACY_MODEL",  # private/sensitive content
    "general":   "OLLAMA_GENERAL_MODEL",  # offline general fallback
    "large":     "OLLAMA_LARGE_MODEL",    # best local reasoning (gemma3:12b)
    "fast":      "OLLAMA_FAST_MODEL",     # quick responses (gemma3:4b)
    "roleplay":  "OLLAMA_ROLEPLAY_MODEL", # roleplay (dolphin)
    "joi":       "OLLAMA_JOI_MODEL",      # custom Joi model
}

# -----------------------------
# AGENT ROLE MAPPING
# -----------------------------

AGENT_MODEL_MAP = {
    "supervisor_agent": {
        "model":    ("openai", "gpt-5"),
        "fallback": ("openai", "o4-mini"),
    },
    "coder_agent": {
        "model":    ("openai", "gpt-4o"),       # gpt-5-codex-mini returns 404
        "fallback": ("openai", "gpt-5-mini"),
    },
    "validator_agent": {
        "model":    ("openai", "o4-mini"),
        "fallback": ("openai", "o3-mini"),
    },
    "worker_agent": {
        "model":    ("openai", "gpt-5-mini"),
        "fallback": ("openai", "gpt-5-nano"),
    },
    "chat_agent": {
        # Primary brain for general chat: Gemini 2.5 Flash (best on free tier, 1M context)
        # Fallback: Flash Lite (emergency ~1000 RPD)
        "model":    ("gemini", "gemini-2.5-flash"),
        "fallback": ("gemini", "gemini-2.5-flash-lite"),
    },
    "explore_agent": {
        "model":    ("openai", "gpt-4.1-mini"),
        "fallback": ("openai", "gpt-5-mini"),
    },
    "security_agent": {
        "model":    ("openai", "o4-mini"),
        "fallback": ("openai", "gpt-4o"),   # gpt-5-codex-mini returns 404
    },
    "vision_agent": {
        "model":    ("openai", "gpt-4o"),
        "fallback": ("openai", "gpt-4o-mini"),
    },
    "analyst_agent": {
        "model":    ("openai", "gpt-4.1-mini"),
        "fallback": ("openai", "gpt-5-mini"),
    },
    "report_agent": {
        "model":    ("openai", "gpt-5-mini"),
        "fallback": ("gemini", "gemini-2.5-flash"),
    },
    "doc_agent": {
        "model":    ("openai", "gpt-4o"),       # gpt-5-codex-mini returns 404
        "fallback": ("openai", "gpt-5-mini"),
    },
}

# -----------------------------
# TASK -> MODEL ROUTING
# -----------------------------

TASK_MODEL_ROUTING = {
    "planning": {
        "primary":  ("openai", "gpt-5"),
        "fallback": ("openai", "o4-mini"),
    },
    "coding": {
        "primary":  ("openai", "gpt-4o"),       # gpt-5-codex-mini returns 404
        "fallback": ("openai", "gpt-5-mini"),
    },
    "validation": {
        "primary":  ("openai", "o4-mini"),
        "fallback": ("openai", "o3-mini"),
    },
    "chat": {
        # Gemini Flash as primary chat brain (best on free tier, 1M context)
        "primary":  ("gemini", "gemini-2.5-flash"),
        "fallback": ("gemini", "gemini-2.5-flash-lite"),
    },
    "exploration": {
        "primary":  ("openai", "gpt-4.1-mini"),
        "fallback": ("openai", "gpt-5-mini"),
    },
    "security": {
        "primary":  ("openai", "o4-mini"),
        "fallback": ("openai", "gpt-5"),
    },
    "security_audit": {
        "primary":  ("openai", "o4-mini"),
        "fallback": ("openai", "gpt-5"),
    },
    "vision": {
        "primary":  ("openai", "gpt-4o"),
        "fallback": ("openai", "gpt-4o-mini"),
    },
    "quick": {
        "primary":  ("openai", "gpt-5-nano"),
        "fallback": ("openai", "gpt-5-mini"),
    },
    "quick_response": {
        "primary":  ("openai", "gpt-5-nano"),
        "fallback": ("openai", "gpt-5-mini"),
    },
    "supervisor": {
        "primary":  ("openai", "gpt-5"),
        "fallback": ("openai", "o4-mini"),
    },
}

# -----------------------------
# MODEL KNOWLEDGE (injected into system prompt)
# -----------------------------

MODEL_DESCRIPTIONS = {
    # Gemini — free tier routing (Pro requires paid billing, limit: 0 on free tier)
    "gemini-2.5-flash":     "PRIMARY BRAIN: Best available on free tier, 1M context. High quality for all standard work.",
    "gemini-2.5-flash-lite":"EMERGENCY: Rate-limit fallback only (~1000 requests/day). Fast but limited.",
    # OpenAI — specialist roles
    "gpt-5":        "Best OpenAI quality for architect planning, complex analysis, deep reasoning",
    "gpt-5-mini":   "Swarm workers — 500k TPM, never rate-limits parallel runs, great value",
    "gpt-5-nano":   "Fastest/cheapest for simple transforms, data cleanup, scaffolding",
    "o4-mini":      "Reasoning chains, validation, orchestration logic, verification",
    "o3-mini":      "Heavy reasoning fallback when o4-mini unavailable",
    "gpt-4.1-mini": "1M token context window — use when reading very large files",
    "gpt-4o":       "Vision/screenshots, image analysis, code edits, multimodal tasks",
    "gpt-4o-mini":  "Cheaper multimodal fallback for vision tasks",
}

# -----------------------------
# GLOBAL FAILOVER RULES
# -----------------------------

MAX_RETRIES = 3
TIMEOUT_SECONDS = 60
ENABLE_LOGGING = True
ENABLE_MODEL_DEBUG = True
