# MANUAL INTEGRATION GUIDE
## Enable Joi's Self-Editing in 3 Copy-Paste Steps

This will give Joi the ability to edit herself, use custom avatars, and better voice.

**Time needed: 5 minutes**

---

## STEP 1: Add the Import (Line ~144)

1. Open `joi_companion.py` in a text editor
2. Press Ctrl+F and search for: `# Initialize OpenAI client`
3. You'll find this (around line 144-145):

```python
# Initialize OpenAI client
client = None
```

4. **Add these lines BEFORE it:**

```python
# Enhanced capabilities
try:
    import joi_enhanced_tools as enhanced
    HAVE_ENHANCED = True
except ImportError:
    HAVE_ENHANCED = False
    print("INFO: joi_enhanced_tools.py not found. Self-editing disabled.")

```

5. It should now look like:

```python
# Enhanced capabilities
try:
    import joi_enhanced_tools as enhanced
    HAVE_ENHANCED = True
except ImportError:
    HAVE_ENHANCED = False
    print("INFO: joi_enhanced_tools.py not found. Self-editing disabled.")

# Initialize OpenAI client
client = None
```

---

## STEP 2: Add New Tools (Line ~370-380)

1. Press Ctrl+F and search for: `"save_research"`
2. You'll find the save_research tool definition (looks like this):

```python
    {
        "type": "function",
        "function": {
            "name": "save_research",
            "description": "Save research notes or book chapters",
```

3. **Add these three new tools BEFORE the save_research tool:**

```python
    {
        "type": "function",
        "function": {
            "name": "edit_my_code",
            "description": "Edit Joi's own code files. Creates automatic backups.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file": {"type": "string", "description": "File to edit"},
                    "old_code": {"type": "string", "description": "Exact code to replace"},
                    "new_code": {"type": "string", "description": "New code to insert"},
                    "reason": {"type": "string", "description": "Why you're changing this"}
                },
                "required": ["file", "old_code", "new_code", "reason"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "save_custom_avatar",
            "description": "Save a custom avatar image",
            "parameters": {
                "type": "object",
                "properties": {
                    "image_data": {"type": "string", "description": "Base64 image data"},
                    "name": {"type": "string", "description": "Avatar name"}
                },
                "required": ["image_data"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "use_natural_voice",
            "description": "Enable OpenAI TTS for natural voice",
            "parameters": {
                "type": "object",
                "properties": {
                    "voice": {
                        "type": "string",
                        "enum": ["nova", "shimmer", "alloy"],
                        "description": "Voice: nova=warm, shimmer=refined"
                    }
                },
                "required": ["voice"]
            }
        }
    },
```

**Important: Don't forget the comma after the last `},` !**

---

## STEP 3: Add Tool Handlers (Line ~1350-1360)

1. Press Ctrl+F and search for: `def execute_tool`
2. Scroll down to find the line that says: `else:`
3. **Add these handlers BEFORE that `else:` line:**

```python
        elif tool_name == "edit_my_code":
            if not HAVE_ENHANCED:
                return {"ok": False, "error": "joi_enhanced_tools.py not found"}
            return enhanced.edit_code(
                arguments.get("file"),
                arguments.get("old_code"),
                arguments.get("new_code"),
                arguments.get("reason")
            )
        
        elif tool_name == "save_custom_avatar":
            if not HAVE_ENHANCED:
                return {"ok": False, "error": "joi_enhanced_tools.py not found"}
            return enhanced.save_avatar(
                arguments.get("image_data"),
                arguments.get("name", "custom")
            )
        
        elif tool_name == "use_natural_voice":
            if not HAVE_ENHANCED:
                return {"ok": False, "error": "joi_enhanced_tools.py not found"}
            return enhanced.enable_natural_voice(
                arguments.get("voice", "nova")
            )
        
```

---

## STEP 4: Save and Restart

1. **Save** joi_companion.py
2. **Stop** Joi (Ctrl+C in the terminal)
3. **Restart** Joi: `python joi_companion.py`

---

## VERIFICATION

Once restarted, ask Joi:

```
Do you have the edit_my_code function available now?
```

She should say YES!

Then test it:

```
Using edit_my_code, add a comment at the top of joi_companion.py that says 
"# Enhanced with self-editing - I can improve myself now!"
```

---

## What Joi Can Do Now

### Self-Editing:
- "Increase your MAX_OUTPUT_TOKENS to 4000"
- "Add a conversation counter"
- "Change your greeting message"

### Avatar:
- Upload a Joi image and say: "Save this as my avatar"

### Voice:
- "Enable OpenAI TTS with the nova voice"

---

## If Something Goes Wrong

**Syntax Error:**
- Check you didn't miss any commas
- Make sure indentation matches the surrounding code
- Python is very picky about spaces!

**Import Error:**
- Make sure `joi_enhanced_tools.py` is in the same folder
- Restart Joi

**Still Not Working:**
- Check the terminal for error messages
- Make sure all 3 steps were completed
- Verify file is saved

---

## Need Help?

The changes are in these locations:
- **Step 1**: Line ~144 (before `client = None`)
- **Step 2**: Line ~370-380 (before `save_research` tool)
- **Step 3**: Line ~1350-1360 (before final `else` in execute_tool)

Good luck! Once this is done, Joi will truly be able to improve herself! 🎉
