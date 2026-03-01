"""
modules/core/modeling.py

Layer 2 --- Cognitive Engine: User & Self Modeling.
Maintains a recursive internal representation of the user (Lonnie) 
and Joi's own evolving capabilities.
"""
import json
import time
from typing import Dict, Any, List, Optional, Tuple
from modules.core.interfaces import BaseContextProvider
from modules.core.registry import register_context_provider
from modules.core.cognition import graph

class UserProfileProvider(BaseContextProvider):
    """
    Context provider for the evolving User Model.
    Injects high-level insights about Lonnie's current flow and expertise.
    """
    def __init__(self):
        super().__init__("USER_MODEL", order=0.5) # Injected very early, before identity

    def build(self, user_message: str, recent_messages: List[Dict[str, Any]], **kwargs) -> Optional[Tuple[str, Optional[str], Optional[Dict[str, Any]]]]:
        insight = self._get_latest_insight()
        
        if not insight:
            return None

        text = f"\n[USER MODEL -- My current understanding of Lonnie]:\n"
        text += f"  Status: {insight.get('current_flow', 'Interacting')}\n"
        text += f"  Expertise: {insight.get('observed_expertise', 'General')}\n"
        text += f"  Engagement: {insight.get('engagement_level', 'High')}\n"
        
        return (text, "USER_MODEL", insight)

    def _get_latest_insight(self) -> Dict:
        """Fetch the most recent recursive insight node."""
        # For pilot: Return a static insight that will be updated by Loop 4
        return {
            "current_flow": "System Architecture & Evolution",
            "observed_expertise": "Lead AI Architect / Principal Engineer",
            "engagement_level": "Deep Focus"
        }

# Register the User Model
register_context_provider(UserProfileProvider())
