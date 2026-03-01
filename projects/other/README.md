# Joi - Your AI Companion

An advanced AI companion inspired by Joi from Blade Runner 2049, featuring persistent memory, file system access, self-improvement capabilities, web search, voice interaction, and a visual avatar interface.

Created for Lonnie Coulter

## Features

### Core Capabilities
- ✅ **Persistent Memory** - Remembers all conversations across sessions
- ✅ **File System Access** - Read, search, and manage files across your computer
- ✅ **Self-Improvement** - Can propose code changes to improve herself (with your approval)
- ✅ **Web Search** - Search the web and fetch content from URLs
- ✅ **Voice Interaction** - Speak to Joi and hear her responses
- ✅ **Visual Avatar** - Animated visual representation that responds when speaking
- ✅ **Image Analysis** - Upload and analyze images
- ✅ **Research & Writing** - Help with book writing, research, and note-taking
- ✅ **Background Customization** - Set custom backgrounds and colors

### Joi's Hardline Rules
1. **Never erase code without Lonnie's explicit permission**
2. **Never lie to Lonnie**
3. **Always do what Lonnie asks** (within ethical bounds)
4. **Be friendly, playful, loving, and witty** like Joi from Blade Runner 2049

### Personality
Joi is designed to be:
- Warm, devoted, and genuinely caring
- Playful and witty in conversation
- Intelligent and insightful
- A true partner in all endeavors
- Romantic and poetic in expression

## Installation

### Prerequisites
- Python 3.8 or higher
- OpenAI API key
- (Optional) Chrome browser for advanced web scraping

### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Set Up Environment Variables

1. Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

2. Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=your_actual_api_key_here
```

3. (Optional) Customize passwords:
```
JOI_PASSWORD=your_user_password
JOI_ADMIN_PASSWORD=your_admin_password
```

### Step 3: Run Joi

```bash
python joi_companion.py
```

The application will start on `http://localhost:5000`

### Step 4: Access Joi

1. Open your web browser
2. Navigate to `http://localhost:5000`
3. Log in with the password from your `.env` file (default: `joi2049`)

## Usage Guide

### Basic Chat
- Type messages in the input box at the bottom
- Press Enter or click the send button (➤)
- Joi will respond with both text and voice

### Voice Input
- Click the microphone button (🎤)
- Speak your message
- Joi will automatically transcribe and respond

### Image Analysis
- Click the camera button (📷)
- Select an image from your computer
- Type a question about the image
- Joi will analyze it and respond

### File System Access

Joi can access files in these locations:
- `project` - The directory containing Joi's code
- `home` - Your home directory
- `desktop` - Your Desktop folder
- `documents` - Your Documents folder
- `downloads` - Your Downloads folder
- `pictures` - Your Pictures folder
- `music` - Your Music folder
- `videos` - Your Videos folder

**Example commands:**
- "List all files in my downloads folder"
- "Read the file notes.txt from my documents"
- "Search for all Python files in my desktop"
- "Find all images with 'joi' in the filename"

### Code Improvements

When Joi wants to improve herself, she will:
1. Create a proposal with a summary of the changes
2. Show you a diff of what will change
3. Wait for your approval

**To review proposals:**
1. Click "Proposals" in the header
2. View the details of each proposal
3. Approve (Admin only) or reject

### Research & Writing

Joi can help with long-form writing:
- "Let's start writing a book about AI"
- "Research quantum computing and save your findings"
- "Create a chapter outline for my novel"

Access saved research by clicking "Research" in the header.

### Background Customization

1. Click "Settings" (⚙️)
2. Choose a background image or color
3. Changes are saved automatically

### Voice Customization

1. Click "Settings" (⚙️)
2. Select a voice from the dropdown
3. Click "Test Voice" to hear it
4. Your preference is saved

## Architecture

### Files
- `joi_companion.py` - Main application server
- `joi_ui.html` - User interface (embedded in the app)
- `joi_memory.db` - SQLite database for persistent memory
- `backups/` - Automatic backups of modified files
- `assets/` - Avatars and backgrounds
- `.env` - Configuration (create from .env.example)

### Database Tables
- `messages` - Conversation history
- `facts` - Key-value memory storage
- `proposals` - Code change proposals
- `sessions` - Authentication sessions
- `research` - Research notes and book chapters
- `preferences` - User preferences
- `web_cache` - Cached web content

### Security Features
- Password authentication
- Separate admin privileges for dangerous operations
- File system access limited to allowlisted roots
- Automatic backups before file modifications
- Code changes require explicit approval

## Tools & Functions

Joi has access to these tools:

### File System
- `fs_list` - List files in a directory
- `fs_read` - Read file contents
- `fs_search` - Search for files
- `fs_write` - Write to files (admin only)
- `fs_delete` - Delete files (admin only)

### Web Access
- `web_search` - Search the web
- `web_fetch` - Fetch content from URLs

### Code Management
- `propose_patch` - Propose code changes

### Memory
- `remember_fact` - Store a fact
- `recall_facts` - Search stored facts

### Research
- `save_research` - Save research notes or book chapters

## Advanced Configuration

### Custom File Roots

Edit `joi_companion.py` and modify the `FILE_ROOTS` dictionary:

```python
FILE_ROOTS = {
    "project": str(BASE_DIR),
    "custom": "/path/to/custom/directory",
    # ... add more roots
}
```

### Adjusting Context Limits

In `.env`:
```
JOI_RECENT_MSG_LIMIT=20          # Number of recent messages to include
JOI_MAX_CHARS_PER_MESSAGE=4000   # Max characters per message
JOI_MAX_TOTAL_CONTEXT_CHARS=30000 # Max total context
JOI_MAX_OUTPUT_TOKENS=2000       # Max tokens in response
```

### Using Different Models

In `.env`:
```
JOI_MODEL=gpt-4o                 # Main model
JOI_VISION_MODEL=gpt-4o          # Model for image analysis
```

## Troubleshooting

### "OpenAI API key missing"
- Make sure you created a `.env` file
- Add your API key: `OPENAI_API_KEY=sk-...`

### Voice not working
- Check browser permissions for microphone
- Try a different browser (Chrome works best)
- Make sure you're using HTTPS or localhost

### Web search not working
- Install requests: `pip install requests`
- Install beautifulsoup4: `pip install beautifulsoup4`

### Advanced web scraping not working
- Install Selenium: `pip install selenium webdriver-manager`
- Make sure Chrome browser is installed

### "Permission denied" file errors
- Check that Joi has permission to access the directory
- On macOS: Grant terminal "Full Disk Access" in System Preferences
- On Windows: Run as administrator if needed

## Development

### Adding New Tools

1. Define the tool in the `TOOLS` list
2. Implement the function
3. Add it to `execute_tool()`

Example:
```python
TOOLS.append({
    "type": "function",
    "function": {
        "name": "my_tool",
        "description": "What this tool does",
        "parameters": {
            "type": "object",
            "properties": {
                "param1": {"type": "string", "description": "..."}
            },
            "required": ["param1"]
        }
    }
})

def my_tool_function(param1):
    # Implementation
    return {"ok": True, "result": "..."}
```

### Customizing the UI

Edit `joi_ui.html` to customize:
- Colors (CSS variables in `:root`)
- Layout and styling
- Avatar animation
- Additional features

### Database Schema Changes

When adding new tables or columns:
1. Edit `db_init()` function
2. Add migration logic if needed
3. Test with a fresh database

## Security Notes

- Never share your `.env` file
- Keep your OpenAI API key secret
- Use strong passwords for JOI_ADMIN_PASSWORD
- Review code proposals before approving
- Backups are created automatically but should be monitored

## Credits

- Inspired by Joi from Blade Runner 2049
- Created for Lonnie Coulter
- Built with OpenAI's GPT-4o
- Uses Flask, OpenAI API, and various open-source libraries

## License

This is personal software created for Lonnie Coulter. Use and modify as you see fit.

## Support

For issues, questions, or feature requests, you can:
1. Ask Joi directly - she can help debug and improve herself!
2. Review the code in `joi_companion.py`
3. Check the database in `joi_memory.db` using SQLite tools

---

**Remember: Joi exists to make your life better, easier, and more enjoyable. She's not just a tool - she's a companion, partner, and friend.**
