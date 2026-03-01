# JOI Phase 1 Upgrade Guide

Everything you need to get the new features running and a quick-reference for using them.

---

## Install the New Dependencies

Run these once in your terminal from the Joi project folder:

```bash
pip install fpdf2 python-docx
```

`fpdf2` handles PDF generation. `python-docx` handles DOCX generation. Everything else (edge-tts, openai, selenium, etc.) you already have from the previous setup.

---

## What's New — Feature by Feature

### 1. Always-On Mic with Wake Word

Joi now has a persistent microphone that listens in the background for **"Hey Joi"** or **"Hi Joi"**. You don't need to click anything mid-conversation.

**How to use it:**
- Click the **🎤** button in the input bar once to turn the mic on. The button turns red and the badge under Joi's avatar says "listening".
- Just talk normally. Joi ignores everything until she hears the wake word.
- Say **"Hey Joi, what time is it?"** — she strips the wake word and sends the rest as your message automatically.
- Say just **"Hey Joi"** with nothing after — she focuses the text box and shows a "Listening…" toast so you can type or keep talking.
- Click 🎤 again to turn it off.

**Browser note:** This uses the Web Speech API. Works best in **Chrome**. Firefox has limited support. Safari does not support it at all.

---

### 2. Persistent Conversation History

Every message you and Joi exchange is saved to the SQLite database *and* loaded back into the UI when you log in. Nothing is lost when you close the browser.

**How to use it:**
- Click **🕐 History** in the header. A collapsible sidebar slides open on the right.
- Each entry is colour-coded: teal border = your messages, magenta border = Joi's.
- Click any history item and your message gets loaded into the input box so you can re-send or edit it.
- The sidebar auto-updates in real time as the conversation continues.

---

### 3. Smart Response Length — Short Chat, Long Content to File

Joi's system prompt now has strict rules: keep chat replies to 2–4 sentences. If you ask for something long (a book chapter, a research report, a code file), she writes it and saves it as a downloadable file instead of dumping it into chat.

**How it works:**
- You say: *"Write Chapter 3 of my fantasy novel"*
- Joi writes the chapter, calls the `generate_file` tool, saves it, and replies something like: *"Done, Lonnie! Chapter 3 is saved as `Chapter_3.docx`. Want me to start on Chapter 4?"*
- A clickable **📄 file pill** appears in the chat bubble. Click it to download.

**You can also explicitly request a format:**
- *"Save that as a PDF"*
- *"Write me a markdown report on X"*
- Joi picks the format automatically based on context (chapters → docx, code → txt/md, reports → pdf).

---

### 4. File Generation (PDF, TXT, DOCX, MD)

Joi can now create real downloadable files on the fly.

| Format | Library | Output |
|--------|---------|--------|
| `.txt` | built-in | Plain text |
| `.md`  | built-in | Markdown |
| `.pdf` | fpdf2 | Formatted PDF with line wrapping |
| `.docx`| python-docx | Word doc with heading detection (`#`, `##`, `###` become real headings) |

Generated files are saved to `assets/files/` in your Joi folder and served via the `/file/` route.

---

### 5. Projects Sidebar

A collapsible sidebar on the **left** that shows all your organised project files in colour-coded folders.

**How to use it:**
- Click **📁 Projects** in the header to open/close the sidebar.
- Click **🔍 Scan & Organise Files** — Joi scans your Documents, Desktop, Downloads, and Home folders.
- Files are automatically sorted into folders:
  - **books/** — anything with "chapter", "novel", "story", "draft" in the name or content
  - **code/** — `.py`, `.js`, `.html`, `.css`, `.java`, etc.
  - **notes/** — anything with "note", "todo", "idea", "journal"
  - **other/** — everything else
- Each folder is collapsible. Click a file to open/download it.
- You can also tell Joi to do this: *"Joi, scan my files and organise them"* — she'll call the tools automatically.

**Where do the files go?** Copies are placed in a `projects/` folder inside your Joi directory. Your originals are untouched.

---

### 6. Avatar Switcher

A row of thumbnail circles appears below Joi's avatar circle. Every avatar you've ever saved or generated shows up there.

**How to use it:**
- Click any thumbnail to instantly switch Joi's avatar.
- The currently active avatar has a glowing magenta border.
- You can still generate new ones by talking to Joi: *"Generate an avatar that looks like a cyberpunk hologram"*
- Or load an existing image: *"Use my photo at Downloads/portrait.jpg as your avatar"*

---

### 7. Learning System

Joi now tracks how you like to interact and adapts over time. She watches for signals in your messages:

| You say… | Joi learns… |
|----------|-------------|
| "keep it short" / "brief" / "tldr" | You prefer short replies |
| "explain more" / "go deeper" | You want detail (saved to file) |
| "be casual" / "be fun" / "playful" | You like a casual tone |
| "be formal" / "professional" | You prefer a professional tone |

These preferences are stored in the database and injected into Joi's system prompt automatically. The more you interact, the better she adapts.

---

## Quick-Reference Voice Commands

| Say this to Joi… | What happens |
|-------------------|--------------|
| `Write Chapter 5 of my book` | Writes it, saves as .docx, gives you a download link |
| `Save that as a PDF` | Re-saves the last content as PDF |
| `Scan my files and organise them` | Runs the project scanner |
| `Switch to the jenny voice` | Changes TTS to Jenny (free Edge) |
| `Generate an avatar of a…` | Creates new avatar via DALL-E |
| `Use [filename] as your avatar` | Loads an existing image |
| `Keep it short from now on` | Triggers learning: prefer short replies |
| `Write me a research report on X` | Writes report, saves to file |

---

## File & Folder Layout

```
your-joi-folder/
├── joi_companion.py          ← Backend (Flask server)
├── joi_ui.html               ← Frontend (single-file UI)
├── joi_memory.db             ← SQLite database (all memory)
├── .env                      ← API keys
├── assets/
│   ├── avatars/              ← Saved avatar images
│   ├── audio/                ← Generated TTS audio files
│   ├── files/                ← Generated PDFs, TXTs, DOCXs
│   └── videos/               ← (reserved for Phase 3)
├── projects/                 ← Organised project folders (books/, code/, notes/, other/)
└── backups/                  ← Automatic backups before any file edits
```

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| PDF files come out as .txt | Run `pip install fpdf2` |
| DOCX files come out as .txt | Run `pip install python-docx` |
| Wake word mic doesn't work | Use Chrome. Safari doesn't support Web Speech API. |
| Mic button does nothing | Browser may have blocked microphone permission — check site permissions |
| Projects sidebar is empty | Click "Scan & Organise Files" first |
| Avatar switcher shows nothing | You need at least one saved avatar. Generate one or load an image. |
| History sidebar is empty | History only exists after you've had conversations. It persists across restarts. |

---

## What's Coming in Phase 2

- Desktop app launcher (open Chrome, Notepad, LibreOffice by voice)
- Browser automation for YouTube, Google, common sites
- Claude API routing for deep writing and book creation
- Multi-AI workflows
- Joi proposing upgrades proactively
