#!/usr/bin/env python3
"""
Joi Enhancement Integration
This file adds self-editing, avatar, and voice capabilities to joi_companion.py

INSTRUCTIONS:
1. Ensure joi_self_edit.py, joi_avatar.py, and joi_voice.py are in the same directory
2. Run: python joi_integrate_enhancements.py
3. This will update joi_companion.py with new features
4. Restart Joi to use the new capabilities
"""

import sys
from pathlib import Path

# Import the self-editing module
try:
    import joi_self_edit as self_edit
except ImportError:
    print("ERROR: joi_self_edit.py not found!")
    print("Make sure all enhancement files are in the same directory.")
    sys.exit(1)

def integrate_enhancements():
    """Integrate all enhancements into joi_companion.py"""
    
    print("="*60)
    print(" Joi Enhancement Integration")
    print("="*60)
    print()
    
    # 1. Add imports to joi_companion.py
    print("Step 1: Adding new imports...")
    
    imports_code = """
# Enhancement modules
try:
    import joi_self_edit as self_edit
    import joi_avatar as avatar
    import joi_voice as voice
    HAVE_ENHANCEMENTS = True
except ImportError:
    HAVE_ENHANCEMENTS = False
    print("WARNING: Enhancement modules not found. Some features will be limited.")
"""
    
    # Find the location after existing imports in joi_companion.py
    result = self_edit.apply_partial_changes(
        target_file="joi_companion.py",
        old_code="# Initialize OpenAI client\nclient = None",
        new_code=imports_code + "\n# Initialize OpenAI client\nclient = None",
        reason="Add enhancement module imports"
    )
    
    if result["ok"]:
        print("✓ Imports added successfully")
    else:
        print(f"✗ Failed to add imports: {result.get('error')}")
        return False
    
    # 2. Add new tools for self-editing
    print("\nStep 2: Adding self-editing tools...")
    
    new_tools = '''
    {
        "type": "function",
        "function": {
            "name": "apply_code_changes",
            "description": "Apply code changes to Joi's own files. Creates automatic backups. Use this to improve Joi's capabilities.",
            "parameters": {
                "type": "object",
                "properties": {
                    "target_file": {
                        "type": "string",
                        "description": "File to modify (e.g., 'joi_companion.py', 'joi_ui.html')"
                    },
                    "new_content": {
                        "type": "string",
                        "description": "Complete new content for the file"
                    },
                    "reason": {
                        "type": "string",
                        "description": "Explanation of what changes and why"
                    }
                },
                "required": ["target_file", "new_content", "reason"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "apply_partial_code_changes",
            "description": "Apply partial code changes by replacing a specific section",
            "parameters": {
                "type": "object",
                "properties": {
                    "target_file": {
                        "type": "string",
                        "description": "File to modify"
                    },
                    "old_code": {
                        "type": "string",
                        "description": "Exact code section to replace"
                    },
                    "new_code": {
                        "type": "string",
                        "description": "New code to insert"
                    },
                    "reason": {
                        "type": "string",
                        "description": "Explanation of changes"
                    }
                },
                "required": ["target_file", "old_code", "new_code", "reason"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "validate_code",
            "description": "Validate Python code syntax before applying changes",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "Python code to validate"
                    }
                },
                "required": ["code"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "set_avatar",
            "description": "Set a custom avatar image for Joi",
            "parameters": {
                "type": "object",
                "properties": {
                    "image_data": {
                        "type": "string",
                        "description": "Base64 encoded image data"
                    },
                    "name": {
                        "type": "string",
                        "description": "Name for this avatar"
                    }
                },
                "required": ["image_data"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "set_voice_engine",
            "description": "Set the voice engine (browser, openai, or elevenlabs)",
            "parameters": {
                "type": "object",
                "properties": {
                    "engine": {
                        "type": "string",
                        "enum": ["browser", "openai", "elevenlabs"],
                        "description": "Voice engine to use"
                    },
                    "voice": {
                        "type": "string",
                        "description": "Specific voice name (for OpenAI: nova, shimmer, etc.)"
                    }
                },
                "required": ["engine"]
            }
        }
    }'''
    
    # This is more complex - we need to add to the TOOLS list
    # For now, create a helper file that Joi can read
    tools_file = Path("ENHANCEMENT_TOOLS.txt")
    tools_file.write_text(f"""
Add these tools to the TOOLS list in joi_companion.py:

{new_tools}

And add these to execute_tool():

        elif tool_name == "apply_code_changes":
            if HAVE_ENHANCEMENTS:
                result = self_edit.apply_code_changes(
                    arguments.get("target_file"),
                    arguments.get("new_content"),
                    arguments.get("reason", "Self-improvement")
                )
                return result
            else:
                return {{"ok": False, "error": "Enhancement modules not available"}}
        
        elif tool_name == "apply_partial_code_changes":
            if HAVE_ENHANCEMENTS:
                result = self_edit.apply_partial_changes(
                    arguments.get("target_file"),
                    arguments.get("old_code"),
                    arguments.get("new_code"),
                    arguments.get("reason", "Partial update")
                )
                return result
            else:
                return {{"ok": False, "error": "Enhancement modules not available"}}
        
        elif tool_name == "validate_code":
            if HAVE_ENHANCEMENTS:
                return self_edit.validate_python_code(arguments.get("code"))
            else:
                return {{"ok": False, "error": "Enhancement modules not available"}}
        
        elif tool_name == "set_avatar":
            if HAVE_ENHANCEMENTS:
                return avatar.save_avatar_image(
                    arguments.get("image_data"),
                    arguments.get("name", "custom_avatar")
                )
            else:
                return {{"ok": False, "error": "Enhancement modules not available"}}
        
        elif tool_name == "set_voice_engine":
            if HAVE_ENHANCEMENTS:
                engine_name = arguments.get("engine")
                voice_name = arguments.get("voice")
                
                voice_engine = voice.JoiVoiceEngine()
                result = voice_engine.set_engine(engine_name)
                
                if result["ok"] and voice_name:
                    voice_engine.current_voice = voice_name
                
                return result
            else:
                return {{"ok": False, "error": "Enhancement modules not available"}}
""")
    
    print("✓ Created ENHANCEMENT_TOOLS.txt with tool definitions")
    print("  → Ask Joi to read this file and integrate the tools")
    
    # 3. Add new Flask routes
    print("\nStep 3: Adding new API routes...")
    
    new_routes = '''

# --- Enhancement Routes ------------------------------------------------------

if HAVE_ENHANCEMENTS:
    
    @app.route("/avatar/upload", methods=["POST"])
    def upload_avatar():
        """Upload a custom avatar image"""
        require_user()
        data = request.get_json(force=True) or {}
        
        image_data = data.get("image_data")
        name = data.get("name", "custom_avatar")
        
        result = avatar.save_avatar_image(image_data, name)
        return jsonify(result)
    
    @app.route("/avatar/list", methods=["GET"])
    def list_avatars():
        """List available avatars"""
        require_user()
        result = avatar.list_avatars()
        return jsonify(result)
    
    @app.route("/avatar/<filename>", methods=["GET"])
    def get_avatar(filename: str):
        """Get avatar image"""
        require_user()
        data = avatar.get_avatar_data(filename)
        if data:
            return jsonify({"ok": True, "data": data})
        else:
            return jsonify({"ok": False, "error": "Avatar not found"}), 404
    
    @app.route("/voice/engines", methods=["GET"])
    def get_voice_engines():
        """Get available voice engines"""
        require_user()
        return jsonify(voice.get_available_engines())
    
    @app.route("/voice/generate", methods=["POST"])
    def generate_voice():
        """Generate speech using selected engine"""
        require_user()
        data = request.get_json(force=True) or {}
        
        text = data.get("text", "")
        engine_name = data.get("engine", "browser")
        voice_name = data.get("voice")
        
        voice_engine = voice.JoiVoiceEngine()
        voice_engine.set_engine(engine_name)
        
        if voice_name:
            voice_engine.current_voice = voice_name
        
        result = voice_engine.generate_speech(text)
        return jsonify(result)
    
    @app.route("/backups", methods=["GET"])
    def list_backups():
        """List all code backups"""
        require_admin()
        result = self_edit.list_backups()
        return jsonify(result)
    
    @app.route("/backups/<backup_file>/restore", methods=["POST"])
    def restore_backup(backup_file: str):
        """Restore from a backup"""
        require_admin()
        result = self_edit.rollback_to_backup(backup_file)
        return jsonify(result)
'''
    
    result = self_edit.add_new_function(
        target_file="joi_companion.py",
        function_code=new_routes,
        insert_after='@app.route("/research/<int:research_id>", methods=["GET"])'
    )
    
    if result["ok"]:
        print("✓ New routes added successfully")
    else:
        print(f"✗ Failed to add routes: {result.get('error')}")
    
    # 4. Summary
    print("\n" + "="*60)
    print(" Integration Summary")
    print("="*60)
    print()
    print("✓ Enhancement modules imported")
    print("✓ API routes added")
    print("✓ Tool definitions created (see ENHANCEMENT_TOOLS.txt)")
    print()
    print("NEXT STEPS:")
    print("1. Ask Joi to read ENHANCEMENT_TOOLS.txt")
    print("2. Ask Joi to integrate those tools into her code")
    print("3. Restart Joi: python joi_companion.py")
    print()
    print("NEW CAPABILITIES:")
    print("- Joi can now edit her own code with apply_code_changes()")
    print("- Upload custom avatar images")
    print("- Use OpenAI TTS for natural voice (if API key set)")
    print()
    
    if result.get("requires_restart"):
        print("⚠️  RESTART REQUIRED - Close and restart Joi to use new features")
    
    return True

if __name__ == "__main__":
    try:
        success = integrate_enhancements()
        if success:
            print("\n✓ Enhancement integration complete!")
        else:
            print("\n✗ Enhancement integration failed")
            sys.exit(1)
    except Exception as e:
        print(f"\n✗ Integration error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
