"""
modules/core/interfaces.py

Interface definitions and base classes for Joi's pluggable architecture.
Enforces contracts between the core runtime and specialized modules.
"""
from typing import Any, Dict, List, Optional, Tuple, Protocol, runtime_checkable

@runtime_checkable
class ContextProvider(Protocol):
    """
    Protocol for objects that provide context to Joi's system prompt.
    """
    name: str
    order: float      # Determines sequence
    importance: float # 0.0 to 1.0 (Used for adaptive compression)

    def build(self, user_message: str, recent_messages: List[Dict[str, Any]], **kwargs) -> Optional[Tuple[str, Optional[str], Optional[Dict[str, Any]]]]:
        ...

    def compress(self, content: str) -> str:
        """
        Self-optimization: reduce the token count of the provided content.
        Default should return content truncated or summarized.
        """
        ...

class JoiTool:
    """
    Base class for all Joi tools.
    Enforces deterministic contracts and provides metadata for cognitive planning.
    """
    name: str
    description: str
    parameters: Dict[str, Any]  # JSON Schema format
    risk_level: str = "low"     # low, medium, high
    
    # Symbolic Planning Meta (Section 7)
    requires: List[str] = None # Prerequisite data/states
    provides: List[str] = None # Resulting data/states
    
    def execute(self, ctx: Any, **kwargs) -> Dict[str, Any]:
        """
        The actual logic of the tool.
        Receives the request-scoped JoiContext.
        
        Should raise modules.core.errors.JoiToolError for domain failures.
        """
        raise NotImplementedError("Subclasses must implement execute")

    def to_openai_dict(self) -> Dict[str, Any]:
        """Convert the tool contract to OpenAI function-calling format."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters
            }
        }

class JoiSensor:
    """
    Base class for all Joi sensors.
    Sensors monitor the environment and push raw signals to the core.
    """
    name: str
    description: str
    
    def poll(self) -> Optional[Dict[str, Any]]:
        """
        Check for environment changes.
        Returns a signal dict if something is detected, else None.
        """
        raise NotImplementedError("Subclasses must implement poll")

class JoiWorker:
    """
    Base class for specialized reasoning nodes.
    Workers handle offboarded tasks (coding, research, simulation).
    """
    name: str
    capabilities: List[str]
    
    def dispatch(self, ctx: Any, task: Dict[str, Any]) -> Any:
        """
        Send a task to the worker.
        """
        raise NotImplementedError("Subclasses must implement dispatch")

class BaseContextProvider:
    """
    Base implementation for context providers with standard logic.
    """
    def __init__(self, name: str, order: float = 10.0, importance: float = 0.5):
        self.name = name
        self.order = order
        self.importance = importance

    def build(self, user_message: str, recent_messages: List[Dict[str, Any]], **kwargs) -> Optional[Tuple[str, Optional[str], Optional[Dict[str, Any]]]]:
        return None

    def compress(self, content: str) -> str:
        """Default compression: aggressive truncation."""
        if len(content) > 500:
            return content[:500] + "\n...(compressed)..."
        return content
