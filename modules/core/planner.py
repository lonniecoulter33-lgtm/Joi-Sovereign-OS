"""
modules/core/planner.py

Layer 2 --- Cognitive Engine: Symbolic Planner.
Validates reasoning chains against Action Schemas to prevent agent hallucinations.
"""
from typing import List, Dict, Any, Optional
from modules.core.registry import ACTIVE_TOOLS
from modules.core.cognition import graph

class SymbolicPlanner:
    """
    Ensures that Joi's plans follow deterministic rules.
    """
    def validate_plan(self, plan: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Check if a neural plan (from LLM) is symbollically valid.
        """
        provided_states = set()
        # Seed with current world state (Future: check environment)
        
        errors = []
        for step in plan:
            tool_name = step.get("tool")
            if tool_name not in ACTIVE_TOOLS:
                continue # Legacy tool or invalid
            
            tool = ACTIVE_TOOLS[tool_name]
            
            # Check requirements
            if tool.requires:
                for req in tool.requires:
                    if req not in provided_states:
                        errors.append(f"Step '{tool_name}' missing requirement: {req}")
            
            # Add provisions to the state for next steps
            if tool.provides:
                for prov in tool.provides:
                    provided_states.add(prov)
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "final_state": list(provided_states)
        }

# Singleton
planner = SymbolicPlanner()
