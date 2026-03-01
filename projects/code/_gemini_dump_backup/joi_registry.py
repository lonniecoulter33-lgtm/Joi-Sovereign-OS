"""
Shared registry for JOI tools and plugin routes.

This avoids circular imports between joi_companion.py and modules/*.
Modules should import from joi_registry and call register_tool/register_route.
"""
from __future__ import annotations
from typing import Callable, Dict, List, Any

TOOLS: List[dict] = []
TOOL_EXECUTORS: Dict[str, Callable[..., Any]] = {}
ROUTES: List[dict] = []

def register_tool(tool_def: dict, executor_fn: Callable[..., Any]) -> None:
    TOOLS.append(tool_def)
    TOOL_EXECUTORS[tool_def["function"]["name"]] = executor_fn

def register_route(rule: str, methods: list, handler_fn, name: str) -> None:
    ROUTES.append({"rule": rule, "methods": methods, "handler": handler_fn, "name": name})
