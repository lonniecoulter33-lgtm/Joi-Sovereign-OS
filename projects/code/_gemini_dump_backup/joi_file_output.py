"""
modules/joi_file_output.py

File Output & Presentation System
==================================

Fixes Joi's file handling capabilities:
- Properly saves files to accessible locations
- Creates downloadable files in /mnt/user-data/outputs/
- Handles large code files (not just snippets)
- Integrates with proposals system
- Provides file preview capabilities
- Manages file organization (projects/, proposals/, research/)

This enables Joi to:
1. Save complete code files (not just show in chat)
2. Present files for download
3. Organize files by project/purpose
4. Save research findings properly
5. Export analysis results
"""

from __future__ import annotations

import os
import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime

import joi_companion
from flask import jsonify, request as flask_req, send_file
from modules.joi_memory import require_user

# ============================================================================
# CONFIGURATION
# ============================================================================

# Output directories
OUTPUTS_DIR = Path("/mnt/user-data/outputs")
PROJECTS_DIR = Path("projects")
RESEARCH_DIR = Path("research")
PROPOSALS_DIR = Path("proposals")

# Ensure all directories exist
for directory in [OUTPUTS_DIR, PROJECTS_DIR, RESEARCH_DIR, PROPOSALS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# File registry
FILE_REGISTRY = Path("file_registry.json")

# ============================================================================
# FILE REGISTRY
# ============================================================================

def _load_registry() -> Dict[str, Any]:
    """Load file registry"""
    if not FILE_REGISTRY.exists():
        return {"files": [], "projects": {}, "research_topics": {}}
    try:
        return json.loads(FILE_REGISTRY.read_text())
    except:
        return {"files": [], "projects": {}, "research_topics": {}}


def _save_registry(registry: Dict[str, Any]):
    """Save file registry"""
    FILE_REGISTRY.write_text(json.dumps(registry, indent=2))


def _register_file(
    filepath: Path,
    category: str,
    description: str = "",
    project_name: str = None,
    metadata: Dict[str, Any] = None
) -> str:
    """Register a file in the registry"""
    registry = _load_registry()
    
    file_id = f"file_{int(__import__('time').time() * 1000)}"
    
    file_record = {
        "file_id": file_id,
        "filename": filepath.name,
        "filepath": str(filepath),
        "category": category,
        "description": description,
        "project_name": project_name,
        "size_bytes": filepath.stat().st_size if filepath.exists() else 0,
        "created_at": __import__('time').time(),
        "created_datetime": datetime.now().isoformat(),
        "metadata": metadata or {}
    }
    
    registry["files"].append(file_record)
    
    # Update project tracking
    if project_name:
        if project_name not in registry["projects"]:
            registry["projects"][project_name] = []
        registry["projects"][project_name].append(file_id)
    
    # Keep last 1000 files
    if len(registry["files"]) > 1000:
        registry["files"] = registry["files"][-1000:]
    
    _save_registry(registry)
    
    return file_id


# ============================================================================
# FILE SAVING FUNCTIONS
# ============================================================================

def save_code_file(**params) -> Dict[str, Any]:
    """
    Tool: Save code to a file
    
    Args:
        code: The code content
        filename: Name for the file
        description: What this code does
        project_name: Optional project to associate with
        destination: Where to save ("outputs", "projects", "proposals")
    
    Returns:
        File path and download info
    """
    require_user()
    
    code = params.get("code", "")
    filename = params.get("filename", "code.py")
    description = params.get("description", "")
    project_name = params.get("project_name")
    destination = params.get("destination", "outputs")
    
    if not code:
        return {"ok": False, "error": "No code provided"}
    
    # Determine destination directory
    if destination == "outputs":
        dest_dir = OUTPUTS_DIR
    elif destination == "projects":
        dest_dir = PROJECTS_DIR
        if project_name:
            dest_dir = dest_dir / project_name
            dest_dir.mkdir(parents=True, exist_ok=True)
    elif destination == "proposals":
        dest_dir = PROPOSALS_DIR
    else:
        dest_dir = OUTPUTS_DIR
    
    # Create file path
    filepath = dest_dir / filename
    
    # Save file
    try:
        filepath.write_text(code)
        
        # Register file
        file_id = _register_file(
            filepath,
            category="code",
            description=description,
            project_name=project_name,
            metadata={
                "language": _detect_language(filename),
                "line_count": code.count('\n') + 1,
                "char_count": len(code)
            }
        )
        
        return {
            "ok": True,
            "file_id": file_id,
            "filename": filename,
            "filepath": str(filepath),
            "size_bytes": len(code),
            "line_count": code.count('\n') + 1,
            "message": f"File saved: {filepath}",
            "downloadable": destination == "outputs"
        }
        
    except Exception as e:
        return {"ok": False, "error": str(e)}


def save_text_file(**params) -> Dict[str, Any]:
    """
    Tool: Save text content to a file
    
    Args:
        content: Text content
        filename: Name for the file
        description: What this file contains
        format: File format ("txt", "md", "json")
        destination: Where to save
    
    Returns:
        File path and info
    """
    require_user()
    
    content = params.get("content", "")
    filename = params.get("filename", "document.txt")
    description = params.get("description", "")
    file_format = params.get("format", "txt")
    destination = params.get("destination", "outputs")
    
    if not content:
        return {"ok": False, "error": "No content provided"}
    
    # Ensure correct extension
    if not filename.endswith(f".{file_format}"):
        filename = f"{filename}.{file_format}"
    
    # Determine destination
    if destination == "outputs":
        dest_dir = OUTPUTS_DIR
    elif destination == "research":
        dest_dir = RESEARCH_DIR
    else:
        dest_dir = OUTPUTS_DIR
    
    filepath = dest_dir / filename
    
    try:
        filepath.write_text(content)
        
        file_id = _register_file(
            filepath,
            category="document",
            description=description,
            metadata={
                "format": file_format,
                "word_count": len(content.split()),
                "char_count": len(content)
            }
        )
        
        return {
            "ok": True,
            "file_id": file_id,
            "filename": filename,
            "filepath": str(filepath),
            "size_bytes": len(content),
            "message": f"File saved: {filepath}",
            "downloadable": destination == "outputs"
        }
        
    except Exception as e:
        return {"ok": False, "error": str(e)}


def save_research_findings(**params) -> Dict[str, Any]:
    """
    Tool: Save research findings to research directory
    
    Args:
        topic: Research topic
        findings: Research content (markdown format)
        sources: List of sources
        summary: Brief summary
    
    Returns:
        File path and research ID
    """
    require_user()
    
    topic = params.get("topic", "Research")
    findings = params.get("findings", "")
    sources = params.get("sources", [])
    summary = params.get("summary", "")
    
    if not findings:
        return {"ok": False, "error": "No findings provided"}
    
    # Create filename from topic
    safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_')).strip()
    safe_topic = safe_topic.replace(' ', '_')
    timestamp = int(__import__('time').time())
    filename = f"research_{safe_topic}_{timestamp}.md"
    
    # Format content
    content = f"# Research: {topic}\n\n"
    content += f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    if summary:
        content += f"## Summary\n\n{summary}\n\n"
    
    content += f"## Findings\n\n{findings}\n\n"
    
    if sources:
        content += f"## Sources\n\n"
        for i, source in enumerate(sources, 1):
            content += f"{i}. {source}\n"
    
    filepath = RESEARCH_DIR / filename
    
    try:
        filepath.write_text(content)
        
        # Register in research topics
        registry = _load_registry()
        if topic not in registry["research_topics"]:
            registry["research_topics"][topic] = []
        
        file_id = _register_file(
            filepath,
            category="research",
            description=f"Research findings on: {topic}",
            metadata={
                "topic": topic,
                "sources_count": len(sources),
                "has_summary": bool(summary)
            }
        )
        
        registry["research_topics"][topic].append(file_id)
        _save_registry(registry)
        
        return {
            "ok": True,
            "file_id": file_id,
            "filename": filename,
            "filepath": str(filepath),
            "topic": topic,
            "message": f"Research saved: {filepath}",
            "downloadable": False,  # Research stays in research/ folder
            "view_path": f"/research/{filename}"
        }
        
    except Exception as e:
        return {"ok": False, "error": str(e)}


def _detect_language(filename: str) -> str:
    """Detect programming language from filename"""
    ext_to_lang = {
        ".py": "python",
        ".js": "javascript",
        ".ts": "typescript",
        ".jsx": "react",
        ".html": "html",
        ".css": "css",
        ".json": "json",
        ".md": "markdown",
        ".txt": "text",
        ".sh": "bash",
        ".sql": "sql",
        ".java": "java",
        ".cpp": "cpp",
        ".c": "c",
        ".go": "go",
        ".rs": "rust",
        ".php": "php",
        ".rb": "ruby"
    }
    
    ext = Path(filename).suffix.lower()
    return ext_to_lang.get(ext, "unknown")


# ============================================================================
# FILE LISTING & RETRIEVAL
# ============================================================================

def list_files(**params) -> Dict[str, Any]:
    """
    Tool: List available files
    
    Args:
        category: Filter by category ("code", "document", "research")
        project_name: Filter by project
        limit: Maximum files to return
    
    Returns:
        List of files with metadata
    """
    require_user()

    category = params.get("category")
    project_name = params.get("project_name")
    limit = params.get("limit", 50)
    
    registry = _load_registry()
    
    files = registry["files"]
    
    # Filter by category
    if category:
        files = [f for f in files if f["category"] == category]
    
    # Filter by project
    if project_name:
        files = [f for f in files if f.get("project_name") == project_name]
    
    # Sort by creation time (newest first)
    files.sort(key=lambda x: x["created_at"], reverse=True)
    
    # Limit results
    files = files[:limit]
    
    return {
        "ok": True,
        "files": files,
        "total": len(files),
        "projects": list(registry["projects"].keys()),
        "research_topics": list(registry["research_topics"].keys())
    }


def get_file_content(**params) -> Dict[str, Any]:
    """
    Tool: Get content of a file
    
    Args:
        file_id: File ID from registry
    
    Returns:
        File content and metadata
    """
    require_user()
    
    file_id = params.get("file_id")
    if not file_id:
        return {"ok": False, "error": "file_id required"}
    
    registry = _load_registry()
    
    # Find file
    file_record = next((f for f in registry["files"] if f["file_id"] == file_id), None)
    
    if not file_record:
        return {"ok": False, "error": "File not found"}
    
    filepath = Path(file_record["filepath"])
    
    if not filepath.exists():
        return {"ok": False, "error": "File no longer exists"}
    
    try:
        content = filepath.read_text()
        
        return {
            "ok": True,
            "file_id": file_id,
            "filename": file_record["filename"],
            "content": content,
            "metadata": file_record
        }
        
    except Exception as e:
        return {"ok": False, "error": str(e)}


# ============================================================================
# TOOL REGISTRATION
# ============================================================================

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "save_code_file",
        "description": "Save code to a file. Properly saves complete code (not snippets) to downloadable location.",
        "parameters": {
            "type": "object",
            "properties": {
                "code": {"type": "string", "description": "Complete code content"},
                "filename": {"type": "string", "description": "Filename (e.g., 'module.py')"},
                "description": {"type": "string", "description": "What this code does"},
                "project_name": {"type": "string", "description": "Project name (optional)"},
                "destination": {"type": "string", "enum": ["outputs", "projects", "proposals"], "description": "Where to save"}
            },
            "required": ["code", "filename"]
        }
    }},
    save_code_file
)

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "save_text_file",
        "description": "Save text content to a file (documents, markdown, JSON, etc.)",
        "parameters": {
            "type": "object",
            "properties": {
                "content": {"type": "string", "description": "Text content"},
                "filename": {"type": "string", "description": "Filename"},
                "description": {"type": "string", "description": "File description"},
                "format": {"type": "string", "enum": ["txt", "md", "json"], "description": "File format"},
                "destination": {"type": "string", "enum": ["outputs", "research"], "description": "Where to save"}
            },
            "required": ["content", "filename"]
        }
    }},
    save_text_file
)

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "save_research_findings",
        "description": "Save research findings to research directory with proper formatting and sources",
        "parameters": {
            "type": "object",
            "properties": {
                "topic": {"type": "string", "description": "Research topic"},
                "findings": {"type": "string", "description": "Research content (markdown)"},
                "sources": {"type": "array", "items": {"type": "string"}, "description": "Source URLs/citations"},
                "summary": {"type": "string", "description": "Brief summary"}
            },
            "required": ["topic", "findings"]
        }
    }},
    save_research_findings
)

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "list_files",
        "description": "List saved files with optional filters",
        "parameters": {
            "type": "object",
            "properties": {
                "category": {"type": "string", "enum": ["code", "document", "research"]},
                "project_name": {"type": "string"},
                "limit": {"type": "integer"}
            }
        }
    }},
    list_files
)

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "get_file_content",
        "description": "Get content of a previously saved file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_id": {"type": "string", "description": "File ID from list_files"}
            },
            "required": ["file_id"]
        }
    }},
    get_file_content
)


# ============================================================================
# FLASK ROUTES
# ============================================================================

def files_route():
    """File management endpoint"""
    require_user()
    
    if flask_req.method == "GET":
        # List files
        params = {
            "category": flask_req.args.get("category"),
            "project_name": flask_req.args.get("project"),
            "limit": int(flask_req.args.get("limit", 50))
        }
        return jsonify(list_files(**params))

    elif flask_req.method == "POST":
        data = flask_req.get_json(silent=True) or {}
        action = data.get("action")

        if action == "save_code":
            return jsonify(save_code_file(**data))
        elif action == "save_text":
            return jsonify(save_text_file(**data))
        elif action == "save_research":
            return jsonify(save_research_findings(**data))
        elif action == "get_content":
            return jsonify(get_file_content(**data))
        else:
            return jsonify({"ok": False, "error": "Unknown action"})


joi_companion.register_route("/files", ["GET", "POST"], files_route, "files_route")
