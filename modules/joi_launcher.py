"""
Desktop App Launcher -- open programs by name (50+ apps)
"""
import os
import subprocess
import glob
from pathlib import Path
from typing import Dict, Any, Optional, List

# Comprehensive app registry (50+ apps)
APP_REGISTRY: Dict[str, Dict[str, Any]] = {
    # Browsers
    "chrome": {"exe": "chrome.exe", "paths": [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    ]},
    "firefox": {"exe": "firefox.exe", "paths": [
        r"C:\Program Files\Mozilla Firefox\firefox.exe",
        r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe"
    ]},
    "edge": {"exe": "msedge.exe", "paths": [
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    ]},
    "brave": {"exe": "brave.exe", "paths": [
        r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
    ]},
    "opera": {"exe": "opera.exe", "paths": [
        r"C:\Program Files\Opera\opera.exe"
    ]},

    # Code editors
    "vscode": {"exe": "Code.exe", "paths": []},
    "notepad": {"exe": "notepad.exe", "paths": [r"C:\Windows\notepad.exe"]},
    "notepadpp": {"exe": "notepad++.exe", "paths": [
        r"C:\Program Files\Notepad++\notepad++.exe",
        r"C:\Program Files (x86)\Notepad++\notepad++.exe"
    ]},
    "sublimetext": {"exe": "sublime_text.exe", "paths": [
        r"C:\Program Files\Sublime Text\sublime_text.exe"
    ]},
    "atom": {"exe": "atom.exe", "paths": []},

    # Media players
    "vlc": {"exe": "vlc.exe", "paths": [
        r"C:\Program Files\VideoLAN\VLC\vlc.exe",
        r"C:\Program Files (x86)\VideoLAN\VLC\vlc.exe"
    ]},
    "mediaplayer": {"exe": "wmplayer.exe", "paths": [
        r"C:\Program Files\Windows Media Player\wmplayer.exe",
        r"C:\Program Files (x86)\Windows Media Player\wmplayer.exe"
    ]},
    "wmp": {"exe": "wmplayer.exe", "paths": [  # alias
        r"C:\Program Files\Windows Media Player\wmplayer.exe",
        r"C:\Program Files (x86)\Windows Media Player\wmplayer.exe",
    ]},
    "spotify": {"exe": "Spotify.exe", "paths": [
        rf"C:\Users\{os.getenv('USERNAME','user')}\AppData\Roaming\Spotify\Spotify.exe",
        r"C:\Program Files\Spotify\Spotify.exe",
        r"C:\Program Files (x86)\Spotify\Spotify.exe",
    ]},
    "itunes": {"exe": "iTunes.exe", "paths": [
        r"C:\Program Files\iTunes\iTunes.exe",
        r"C:\Program Files (x86)\iTunes\iTunes.exe",
    ]},

    # Communication
    "discord": {"exe": "Discord.exe", "paths": [
        rf"C:\Users\{os.getenv('USERNAME','user')}\AppData\Local\Discord\app-*\Discord.exe",
    ]},
    "slack": {"exe": "slack.exe", "paths": [
        rf"C:\Users\{os.getenv('USERNAME','user')}\AppData\Local\slack\slack.exe",
    ]},
    "teams": {"exe": "Teams.exe", "paths": [
        rf"C:\Users\{os.getenv('USERNAME','user')}\AppData\Local\Microsoft\Teams\current\Teams.exe",
    ]},
    "zoom": {"exe": "Zoom.exe", "paths": [
        rf"C:\Users\{os.getenv('USERNAME','user')}\AppData\Roaming\Zoom\bin\Zoom.exe",
    ]},
    "skype": {"exe": "Skype.exe", "paths": [
        r"C:\Program Files\Microsoft\Skype for Desktop\Skype.exe",
    ]},

    # Office
    "word": {"exe": "WINWORD.EXE", "paths": [
        r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
        r"C:\Program Files (x86)\Microsoft Office\Office16\WINWORD.EXE",
    ]},
    "excel": {"exe": "EXCEL.EXE", "paths": [
        r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
        r"C:\Program Files (x86)\Microsoft Office\Office16\EXCEL.EXE",
    ]},
    "powerpoint": {"exe": "POWERPNT.EXE", "paths": [
        r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE",
    ]},
    "outlook": {"exe": "OUTLOOK.EXE", "paths": [
        r"C:\Program Files\Microsoft Office\root\Office16\OUTLOOK.EXE",
    ]},

    # System tools
    "explorer": {"exe": "explorer.exe", "paths": [r"C:\Windows\explorer.exe"]},
    "files": {"exe": "explorer.exe", "paths": [r"C:\Windows\explorer.exe"]},
    "taskmanager": {"exe": "taskmgr.exe", "paths": [r"C:\Windows\System32\taskmgr.exe"]},
    "calculator": {"exe": "calc.exe", "paths": [r"C:\Windows\System32\calc.exe"]},
    "cmd": {"exe": "cmd.exe", "paths": [r"C:\Windows\System32\cmd.exe"]},
    "powershell": {"exe": "powershell.exe", "paths": [
        r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
    ]},
    "terminal": {"exe": "wt.exe", "paths": [
        r"C:\Program Files\WindowsApps\Microsoft.WindowsTerminal_*\wt.exe"
    ]},
    "paint": {"exe": "mspaint.exe", "paths": [r"C:\Windows\System32\mspaint.exe"]},
    "snip": {"exe": "SnippingTool.exe", "paths": [r"C:\Windows\System32\SnippingTool.exe"]},
    "wordpad": {"exe": "wordpad.exe", "paths": [r"C:\Program Files\Windows NT\Accessories\wordpad.exe"]},

    # Dev tools
    "git": {"exe": "git.exe", "paths": []},
    "gitkraken": {"exe": "gitkraken.exe", "paths": [
        rf"C:\Users\{os.getenv('USERNAME','user')}\AppData\Local\gitkraken\gitkraken.exe"
    ]},
    "postman": {"exe": "Postman.exe", "paths": [
        rf"C:\Users\{os.getenv('USERNAME','user')}\AppData\Local\Postman\Postman.exe"
    ]},

    # Games
    "steam": {"exe": "steam.exe", "paths": [r"C:\Program Files (x86)\Steam\steam.exe"]},
    "epicgames": {"exe": "EpicGamesLauncher.exe", "paths": [
        r"C:\Program Files (x86)\Epic Games\Launcher\Portal\Binaries\Win32\EpicGamesLauncher.exe"
    ]},

    # Other
    "obs": {"exe": "obs64.exe", "paths": [r"C:\Program Files\obs-studio\bin\64bit\obs64.exe"]},
    "audacity": {"exe": "audacity.exe", "paths": [r"C:\Program Files\Audacity\audacity.exe"]},
    "gimp": {"exe": "gimp-2.10.exe", "paths": [r"C:\Program Files\GIMP 2\bin\gimp-2.10.exe"]},
    "blender": {"exe": "blender.exe", "paths": [r"C:\Program Files\Blender Foundation\Blender *\blender.exe"]},
}


def _resolve_app_exe(app_name: str) -> Optional[str]:
    """Find executable path or return bare exe for PATH lookup."""
    key = app_name.lower().replace(" ", "").replace("-", "").replace("+", "p")
    info = APP_REGISTRY.get(key)
    if not info:
        return app_name if app_name.lower().endswith(".exe") else app_name + ".exe"

    # Check known paths (glob support for versioned folders)
    for p in info.get("paths", []):
        if not p:
            continue
        if "*" in p:
            hits = glob.glob(p)
            if hits:
                return hits[0]
        else:
            if Path(p).exists():
                return p

    # Fallback to bare exe (Windows PATH will resolve)
    return info.get("exe")


def launch_app(app_name: str, args: str = "") -> Dict[str, Any]:
    """Launch a desktop application. Non-blocking."""
    try:
        exe = _resolve_app_exe(app_name)
        if not exe:
            return {"ok": False, "error": f"'{app_name}' not found. May not be installed or in PATH."}

        cmd = [exe] + (args.split() if args else [])
        subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
        return {"ok": True, "message": f"Launched {app_name}.", "exe": exe}
    except FileNotFoundError:
        return {"ok": False, "error": f"'{app_name}' not found. May not be installed or in PATH."}
    except Exception as e:
        return {"ok": False, "error": f"{type(e).__name__}: {str(e)}"}


def list_known_apps() -> List[Dict[str, str]]:
    """Return registry for UI."""
    return [{"name": name, "exe": info.get("exe", "")} for name, info in sorted(APP_REGISTRY.items())]


# ============================================================================
# MEDIA PLAYBACK -- search user's media folders then launch via mpv
# ============================================================================
MPV_PATH = os.getenv("MPV_PATH", "mpv").strip()
MEDIA_EXTENSIONS = {'.mp3', '.wav', '.flac', '.m4a', '.aac', '.ogg',
                    '.mp4', '.mkv', '.webm'}

# Directories to search for media files
_MEDIA_DIRS = [
    Path.home() / "Music",
    Path.home() / "Videos",
    Path.home() / "Downloads",
]


def _collect_media_files(dirs: List[Path]) -> List[Path]:
    """Recursively collect playable media files from given directories."""
    files: List[Path] = []
    for d in dirs:
        if not d.exists():
            continue
        for ext in MEDIA_EXTENSIONS:
            files.extend(d.rglob(f"*{ext}"))
    return files


def _resolve_media_path(query: str) -> tuple:
    """
    Resolve a query to an existing media file.
    Handles: exact path, folder (search within), partial filename.
    Returns (Path | None, error_str | None, sample_list | None).
    """
    # 1. Exact path provided?
    candidate = Path(query)
    if candidate.is_file() and candidate.suffix.lower() in MEDIA_EXTENSIONS:
        return (candidate.resolve(), None, None)

    # 2. Folder provided? Search inside it.
    if candidate.is_dir():
        found: List[Path] = []
        for ext in MEDIA_EXTENSIONS:
            found.extend(candidate.rglob(f"*{ext}"))
        if found:
            return (sorted(found)[0].resolve(), None, None)
        return (None, f"No media files found in folder: {candidate}", None)

    # 3. Fuzzy search across media dirs
    all_files = _collect_media_files(_MEDIA_DIRS)
    if not all_files:
        return (None, "No media files found in Music/Videos/Downloads", None)

    q = query.lower()
    scored: List[tuple] = []
    for f in all_files:
        name_lower = f.stem.lower()
        if q in name_lower:
            scored.append((abs(len(name_lower) - len(q)), f))
        elif any(word in name_lower for word in q.split()):
            scored.append((100 + len(name_lower), f))

    if not scored:
        names = [f.name for f in sorted(all_files)[:15]]
        return (None, f"No file matching '{query}'.", names)

    scored.sort(key=lambda x: x[0])
    return (scored[0][1].resolve(), None, None)


def play_media(query: str = "", **_kwargs) -> Dict[str, Any]:
    """
    Search user's media folders for a matching file and play it with mpv.
    Resolves the query to an actual file path before launching.
    """
    if not query.strip():
        all_files = _collect_media_files(_MEDIA_DIRS)
        if not all_files:
            return {"ok": False, "error": "No media files found in Music/Videos/Downloads."}
        names = [f.name for f in sorted(all_files)[:20]]
        return {"ok": True, "message": f"Found {len(all_files)} media files. Specify a name.", "sample_files": names}

    resolved, error, samples = _resolve_media_path(query)

    if error:
        result: Dict[str, Any] = {"ok": False, "error": error}
        if samples:
            result["available_files"] = samples
        return result

    # Final safety: must be a real file with allowed extension
    if not resolved.is_file():
        return {"ok": False, "error": f"Resolved path is not a file: {resolved}"}
    if resolved.suffix.lower() not in MEDIA_EXTENSIONS:
        return {"ok": False, "error": f"File type not allowed: {resolved.suffix}"}

    # Launch mpv -- list args, shell=False
    try:
        cmd = [MPV_PATH, "--force-window=yes", "--title=Joi Player", "--", str(resolved)]
        print(f"  [play_media] launching: {cmd}")
        subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
        return {
            "ok": True,
            "message": f"Now playing: {resolved.name}",
            "resolved_path": str(resolved),
            "player": "mpv"
        }
    except FileNotFoundError:
        return {"ok": False, "error": f"mpv not found at '{MPV_PATH}'. Set MPV_PATH env var to the correct path."}
    except Exception as e:
        return {"ok": False, "error": f"Failed to launch mpv: {type(e).__name__}: {str(e)}"}


# Register tools
import joi_companion
joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "launch_app",
        "description": "Open a desktop app by name (Chrome, VLC, Spotify, Word, VS Code, etc). Use this when Lonnie says 'open X', 'launch X', 'start X'. Do NOT use this for playing music -- use play_media instead.",
        "parameters": {"type": "object", "properties": {
            "app_name": {"type": "string", "description": "App name: chrome, vlc, spotify, vscode, word, excel, discord, etc"},
            "args": {"type": "string", "description": "Optional arguments (URL for browsers, file path for editors)", "default": ""}
        }, "required": ["app_name"]}
    }},
    launch_app
)

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "play_media",
        "description": "Play a music or video file using mpv. Searches Lonnie's Music, Videos, and Downloads folders for matching files. Use when Lonnie asks to play music, a song, a video, or any media. Always use this instead of launch_app for media playback.",
        "parameters": {"type": "object", "properties": {
            "query": {"type": "string", "description": "Song/video name, keyword, or full file path to play"}
        }, "required": ["query"]}
    }},
    play_media
)

# Register /apps routes
from flask import jsonify
from modules.joi_memory import require_user

def get_apps():
    require_user()
    return jsonify({"ok": True, "apps": list_known_apps()})

def launch_app_route():
    require_user()
    from flask import request
    data = request.get_json(force=True) or {}
    return jsonify(launch_app(data.get("app_name", ""), data.get("args", "")))

joi_companion.register_route("/apps", ["GET"], get_apps, "get_apps")
joi_companion.register_route("/apps/launch", ["POST"], launch_app_route, "launch_app_route")
