"""
modules/core/introspection.py

Layer 3 --- Capability System: Self-Inspection Module.
Scans Joi's codebase, parses function signatures and docstrings, 
and builds a dynamic map of her capabilities.
"""
import ast
import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from modules.core.config import config
from modules.core.interfaces import BaseContextProvider
from modules.core.registry import register_context_provider, register_tool

class IntrospectionEngine:
    def __init__(self):
        self.modules_dir = config.MODULES_DIR
        self.capability_map_path = config.DATA_DIR / "capability_map.json"
        self.capabilities = {}

    def scan(self) -> Dict[str, Any]:
        """
        Scan all modules and build a structured capability catalog.
        """
        print(f"  [INTROSPECTION] Scanning modules in {self.modules_dir}...")
        new_map = {}
        
        for file_path in self.modules_dir.glob("*.py"):
            if file_path.name.startswith("__"):
                continue
            
            try:
                module_info = self._parse_file(file_path)
                new_map[file_path.stem] = module_info
            except Exception as e:
                print(f"    [WARN] Failed to introspect {file_path.name}: {e}")

        self.capabilities = new_map
        self._save_map()
        return self.capabilities

    def _parse_file(self, path: Path) -> Dict[str, Any]:
        """Use AST to extract classes, functions, and docstrings."""
        tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"))
        
        info = {
            "name": path.stem,
            "doc": ast.get_docstring(tree) or "No description available.",
            "functions": [],
            "classes": []
        }

        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                if node.name.startswith("_"): continue
                func_info = {
                    "name": node.name,
                    "doc": ast.get_docstring(node),
                    "args": [arg.arg for arg in node.args.args]
                }
                info["functions"].append(func_info)
            
            elif isinstance(node, ast.ClassDef):
                if node.name.startswith("_"): continue
                class_info = {
                    "name": node.name,
                    "doc": ast.get_docstring(node),
                    "methods": []
                }
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        if item.name.startswith("_"): continue
                        class_info["methods"].append(item.name)
                info["classes"].append(class_info)

        return info

    def _save_map(self):
        """Persist the capability map to disk."""
        with open(self.capability_map_path, "w", encoding="utf-8") as f:
            json.dump(self.capabilities, f, indent=2)

    def get_summary(self) -> str:
        """Return a user-friendly summary of all capabilities."""
        summary = "I have identified the following modules and capabilities:\n"
        for mod_name, info in self.capabilities.items():
            summary += f"- {mod_name}: {info['doc'].split('.')[0]}.\n"
        return summary

# Singleton engine
engine = IntrospectionEngine()

class IntrospectionProvider(BaseContextProvider):
    """
    ContextProvider that injects Joi's self-knowledge into her prompt.
    """
    def __init__(self):
        super().__init__("SELF_AWARENESS", order=15.5, importance=0.6)

    def build(self, user_message: str, recent_messages: List[Dict[str, Any]], **kwargs) -> Optional[Tuple[str, Optional[str], Optional[Dict[str, Any]]]]:
        # Inject a concise summary of capabilities
        if not engine.capabilities:
            engine.scan()
            
        from modules.core.registry import TOOLS, ACTIVE_TOOLS
        legacy_count = len(TOOLS)
        modern_count = len(ACTIVE_TOOLS)
        
        summary = "\n[SELF-AWARENESS -- My Internal Capabilities]:\n"
        summary += f"  I have {modern_count} modern tools and {legacy_count} legacy tools available across {len(engine.capabilities)} modules.\n"
        summary += "  I am fully aware of my entire toolset. Use 'explain_capability' to learn more.\n"
        
        return (summary, "SELF_AWARENESS", {"module_count": len(engine.capabilities), "total_tools": legacy_count + modern_count})

# ── Tool Definitions ─────────────────────────────────────────────────────────

def explain_capability(**kwargs) -> Dict[str, Any]:
    """
    Explains Joi's functions and capabilities.
    If module_name is provided, gives details on that specific module.
    """
    module_name = kwargs.get("module_name")
    if not engine.capabilities:
        engine.scan()

    if module_name:
        if module_name in engine.capabilities:
            return {"ok": True, "module": engine.capabilities[module_name]}
        return {"ok": False, "error": f"Module '{module_name}' not found."}
    
    return {"ok": True, "capabilities_summary": engine.get_summary()}

def get_system_health(**kwargs) -> Dict[str, Any]:
    """
    Returns a self-diagnostic report of Joi's internal modules and performance.
    """
    from modules.core.registry import TELEMETRY, ROUTING_SCORES, TOOLS, ACTIVE_TOOLS
    from modules.core.cognition import graph
    
    cap_stats = graph.get_capability_stats()
    
    return {
        "ok": True,
        "runtime_telemetry": TELEMETRY,
        "tool_registry": {
            "legacy_count": len(TOOLS),
            "modern_count": len(ACTIVE_TOOLS),
            "total": len(TOOLS) + len(ACTIVE_TOOLS)
        },
        "capability_performance": cap_stats,
        "expert_routing_active": len(ROUTING_SCORES) > 0,
        "status": "Healthy" if TELEMETRY["errors"] < 5 else "Degraded"
    }

def explain_decision(**kwargs) -> Dict[str, Any]:
    """
    Analyzes a specific reasoning chain from the graph and explains the logic.
    """
    session_id = kwargs.get("session_id", "")
    from modules.core.cognition import graph
    chain = graph.get_chain(session_id)
    if not chain:
        return {"ok": False, "error": f"No reasoning found for session {session_id}"}
    
    return {
        "ok": True,
        "reasoning_chain": chain,
        "causal_summary": f"This task involved {len(chain)} cognitive nodes."
    }

def explain_meta_cognition(**kwargs) -> Dict[str, Any]:
    """
    Returns insights from the Meta-Cognition Engine.
    Explains current adaptive strategies, performance trends, and optimization decisions.
    """
    from modules.core.meta_cognition import meta
    from modules.core.registry import ROUTING_SCORES
    
    return {
        "ok": True,
        "routing_strategies": ROUTING_SCORES,
        "resource_policy": "Adaptive (CPU/Mem aware)",
        "message": "I am continuously optimizing my tool selection based on historical success rates."
    }

# Register the provider and tools
register_context_provider(IntrospectionProvider())

register_tool(
    {"type": "function", "function": {
        "name": "explain_capability",
        "description": "Explains Joi's internal functions and capabilities. Use this to discover how Joi works or to explain her modules to Lonnie.",
        "parameters": {
            "type": "object",
            "properties": {
                "module_name": {"type": "string", "description": "Optional name of a specific module to explain."}
            }
        }
    }},
    explain_capability
)

register_tool(
    {"type": "function", "function": {
        "name": "get_system_health",
        "description": "Returns a self-aware report on Joi's internal health, module performance, and telemetry. Use this when asked 'How are you doing?' or 'Check your systems.'",
        "parameters": {"type": "object", "properties": {}}
    }},
    get_system_health
)

register_tool(
    {"type": "function", "function": {
        "name": "explain_decision",
        "description": "Retrieves the reasoning chain for a specific task and explains Joi's logic. Use this when Lonnie asks 'Why did you do that?' or 'Explain your logic.'",
        "parameters": {
            "type": "object",
            "properties": {
                "session_id": {"type": "string", "description": "The ID of the reasoning session to explain."}
            },
            "required": ["session_id"]
        }
    }},
    explain_decision
)

register_tool(
    {"type": "function", "function": {
        "name": "explain_meta_cognition",
        "description": "Explains Joi's current adaptive strategies and self-optimization insights. Use this to understand how she is improving herself.",
        "parameters": {"type": "object", "properties": {}}
    }},
    explain_meta_cognition
)
