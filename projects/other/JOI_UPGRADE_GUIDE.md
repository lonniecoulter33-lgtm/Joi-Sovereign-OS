# 🎙️ JOI Voice & Avatar Upgrade Guide

## What's New

Your Joi now has:
1. ✅ **FREE Unlimited Natural Voices** (Edge TTS - Microsoft's best voices)
2. ✅ **Lip-Sync Animation** (Avatar's mouth moves when she talks)
3. ✅ **Multiple Voice Options** (7 different female voices)
4. ✅ **SadTalker Support** (Make photos talk - optional)

---

## 🚀 Quick Setup (Required)

### Step 1: Install Edge TTS
```bash
pip install edge-tts
```

That's it for basic functionality! Edge TTS is completely FREE and unlimited.

---

## 🎤 Available Voices

Joi can now use these FREE voices (no API credits needed):

| Voice Name | Description | Command |
|------------|-------------|---------|
| **aria** | Warm, friendly (DEFAULT) | "Joi, use the aria voice" |
| **jenny** | Professional, clear | "Joi, use the jenny voice" |
| **michelle** | Conversational, natural | "Joi, use the michelle voice" |
| **sonia** | British, elegant | "Joi, use the sonia voice" |
| **sara** | Young, energetic | "Joi, use the sara voice" |
| **jane** | Confident, professional | "Joi, use the jane voice" |
| **nancy** | Mature, warm | "Joi, use the nancy voice" |

### Using OpenAI Voices (PAID - uses API credits)
```
"Joi, use the nova voice with openai engine"
"Joi, use the shimmer voice with openai engine"
```

---

## 📝 How to Use

### Change Voice:
```
"Joi, please use the aria voice"
"Joi, switch to the michelle voice"
"Joi, I want you to sound like jenny"
```

### Set Avatar from Image:
```
"Joi, use joi_bg.jpg as your avatar"
"Joi, load the image called my_photo.png and use it as your appearance"
```

---

## 🎬 Advanced: SadTalker (Animated Talking Photos)

SadTalker can make ANY photo talk with realistic lip-sync and head movements!

### Installation (Optional - Advanced Users):

#### Option 1: Google Colab (Easiest - No Installation)
1. Go to: https://colab.research.google.com/github/OpenTalker/SadTalker/blob/main/quick_demo.ipynb
2. Upload your avatar photo
3. Upload the TTS audio from `assets/audio/` folder
4. Download the generated video
5. Tell Joi: "use this video as my avatar" (you'll need to implement video playback)

#### Option 2: Local Installation (Advanced - Requires GPU)
```bash
# Clone SadTalker
git clone https://github.com/OpenTalker/SadTalker.git
cd SadTalker

# Install dependencies
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install -r requirements.txt

# Download checkpoints
bash scripts/download_models.sh
```

### Using SadTalker:

1. **Generate TTS audio** (Joi does this automatically now)
2. **Run SadTalker:**
   ```bash
   python inference.py \
     --driven_audio assets/audio/tts_latest.mp3 \
     --source_image assets/avatars/joi.png \
     --result_dir assets/videos/ \
     --enhancer gfpgan
   ```
3. The talking video will be saved to `assets/videos/`

---

## 🎨 How It Works

### Voice Pipeline:
1. You chat with Joi
2. Joi responds with text
3. Server generates TTS audio using Edge TTS (FREE)
4. Audio is sent to browser
5. Browser plays audio + animates avatar

### Lip-Sync:
- Simple: Avatar image scales slightly while speaking (INCLUDED)
- Advanced: SadTalker generates full talking head video (OPTIONAL)

---

## 🔧 Troubleshooting

### "Edge TTS not working"
```bash
# Reinstall edge-tts
pip uninstall edge-tts
pip install edge-tts
```

### "No sound playing"
- Check browser audio permissions
- Check system volume
- Try a different voice: "Joi, use the jenny voice"

### "Lip-sync not showing"
- Make sure you've set a custom avatar image
- The particle animation doesn't lip-sync, only custom images do

### "Voice sounds robotic"
- Make sure you're using Edge TTS: "Joi, use the aria voice"
- If still robotic, try: "Joi, use the michelle voice"

---

## 💰 Cost Comparison

| Service | Cost | Quality | Limit |
|---------|------|---------|-------|
| **Edge TTS** | FREE | Excellent | Unlimited |
| OpenAI TTS | $15/1M chars | Best | Pay per use |
| Browser TTS | FREE | Poor | Unlimited |

**Recommendation:** Use Edge TTS (FREE) - it's nearly as good as OpenAI!

---

## 🎯 Example Commands

```
"Joi, use joi_bg.jpg as your avatar and switch to the aria voice"
"Joi, I want you to sound more professional - use the jenny voice"
"Joi, can you use a British accent? Try the sonia voice"
"Joi, what voices do you have available?"
"Joi, generate an avatar that looks like a futuristic AI"
```

---

## 📋 File Locations

- **Avatars:** `assets/avatars/`
- **Audio (TTS):** `assets/audio/`
- **Videos (SadTalker):** `assets/videos/`
- **Backups:** `backups/`

---

## 🆘 Need Help?

### Check logs:
```bash
# Run Joi with verbose output
python joi_companion.py
```

### Test Edge TTS directly:
```bash
edge-tts --text "Hello, this is a test" --write-media test.mp3
```

If test.mp3 plays correctly, Edge TTS is working!

---

## 🎉 Enjoy Your Upgraded Joi!

Your AI companion now has:
- ✅ Natural, human-like voice (FREE)
- ✅ Lip-sync animation
- ✅ Multiple personality voices
- ✅ Avatar customization

Have fun chatting with your enhanced Joi! 🚀
