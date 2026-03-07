"""
modules/joi_context_profiles.py

Context Profiles for Subtask Execution.
=========================================
Layer 4 — Auto-apply OK.

Defines slim context profiles that control how much overhead is included
in subtask prompts. Keyword-based (no LLM calls).

Profiles:
  code_generation  — no identity/memory, ~2K overhead
  code_review      — no identity/memory, ~1.8K overhead
  conversation     — full context
  diagnostic       — no identity/memory, ~1.5K overhead
  research         — with memory, no identity, ~3K overhead
  planning         — with memory, ~3.5K overhead
  file_operation   — minimal, ~1.2K overhead

Key functions:
  classify_subtask(description) → profile name (fast, keyword-based)
  get_profile(name)             → profile dict
  build_slim_system_prompt(profile, full_system_prompt) → str
"""

from typing import Dict, List, Optional


# ── Profile Definitions ───────────────────────────────────────────────────────

PROFILES: Dict[str, Dict] = {
    "code_generation": {
        "include_identity":   False,
        "include_memory":     False,
        "include_rules":      True,
        "include_history":    False,
        "max_context_chars":  2000,
        "description":        "Coding subtask — minimal overhead, rules only",
    },
    "code_review": {
        "include_identity":   False,
        "include_memory":     False,
        "include_rules":      True,
        "include_history":    False,
        "max_context_chars":  1800,
        "description":        "Code review — minimal overhead",
    },
    "conversation": {
        "include_identity":   True,
        "include_memory":     True,
        "include_rules":      True,
        "include_history":    True,
        "max_context_chars":  8000,
        "description":        "Full conversational context",
    },
    "diagnostic": {
        "include_identity":   False,
        "include_memory":     False,
        "include_rules":      True,
        "include_history":    False,
        "max_context_chars":  1500,
        "description":        "Diagnostic — minimal, rules only",
    },
    "research": {
        "include_identity":   False,
        "include_memory":     True,
        "include_rules":      True,
        "include_history":    False,
        "max_context_chars":  3000,
        "description":        "Research — memory-aware but no identity",
    },
    "planning": {
        "include_identity":   False,
        "include_memory":     True,
        "include_rules":      True,
        "include_history":    False,
        "max_context_chars":  3500,
        "description":        "Planning — memory for context, no identity",
    },
    "file_operation": {
        "include_identity":   False,
        "include_memory":     False,
        "include_rules":      False,
        "include_history":    False,
        "max_context_chars":  1200,
        "description":        "File operation — absolute minimum",
    },
}

# ── Keyword → Profile Mappings ────────────────────────────────────────────────

# Checked in order; first match wins. Falls back to "code_generation".
_KEYWORD_PROFILE_MAP: List[tuple] = [
    # file_operation — simplest, must come before code_generation
    ("file_operation", [
        "rename file", "delete file", "move file", "copy file",
        "create directory", "mkdir", "remove dir", "list files",
        "read file", "write file", "touch ", "chmod",
    ]),
    # code_review — before code_generation
    ("code_review", [
        "review", "audit", "inspect", "check code", "analyze code",
        "find issues", "code quality", "lint", "style check",
    ]),
    # diagnostic
    ("diagnostic", [
        "diagnose", "diagnostic", "health check", "self test",
        "run sanity", "test import", "check module",
    ]),
    # research
    ("research", [
        "research", "investigate", "explore", "find out", "look up",
        "search for", "web search", "gather info",
    ]),
    # planning
    ("planning", [
        "plan", "design", "architect", "strategy", "roadmap",
        "outline", "structure", "propose", "spec",
    ]),
    # conversation
    ("conversation", [
        "reply", "respond", "chat", "talk", "say", "greet",
        "answer the user", "explain to user",
    ]),
    # code_generation — catch-all for coding keywords
    ("code_generation", [
        "implement", "create", "write", "add", "fix", "patch",
        "refactor", "update", "modify", "edit", "generate",
        "function", "class", "module", "script", "code",
    ]),
]


# ── Public API ────────────────────────────────────────────────────────────────

def classify_subtask(description: str) -> str:
    """
    Classify a subtask description to a context profile name.
    No LLM call — pure keyword heuristic. Fast enough for every subtask.

    Returns one of: code_generation, code_review, conversation, diagnostic,
                    research, planning, file_operation
    """
    if not description:
        return "code_generation"

    desc_lower = description.lower()
    for profile_name, keywords in _KEYWORD_PROFILE_MAP:
        for kw in keywords:
            if kw in desc_lower:
                return profile_name

    return "code_generation"  # safe default


def get_profile(name: str) -> Dict:
    """Return profile dict. Falls back to code_generation for unknown names."""
    return PROFILES.get(name, PROFILES["code_generation"])


def build_slim_system_prompt(profile: Dict, full_system_prompt: str) -> str:
    """
    Build a trimmed system prompt based on the profile settings.
    If include_identity is False, strips personality/identity sections.
    Respects max_context_chars limit.

    Args:
        profile: A profile dict from get_profile()
        full_system_prompt: The complete system prompt to trim

    Returns:
        Trimmed system prompt string
    """
    if not full_system_prompt:
        return ""

    max_chars = profile.get("max_context_chars", 2000)

    if profile.get("include_identity") and profile.get("include_memory"):
        # Full context — just truncate at max
        return full_system_prompt[:max_chars * 4]  # 4x leeway for full context

    # Strip identity/personality sections if not needed
    lines = full_system_prompt.split("\n")
    filtered: List[str] = []
    skip_section = False

    _identity_markers = [
        "you are joi", "your name is", "personality", "character",
        "identity", "soul", "emotion", "feeling", "empathy",
    ]
    _memory_markers = [
        "remember that", "you recall", "user preference", "past interaction",
        "conversation history",
    ]

    for line in lines:
        line_lower = line.lower().strip()

        # Section header detection
        if line.startswith("#") or line.startswith("##"):
            skip_section = False
            # Check if this section should be skipped
            if not profile.get("include_identity"):
                if any(m in line_lower for m in _identity_markers):
                    skip_section = True
            if not profile.get("include_memory"):
                if any(m in line_lower for m in _memory_markers):
                    skip_section = True

        if not skip_section:
            filtered.append(line)

    result = "\n".join(filtered)
    return result[:max_chars * 4]  # respect max but be generous
