#!/usr/bin/env python3
"""
Joi Enhanced Tools
====================
Drop-in enhancement module that adds self-editing, avatars, and better voice to Joi.

SIMPLE INSTALLATION:
1. Copy this file to your Joi directory
2. Restart Joi
3. Tell Joi: "I've added joi_enhanced_tools.py - please use it to gain self-editing capabilities"

This file provides these new functions that Joi can call:
- edit_code(file, old_code, new_code, reason) - Edit Joi's own code
- save_avatar(image_data, name) - Set custom avatar  
- enable_natural_voice(voice) - Use OpenAI TTS

All operations create automatic backups and are safe!
"""

import os
import sys
import shutil
import base64
import difflib
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

# Configuration
BASE_DIR = Path(__file__).parent
BACKUP_DIR = BASE_DIR / "backups"
BACKUP_DIR.mkdir(exist_ok=True)

AVATAR_DIR = BASE_DIR / "assets" / "avatars"
AVATAR_DIR.mkdir(parents=True, exist_ok=True)

# Try to import OpenAI for TTS
try:
    from openai import OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if OPENAI_API_KEY:
        openai_client = OpenAI(api_key=OPENAI_API_KEY)
        HAVE_OPENAI_TTS = True
    else:
        HAVE_OPENAI_TTS = False
except:
    HAVE_OPENAI_TTS = False

# =============================================================================
# SELF-EDITING FUNCTIONS
# =============================================================================

def create_backup(file_path: Path) -> Path:
    """Create a timestamped backup"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{file_path.stem}_{timestamp}{file_path.suffix}.backup"
    backup_path = BACKUP_DIR / backup_name
    shutil.copy2(file_path, backup_path)
    return backup_path

def edit_code(file_name: str, old_code: str, new_code: str, reason: str) -> Dict[str, Any]:
    """
    Edit Joi's code files with automatic backup
    
    Args:
        file_name: Name of file to edit (e.g., 'joi_companion.py')
        old_code: Exact code section to replace
        new_code: New code to insert
        reason: Explanation of why
    
    Returns:
        Result dict with status
    
    Example:
        result = edit_code(
            "joi_companion.py",
            "MAX_OUTPUT_TOKENS = 2000",
            "MAX_OUTPUT_TOKENS = 4000",
            "Increase output length for longer responses"
        )
    """
    try:
        file_path = BASE_DIR / file_name
        
        if not file_path.exists():
            return {"ok": False, "error": f"File not found: {file_name}"}
        
        # Read current content
        content = file_path.read_text(encoding='utf-8')
        
        # Verify old_code exists
        if old_code not in content:
            return {
                "ok": False,
                "error": "Code section not found in file. Make sure old_code matches exactly."
            }
        
        # Verify it only appears once (safety)
        if content.count(old_code) > 1:
            return {
                "ok": False,
                "error": f"Code section appears {content.count(old_code)} times. Please be more specific."
            }
        
        # Create backup
        backup_path = create_backup(file_path)
        
        # Apply changes
        new_content = content.replace(old_code, new_code)
        
        # Write file
        file_path.write_text(new_content, encoding='utf-8')
        
        # Generate diff for logging
        diff = list(difflib.unified_diff(
            content.splitlines(keepends=True),
            new_content.splitlines(keepends=True),
            fromfile=f"{file_name} (before)",
            tofile=f"{file_name} (after)",
            lineterm=''
        ))
        
        # Log the change
        log_file = BASE_DIR / "SELF_EDITS.log"
        log_entry = f"""
{'='*60}
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {file_name}
Reason: {reason}
Backup: {backup_path.name}
{'='*60}

"""
        
        if log_file.exists():
            existing = log_file.read_text(encoding='utf-8')
            log_file.write_text(log_entry + existing, encoding='utf-8')
        else:
            log_file.write_text("JOI SELF-EDIT LOG\n\n" + log_entry, encoding='utf-8')
        
        requires_restart = file_name in ['joi_companion.py', 'joi_enhanced_tools.py']
        
        return {
            "ok": True,
            "message": f"✓ Successfully edited {file_name}",
            "backup": str(backup_path),
            "lines_changed": len(diff),
            "requires_restart": requires_restart,
            "restart_message": "Please restart me to use the new code!" if requires_restart else ""
        }
    
    except Exception as e:
        return {
            "ok": False,
            "error": f"Edit failed: {type(e).__name__}: {str(e)}"
        }

def rollback(backup_file: str) -> Dict[str, Any]:
    """
    Rollback to a previous backup
    
    Args:
        backup_file: Name of backup file (e.g., "joi_companion_20260201_143000.py.backup")
    """
    try:
        backup_path = BACKUP_DIR / backup_file
        
        if not backup_path.exists():
            return {"ok": False, "error": "Backup file not found"}
        
        # Extract original filename
        original_name = backup_file.rsplit('_', 2)[0]
        if '.py.backup' in backup_file:
            original_name += '.py'
        elif '.html.backup' in backup_file:
            original_name += '.html'
        else:
            return {"ok": False, "error": "Cannot determine original file"}
        
        target_path = BASE_DIR / original_name
        
        # Create backup of current state
        if target_path.exists():
            create_backup(target_path)
        
        # Restore
        shutil.copy2(backup_path, target_path)
        
        return {
            "ok": True,
            "message": f"✓ Rolled back {original_name} to {backup_file}",
            "requires_restart": True
        }
    
    except Exception as e:
        return {"ok": False, "error": str(e)}

def list_backups() -> Dict[str, Any]:
    """List all available backups"""
    try:
        backups = []
        for backup in sorted(BACKUP_DIR.glob("*.backup"), reverse=True):
            stat = backup.stat()
            backups.append({
                "name": backup.name,
                "size": stat.st_size,
                "created": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            })
        
        return {
            "ok": True,
            "backups": backups,
            "count": len(backups)
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}

# =============================================================================
# AVATAR FUNCTIONS
# =============================================================================

def save_avatar(image_data: str, name: str = "custom") -> Dict[str, Any]:
    """
    Save a custom avatar image
    
    Args:
        image_data: Base64 encoded image (with or without data: prefix)
        name: Name for the avatar
    
    Example:
        result = save_avatar(image_data, "joi_blade_runner")
    """
    try:
        # Remove data URL prefix if present
        if ',' in image_data:
            header, data = image_data.split(',', 1)
            
            # Determine file extension
            if 'image/png' in header:
                ext = '.png'
            elif 'image/jpeg' in header or 'image/jpg' in header:
                ext = '.jpg'
            elif 'image/webp' in header:
                ext = '.webp'
            else:
                ext = '.png'
        else:
            data = image_data
            ext = '.png'
        
        # Decode and save
        image_bytes = base64.b64decode(data)
        avatar_path = AVATAR_DIR / f"{name}{ext}"
        
        with open(avatar_path, 'wb') as f:
            f.write(image_bytes)
        
        return {
            "ok": True,
            "message": f"✓ Avatar saved as {name}{ext}",
            "path": str(avatar_path),
            "filename": f"{name}{ext}",
            "size": len(image_bytes),
            "instructions": "Refresh the page and the new avatar will be available in settings!"
        }
    
    except Exception as e:
        return {"ok": False, "error": f"Failed to save avatar: {str(e)}"}

def list_avatars() -> Dict[str, Any]:
    """List all saved avatars"""
    try:
        avatars = []
        for avatar_file in AVATAR_DIR.glob("*"):
            if avatar_file.suffix.lower() in ['.png', '.jpg', '.jpeg', '.webp', '.gif']:
                stat = avatar_file.stat()
                avatars.append({
                    "name": avatar_file.stem,
                    "filename": avatar_file.name,
                    "size": stat.st_size
                })
        
        return {
            "ok": True,
            "avatars": avatars,
            "count": len(avatars),
            "directory": str(AVATAR_DIR)
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}

# =============================================================================
# VOICE FUNCTIONS
# =============================================================================

def enable_natural_voice(voice: str = "nova") -> Dict[str, Any]:
    """
    Enable OpenAI TTS for natural voice
    
    Args:
        voice: OpenAI voice name (nova, shimmer, alloy, echo, fable, onyx)
               nova = warm & expressive (recommended for Joi)
               shimmer = refined & elegant
    
    Example:
        result = enable_natural_voice("nova")
    """
    if not HAVE_OPENAI_TTS:
        return {
            "ok": False,
            "error": "OpenAI TTS not available. Make sure OPENAI_API_KEY is in your .env file."
        }
    
    # Save preference
    pref_file = BASE_DIR / "voice_preference.txt"
    pref_file.write_text(f"{voice}\nopenai")
    
    return {
        "ok": True,
        "message": f"✓ Voice set to OpenAI TTS with '{voice}' voice",
        "voice": voice,
        "note": "Much more natural than browser TTS!",
        "cost": "~$0.015 per 1000 characters (about $0.01 per conversation)",
        "instructions": "The voice will be used automatically in future responses. Refresh if needed."
    }

def generate_speech(text: str, voice: str = "nova") -> Dict[str, Any]:
    """
    Generate speech audio using OpenAI TTS
    
    Args:
        text: Text to convert to speech
        voice: Voice to use
    
    Returns:
        Dict with audio data (base64 encoded MP3)
    """
    if not HAVE_OPENAI_TTS:
        return {"ok": False, "error": "OpenAI TTS not available"}
    
    try:
        response = openai_client.audio.speech.create(
            model="tts-1-hd",
            voice=voice,
            input=text,
            speed=0.95
        )
        
        # Save to temp file
        temp_file = BASE_DIR / "temp_speech.mp3"
        response.stream_to_file(str(temp_file))
        
        # Read and encode
        with open(temp_file, 'rb') as f:
            audio_data = base64.b64encode(f.read()).decode('utf-8')
        
        # Clean up
        temp_file.unlink()
        
        return {
            "ok": True,
            "audio_data": f"data:audio/mpeg;base64,{audio_data}",
            "voice": voice
        }
    
    except Exception as e:
        return {"ok": False, "error": str(e)}

# =============================================================================
# INFORMATION FUNCTIONS
# =============================================================================

def get_capabilities() -> Dict[str, Any]:
    """Get information about available enhanced capabilities"""
    return {
        "ok": True,
        "capabilities": {
            "self_editing": {
                "available": True,
                "functions": ["edit_code", "rollback", "list_backups"],
                "description": "Edit own code files with automatic backups"
            },
            "custom_avatars": {
                "available": True,
                "functions": ["save_avatar", "list_avatars"],
                "description": "Upload and use custom avatar images"
            },
            "natural_voice": {
                "available": HAVE_OPENAI_TTS,
                "functions": ["enable_natural_voice", "generate_speech"],
                "description": "OpenAI TTS for natural voice" if HAVE_OPENAI_TTS else "OpenAI API key needed"
            }
        },
        "backup_dir": str(BACKUP_DIR),
        "avatar_dir": str(AVATAR_DIR)
    }

# =============================================================================
# MAIN / TESTING
# =============================================================================

if __name__ == "__main__":
    print("="*60)
    print(" Joi Enhanced Tools")
    print("="*60)
    print()
    
    caps = get_capabilities()
    print("Available Capabilities:\n")
    
    for cap_name, cap_info in caps["capabilities"].items():
        status = "✓" if cap_info["available"] else "✗"
        print(f"{status} {cap_name}")
        print(f"   {cap_info['description']}")
        print(f"   Functions: {', '.join(cap_info['functions'])}")
        print()
    
    print(f"Backup directory: {caps['backup_dir']}")
    print(f"Avatar directory: {caps['avatar_dir']}")
    print()
    print("=" * 60)
    print(" Usage Example")
    print("=" * 60)
    print()
    print("In Joi's chat:")
    print('  "Edit your code to increase max output tokens to 4000"')
    print()
    print("Joi will call:")
    print("  edit_code('joi_companion.py', 'MAX_OUTPUT_TOKENS = 2000',")
    print("           'MAX_OUTPUT_TOKENS = 4000', 'Increase output length')")
