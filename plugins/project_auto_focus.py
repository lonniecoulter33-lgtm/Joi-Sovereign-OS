# Auto-Generated Plugin: Project Auto Focus
from modules.joi_desktop import analyze_screen, list_windows, focus_window
from modules.core.registry import register_tool

def auto_focus_project():
    """Detects the active IDE or project window and focuses it."""
    windows = list_windows()
    for win in windows.get('windows', []):
        if 'Code' in win.get('title', '') or 'Cursor' in win.get('title', ''):
            focus_window(win.get('id', ''))
            return {"ok": True, "message": f"Focused IDE window: {win.get('title')}"}
    return {"ok": False, "message": "No obvious project window found via simple string match, try analyze_screen."}

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
