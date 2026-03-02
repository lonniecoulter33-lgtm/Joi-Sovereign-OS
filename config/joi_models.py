"""
JOI CENTRAL MODEL CONFIGURATION — Paid Tier Update (March 2026)
Single source of truth for all LLM usage.

Do not hardcode models anywhere else.
All routing must reference this file.

Model Tiers (updated March 1, 2026 — PAID TIERS ACTIVE):
  PRIMARY BRAIN  -- GPT-5               : Complex logic, architecture, planning
  LARGE CONTEXT  -- Gemini 2.5 Pro      : 2M context — entire codebases, large files
  FAST TOOLS     -- o4-mini / Gemini 2.5 Flash : Tool routing, quick tasks
  DEBUGGING      -- Gemini 2.0 Flash Thinking : Structured reasoning for failure analysis
  FALLBACK       -- GPT-5-mini / Gemini 2.5 Flash : Always-on fallback

Paid Tier Status:
  OpenAI: Tier 2 — 1,000,000 TPM flagship / 10,000,000 TPM mini
  Gemini: Paid Tier 1 — 150-300 RPM, data NOT used for training
"""

# -----------------------------
# ALLOWED MODELS (enforced everywhere)
# -----------------------------
ALLOWED_GEMINI = (
    "gemini-2.5-pro",              # T1: PRIMARY — 2M context, paid tier, best quality
    "gemini-2.5-flash",            # T2: Fast, high quality — 1M context
    "gemini-2.0-flash-thinking",   # T3: Structured reasoning / debugging (Flash family)
    "gemini-2.5-flash-lite",       # T4: Emergency rate-limit fallback
)

ALLOWED_OPENAI = (
    "gpt-5", "gpt-5-mini", "gpt-5-nano",
    "gpt-4.1",                     # 1M context — full file/codebase ingestion
    "gpt-4.1-mini",                # 1M context — cheaper variant
    "o3-mini", "o4-mini",
    "gpt-4o", "gpt-4o-mini",
)

# Legacy model names -> modern replacement
GEMINI_MODEL_ALIASES = {
    "gemini-2.5-pro":           "gemini-2.5-pro",           # canonical
    "gemini-2.5-pro-preview":   "gemini-2.5-pro",
    "gemini-2.5-flash":         "gemini-2.5-flash",         # canonical
    "gemini-2.5-flash-lite":    "gemini-2.5-flash-lite",    # canonical
    "gemini-2.0-flash-thinking":"gemini-2.0-flash-thinking",# canonical
    # Legacy pro aliases -> paid Pro now
    "gemini-3-pro-preview":     "gemini-2.5-pro",
    "gemini-1.5-pro":           "gemini-2.5-pro",
    # Legacy flash names
    "gemini-1.5-flash":         "gemini-2.5-flash",
    "gemini-2-flash":           "gemini-2.5-flash",
    "gemini-2.0-flash":         "gemini-2.5-flash",
    "gemini-2.0-flash-001":     "gemini-2.5-flash",
    "gemini-3-flash":           "gemini-2.5-flash",
    "gemini-3-flash-preview":   "gemini-2.5-flash",
    "gemini-2.5-flash-preview": "gemini-2.5-flash",
    # Thinking aliases
    "gemini-2.0-flash-thinking-exp": "gemini-2.0-flash-thinking",
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

# Thinking level tokens per model (Gemini thinking models)
GEMINI_THINKING_BUDGETS = {
    "gemini-2.5-pro":             {"low": 512, "medium": 2048, "high": 8000},
    "gemini-2.5-flash":           {"low": 256, "medium": 1024, "high": 4000},
    "gemini-2.0-flash-thinking":  {"low": 512, "medium": 2048, "high": 8000},
    "gemini-2.5-flash-lite":      {"low": 0,   "medium": 0,    "high": 512},
}

# Context window map (tokens) — used for dynamic 1M routing decisions
MODEL_CONTEXT_WINDOWS = {
    "gemini-2.5-pro":            2_000_000,
    "gemini-2.5-flash":          1_000_000,
    "gemini-2.0-flash-thinking": 1_000_000,
    "gemini-2.5-flash-lite":       500_000,
    "gpt-5":                       128_000,
    "gpt-5-mini":                  128_000,
    "gpt-5-nano":                   32_000,
    "gpt-4.1":                   1_000_000,
    "gpt-4.1-mini":              1_000_000,
    "o4-mini":                     128_000,
    "o3-mini":                     128_000,
    "gpt-4o":                      128_000,
    "gpt-4o-mini":                 128_000,
}

# ── Gemini Context Caching (Paid Tier) ───────────────────────────────────
# When enabled, large prompts (>32k tokens) use Gemini's Cached Content API.
# This can reduce costs by 90%+ on repeated large-context calls (e.g., books,
# large codebases). Override via JOI_GEMINI_CONTEXT_CACHE env var.
import os as _os
GEMINI_CONTEXT_CACHE_ENABLED = _os.getenv("JOI_GEMINI_CONTEXT_CACHE", "1").strip() == "1"
GEMINI_CONTEXT_CACHE_TTL_SECONDS = int(_os.getenv("JOI_GEMINI_CACHE_TTL", "3600"))  # 1 hour default
GEMINI_CONTEXT_CACHE_MIN_TOKENS = int(_os.getenv("JOI_GEMINI_CACHE_MIN_TOKENS", "32768"))  # 32k min

# Legacy thinking level strings
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

# Gemini model roles — Paid Tier 1 routing
GEMINI_MODELS = {
    "primary":   "gemini-2.5-pro",         # T1: Best quality, 2M context (PAID)
    "large":     "gemini-2.5-pro",         # T1: Alias for large-context routing
    "thinking":  "gemini-2.0-flash-thinking",# T2: Debugging, structured reasoning
    "standard":  "gemini-2.5-flash",       # T3: Fast, high quality, 1M context
    "general":   "gemini-2.5-flash",       # T3: Backward-compat alias
    "fallback":  "gemini-2.5-flash",       # T3: Fallback (Flash is free-tier-safe too)
    "emergency": "gemini-2.5-flash-lite",  # T4: Rate-limit last resort only
}

OPENAI_MODELS = {
    "architect":    "gpt-5",        # T1: Complex planning, deep reasoning — flagship
    "reasoning":    "o4-mini",      # T1: Orchestration, validation, tool routing
    "coding":       "gpt-5",        # T1: Code edits on paid tier (use best quality)
    "worker":       "gpt-5-mini",   # T2: Swarm workers — 10M TPM, never rate-limits
    "fast":         "gpt-5-nano",   # T3: Simple transforms, scaffolding — cheapest
    "long_context": "gpt-4.1",      # Special: 1M token window, full file/codebase reads
    "vision":       "gpt-4o",       # Special: image/screenshot analysis (multimodal)
    "vision_fast":  "gpt-4o-mini",  # Special: cheaper multimodal fallback
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
        "model":    ("openai", "gpt-5"),
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
        "fallback": ("openai", "gpt-5"),
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
        "model":    ("openai", "gpt-5"),
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
        "primary":  ("openai", "gpt-5"),         # Up from gpt-4o — paid tier allows best
        "fallback": ("openai", "gpt-5-mini"),
    },
    "validation": {
        "primary":  ("openai", "o4-mini"),
        "fallback": ("openai", "o3-mini"),
    },
    "chat": {
        "primary":  ("gemini", "gemini-2.5-pro"),     # Paid: use Pro for all chat
        "fallback": ("gemini", "gemini-2.5-flash"),
    },
    "debugging": {                                    # NEW: dedicated debugging route
        "primary":  ("gemini", "gemini-2.0-flash-thinking"),
        "fallback": ("openai", "o4-mini"),
    },
    "large_context": {                                # NEW: 1M-token read tasks
        "primary":  ("gemini", "gemini-2.5-pro"),
        "fallback": ("openai", "gpt-4.1"),
    },
    "exploration": {
        "primary":  ("openai", "gpt-4.1"),            # Up from gpt-4.1-mini — full 1M
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
    # Gemini — Paid Tier 1
    "gemini-2.5-pro":             "PRIMARY BRAIN: 2M context, highest quality. Best for large files, full codebases, complex reasoning. PAID tier.",
    "gemini-2.5-flash":           "FAST BRAIN: 1M context, fast, high quality. General purpose and fallback.",
    "gemini-2.0-flash-thinking":  "DEBUGGER: Flash Thinking — structured reasoning for failure analysis, whys, and deep logic chains.",
    "gemini-2.5-flash-lite":      "EMERGENCY: Rate-limit last resort only. Fastest/cheapest Gemini.",
    # OpenAI — Tier 2
    "gpt-5":        "Best OpenAI flagship — complex planning, coding, architecture, deep reasoning. Tier 2 capacity.",
    "gpt-5-mini":   "Swarm workers — 10M TPM on Tier 2, never rate-limits parallel runs, great value.",
    "gpt-5-nano":   "Fastest/cheapest for simple transforms, scaffolding, data cleanup.",
    "o4-mini":      "Reasoning chains, validation, tool routing, orchestration logic.",
    "o3-mini":      "Heavy reasoning fallback when o4-mini unavailable.",
    "gpt-4.1":      "1M token context window — use when reading entire files or codebases (OpenAI alternative to Gemini Pro).",
    "gpt-4.1-mini": "1M token context window, cheaper variant. Use for exploration and moderate-sized file reads.",
    "gpt-4o":       "Vision/screenshots, image analysis, multimodal tasks.",
    "gpt-4o-mini":  "Cheaper multimodal fallback for vision tasks.",
}

# -----------------------------
# GLOBAL FAILOVER RULES
# -----------------------------

MAX_RETRIES = 3
TIMEOUT_SECONDS = 60
ENABLE_LOGGING = True
ENABLE_MODEL_DEBUG = True
