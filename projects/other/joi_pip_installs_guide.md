# Joi – Suggested Python Packages (from your screenshots)

This list is **best-effort** based on the features shown in the screenshots you shared (desktop screenshots/vision, camera vision, VTube Studio bridge, file generation, TTS/LLM, memory embeddings).  
Because I’m reading from screenshots (not your full repo), treat this as a **checklist**: install only what you use, and verify by running Joi and watching for `ModuleNotFoundError`.

---

## Recommended setup (Windows)

### 1) Create + activate a virtual environment (strongly recommended)
From your Joi project folder:

```bat
py -m venv .venv
.venv\Scripts\activate
py -m pip install --upgrade pip
```

### 2) Install “core” packages (common across the features you showed)

```bat
pip install requests python-dotenv openai
```

**What these do**
- `requests` – HTTP calls (APIs, local servers, model endpoints).
- `python-dotenv` – loads `.env` variables (keys, settings).
- `openai` – OpenAI-compatible API client (cloud or local OpenAI-compatible servers).

---

## Feature-based installs

### A) Desktop screenshots + screen analysis tools
Your screenshots show modules like `capture_screen`, `analyze_screen`, screenshot saving/cleanup, and notes like “Run: pip install mss pillow”.

```bat
pip install mss pillow pyautogui
```

**What these do**
- `mss` – fast screenshot capture on Windows.
- `pillow` – image loading/saving/resizing (PIL).
- `pyautogui` – optional fallback for screenshots + basic UI automation (if you ever enable it).

**Notes**
- `pyautogui` can require additional Windows dependencies in rare cases; only install if you need the fallback.

---

### B) Camera “Spatial Vision” (OpenCV + MediaPipe)
Your screenshot explicitly lists:

> `pip install opencv-python mediapipe pillow`  
> Optional: `pip install face-recognition`

Install:

```bat
pip install opencv-python mediapipe pillow
```

**What these do**
- `opencv-python` – camera capture + image processing.
- `mediapipe` – face landmarks / gaze-ish signals / pose/hand tracking primitives.
- `pillow` – image conversions and saving.

#### Optional (advanced / heavier): named face matching
```bat
pip install face-recognition
```

**Important**
- `face-recognition` depends on `dlib`, which can be **painful on Windows** (may require a prebuilt wheel that matches your Python version).  
If it fails, skip it and keep “face detected / not detected” without identity matching.

---

### C) VTube Studio bridge (pyvts)
Your screenshot shows `joi_vtube.py` and states:

> REQUIRES: `pip install pyvts`  
> VTube Studio must be running with API enabled (port 8001 default)

Install:

```bat
pip install pyvts
```

**What it does**
- `pyvts` – connects to VTube Studio API to drive Live2D/VRM parameters (lip-sync, expression, etc.).

---

### D) File generation (PDF / DOCX / etc.)
From your earlier logs you have tools like `generate_file()` that can create PDF/TXT/DOCX/MD.

Install (safe baseline):
```bat
pip install fpdf2 python-docx
```

**What these do**
- `fpdf2` – PDF creation.
- `python-docx` – generate `.docx` files.

**If your code uses the older `fpdf` import**
- Some projects import `from fpdf import FPDF`. That works with `fpdf2` as well, but if you see import issues, tell me the exact error.

---

### E) Speech / TTS (Python-side)
From your screenshots: your UI uses browser speech (no pip), and the backend has TTS routes that may use OpenAI or Edge TTS.

#### If you use Microsoft Edge TTS in Python
```bat
pip install edge-tts
```

**What it does**
- `edge-tts` – free(ish) neural voices via Microsoft Edge’s TTS endpoints (commonly used in hobby projects).

#### If you only use OpenAI TTS
You already have:
```bat
pip install openai
```

---

### F) Local Whisper speech-to-text (optional, heavy)
Only install if you truly want **local** transcription.

```bat
pip install openai-whisper
```

Whisper usually also needs PyTorch. The correct Torch install varies by CPU/GPU.  
If you tell me whether you have an NVIDIA GPU (and which), I can give the exact Torch command. Otherwise, **skip Whisper for now**.

---

### G) Vector memory embeddings (what your screenshot implies)
Your screenshot mentions OpenAI embeddings (`text-embedding-3-small`) and “no numpy needed”.

If you are using OpenAI embeddings via the OpenAI client, you already have:
```bat
pip install openai
```

No extra packages required unless your repo uses a local vector DB (FAISS/Chroma/etc.).  
If later you add one, common choices are:
- `chromadb`
- `faiss-cpu`
- `numpy`

(Only install once you confirm you’re actually using them.)

---

## One-shot “everything from screenshots” install

If you just want to install the likely set in one go (excluding Whisper + face-recognition):

```bat
pip install requests python-dotenv openai mss pillow pyautogui opencv-python mediapipe pyvts fpdf2 python-docx edge-tts
```

---

## Quick verification checklist (after installs)

Run Joi and look for these common errors:

- `ModuleNotFoundError: No module named 'mss'` → install `mss`
- `No module named 'PIL'` → install `pillow`
- `No module named 'cv2'` → install `opencv-python`
- `No module named 'mediapipe'` → install `mediapipe`
- `No module named 'pyvts'` → install `pyvts`
- `No module named 'fpdf'` → install `fpdf2`
- `No module named 'docx'` → install `python-docx`
- `No module named 'edge_tts'` → install `edge-tts`
- `No module named 'openai'` → install `openai`
- `No module named 'dotenv'` → install `python-dotenv`

---

## Safety note about “biometric” features
Some of the “Spatial & Biometric Vision” claims in the screenshot (recognize a specific person, gaze tracking, etc.) can be unreliable unless you *explicitly* implement and test them.  
Installing packages alone doesn’t guarantee it works—camera permissions, model quality, and code paths matter.

---

## If you want this to be exact
The most accurate approach is:
1) Run `py -m pip freeze > requirements_freeze.txt` inside your venv (current state)
2) Run Joi and copy/paste the **first** `ModuleNotFoundError` you see
3) I’ll tell you the **one** package to install next (minimal installs, no bloat)

