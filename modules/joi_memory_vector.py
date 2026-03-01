"""
modules/joi_memory_vector.py

Bridge module -- loads the memory/ subsystem into Joi's module loader.
(The loader picks up modules/joi_*.py files automatically.)
"""

from modules.memory.memory_manager import init

# Initialize on import (like all joi_* modules)
init()
