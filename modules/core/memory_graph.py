"""
modules/core/memory_graph.py

ContextProvider for Long-Horizon causal memory.
Injects past successful reasoning chains into Joi's current context.
"""
import json
from typing import List, Dict, Any, Optional, Tuple
from modules.core.interfaces import BaseContextProvider
from modules.core.registry import register_context_provider
from modules.core.cognition import graph

class LongHorizonMemoryProvider(BaseContextProvider):
    """
    Retrieves and injects successful historical plans (DELIBERATION nodes).
    """
    def __init__(self):
        super().__init__("CAUSAL_MEMORY", order=6.5) # Injected between vector memory and facts

    def build(self, user_message: str, recent_messages: List[Dict[str, Any]], **kwargs) -> Optional[Tuple[str, Optional[str], Optional[Dict[str, Any]]]]:
        # In future: Use semantic search to find RELEVANT successes.
        # For now: Provide top 2 recent successes to demonstrate continuity.
        successes = graph.get_successful_strategies(limit=2)
        if not successes:
            return None

        text = "\n[CAUSAL MEMORY -- Logic from past successful tasks]:\n"
        for s in successes:
            content = json.loads(s['content'])
            text += f"  - Strategy: {content.get('decision', 'N/A')}\n"
            text += f"    Context: {content.get('reason', 'N/A')}\n"
        
        return (text, "CAUSAL_MEMORY", {"count": len(successes)})

# Register the provider
register_context_provider(LongHorizonMemoryProvider())
