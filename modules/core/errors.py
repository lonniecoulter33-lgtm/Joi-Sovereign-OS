"""
modules/core/errors.py

Standardized error classes for Joi.
Enables graded failure handling across context builders and tool executions.
"""

class JoiError(Exception):
    """Base class for all Joi-related errors."""
    pass

class JoiRecoverableError(JoiError):
    """
    An error that indicates a sub-system failed but the main loop can continue.
    Example: A context provider failed to fetch data.
    """
    pass

class JoiToolError(JoiError):
    """
    An error during tool execution. Should be caught and returned 
    as a structured 'ok: False' response to the LLM.
    """
    pass

class JoiSystemError(JoiError):
    """
    A critical error that means the system cannot safely continue operation.
    Should trigger a log + abort/restart.
    """
    pass
