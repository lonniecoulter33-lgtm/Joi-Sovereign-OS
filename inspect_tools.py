import os
import sys

# Add the project root to the path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

try:
    # Stub Flask to avoid import errors if the venv isn't cleanly active
    import sys
    from unittest.mock import MagicMock
    sys.modules['flask'] = MagicMock()
    sys.modules['flask_cors'] = MagicMock()
    sys.modules['werkzeug'] = MagicMock()
    sys.modules['werkzeug.exceptions'] = MagicMock()
    sys.modules['waitress'] = MagicMock()
    sys.modules['colorama'] = MagicMock()

    from joi_companion import TOOL_REGISTRY
    
    for i, t in enumerate(TOOL_REGISTRY):
        func = t.get("function", {})
        desc = func.get("description", "")
        if not isinstance(desc, str):
            print(f"Index: {i}, Name: {func.get('name')}, Type: {type(desc)}, Value: {desc}")
            
except Exception as e:
    print(f"Error loading registry: {e}")
