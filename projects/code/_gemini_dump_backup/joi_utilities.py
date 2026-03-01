#!/usr/bin/env python3
"""
Joi Utilities - Helper functions for self-improvement and maintenance
"""

import subprocess
import sys
from pathlib import Path
from typing import List, Dict, Any

def install_package(package_name: str) -> Dict[str, Any]:
    """Install a Python package using pip"""
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", package_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return {
            "ok": True,
            "message": f"Successfully installed {package_name}"
        }
    except subprocess.CalledProcessError as e:
        return {
            "ok": False,
            "error": f"Failed to install {package_name}: {str(e)}"
        }

def check_package(package_name: str) -> bool:
    """Check if a Python package is installed"""
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False

def list_installed_packages() -> List[str]:
    """List all installed Python packages"""
    try:
        result = subprocess.check_output(
            [sys.executable, "-m", "pip", "list"],
            text=True
        )
        # Parse the output (skip header)
        lines = result.strip().split('\n')[2:]
        packages = [line.split()[0] for line in lines if line]
        return packages
    except Exception as e:
        return []

def suggest_improvements() -> List[Dict[str, str]]:
    """Suggest potential improvements to Joi"""
    suggestions = []
    
    # Check for optional dependencies
    optional_deps = {
        "selenium": "Enable advanced web scraping with JavaScript support",
        "pypdf": "Enable PDF reading and text extraction",
        "PiL": "Enable advanced image processing",
        "bs4": "Improve web content parsing"
    }
    
    for package, benefit in optional_deps.items():
        if not check_package(package):
            suggestions.append({
                "type": "dependency",
                "package": package,
                "description": benefit,
                "command": f"pip install {package}"
            })
    
    # Feature suggestions
    feature_suggestions = [
        {
            "type": "feature",
            "title": "Add database backup/restore",
            "description": "Implement automatic database backups and restoration",
            "difficulty": "medium"
        },
        {
            "type": "feature",
            "title": "Add export chat history",
            "description": "Allow exporting conversations to text/PDF/JSON",
            "difficulty": "easy"
        },
        {
            "type": "feature",
            "title": "Add scheduled tasks",
            "description": "Enable Joi to perform tasks on a schedule",
            "difficulty": "hard"
        },
        {
            "type": "feature",
            "title": "Add cloud sync",
            "description": "Sync memory and preferences to cloud storage",
            "difficulty": "hard"
        },
        {
            "type": "feature",
            "title": "Add more avatar animations",
            "description": "Create more sophisticated visual representations",
            "difficulty": "medium"
        }
    ]
    
    suggestions.extend(feature_suggestions)
    
    return suggestions

def create_backup(source_file: Path, backup_dir: Path) -> Path:
    """Create a backup of a file"""
    import shutil
    from datetime import datetime
    
    backup_dir.mkdir(exist_ok=True, parents=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{source_file.stem}_{timestamp}{source_file.suffix}"
    backup_path = backup_dir / backup_name
    
    shutil.copy2(source_file, backup_path)
    return backup_path

def analyze_code_quality(file_path: Path) -> Dict[str, Any]:
    """Basic code quality analysis"""
    content = file_path.read_text(encoding='utf-8')
    lines = content.split('\n')
    
    stats = {
        "total_lines": len(lines),
        "code_lines": len([l for l in lines if l.strip() and not l.strip().startswith('#')]),
        "comment_lines": len([l for l in lines if l.strip().startswith('#')]),
        "blank_lines": len([l for l in lines if not l.strip()]),
        "avg_line_length": sum(len(l) for l in lines) / len(lines) if lines else 0,
        "long_lines": len([l for l in lines if len(l) > 100])
    }
    
    issues = []
    if stats["long_lines"] > 10:
        issues.append("Many lines exceed 100 characters (PEP 8 recommends 79)")
    
    comment_ratio = stats["comment_lines"] / stats["code_lines"] if stats["code_lines"] > 0 else 0
    if comment_ratio < 0.1:
        issues.append("Low comment ratio - consider adding more documentation")
    
    return {
        "stats": stats,
        "issues": issues
    }

if __name__ == "__main__":
    print("Joi Utilities")
    print("=============\n")
    
    print("Checking dependencies...")
    for package in ["flask", "openai", "requests", "beautifulsoup4", "selenium", "pypdf"]:
        status = "✓" if check_package(package) else "✗"
        print(f"{status} {package}")
    
    print("\nSuggestions for improvement:")
    for i, suggestion in enumerate(suggest_improvements(), 1):
        if suggestion["type"] == "dependency":
            print(f"\n{i}. Install {suggestion['package']}")
            print(f"   {suggestion['description']}")
            print(f"   Command: {suggestion['command']}")
        else:
            print(f"\n{i}. {suggestion['title']} ({suggestion['difficulty']})")
            print(f"   {suggestion['description']}")
