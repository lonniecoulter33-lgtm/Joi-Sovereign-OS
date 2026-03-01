"""
modules/core/joi_manager.py

Layer 2 --- Cognitive Engine: HTN Planner (Hierarchical Task Network).
Decomposes high-level goals into sequences of atomic tool calls.
"""
from typing import List, Dict, Any
from modules.core.registry import ACTIVE_TOOLS, TOOLS

# Common task decomposition templates
_TEMPLATES = {
    "code_change": [
        {"tool": "code_read_section", "desc": "Read target file"},
        {"tool": "review_change", "desc": "Architect review"},
        {"tool": "code_edit", "desc": "Apply edit"},
    ],
    "research": [
        {"tool": "web_search", "desc": "Search for information"},
        {"tool": "recall", "desc": "Check existing memory"},
        {"tool": "remember", "desc": "Save findings"},
    ],
    "file_operation": [
        {"tool": "fs_read", "desc": "Read file"},
        {"tool": "fs_list", "desc": "List directory"},
    ],
    "vision": [
        {"tool": "analyze_screen", "desc": "Capture and analyze screen"},
    ],
}

# Keywords that map to templates
_KEYWORD_MAP = {
    "edit": "code_change", "fix": "code_change", "modify": "code_change",
    "change": "code_change", "update": "code_change", "refactor": "code_change",
    "search": "research", "find": "research", "look up": "research",
    "research": "research", "learn": "research",
    "read": "file_operation", "list": "file_operation", "show": "file_operation",
    "see": "vision", "look": "vision", "screen": "vision",
}


class HTNPlanner:
    def __init__(self):
        self.active_tasks = []

    def decompose(self, goal: str) -> List[Dict[str, Any]]:
        """Break a high-level goal into a sequence of atomic actions."""
        goal_lower = goal.lower()

        # Match goal to a template via keywords
        template_key = None
        for keyword, tkey in _KEYWORD_MAP.items():
            if keyword in goal_lower:
                template_key = tkey
                break

        if not template_key:
            return [{"tool": "internal_monologue", "desc": "Think about how to approach this", "args": {"thought": goal}}]

        # Get template and filter to tools that actually exist
        template = _TEMPLATES.get(template_key, [])
        available_tools = {t["function"]["name"] for t in TOOLS}
        available_tools.update(ACTIVE_TOOLS.keys())

        steps = []
        for step in template:
            if step["tool"] in available_tools:
                steps.append({
                    "tool": step["tool"],
                    "desc": step["desc"],
                    "args": {"goal": goal},
                })

        if not steps:
            steps = [{"tool": "internal_monologue", "desc": "Plan approach", "args": {"thought": goal}}]

        return steps


# Singleton
manager = HTNPlanner()
