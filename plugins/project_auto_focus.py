# Plugin: Project Auto Focus
# Detects the active IDE/project window and focuses it.
from modules.joi_desktop import list_windows, focus_window
from modules.core.registry import register_tool

def auto_focus_project():
    """Detects the active IDE or project window and focuses it."""
    windows = list_windows()
    for win in windows.get('windows', []):
        title = win.get('title', '')
        if 'Code' in title or 'Cursor' in title or 'PyCharm' in title or 'Vim' in title:
            focus_window(win.get('id', ''))
            return {"ok": True, "message": f"Focused IDE window: {title}"}
    return {"ok": False, "message": "No IDE window found. Try list_windows() to see open windows."}

register_tool(
    {
        "type": "function",
        "function": {
            "name": "auto_focus_project",
            "description": "Detects the active active project and focuses its window."
        }
    },
    auto_focus_project
)
