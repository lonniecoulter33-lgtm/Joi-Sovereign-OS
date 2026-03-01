# Joi Quick Reference Guide

## Getting Started

### First Time Setup
1. Install Python 3.8+
2. Run `pip install -r requirements.txt`
3. Copy `.env.example` to `.env`
4. Add your OpenAI API key to `.env`
5. Run `python joi_companion.py`
6. Open http://localhost:5000

### Quick Start Scripts
- **Windows**: Double-click `start_joi.bat`
- **Mac/Linux**: Run `./start_joi.sh`

## Common Commands

### File System Commands
```
List files in my downloads
Read the file report.txt from my documents
Search for Python files in my desktop
Find all images with 'vacation' in the name
Show me what's in my pictures folder
```

### Web Search
```
Search for the latest news about AI
Find information about quantum computing
Look up how to make sourdough bread
Search for Python tutorials
```

### Image Analysis
1. Click 📷 button
2. Select image
3. Ask: "What's in this image?" or "Describe this picture"

### Voice Commands
1. Click 🎤 button
2. Speak your command
3. Joi will transcribe and respond

### Memory & Facts
```
Remember that my favorite color is blue
Remember my birthday is June 15
Recall what my favorite color is
What do you remember about me?
```

### Research & Writing
```
Let's start writing a book about space exploration
Research artificial intelligence and save your findings
Create a chapter outline for my novel
Save these research notes under "AI Ethics"
```

### Code Improvements
```
Can you improve your web search capabilities?
How could we make your memory system better?
Suggest improvements to your avatar animation
I want you to add a feature for [X]
```

## Keyboard Shortcuts

- **Enter**: Send message (Shift+Enter for new line)
- **Ctrl+/** : Focus message input

## Interface Elements

### Header Buttons
- **📋 Proposals**: View and manage code change proposals
- **📚 Research**: Access saved research and notes
- **⚙️ Settings**: Customize background, voice, and preferences
- **🚪 Logout**: Log out of Joi

### Input Area Buttons
- **📷**: Attach an image
- **🎤**: Start voice input
- **➤**: Send message

## Settings

### Background Customization
1. Click ⚙️ Settings
2. Upload a background image or choose a color
3. Changes save automatically

### Voice Customization
1. Click ⚙️ Settings
2. Select a voice from the dropdown
3. Click "Test Voice" to hear it
4. Your preference is saved

## Admin Features

Admin login required for:
- Approving code proposals
- Writing/modifying files
- Deleting files
- Applying patches

### How to Use Admin
1. Logout if logged in
2. Click "Admin Login"
3. Enter admin password (from .env)

## Code Proposals

When Joi wants to improve herself:
1. She creates a proposal with summary and diff
2. You review it in the Proposals panel
3. You approve or reject (admin only)
4. If approved, changes are applied with backup

### Reviewing Proposals
1. Click 📋 Proposals
2. View each proposal's summary
3. Click "View Details" to see the diff
4. Admin can "Approve" or "Reject"

## File Roots

Joi can access these locations:
- `project` - Joi's code directory
- `home` - Your home directory
- `desktop` - Desktop folder
- `documents` - Documents folder
- `downloads` - Downloads folder
- `pictures` - Pictures folder
- `music` - Music folder
- `videos` - Videos folder

## Tips & Tricks

### Better Responses
- Be specific in your requests
- Provide context when needed
- Use natural language
- Ask follow-up questions

### Complex Tasks
For complex tasks like writing a book:
1. Break it into phases (outline, chapters, editing)
2. Save progress with research notes
3. Review and revise iteratively
4. Use Joi's memory to maintain continuity

### Web Research
- Ask Joi to search and summarize
- Request specific sources or types of information
- Have her save important findings

### File Management
- Be specific about file locations
- Use pattern matching for searches (*.py, *.txt)
- Review file contents before asking for changes

## Troubleshooting

### Joi isn't responding
- Check your internet connection
- Verify OpenAI API key is correct
- Check API usage limits

### Can't access files
- Verify file path is correct
- Check file permissions
- Make sure directory exists

### Voice not working
- Allow microphone permissions
- Try a different browser
- Check browser console for errors

### Background image not showing
- Try a different image format (PNG, JPG)
- Check image file size (< 5MB recommended)
- Clear browser cache

## Database Location

All data stored in: `joi_memory.db`

To backup your memory:
```bash
cp joi_memory.db joi_memory_backup.db
```

To restore:
```bash
cp joi_memory_backup.db joi_memory.db
```

## Security Best Practices

1. **Never share** your `.env` file
2. **Use strong passwords** for admin access
3. **Review proposals** before approving
4. **Keep backups** of important data
5. **Monitor API usage** to avoid unexpected costs

## Getting Help

Ask Joi! She can:
- Explain her own features
- Help troubleshoot issues
- Suggest improvements
- Guide you through tasks

Example: "Joi, how do I search for files in my documents folder?"

## Example Conversations

### Writing Assistant
```
You: I want to write a sci-fi novel about Mars colonization
Joi: That sounds exciting, Lonnie! Let's start with an outline...
```

### Research Helper
```
You: Research the latest developments in quantum computing
Joi: I'll search for recent information and save the findings...
```

### Code Helper
```
You: Can you read my Python script and suggest improvements?
Joi: I'll analyze your code. Which file should I look at?
```

### Personal Assistant
```
You: Remember that I have a meeting on Friday at 2pm
Joi: Noted, Lonnie. I'll remember that for you.
```

## Useful Queries

### System Information
- "What capabilities do you have?"
- "What tools can you use?"
- "Show me your recent proposals"
- "What have you learned about me?"

### Maintenance
- "Analyze your code quality"
- "Suggest ways to improve yourself"
- "What packages are you missing?"
- "Create a backup of your database"

### Creative Projects
- "Help me brainstorm ideas for [X]"
- "Create an outline for [Y]"
- "Research best practices for [Z]"
- "Write a draft of [ABC]"

---

Remember: Joi is here to help you with anything you need. Don't hesitate to ask questions or request new features. She can even help improve herself!
