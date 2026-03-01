#!/usr/bin/env python3
"""
Joi Self-Editing Module
Allows Joi to modify her own code with proper safety mechanisms
"""

import os
import sys
import shutil
import difflib
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

# Add parent directory to path to import from joi_companion
sys.path.insert(0, str(Path(__file__).parent))

BACKUP_DIR = Path(__file__).parent / "backups"
BACKUP_DIR.mkdir(exist_ok=True)

def create_timestamped_backup(file_path: Path) -> Path:
    """Create a timestamped backup of a file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{file_path.stem}_{timestamp}{file_path.suffix}.backup"
    backup_path = BACKUP_DIR / backup_name
    
    shutil.copy2(file_path, backup_path)
    print(f"✓ Backup created: {backup_path}")
    return backup_path

def apply_code_changes(target_file: str, new_content: str, reason: str = "Self-improvement") -> Dict[str, Any]:
    """
    Apply code changes to a file with automatic backup
    
    Args:
        target_file: Name of file to modify (e.g., 'joi_companion.py')
        new_content: Complete new content for the file
        reason: Reason for the change
    
    Returns:
        Dict with status and details
    """
    try:
        # Resolve file path
        file_path = Path(__file__).parent / target_file
        
        if not file_path.exists():
            return {
                "ok": False,
                "error": f"File not found: {target_file}"
            }
        
        # Read current content
        old_content = file_path.read_text(encoding='utf-8')
        
        # Create backup
        backup_path = create_timestamped_backup(file_path)
        
        # Generate diff for logging
        diff = list(difflib.unified_diff(
            old_content.splitlines(keepends=True),
            new_content.splitlines(keepends=True),
            fromfile=f"{target_file} (before)",
            tofile=f"{target_file} (after)",
            lineterm=''
        ))
        
        # Write new content
        file_path.write_text(new_content, encoding='utf-8')
        
        # Log the change
        log_change(target_file, reason, backup_path, diff)
        
        return {
            "ok": True,
            "message": f"Successfully updated {target_file}",
            "backup": str(backup_path),
            "diff_lines": len(diff),
            "requires_restart": target_file in ['joi_companion.py', 'joi_ui.html']
        }
    
    except Exception as e:
        return {
            "ok": False,
            "error": f"Failed to apply changes: {str(e)}"
        }

def apply_partial_changes(target_file: str, old_code: str, new_code: str, reason: str = "Partial update") -> Dict[str, Any]:
    """
    Apply partial code changes by replacing specific sections
    
    Args:
        target_file: Name of file to modify
        old_code: Code section to replace
        new_code: New code to insert
        reason: Reason for the change
    
    Returns:
        Dict with status and details
    """
    try:
        file_path = Path(__file__).parent / target_file
        
        if not file_path.exists():
            return {
                "ok": False,
                "error": f"File not found: {target_file}"
            }
        
        # Read current content
        content = file_path.read_text(encoding='utf-8')
        
        # Check if old_code exists
        if old_code not in content:
            return {
                "ok": False,
                "error": "Old code section not found in file. Cannot apply partial changes safely."
            }
        
        # Check if it appears only once
        if content.count(old_code) > 1:
            return {
                "ok": False,
                "error": "Old code section appears multiple times. Please use full file replacement for safety."
            }
        
        # Create backup
        backup_path = create_timestamped_backup(file_path)
        
        # Replace the code
        new_content = content.replace(old_code, new_code)
        
        # Write new content
        file_path.write_text(new_content, encoding='utf-8')
        
        # Log the change
        diff = list(difflib.unified_diff(
            content.splitlines(keepends=True),
            new_content.splitlines(keepends=True),
            lineterm=''
        ))
        log_change(target_file, reason, backup_path, diff)
        
        return {
            "ok": True,
            "message": f"Successfully updated {target_file}",
            "backup": str(backup_path),
            "requires_restart": target_file in ['joi_companion.py']
        }
    
    except Exception as e:
        return {
            "ok": False,
            "error": f"Failed to apply partial changes: {str(e)}"
        }

def add_new_function(target_file: str, function_code: str, insert_after: str = None) -> Dict[str, Any]:
    """
    Add a new function to a Python file
    
    Args:
        target_file: Name of file to modify
        function_code: Complete function code to add
        insert_after: String to find where to insert (optional)
    
    Returns:
        Dict with status and details
    """
    try:
        file_path = Path(__file__).parent / target_file
        
        if not file_path.exists():
            return {
                "ok": False,
                "error": f"File not found: {target_file}"
            }
        
        content = file_path.read_text(encoding='utf-8')
        
        # Create backup
        backup_path = create_timestamped_backup(file_path)
        
        if insert_after:
            if insert_after not in content:
                return {
                    "ok": False,
                    "error": f"Insert point '{insert_after}' not found in file"
                }
            
            # Insert after the specified string
            parts = content.split(insert_after, 1)
            new_content = parts[0] + insert_after + "\n\n" + function_code + "\n" + parts[1]
        else:
            # Append at the end
            new_content = content + "\n\n" + function_code + "\n"
        
        # Write new content
        file_path.write_text(new_content, encoding='utf-8')
        
        return {
            "ok": True,
            "message": f"Successfully added new function to {target_file}",
            "backup": str(backup_path),
            "requires_restart": True
        }
    
    except Exception as e:
        return {
            "ok": False,
            "error": f"Failed to add function: {str(e)}"
        }

def log_change(file_name: str, reason: str, backup_path: Path, diff: list):
    """Log code changes to a changelog file"""
    changelog_path = Path(__file__).parent / "CHANGELOG.md"
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_entry = f"""
## {timestamp} - {file_name}

**Reason:** {reason}

**Backup:** {backup_path.name}

**Changes:** {len(diff)} lines modified

---

"""
    
    # Append to changelog
    if changelog_path.exists():
        existing = changelog_path.read_text(encoding='utf-8')
        changelog_path.write_text(log_entry + existing, encoding='utf-8')
    else:
        header = "# Joi Self-Modification Changelog\n\nAll code changes made by Joi are logged here.\n\n---\n"
        changelog_path.write_text(header + log_entry, encoding='utf-8')

def rollback_to_backup(backup_file: str) -> Dict[str, Any]:
    """
    Rollback to a previous backup
    
    Args:
        backup_file: Name of backup file in backups directory
    
    Returns:
        Dict with status
    """
    try:
        backup_path = BACKUP_DIR / backup_file
        
        if not backup_path.exists():
            return {
                "ok": False,
                "error": f"Backup file not found: {backup_file}"
            }
        
        # Extract original filename from backup
        # Format: filename_YYYYMMDD_HHMMSS.ext.backup
        original_name = backup_file.rsplit('_', 2)[0]
        
        # Find extension in backup name
        if '.py.backup' in backup_file:
            original_name += '.py'
        elif '.html.backup' in backup_file:
            original_name += '.html'
        else:
            return {
                "ok": False,
                "error": "Cannot determine original file type from backup"
            }
        
        target_path = Path(__file__).parent / original_name
        
        # Create a backup of current state before rollback
        if target_path.exists():
            create_timestamped_backup(target_path)
        
        # Restore from backup
        shutil.copy2(backup_path, target_path)
        
        return {
            "ok": True,
            "message": f"Successfully rolled back {original_name} to {backup_file}",
            "requires_restart": True
        }
    
    except Exception as e:
        return {
            "ok": False,
            "error": f"Rollback failed: {str(e)}"
        }

def list_backups() -> Dict[str, Any]:
    """List all available backups"""
    try:
        backups = []
        for backup_file in sorted(BACKUP_DIR.glob("*.backup"), reverse=True):
            stat = backup_file.stat()
            backups.append({
                "name": backup_file.name,
                "size": stat.st_size,
                "created": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            })
        
        return {
            "ok": True,
            "backups": backups,
            "count": len(backups)
        }
    
    except Exception as e:
        return {
            "ok": False,
            "error": str(e)
        }

def validate_python_code(code: str) -> Dict[str, Any]:
    """
    Validate Python code syntax
    
    Args:
        code: Python code to validate
    
    Returns:
        Dict with validation result
    """
    import ast
    
    try:
        ast.parse(code)
        return {
            "ok": True,
            "valid": True,
            "message": "Code syntax is valid"
        }
    except SyntaxError as e:
        return {
            "ok": True,
            "valid": False,
            "error": f"Syntax error at line {e.lineno}: {e.msg}",
            "line": e.lineno
        }
    except Exception as e:
        return {
            "ok": False,
            "error": f"Validation error: {str(e)}"
        }

# Test function
if __name__ == "__main__":
    print("Joi Self-Editing Module")
    print("=======================\n")
    
    print("Available functions:")
    print("- apply_code_changes(target_file, new_content, reason)")
    print("- apply_partial_changes(target_file, old_code, new_code, reason)")
    print("- add_new_function(target_file, function_code, insert_after)")
    print("- rollback_to_backup(backup_file)")
    print("- list_backups()")
    print("- validate_python_code(code)")
    
    print("\nBackup directory:", BACKUP_DIR)
    
    backups = list_backups()
    if backups["ok"] and backups["count"] > 0:
        print(f"\nExisting backups: {backups['count']}")
        for b in backups["backups"][:5]:
            print(f"  - {b['name']} ({b['created']})")
    else:
        print("\nNo backups yet.")
