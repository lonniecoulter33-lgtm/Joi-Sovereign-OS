"""
Dynamic tool selector -- gates which tools are sent to OpenAI per request.

OpenAI limit: 128 tools max. Joi has 130+. This module selects
a relevant subset (target: 40-80) based on user message + task classification.

Full registry is preserved. If the model requests a tool that wasn't included,
the caller can rerun with an expanded set via get_expanded_tools().
"""

from typing import Dict, List, Optional, Set

# ── Tool Groups ─────────────────────────────────────────────────────────────
# Each tool belongs to exactly one group. Groups have a priority (lower = higher priority).
# Priority 1 = always included. Priority 2 = included if relevant. Priority 3+ = on-demand.

TOOL_GROUPS: Dict[str, Dict] = {
    "core_chat": {
        "priority": 1,  # ALWAYS included — every message gets these
        "tools": {
            # Memory
            "remember", "recall",
            # File basics (always needed — users constantly ask about files)
            # NOTE: these are owned here; do NOT duplicate in filesystem group
            "read_upload", "list_uploads", "fs_read", "fs_list",
            # App launching & media (most common single-turn actions)
            # NOTE: owned here; do NOT duplicate in desktop group
            "launch_app", "play_media", "open_url",
            # Web
            "web_search", "web_fetch",
            # Perception — always available so Joi can narrate screen
            # NOTE: owned here; do NOT duplicate in vision group
            "screenshot", "analyze_screen",
            # Self-awareness
            "get_capability_report",
            # Conversation
            "internal_monologue", "set_mode", "toggle_commentary",
            # Memory visualization
            "get_memory_viz",
        },
        "keywords": [],  # always included, no keywords needed
    },
    "memory": {
        "priority": 1,
        "tools": {
            "record_interaction", "analyze_learning_patterns",
            "suggest_improvements", "learn_communication_style",
            "get_learning_stats",
        },
        "keywords": ["remember", "memory", "recall", "forget", "learn", "pattern"],
    },
    "filesystem": {
        "priority": 2,
        "tools": {
            # fs_read, fs_list, read_upload, list_uploads owned by core_chat — not duplicated here
            "fs_search", "search_files",
            "generate_file", "save_code_file", "save_text_file",
            "save_research_findings", "save_binary_file", "project_tree",
        },
        "keywords": ["file", "folder", "directory", "read", "write", "save", "document",
                      "pdf", "txt", "download", "find file", "open file",
                      "book", "upload", "uploaded",
                      "tree", "structure", "layout", "project structure", "directory tree"],
    },
    "code_edit": {
        "priority": 2,
        "tools": {
            "code_edit", "code_insert", "code_read_section", "code_search",
            "code_rollback", "code_list_backups", "creative_edit", "code_backup",
            "analyze_code", "project_tree", "execute_python_code",
        },
        "keywords": ["code", "edit", "fix", "bug", "function", "script", "module",
                      "patch", "refactor", "syntax", "html", "css", "python", "javascript",
                      "project structure", "tree", "layout", "execute", "run code", "run python"],
    },
    "evolution": {
        "priority": 3,
        "tools": {
            "monitor_ai_research", "analyze_capabilities", "propose_upgrade",
            "apply_upgrade", "list_proposals", "get_evolution_stats",
            "compare_with_ai", "introspect_system", "evaluate_research",
            "acquire_capability", "test_upgrade", "propose_patch", "create_plugin",
        },
        "keywords": ["upgrade", "evolve", "evolution", "proposal", "capability",
                      "research", "compare", "introspect", "patch", "plugin"],
    },
    "desktop": {
        "priority": 2,
        "tools": {
            # launch_app, play_media, screenshot owned by core_chat — not duplicated here
            "move_mouse", "click_mouse", "type_text", "press_key",
            "get_mouse_position", "smart_click", "find_file_smart",
            "list_windows", "find_window", "focus_window", "close_window",
        },
        "keywords": ["click", "mouse", "type", "keyboard", "window",
                      "desktop", "focus", "minimize",
                      "start", "run", "app", "application", "program", "notepad",
                      "calculator", "explorer", "vlc", "winamp", "itunes",
                      "open notepad", "open calculator"],
    },
    "camera": {
        "priority": 2,
        "tools": {
            "analyze_camera", "enroll_face", "update_face",
            "list_known_faces", "forget_face", "learn_face",
        },
        "keywords": ["camera", "webcam", "face", "look at me", "see me",
                      "who is", "recognize", "enroll"],
    },
    "voice_tts": {
        "priority": 2,
        "tools": {"generate_avatar_image", "generate_image"},
        "keywords": ["avatar", "image", "picture", "generate image", "dalle"],
    },
    "voice_id": {
        "priority": 3,
        "tools": {"enroll_voice", "check_voice_id", "set_voice_threshold"},
        "keywords": ["voice", "enroll voice", "speaker", "voice id", "voice threshold"],
    },
    "browser": {
        "priority": 2,
        "tools": {
            "open_url", "click_element", "fill_input", "extract_text",
            "browser_screenshot", "execute_js", "wait_for_element",
        },
        "keywords": ["browser", "website", "url", "webpage", "selenium",
                      "click element", "fill form", "navigate",
                      "youtube", "video", "play video", "watch video", "open youtube",
                      "open browser", "play a video", "stream", "open a tab",
                      "chrome", "firefox", "edge", "safari", "open chrome",
                      "open firefox", "google", "search the web", "go to"],
    },
    "obs": {
        "priority": 3,
        "tools": {
            "obs_connect", "obs_status", "obs_get_scenes", "obs_switch_scene",
            "obs_start_recording", "obs_stop_recording", "obs_pause_recording",
            "obs_start_streaming", "obs_stop_streaming", "obs_get_sources",
            "obs_toggle_source", "obs_screenshot", "manage_obs",
        },
        "keywords": ["obs", "record", "stream", "scene", "recording",
                      "streaming", "broadcast", "capture"],
    },
    "homeassistant": {
        "priority": 3,
        "tools": {
            "ha_get_entities", "ha_get_state", "ha_turn_on", "ha_turn_off",
            "ha_set_temperature", "ha_call_service", "ha_camera_snapshot",
        },
        "keywords": ["light", "lights", "temperature", "thermostat", "smart home",
                      "home assistant", "turn on", "turn off", "climate", "iot"],
    },
    "publisher": {
        "priority": 3,
        "tools": {
            "publisher_init_project", "publisher_edit_chapter",
            "publisher_generate_asset", "publisher_generate_cover_script",
            "publisher_format_interior_script", "test_generate_avatar"
        },
        "keywords": ["publish", "book", "chapter", "cover", "image", "generate image",
                      "publisher", "format", "asset", "dalle", "stable diffusion",
                      "picture", "art", "drawing"],
    },
    "security": {
        "priority": 3,
        "tools": {
            "security_arm", "security_disarm", "security_status",
            "security_get_recordings", "security_set_sensitivity",
        },
        "keywords": ["security", "arm", "disarm", "motion", "alert",
                      "intruder", "surveillance"],
    },
    "orchestrator": {
        "priority": 1,  # ALWAYS included -- core multi-agent capability
        "tools": {
            "create_orchestration_proposal",  # proposals first, then approve -> Agent Terminal
            "orchestrate_task", "approve_subtask", "reject_subtask",
            "get_orchestrator_status", "cancel_orchestration",
        },
        "keywords": ["orchestrate", "agent terminal", "terminal", "pipeline", "proposal",
                      "multi-agent", "deploy", "multi-step", "multi-file",
                      "work on", "handle this", "take care of", "agent"],
    },
    "app_factory": {
        "priority": 2,
        "tools": {"scaffold_project", "list_templates", "build_project",
                  "run_setup_command", "get_build_configs"},
        "keywords": ["scaffold", "template", "new project", "create app", "build",
                      "package", "pyinstaller", "compile", "zip", "bundle",
                      "new app", "starter", "boilerplate"],
    },
    "swarm": {
        "priority": 2,
        "tools": {"swarm_orchestrate", "swarm_status", "swarm_cancel", "send_agent_message"},
        "keywords": ["swarm", "parallel", "concurrent", "hive", "queen",
                      "multi-agent", "parallel agents"],
    },
    "brain": {
        "priority": 1,  # ALWAYS included -- model routing awareness
        "tools": {"brain_route", "brain_stats", "get_brain_state"},
        "keywords": ["brain", "model", "route", "routing"],
    },
    "git_agency": {
        "priority": 2,
        "tools": {"git_manager"},
        "keywords": [
            "git", "commit", "push", "pull", "merge", "branch", "repo",
            "repository", "version control", "stage", "staging", "diff",
            "checkout", "clone", "stash", "status", "auto commit",
            "save changes", "save my work", "push to github", "push to git",
            "commit my code", "what changed", "git history", "git log",
            "did you commit", "commit the changes", "save this to git",
        ],
    },

    "diagnostics": {
        "priority": 3,
        "tools": {
            "run_system_diagnostic", "self_diagnose", "self_fix",
            "visual_self_diagnose", "code_self_repair",
            "run_supervisor_check", "get_routing_stats",
            "get_capability_report", "get_dpo_insights",
        },
        "keywords": ["diagnose", "diagnostic", "self test", "health check",
                      "self heal", "self fix", "repair", "supervisor",
                      "check model", "what model", "which model", "model status", "run diagnostic",
                      "what tools", "list tools", "what can you do", "capabilities",
                      "what are you capable", "show me your tools"],
    },
    "consciousness": {
        "priority": 2,
        "tools": {
            "reflect", "read_journal", "how_have_i_grown",
            "update_manuscript",
        },
        "keywords": ["journal", "reflect", "growth", "autobiography",
                      "manuscript", "evolved", "consciousness"],
    },
    "autonomy": {
        "priority": 3,
        "tools": {
            "start_autonomy", "stop_autonomy", "get_autonomy_status",
            "run_autonomy_cycle",
        },
        "keywords": ["autonomy", "autonomous", "self-improve", "cycle"],
    },
    "projects": {
        "priority": 3,
        "tools": {"scan_projects", "organise_projects", "create_project", "list_saved_projects"},
        "keywords": ["project", "organize", "scan projects", "categorize", "new project",
                      "list projects", "saved projects"],
    },
    "scheduler": {
        "priority": 3,
        "tools": {"scheduler_control", "configure_scheduler"},
        "keywords": ["schedule", "timer", "cron", "recurring", "alarm", "reminder"],
    },
    "market": {
        "priority": 3,
        "tools": {
            "get_market_summary", "analyze_stock", "analyze_crypto",
            "check_price_alerts", "create_price_alert",
        },
        "keywords": ["market", "stock", "crypto", "xrp", "bitcoin", "price",
                      "trading", "portfolio", "alert", "price alert"],
    },
    "search": {
        "priority": 2,
        "tools": {"web_search", "search_web", "google_search", "web_fetch"},
        "keywords": ["search", "look up", "find out", "what is", "who is", "when did",
                      "google", "current", "latest", "news", "today", "right now", "fetch",
                      "get page", "scrape"],
    },
    "skills": {
        "priority": 3,
        "tools": {
            "synthesize_skill", "find_skill", "run_self_correction",
            "generate_practice_goals", "get_skill_stats",
        },
        "keywords": ["skill", "learn how", "practice", "self-correct", "get better at"],
    },
    "watchdog": {
        "priority": 3,
        "tools": {
            "manual_checkpoint", "manual_override", "manual_revert",
            "render_diff", "watchdog_status",
        },
        "keywords": ["watchdog", "checkpoint", "revert", "diff", "override", "rollback git",
                      "undo change", "restore checkpoint"],
    },
}

# Reverse lookup: tool_name -> group_name
_TOOL_TO_GROUP: Dict[str, str] = {}
for _gname, _gdata in TOOL_GROUPS.items():
    for _tname in _gdata["tools"]:
        _TOOL_TO_GROUP[_tname] = _gname

# Task type -> relevant groups (from joi_router.py classifications)
_TASK_TYPE_GROUPS: Dict[str, List[str]] = {
    "conversation":     [],  # core_chat is always included
    "question":         ["filesystem", "consciousness", "search"],
    "code_edit":        ["code_edit", "filesystem", "evolution", "orchestrator"],
    "code_review":      ["code_edit", "filesystem", "orchestrator"],
    "orchestration":    ["orchestrator", "app_factory", "code_edit", "filesystem", "diagnostics", "swarm"],
    "file_operation":   ["filesystem", "desktop"],
    "research":         ["filesystem", "browser", "search"],
    "writing":          ["filesystem"],
    "system_admin":     ["diagnostics", "desktop", "brain"],
    "creative":         ["voice_tts", "filesystem"],
    "automation":       ["desktop", "browser", "obs", "homeassistant"],
    "media":            ["browser", "desktop"],
    "capability_query": ["diagnostics"],  # get_capability_report lives in diagnostics
    "vision":           ["vision", "camera"],
    "memory":           ["memory"],
    "schedule":         ["scheduler"],
    "market_data":      ["market"],
    "home_control":     ["homeassistant"],
    "security":         ["security", "camera"],
}

HARD_CAP = 128   # OpenAI API hard limit
TARGET_MAX = 125  # Max safe tools to send without hitting limit
GATE_THRESHOLD = 50  # start filtering once registry exceeds this count

# NOTE: select_tools_for_subtask() is defined below but coder agents don't use tools.
# Tool selection only applies to the main chat path (run_conversation in joi_llm.py).
# ORCHESTRATOR_TOOL_CAP removed — it was a premature cap that doesn't match architecture.

# Keyword → group mappings used by select_tools_for_subtask
_SUBTASK_KEYWORD_GROUPS: Dict[str, List[str]] = {
    # coding / file writing
    "code": ["code_edit", "filesystem"],
    "edit": ["code_edit", "filesystem"],
    "write": ["code_edit", "filesystem"],
    "create": ["code_edit", "filesystem"],
    "fix": ["code_edit", "filesystem", "diagnostics"],
    "bug": ["code_edit", "filesystem", "diagnostics"],
    "refactor": ["code_edit", "filesystem"],
    "function": ["code_edit"],
    "module": ["code_edit", "filesystem"],
    "class": ["code_edit"],
    "import": ["code_edit"],
    "syntax": ["code_edit", "diagnostics"],
    "python": ["code_edit", "filesystem"],
    "javascript": ["code_edit", "filesystem"],
    "html": ["code_edit", "filesystem"],
    "css": ["code_edit", "filesystem"],
    # running / testing
    "test": ["code_edit", "diagnostics"],
    "run": ["code_edit"],
    "execute": ["code_edit"],
    "install": ["app_factory"],
    "npm": ["app_factory"],
    "pip": ["app_factory"],
    # validation / diagnostics
    "diagnose": ["diagnostics"],
    "diagnostic": ["diagnostics"],
    "repair": ["diagnostics"],
    "validate": ["diagnostics"],
    # git / version control
    "git": ["git_agency", "watchdog"],
    "commit": ["git_agency"],
    "push": ["git_agency"],
    # file system
    "file": ["filesystem"],
    "folder": ["filesystem"],
    "directory": ["filesystem"],
    "read": ["filesystem"],
    "save": ["filesystem"],
    "tree": ["filesystem"],
    # web / search
    "search": ["search"],
    "web": ["search", "browser"],
    "fetch": ["search"],
    "url": ["browser"],
    # build / scaffold
    "scaffold": ["app_factory"],
    "build": ["app_factory"],
    "package": ["app_factory"],
    # watchdog
    "revert": ["watchdog"],
    "rollback": ["watchdog"],
    "checkpoint": ["watchdog"],
}

# Core tools always included in orchestrator subtask context
_ORCHESTRATOR_CORE_TOOLS: set = {
    "orchestrate_task", "get_orchestrator_status",
    "joicode_run_bash", "run_system_diagnostic",
    "fs_read", "fs_list", "fs_search", "project_tree",
    "code_edit", "code_read_section",
    "remember", "recall",
    "validate_python_file",
}


def _get_tool_name(tool_def: dict) -> str:
    """Extract name from OpenAI tool definition."""
    return tool_def.get("function", {}).get("name", "")


def _match_keywords(text: str, keywords: List[str]) -> bool:
    """Check if any keyword appears in the text (case-insensitive)."""
    text_lower = text.lower()
    return any(kw in text_lower for kw in keywords)


def select_tools(
    all_tools: List[Dict],
    user_text: str = "",
    classification: Optional[Dict] = None,
    extra_groups: Optional[List[str]] = None,
) -> List[Dict]:
    """
    Select a relevant subset of tools for this request.

    Filtering kicks in once the registry exceeds GATE_THRESHOLD (50).
    Result is capped at TARGET_MAX (60) to keep model focus sharp.
    """
    if len(all_tools) <= GATE_THRESHOLD:
        # Small registry — no gating needed
        print(f"  [TOOL-SELECT] {len(all_tools)} tools (under gate threshold, no filtering)")
        return all_tools

    # Build name->def lookup
    tool_lookup: Dict[str, Dict] = {}
    for t in all_tools:
        name = _get_tool_name(t)
        if name:
            tool_lookup[name] = t

    # Determine which groups to include
    included_groups: Set[str] = set()

    # Always include priority-1 groups
    for gname, gdata in TOOL_GROUPS.items():
        if gdata["priority"] == 1:
            included_groups.add(gname)

    # Include groups based on task classification
    if classification:
        task_type = classification.get("task_type", "conversation")
        for gname in _TASK_TYPE_GROUPS.get(task_type, []):
            included_groups.add(gname)

    # Include groups based on keyword matching in user message
    if user_text:
        for gname, gdata in TOOL_GROUPS.items():
            if gdata["keywords"] and _match_keywords(user_text, gdata["keywords"]):
                included_groups.add(gname)

    # Include explicitly requested extra groups
    if extra_groups:
        included_groups.update(extra_groups)

    # Collect tool names from included groups
    selected_names: Set[str] = set()
    for gname in included_groups:
        gdata = TOOL_GROUPS.get(gname, {})
        selected_names.update(gdata.get("tools", set()))

    # Also include any registered tools that aren't in ANY group (ungrouped safety net)
    grouped_tools = set(_TOOL_TO_GROUP.keys())
    for name in tool_lookup:
        if name not in grouped_tools:
            selected_names.add(name)

    # If still over HARD_CAP, trim by removing lowest-priority groups first
    if len(selected_names) > HARD_CAP:
        # Sort included groups by priority (highest number = lowest priority = trim first)
        sorted_groups = sorted(included_groups, key=lambda g: -TOOL_GROUPS.get(g, {}).get("priority", 99))
        for gname in sorted_groups:
            if len(selected_names) <= HARD_CAP:
                break
            gdata = TOOL_GROUPS.get(gname, {})
            if gdata.get("priority", 99) <= 1:
                continue  # never trim priority-1 groups
            selected_names -= gdata.get("tools", set())
            included_groups.discard(gname)

    # Build final tool list preserving original order
    selected_tools = [t for t in all_tools if _get_tool_name(t) in selected_names]

    # Apply TARGET_MAX cap (keeps model focus sharp; HARD_CAP is the API limit)
    if len(selected_tools) > TARGET_MAX:
        final_tools = []
        # First pass: always grab Priority 1 tools (like core chat, memory, and orchestrator)
        for t in selected_tools:
            name = _get_tool_name(t)
            gname = _TOOL_TO_GROUP.get(name)
            if gname and TOOL_GROUPS.get(gname, {}).get("priority", 99) <= 1:
                final_tools.append(t)
                
        # Second pass: fill remaining slots up to TARGET_MAX
        for t in selected_tools:
            if len(final_tools) >= TARGET_MAX:
                break
            if t not in final_tools:
                final_tools.append(t)
                
        # Restore original order
        selected_tools = [t for t in selected_tools if t in final_tools]

    # Final API hard cap safety
    if len(selected_tools) > HARD_CAP:
        selected_tools = selected_tools[:HARD_CAP]

    # Log
    trimmed = len(all_tools) != len(selected_tools)
    groups_str = ", ".join(sorted(included_groups))
    print(f"  [TOOL-SELECT] {len(selected_tools)}/{len(all_tools)} tools"
          f" | groups: {groups_str}"
          f"{' | TRIMMED' if trimmed else ''}")

    return selected_tools


def get_group_for_tool(tool_name: str) -> Optional[str]:
    """Get the group name for a tool."""
    return _TOOL_TO_GROUP.get(tool_name)


def select_tools_for_subtask(
    all_tools: List[Dict],
    subtask_description: str = "",
    extra_tool_names: Optional[List[str]] = None,
) -> List[Dict]:
    """
    Semantic tool filter for orchestrator subtask execution.

    NOTE: Coder agents don't use tools — they output pure JSON via route_and_call_for_agent().
    This function is available for future non-Layer-1 paths that do use tools in subtask context.

    Strategy:
      1. Always include _ORCHESTRATOR_CORE_TOOLS
      2. Keyword-match subtask description to additional groups
      3. Include any explicitly requested extra_tool_names
    """
    tool_lookup: Dict[str, Dict] = {_get_tool_name(t): t for t in all_tools if _get_tool_name(t)}

    # Start with core set
    selected_names: Set[str] = set(_ORCHESTRATOR_CORE_TOOLS)

    # Keyword-match subtask description to extra groups
    desc_lower = subtask_description.lower()
    matched_groups: Set[str] = set()
    for keyword, groups in _SUBTASK_KEYWORD_GROUPS.items():
        if keyword in desc_lower:
            matched_groups.update(groups)

    for gname in matched_groups:
        gdata = TOOL_GROUPS.get(gname, {})
        selected_names.update(gdata.get("tools", set()))

    # Always include priority-1 group tools (they're tiny and always relevant)
    for gname, gdata in TOOL_GROUPS.items():
        if gdata.get("priority") == 1:
            selected_names.update(gdata.get("tools", set()))

    # Include explicitly requested tools
    if extra_tool_names:
        selected_names.update(extra_tool_names)

    # Build ordered list (preserving registry order)
    selected = [t for t in all_tools if _get_tool_name(t) in selected_names]

    print(f"  [SUBTASK-TOOLS] {len(selected)}/{len(all_tools)} tools for subtask"
          f" | groups: {', '.join(sorted(matched_groups)) or 'core-only'}")
    return selected


def get_expanded_tools(
    all_tools: List[Dict],
    missing_tool_name: str,
    previous_groups: Optional[List[str]] = None,
    user_text: str = "",
    classification: Optional[Dict] = None,
) -> List[Dict]:
    """
    Called when the model requested a tool that wasn't in the selected set.
    Reselects tools with the missing tool's group forcibly included.

    Returns expanded tool list (still capped at HARD_CAP).
    If the tool has no group (ungrouped), returns full set so the tool is always available.
    """
    group = get_group_for_tool(missing_tool_name)
    if group is None:
        # Tool not in any group - use full set to ensure it's available
        print(f"  [TOOL-SELECT] FALLBACK RERUN: tool '{missing_tool_name}' ungrouped -> using full set")
        return all_tools if len(all_tools) <= HARD_CAP else all_tools[:HARD_CAP]

    extra = list(previous_groups or [])
    if group not in extra:
        extra.append(group)
    print(f"  [TOOL-SELECT] FALLBACK RERUN: adding group '{group}' for missing tool '{missing_tool_name}'")

    return select_tools(all_tools, user_text=user_text,
                        classification=classification, extra_groups=extra)


def build_tool_hint_suffix(all_tools: List[Dict], primary_tools: List[Dict]) -> str:
    """
    Build a system-prompt hint listing 'available but not primary' tools
    as compressed name + one-liner entries. This does NOT reduce the tools
    array sent to the API — it provides a compressed hint for tools that
    were filtered out, so the LLM knows they exist and can ask for them.

    Architecture note: The main chat path calls select_tools() from joi_llm.py
    (Layer 1 — cannot modify). This function is infrastructure for future
    non-Layer-1 paths that build their own system prompts.

    Returns empty string if no tools were filtered out.
    """
    primary_names = {_get_tool_name(t) for t in primary_tools}
    all_names = {_get_tool_name(t) for t in all_tools}
    hidden_names = all_names - primary_names

    if not hidden_names:
        return ""

    hints = []
    for t in all_tools:
        name = _get_tool_name(t)
        if name in hidden_names:
            desc = t.get("function", {}).get("description", "")
            # One-liner: first sentence only, max 80 chars
            one_liner = desc.split(".")[0].strip()[:80]
            hints.append(f"  \u2022 {name}: {one_liner}")

    if not hints:
        return ""

    return "\nAdditional tools available on request:\n" + "\n".join(hints[:20])
