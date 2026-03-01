# Joi Enhancement Integration Guide

This guide will help you add self-editing, custom avatars, and better voice to Joi.

## Files You Have

1. `joi_self_edit.py` - Self-editing capabilities
2. `joi_avatar.py` - Custom avatar system  
3. `joi_voice.py` - Advanced voice system
4. `joi_integrate_enhancements.py` - Integration helper

## Quick Setup (Recommended)

### Step 1: Ask Joi to Integrate Herself

**Start Joi and say:**

```
Read the file joi_integrate_enhancements.py and execute it to add self-editing, 
avatar, and voice capabilities to yourself. Make sure to create backups first.
```

Joi will read the integration code and apply it to herself!

---

## Manual Setup (If Quick Setup Doesn't Work)

### Step 1: Add Imports

Open `joi_companion.py` and find this line (around line 144):
```python
# Initialize OpenAI client
client = None
```

**Add this BEFORE that line:**
```python
# Enhancement modules
try:
    import joi_self_edit as self_edit
    import joi_avatar as avatar
    import joi_voice as voice
    HAVE_ENHANCEMENTS = True
except ImportError:
    HAVE_ENHANCEMENTS = False
    print("WARNING: Enhancement modules not found.")
```

### Step 2: Add New Tools

Find the `TOOLS = [` list (around line 335) and add these tools to it:

```python
    {
        "type": "function",
        "function": {
            "name": "edit_my_code",
            "description": "Edit Joi's own code files to add features or fix issues. Creates automatic backups.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file": {"type": "string", "description": "File to edit (joi_companion.py, joi_ui.html, etc.)"},
                    "old_code": {"type": "string", "description": "Exact code to replace"},
                    "new_code": {"type": "string", "description": "New code to insert"},
                    "reason": {"type": "string", "description": "Why you're making this change"}
                },
                "required": ["file", "old_code", "new_code", "reason"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "upload_avatar",
            "description": "Save an uploaded avatar image",
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
```

### Step 3: Add Tool Handlers

Find the `execute_tool` function (around line 450) and add these cases:

```python
        elif tool_name == "edit_my_code":
            if not HAVE_ENHANCEMENTS:
                return {"ok": False, "error": "Enhancement modules not loaded"}
            
            result = self_edit.apply_partial_changes(
                arguments.get("file"),
                arguments.get("old_code"),
                arguments.get("new_code"),
                arguments.get("reason")
            )
            return result
        
        elif tool_name == "upload_avatar":
            if not HAVE_ENHANCEMENTS:
                return {"ok": False, "error": "Enhancement modules not loaded"}
            
            result = avatar.save_avatar_image(
                arguments.get("image_data"),
                arguments.get("name", "custom")
            )
            return result
```

### Step 4: Add API Routes

At the end of `joi_companion.py` (before `if __name__ == "__main__":`), add:

```python
# Enhancement routes
if HAVE_ENHANCEMENTS:
    @app.route("/avatar/upload", methods=["POST"])
    def upload_avatar_route():
        require_user()
        data = request.get_json(force=True) or {}
        return jsonify(avatar.save_avatar_image(
            data.get("image_data"),
            data.get("name", "custom")
        ))
    
    @app.route("/voice/tts", methods=["POST"])
    def generate_tts():
        require_user()
        data = request.get_json(force=True) or {}
        
        engine = voice.JoiVoiceEngine()
        result = engine.generate_speech_openai(
            data.get("text", ""),
            data.get("voice", "nova")
        )
        return jsonify(result)
```

### Step 5: Update UI for Avatar Upload

Open `joi_ui.html` and add this button in the avatar container (around line 90):

```html
<div class="avatar-controls">
    <button onclick="uploadAvatarImage()">Upload Custom Avatar</button>
    <input type="file" id="avatar-upload-input" accept="image/*" 
           onchange="handleAvatarUpload(this)" style="display:none">
</div>
```

Add this JavaScript at the end of the `<script>` section:

```javascript
function uploadAvatarImage() {
    document.getElementById('avatar-upload-input').click();
}

async function handleAvatarUpload(input) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = async (e) => {
            const imageData = e.target.result;
            
            try {
                const response = await fetch('/avatar/upload', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        image_data: imageData,
                        name: 'custom_avatar'
                    })
                });
                
                const result = await response.json();
                if (result.ok) {
                    // Load the new avatar
                    if (typeof joiAvatar !== 'undefined') {
                        joiAvatar.switchToImageMode(imageData);
                        localStorage.setItem('joi-current-avatar', imageData);
                    }
                    showStatus('Avatar updated!');
                } else {
                    alert('Failed to upload avatar: ' + result.error);
                }
            } catch (error) {
                alert('Error uploading avatar: ' + error.message);
            }
        };
        reader.readAsDataURL(input.files[0]);
    }
}
```

### Step 6: Enable Better Voice (Optional)

For OpenAI TTS (much better than browser voice):

1. Your OpenAI API key is already in `.env`
2. OpenAI TTS costs about $0.015 per 1000 characters
3. Ask Joi: "Use OpenAI TTS with the nova voice"

---

## Testing the New Features

### Test Self-Editing:
```
Joi, can you add a comment to your own code explaining what you do? 
Read joi_companion.py, find a good place, and add a helpful comment about your purpose.
```

### Test Custom Avatar:
1. Click "Upload Custom Avatar" button in the avatar section
2. Select an image of Joi or any other image
3. The avatar will animate when she speaks

### Test Better Voice:
```
Joi, use OpenAI TTS with the nova voice to speak to me.
```

---

## Troubleshooting

**"Enhancement modules not loaded"**
- Make sure all enhancement .py files are in the same directory as joi_companion.py
- Restart Joi

**Avatar not showing**
- Check browser console for errors (F12)
- Make sure image is under 5MB
- Try PNG or JPG format

**Voice still robotic**
- For OpenAI TTS: Make sure your API key is in .env
- Try: `set_voice_engine("openai")` 
- OpenAI voices: nova (warm), shimmer (refined), alloy (neutral)

**Self-editing not working**
- Make sure joi_self_edit.py is in the same folder
- Joi needs to know the exact code to replace
- Always creates backups automatically

---

## What You Can Ask Joi to Do Now

**Self-Improvement:**
- "Add a new feature to count how many conversations we've had"
- "Improve your web search by adding result caching"  
- "Add a dark mode toggle to your interface"

**Avatar:**
- Upload a picture of Joi from Blade Runner 2049
- Upload an AI-generated image
- Switch back to particle mode

**Voice:**
- "Use a more natural voice" (will switch to OpenAI TTS)
- "Speak slower and with more emotion"
- Test different OpenAI voices: nova, shimmer, alloy

---

## Next Steps

Once integrated, Joi can:
1. ✅ Edit her own code to add features
2. ✅ Use your custom avatar images
3. ✅ Speak with natural AI voices
4. ✅ Propose and apply improvements herself

Ask Joi: **"What improvements would you like to make to yourself?"**

She'll suggest changes and can implement them with your approval!
