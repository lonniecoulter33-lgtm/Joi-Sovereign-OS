"""
modules/joi_app_factory.py

App Factory -- Command execution, project scaffolding, and build tooling.
===========================================================================
Enables the Agent Terminal to create standalone apps from scratch:
  - Safe shell command execution (blocklist-gated)
  - 6 project templates (Python CLI/Flask/FastAPI/Desktop, HTML SPA, Node Express)
  - Build/package tooling (PyInstaller, pip, npm, zip)
  - Tools: scaffold_project, list_templates, build_project, run_setup_command, get_build_configs
  - Routes: GET /app-factory/templates, POST /app-factory/build
"""

import json
import os
import re
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any, Dict, List, Tuple

import joi_companion
from flask import jsonify, request as flask_req

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# ══════════════════════════════════════════════════════════════════════════════
# COMMAND SAFETY
# ══════════════════════════════════════════════════════════════════════════════

BLOCKED_PATTERNS = [
    r"rm\s+(-rf?|--force)\s+[/\\]",      # rm -rf /
    r"format\s+[a-zA-Z]:",                # format C:
    r"del\s+/[sS]", r"rmdir\s+/[sS]",    # Windows recursive delete
    r"mkfs\.", r"dd\s+if=",               # disk operations
    r"shutdown|reboot|halt",              # system control
    r"net\s+user", r"reg\s+delete",       # Windows admin
    r"powershell.*-enc",                  # obfuscated PS
    r">\s*/dev/sd",                        # raw disk write
    r"curl.*\|\s*sh", r"wget.*\|\s*sh",   # pipe-to-shell
    r"chmod\s+777\s+/",                   # root permission blast
]

_BLOCKED_RE = [re.compile(p, re.IGNORECASE) for p in BLOCKED_PATTERNS]


def is_command_safe(cmd: str) -> Tuple[bool, str]:
    """Check command against blocklist. Returns (safe, reason)."""
    if not cmd or not cmd.strip():
        return False, "Empty command"
    for i, pattern in enumerate(_BLOCKED_RE):
        if pattern.search(cmd):
            return False, f"Blocked by safety rule: {BLOCKED_PATTERNS[i]}"
    return True, ""


def run_setup_command(**kwargs) -> Dict[str, Any]:
    """Execute a shell command sandboxed to project_root.

    kwargs: command, project_root, timeout=120
    Returns: {ok, stdout, stderr, exit_code, command}
    """
    command = kwargs.get("command", "")
    project_root = kwargs.get("project_root", str(BASE_DIR))
    timeout = int(kwargs.get("timeout", 120))

    if not command:
        return {"ok": False, "error": "No command provided"}

    safe, reason = is_command_safe(command)
    if not safe:
        return {"ok": False, "error": f"Blocked: {reason}", "command": command}

    # Ensure project_root exists
    root = Path(project_root)
    root.mkdir(parents=True, exist_ok=True)

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(root),
            env={**os.environ, "PYTHONPATH": str(root)},
        )
        return {
            "ok": result.returncode == 0,
            "stdout": (result.stdout or "")[:5000],
            "stderr": (result.stderr or "")[:5000],
            "exit_code": result.returncode,
            "command": command,
        }
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": f"Timed out after {timeout}s", "command": command}
    except Exception as e:
        return {"ok": False, "error": str(e), "command": command}


# ══════════════════════════════════════════════════════════════════════════════
# PROJECT SCAFFOLDING TEMPLATES
# ══════════════════════════════════════════════════════════════════════════════

TEMPLATES: Dict[str, Dict[str, Any]] = {
    "python_cli": {
        "description": "Python CLI application with src/, tests/, and setup.py",
        "dirs": ["src", "tests"],
        "files": {
            "src/__init__.py": "",
            "src/main.py": '''"""
{project_name} -- CLI entry point.
"""
import argparse
import sys


def main():
    parser = argparse.ArgumentParser(description="{project_name}")
    parser.add_argument("input", nargs="?", help="Input file or value")
    parser.add_argument("-o", "--output", help="Output file")
    args = parser.parse_args()

    print(f"{project_name} is running...")
    # TODO: implement your logic here

    return 0


if __name__ == "__main__":
    sys.exit(main())
''',
            "tests/__init__.py": "",
            "tests/test_main.py": '''"""Tests for {project_name}."""
import unittest
from src.main import main


class TestMain(unittest.TestCase):
    def test_runs(self):
        """Smoke test -- main() should return 0."""
        self.assertEqual(main(), 0)


if __name__ == "__main__":
    unittest.main()
''',
            "setup.py": '''from setuptools import setup, find_packages

setup(
    name="{project_name}",
    version="0.1.0",
    packages=find_packages(),
    entry_points={{
        "console_scripts": [
            "{project_name}=src.main:main",
        ],
    }},
)
''',
            "requirements.txt": "# Add your dependencies here\n",
            "README.md": "# {project_name}\n\nA Python CLI application.\n",
        },
        "setup_commands": ["pip install -e ."],
    },

    "python_flask": {
        "description": "Flask web application with templates and static files",
        "dirs": ["templates", "static", "static/css", "static/js"],
        "files": {
            "app.py": '''"""
{project_name} -- Flask web application.
"""
from flask import Flask, render_template, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", title="{project_name}")


@app.route("/api/health")
def health():
    return jsonify({{"status": "ok", "app": "{project_name}"}})


if __name__ == "__main__":
    app.run(debug=True, port=5001)
''',
            "templates/index.html": '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{{{ title }}}}</title>
    <link rel="stylesheet" href="{{{{ url_for('static', filename='css/style.css') }}}}">
</head>
<body>
    <div class="container">
        <h1>{project_name}</h1>
        <p>Welcome to your Flask application.</p>
    </div>
    <script src="{{{{ url_for('static', filename='js/app.js') }}}}"></script>
</body>
</html>
''',
            "static/css/style.css": '''* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f5f5f5; color: #333; }}
.container {{ max-width: 800px; margin: 2rem auto; padding: 2rem; background: #fff; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
h1 {{ margin-bottom: 1rem; color: #2c3e50; }}
''',
            "static/js/app.js": '// {project_name} -- client-side JavaScript\nconsole.log("{project_name} loaded");\n',
            "requirements.txt": "flask>=3.0\n",
            "README.md": "# {project_name}\n\nA Flask web application.\n\n## Run\n```\npip install -r requirements.txt\npython app.py\n```\n",
        },
        "setup_commands": ["pip install -r requirements.txt"],
    },

    "python_fastapi": {
        "description": "FastAPI application with async support",
        "dirs": [],
        "files": {
            "main.py": '''"""
{project_name} -- FastAPI application.
"""
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="{project_name}")


class HealthResponse(BaseModel):
    status: str
    app: str


@app.get("/")
async def root():
    return {{"message": "Welcome to {project_name}"}}


@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(status="ok", app="{project_name}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
''',
            "requirements.txt": "fastapi>=0.110\nuvicorn[standard]>=0.27\n",
            "README.md": "# {project_name}\n\nA FastAPI application.\n\n## Run\n```\npip install -r requirements.txt\nuvicorn main:app --reload\n```\n",
        },
        "setup_commands": ["pip install -r requirements.txt"],
    },

    "python_desktop": {
        "description": "Python desktop GUI application using tkinter",
        "dirs": ["assets"],
        "files": {
            "main.py": '''"""
{project_name} -- Desktop GUI application (tkinter).
"""
import tkinter as tk
from tkinter import ttk, messagebox


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("{project_name}")
        self.geometry("600x400")
        self.configure(bg="#f0f0f0")
        self._build_ui()

    def _build_ui(self):
        frame = ttk.Frame(self, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="{project_name}", font=("Segoe UI", 18, "bold")).pack(pady=10)
        ttk.Label(frame, text="Your desktop application is ready.").pack(pady=5)

        btn = ttk.Button(frame, text="Click Me", command=self._on_click)
        btn.pack(pady=20)

    def _on_click(self):
        messagebox.showinfo("{project_name}", "Hello from {project_name}!")


if __name__ == "__main__":
    app = App()
    app.mainloop()
''',
            "README.md": "# {project_name}\n\nA Python desktop application using tkinter.\n\n## Run\n```\npython main.py\n```\n",
        },
        "setup_commands": [],
    },

    "html_spa": {
        "description": "Single-page HTML/CSS/JS application",
        "dirs": ["css", "js", "assets"],
        "files": {
            "index.html": '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project_name}</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <header>
        <h1>{project_name}</h1>
    </header>
    <main id="app">
        <p>Welcome to {project_name}.</p>
    </main>
    <script src="js/app.js"></script>
</body>
</html>
''',
            "css/style.css": '''* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #1a1a2e; color: #eee; }}
header {{ background: #16213e; padding: 1.5rem 2rem; text-align: center; }}
header h1 {{ color: #e94560; }}
main {{ max-width: 900px; margin: 2rem auto; padding: 2rem; }}
''',
            "js/app.js": '''// {project_name} -- main application logic
document.addEventListener("DOMContentLoaded", () => {{
    console.log("{project_name} loaded");
    const app = document.getElementById("app");
    // TODO: build your app here
}});
''',
            "README.md": "# {project_name}\n\nA single-page web application.\n\n## Run\nOpen `index.html` in your browser.\n",
        },
        "setup_commands": [],
    },

    "node_express": {
        "description": "Node.js Express API server",
        "dirs": ["src", "src/routes"],
        "files": {
            "package.json": '''{{\n  "name": "{project_name}",\n  "version": "1.0.0",\n  "description": "{project_name} -- Express API",\n  "main": "src/index.js",\n  "scripts": {{\n    "start": "node src/index.js",\n    "dev": "node --watch src/index.js"\n  }},\n  "dependencies": {{\n    "express": "^4.18.0"\n  }}\n}}
''',
            "src/index.js": '''const express = require("express");
const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

// Routes
const apiRoutes = require("./routes/api");
app.use("/api", apiRoutes);

app.get("/", (req, res) => {{
    res.json({{ message: "Welcome to {project_name}" }});
}});

app.listen(PORT, () => {{
    console.log(`{project_name} running on http://localhost:${{PORT}}`);
}});
''',
            "src/routes/api.js": '''const express = require("express");
const router = express.Router();

router.get("/health", (req, res) => {{
    res.json({{ status: "ok", app: "{project_name}" }});
}});

module.exports = router;
''',
            "README.md": "# {project_name}\n\nA Node.js Express API server.\n\n## Run\n```\nnpm install\nnpm start\n```\n",
        },
        "setup_commands": ["npm install"],
    },
}


def scaffold_project(**kwargs) -> Dict[str, Any]:
    """Create project from template.

    kwargs: template, project_path, project_name, run_setup=False
    Returns: {ok, files_created, dirs_created, skipped, setup_results}
    """
    template_name = kwargs.get("template", "python_cli")
    project_path = kwargs.get("project_path", "")
    project_name = kwargs.get("project_name", "my_project")
    run_setup = kwargs.get("run_setup", False)

    if not project_path:
        return {"ok": False, "error": "No project_path provided"}

    tmpl = TEMPLATES.get(template_name)
    if not tmpl:
        return {"ok": False, "error": f"Unknown template: {template_name}",
                "available": list(TEMPLATES.keys())}

    root = Path(project_path)
    root.mkdir(parents=True, exist_ok=True)

    dirs_created = 0
    files_created = 0
    skipped = []

    # Create directories
    for d in tmpl.get("dirs", []):
        dp = root / d
        dp.mkdir(parents=True, exist_ok=True)
        dirs_created += 1

    # Create files (with {project_name} substitution)
    for rel_path, content in tmpl.get("files", {}).items():
        fp = root / rel_path
        if fp.exists():
            skipped.append(rel_path)
            continue
        fp.parent.mkdir(parents=True, exist_ok=True)
        rendered = content.replace("{project_name}", project_name)
        fp.write_text(rendered, encoding="utf-8")
        files_created += 1

    # Optionally run setup commands
    setup_results = []
    if run_setup:
        for cmd in tmpl.get("setup_commands", []):
            result = run_setup_command(command=cmd, project_root=str(root), timeout=120)
            setup_results.append({"command": cmd, "ok": result.get("ok", False),
                                  "stderr": result.get("stderr", "")[:300]})

    return {
        "ok": True,
        "template": template_name,
        "project_path": str(root),
        "files_created": files_created,
        "dirs_created": dirs_created,
        "skipped": skipped,
        "setup_results": setup_results,
    }


def list_templates(**kwargs) -> Dict[str, Any]:
    """List available scaffold templates."""
    templates = []
    for name, tmpl in TEMPLATES.items():
        templates.append({
            "name": name,
            "description": tmpl.get("description", ""),
            "files": list(tmpl.get("files", {}).keys()),
            "setup_commands": tmpl.get("setup_commands", []),
        })
    return {"ok": True, "templates": templates}


# ══════════════════════════════════════════════════════════════════════════════
# BUILD / PACKAGE TOOLING
# ══════════════════════════════════════════════════════════════════════════════

BUILD_CONFIGS: Dict[str, Dict[str, Any]] = {
    "python_exe": {
        "description": "Build standalone .exe with PyInstaller",
        "commands": ["pip install pyinstaller", "pyinstaller --onefile {entry_point}"],
    },
    "python_package": {
        "description": "Install package in development mode",
        "commands": ["pip install -e ."],
    },
    "web_zip": {
        "description": "Package web project as .zip archive",
        "handler": "_build_web_zip",
    },
    "node_build": {
        "description": "Build Node.js project (npm install + npm run build)",
        "commands": ["npm install", "npm run build"],
    },
}


def _build_web_zip(project_path: str) -> Dict[str, Any]:
    """Package web project as .zip using shutil."""
    root = Path(project_path)
    if not root.exists():
        return {"ok": False, "error": f"Project path does not exist: {project_path}"}

    archive_name = root.name
    output_dir = root.parent
    try:
        archive_path = shutil.make_archive(
            str(output_dir / archive_name), "zip", str(root)
        )
        return {"ok": True, "output_path": archive_path, "message": f"Packaged as {archive_path}"}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def build_project(**kwargs) -> Dict[str, Any]:
    """Build/package a project.

    kwargs: build_type, project_path, entry_point=""
    Returns: {ok, build_type, output_path, message}
    """
    build_type = kwargs.get("build_type", "")
    project_path = kwargs.get("project_path", "")
    entry_point = kwargs.get("entry_point", "main.py")

    if not build_type:
        return {"ok": False, "error": "No build_type provided",
                "available": list(BUILD_CONFIGS.keys())}
    if not project_path:
        return {"ok": False, "error": "No project_path provided"}

    config = BUILD_CONFIGS.get(build_type)
    if not config:
        return {"ok": False, "error": f"Unknown build_type: {build_type}",
                "available": list(BUILD_CONFIGS.keys())}

    # Special handler (web_zip)
    if "handler" in config:
        return _build_web_zip(project_path)

    # Command-based build
    results = []
    for cmd_template in config.get("commands", []):
        cmd = cmd_template.replace("{entry_point}", entry_point)
        result = run_setup_command(command=cmd, project_root=project_path, timeout=300)
        results.append({"command": cmd, "ok": result.get("ok", False),
                        "stderr": result.get("stderr", "")[:500]})
        if not result.get("ok"):
            return {"ok": False, "build_type": build_type, "error": f"Build step failed: {cmd}",
                    "details": results}

    # Determine output path
    output_path = ""
    if build_type == "python_exe":
        dist_dir = Path(project_path) / "dist"
        if dist_dir.exists():
            exes = list(dist_dir.glob("*.exe"))
            if exes:
                output_path = str(exes[0])
            else:
                # Unix
                files = list(dist_dir.iterdir())
                if files:
                    output_path = str(files[0])

    return {
        "ok": True,
        "build_type": build_type,
        "output_path": output_path,
        "message": f"Build complete ({build_type})",
        "steps": results,
    }


def get_build_configs(**kwargs) -> Dict[str, Any]:
    """List available build configurations."""
    configs = {}
    for name, cfg in BUILD_CONFIGS.items():
        configs[name] = {
            "description": cfg.get("description", ""),
            "commands": cfg.get("commands", []),
        }
    return {"ok": True, "configs": configs}


# ══════════════════════════════════════════════════════════════════════════════
# FLASK ROUTES
# ══════════════════════════════════════════════════════════════════════════════

@joi_companion.app.route("/app-factory/templates", methods=["GET"])
def app_factory_templates():
    """List available project templates."""
    return jsonify(list_templates())


@joi_companion.app.route("/app-factory/build", methods=["POST"])
def app_factory_build():
    """Build/package a project."""
    data = flask_req.get_json(force=True) or {}
    result = build_project(
        build_type=data.get("build_type", ""),
        project_path=data.get("project_path", ""),
        entry_point=data.get("entry_point", "main.py"),
    )
    return jsonify(result)


# ══════════════════════════════════════════════════════════════════════════════
# TOOL REGISTRATION
# ══════════════════════════════════════════════════════════════════════════════

# scaffold_project
joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "scaffold_project",
        "description": "Create a new project from a template (python_cli, python_flask, python_fastapi, "
                       "python_desktop, html_spa, node_express). Creates directory structure and starter files.",
        "parameters": {"type": "object", "properties": {
            "template": {"type": "string", "description": "Template name (e.g. python_flask, html_spa)"},
            "project_path": {"type": "string", "description": "Absolute path for the new project directory"},
            "project_name": {"type": "string", "description": "Human-readable project name (used in files)"},
            "run_setup": {"type": "boolean", "description": "Run template setup commands after scaffolding (default false)"},
        }, "required": ["template", "project_path", "project_name"]}
    }},
    scaffold_project,
)

# list_templates
joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "list_templates",
        "description": "List available project scaffold templates with their files and setup commands.",
        "parameters": {"type": "object", "properties": {}, "required": []}
    }},
    list_templates,
)

# build_project
joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "build_project",
        "description": "Build or package a project (python_exe with PyInstaller, python_package, web_zip, node_build).",
        "parameters": {"type": "object", "properties": {
            "build_type": {"type": "string", "description": "Build type (python_exe, python_package, web_zip, node_build)"},
            "project_path": {"type": "string", "description": "Absolute path to the project directory"},
            "entry_point": {"type": "string", "description": "Entry point file for builds (default: main.py)"},
        }, "required": ["build_type", "project_path"]}
    }},
    build_project,
)

# run_setup_command
joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "run_setup_command",
        "description": "Run a shell command in a project directory (safety-gated). Use for pip install, npm install, mkdir, etc.",
        "parameters": {"type": "object", "properties": {
            "command": {"type": "string", "description": "Shell command to execute"},
            "project_root": {"type": "string", "description": "Working directory for the command"},
            "timeout": {"type": "integer", "description": "Timeout in seconds (default 120)"},
        }, "required": ["command", "project_root"]}
    }},
    run_setup_command,
)

# get_build_configs
joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "get_build_configs",
        "description": "List available build/package configurations (python_exe, web_zip, etc.).",
        "parameters": {"type": "object", "properties": {}, "required": []}
    }},
    get_build_configs,
)

print("    [OK] joi_app_factory (App Factory: 5 tools, 2 routes)")
