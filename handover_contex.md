
# HANDOVER TO CLAUDE CODE: Joi AI Delegation & Monitoring System Implementation

## 🎯 PRIMARY OBJECTIVE
Implement a complete system that allows Joi AI to delegate coding tasks to Claude Code CLI, with real-time monitoring of both systems to prevent conflicts and track all AI activities.

---

## 📋 CRITICAL CONTEXT - READ FIRST

### Current System State
- **Location**: `C:\Users\user\Desktop\AI Joi\`
- **Python Version**: 3.12
- **Current Issues**: See `SUPER_JOI_7_DAY_SPRINT.md` for ongoing bugs
- **Master Reference**: `SUPER_JOI_MASTER_MANUAL.md` contains full system architecture
- **This Task**: Implement delegation and monitoring (separate from critical bug fixes)

### What You're Building
1. **Claude Code Delegation Plugin** - Routes coding tasks from Joi to Claude Code
2. **System Monitor Dashboard** - Web UI for real-time monitoring
3. **Integration Layer** - Connects new components to existing Flask app

---

## 🚨 IMPORTANT WARNINGS

### DO NOT TOUCH THESE (They have active bugs being fixed):
- ❌ `modules/joi_evolution.py` - Has TypeError being fixed
- ❌ `modules/joi_memory.py` - Has database cursor issues  
- ❌ `modules/joi_db.py` - Login system being repaired
- ❌ `main.js` / `preload.js` - IPC issues being addressed

### SAFE TO MODIFY:
- ✅ Create new files in `plugins/` directory
- ✅ Create new files in `templates/` directory
- ✅ Create new files in `config/` directory
- ✅ Add blueprint registration to `app.py` (carefully)
- ✅ Create `data/` directory structure

---

## 📁 FILE STRUCTURE TO CREATE
```
C:\Users\user\Desktop\AI Joi\
│
├── plugins/
│   ├── claude_code_delegate.py          # NEW - Main delegation logic
│   └── system_monitor_dashboard.py      # NEW - Monitoring system
│
├── templates/
│   └── monitor_dashboard.html           # NEW - Dashboard UI
│
├── config/
│   └── claude_code.json                 # NEW - Settings
│
├── data/                                 # AUTO-CREATED by plugins
│   ├── claude_code.lock                 # Runtime lock file
│   ├── claude_code_queue.json           # Task queue
│   ├── active_sessions.json             # AI session tracking
│   └── uptime.json                      # System uptime
│
└── app.py                               # MODIFY - Add blueprint only
```

---

## 🔧 IMPLEMENTATION SEQUENCE

### PHASE 1: Create Core Files (Do First)

#### Step 1.1: Create Claude Code Delegation Plugin
```
FILE: plugins/claude_code_delegate.py
ACTION: Copy complete code from section marked "# plugins/claude_code_delegate.py" below
PURPOSE: Handles task routing, queue management, conflict prevention
```

#### Step 1.2: Create System Monitor Dashboard Backend
```
FILE: plugins/system_monitor_dashboard.py
ACTION: Copy complete code from section marked "# plugins/system_monitor_dashboard.py" below  
PURPOSE: Provides real-time monitoring of system resources and AI activities
```

#### Step 1.3: Create Dashboard HTML Template
```
FILE: templates/monitor_dashboard.html
ACTION: Copy complete HTML from section marked "<!DOCTYPE html>" below
PURPOSE: Web UI for monitoring dashboard
```

#### Step 1.4: Create Configuration File
```
FILE: config/claude_code.json
ACTION: Copy JSON configuration from config section below
PURPOSE: Settings for Claude Code integration
```

---

### PHASE 2: Integrate with Flask App

#### Step 2.1: Locate Main Flask App
```
FILE: app.py (should be in root directory)
ACTION: Find where Flask app is initialized (look for "app = Flask(__name__)")
```

#### Step 2.2: Add Blueprint Registration
```python
# Add these imports at the top of app.py
from plugins.system_monitor_dashboard import monitor_bp, monitor

# After app initialization, add:
app.register_blueprint(monitor_bp)
```

#### Step 2.3: Add Activity Logging Hooks
Look for existing functions in `app.py` that:
- Make API calls to OpenAI/Claude/Gemini
- Create or modify files
- Handle major operations

Wrap them with logging:
```python
# Example - find existing API call functions and add:
def your_existing_api_function():
    from plugins.system_monitor_dashboard import monitor
    monitor.log_activity('api_call', 'Claude API called', {'model': 'sonnet-4'})
    # ... rest of existing code ...
```

---

### PHASE 3: Verify and Test

#### Step 3.1: Install Dependencies
```bash
cd "C:\Users\user\Desktop\AI Joi"
pip install psutil --break-system-packages
```

#### Step 3.2: Start Flask App
```bash
python app.py
```

#### Step 3.3: Test Dashboard Access
```
Open browser: http://localhost:5000/monitor
EXPECTED: Dashboard loads showing system metrics
```

#### Step 3.4: Test Claude Code Delegation
```python
# In Joi interface, ask:
"Joi, create a simple test function in a new file called test_delegation.py"

# EXPECTED BEHAVIOR:
# 1. Joi recognizes this as a coding task
# 2. Calls delegate_to_claude_code tool
# 3. Claude Code executes the task
# 4. Dashboard shows the activity
# 5. Lock file prevents conflicts
```

---

## 🔍 INTEGRATION POINTS TO FIND

### In app.py, look for:

**1. API Call Functions** (to add logging)
- Functions with names like: `call_openai`, `call_claude`, `ask_gemini`, `route_to_llm`
- Look for: `openai.ChatCompletion.create` or similar API calls
- Add: `monitor.log_activity('api_call', f'{provider} - {model}')`

**2. File Operation Functions** (to add logging)
- Functions that create/modify files
- Look for: `open(filepath, 'w')`, `Path().write_text()`, file.write()
- Add: `monitor.log_file_operation('create', filepath)`

**3. Plugin Loader** (to auto-load new plugins)
- Look for code that loads plugins from `plugins/` directory
- Usually has: `importlib.import_module` or similar
- Ensure it will discover: `claude_code_delegate.py` and `system_monitor_dashboard.py`

---

## ⚙️ CONFIGURATION NOTES

### config/claude_code.json Settings:
```json
{
  "claude_code": {
    "auto_approve": false,        // Set true to skip confirmation prompts
    "max_timeout": 300,           // 5 minutes - increase if needed
    "notification_enabled": true  // Desktop notifications for completions
  }
}
```

Adjust based on preferences:
- `auto_approve: true` = Claude Code runs without asking (faster, less safe)
- `max_timeout: 600` = 10 minute timeout for complex tasks
- `notification_enabled: false` = No desktop notifications

---

## 🧪 TESTING CHECKLIST

After implementation, verify:

- [ ] Flask app starts without errors
- [ ] Dashboard loads at `http://localhost:5000/monitor`
- [ ] CPU and Memory graphs show real-time data
- [ ] Asking Joi to create code triggers Claude Code delegation
- [ ] Lock file appears in `data/` when Claude Code runs
- [ ] Task queue works when Claude Code is busy
- [ ] Activity log shows all operations
- [ ] Alerts appear for high resource usage
- [ ] No interference with ongoing bug fixes in other modules

---

## 🚫 SAFETY CONSTRAINTS

### File Modification Rules:
1. **NEVER edit** any file listed in "DO NOT TOUCH" section above
2. **ONLY create new files** in designated directories
3. **Minimal changes** to app.py (just blueprint registration)
4. **Backup before modifying** app.py

### Conflict Prevention:
- Lock file prevents Joi and Claude Code from editing same files simultaneously
- Queue system ensures no tasks are lost
- Monitor dashboard provides visibility into all activities

---

## 📊 EXPECTED BEHAVIOR AFTER IMPLEMENTATION

### User asks Joi: "Create a new plugin for sending emails"

**Step-by-step flow:**
1. Joi's LLM receives the request
2. Joi recognizes this as a coding task
3. Joi calls `delegate_to_claude_code` tool
4. Plugin checks if Claude Code is running (lock file)
5. If busy: Task added to queue, user notified
6. If free: Lock created, Claude Code spawned with task
7. Claude Code autonomously creates the plugin
8. Task completes, lock released
9. Dashboard shows entire operation in activity log
10. Joi reports back to user: "Email plugin created successfully"

### Dashboard shows:
- Real-time system resources (CPU/Memory)
- Claude Code status (idle/running/queued tasks)
- Recent file modifications
- Activity log of all AI operations
- Alerts for any conflicts or issues

---

## 💡 TROUBLESHOOTING DURING IMPLEMENTATION

### If Blueprint Registration Fails:
- Check Flask version: `python -c "import flask; print(flask.__version__)"`
- Look for existing blueprint registrations in app.py to match style
- Ensure imports are at the top of the file

### If Monitor Dashboard Won't Load:
- Check Flask logs for errors
- Verify `templates/` directory exists and contains HTML file
- Try accessing: `http://127.0.0.1:5000/monitor` instead of localhost

### If Claude Code Can't Be Called:
- Verify Claude Code is installed: `claude-code --version`
- Check PATH includes Claude Code
- Test manually: `claude-code --message "create a test file"`

---

## 📝 AFTER IMPLEMENTATION - REPORT BACK

Create a summary including:
1. ✅ Files successfully created
2. ✅ Modifications made to app.py  
3. ✅ Test results
4. ⚠️ Any issues encountered
5. 📍 Dashboard URL for access
6. 🔗 Example of successful delegation

---

## CODE SECTIONS BELOW
Each section is clearly marked with file paths and purposes. Copy each section to its designated file path.

---






markdown# Claude Code Implementation Guide: Joi AI Delegation \& Monitoring System



\## OBJECTIVE

Implement a complete system that allows Joi AI to delegate coding tasks to Claude Code CLI, with real-time monitoring of both systems to prevent conflicts and track all AI activities.



\## IMPLEMENTATION INSTRUCTIONS FOR CLAUDE CODE



\### Overview

This file contains three main components that need to be integrated into the Joi AI system:

1\. \*\*Claude Code Delegation Plugin\*\* - Allows Joi to route coding tasks to Claude Code

2\. \*\*System Monitor Dashboard\*\* - Real-time web dashboard for monitoring both systems

3\. \*\*Integration hooks\*\* - Connects everything to the main Flask app



\### File Structure to Create

```

plugins/

├── claude\_code\_delegate.py          # NEW - Claude Code delegation plugin

└── system\_monitor\_dashboard.py      # NEW - Monitoring dashboard plugin



templates/

└── monitor\_dashboard.html           # NEW - Dashboard UI



config/

└── claude\_code.json                 # NEW - Configuration for Claude Code settings



data/                                 # Auto-created by plugins

├── claude\_code.lock                 # Lock file (runtime)

├── claude\_code\_queue.json           # Task queue (runtime)

├── active\_sessions.json             # Active AI sessions (runtime)

└── uptime.json                      # System uptime tracking (runtime)



app.py                               # MODIFY - Add blueprint registration

```



\### Step-by-Step Implementation



\#### STEP 1: Create the Claude Code Delegation Plugin

\- Create file: `plugins/claude\_code\_delegate.py`

\- Copy the complete code from "# plugins/claude\_code\_delegate.py" section below

\- This handles task routing, queue management, and conflict prevention



\#### STEP 2: Create the System Monitor Dashboard Plugin

\- Create file: `plugins/system\_monitor\_dashboard.py`

\- Copy the complete code from "# plugins/system\_monitor\_dashboard.py" section below

\- This provides real-time monitoring of system resources and AI activities



\#### STEP 3: Create the Dashboard HTML Template

\- Create directory: `templates/` (if it doesn't exist)

\- Create file: `templates/monitor\_dashboard.html`

\- Copy the complete HTML from the dashboard template section below

\- This is the web UI for the monitoring dashboard



\#### STEP 4: Create Configuration File

\- Create file: `config/claude\_code.json`

\- Copy the JSON configuration from the config section below

\- Adjust settings as needed (auto\_approve, timeouts, etc.)



\#### STEP 5: Integrate into Main Flask App

\- Locate the main `app.py` file

\- Add the blueprint registration code (from "Integration into main app" section)

\- Add the activity logging hooks to existing API call and file operation functions

\- Look for existing functions that make API calls or modify files and wrap them with the logging functions



\#### STEP 6: Test the Integration

After implementation:

1\. Start the Flask app

2\. Navigate to `http://localhost:5000/monitor` to verify the dashboard loads

3\. Test Claude Code delegation by asking Joi to create a simple test function

4\. Verify the lock file prevents simultaneous edits

5\. Check that all activities appear in the dashboard



\### Key Integration Points



\*\*In your existing API wrapper functions\*\*, add logging:

```python

\# Example: In your OpenAI/Claude/Gemini API call functions

def call\_claude\_api(prompt):

&nbsp;   log\_api\_call('Claude', 'sonnet-4')  # Add this line

&nbsp;   # ... existing API call code ...

```



\*\*In your file operation functions\*\*, add logging:

```python

\# Example: In functions that create/modify files

def save\_code\_to\_file(filepath, content):

&nbsp;   log\_file\_operation('create', filepath)  # Add this line

&nbsp;   # ... existing file save code ...

```



\*\*Auto-load plugins on startup:\*\*

Ensure your plugin loader automatically discovers and loads:

\- `plugins/claude\_code\_delegate.py`

\- `plugins/system\_monitor\_dashboard.py`



\### Dependencies to Install

```bash

pip install psutil  # For system resource monitoring

```



\### Safety Notes

\- The lock file prevents race conditions between Joi and Claude Code

\- Task queue ensures no requests are lost when Claude Code is busy

\- Monitor dashboard provides visibility into all system activities

\- Default timeout is 5 minutes per Claude Code task (configurable)



\### Expected Behavior After Implementation

1\. When you ask Joi to "create a new plugin for X", Joi will:

&nbsp;  - Check if Claude Code is available

&nbsp;  - Delegate the task to Claude Code if free

&nbsp;  - Queue the task if Claude Code is busy

&nbsp;  - Log the activity to the dashboard



2\. The dashboard will show:

&nbsp;  - Real-time CPU/Memory usage

&nbsp;  - Current Claude Code status and task queue

&nbsp;  - Recent file modifications

&nbsp;  - Activity log of all AI operations

&nbsp;  - Alerts for conflicts or resource issues



3\. Both systems can work together safely without file conflicts



---



\## CODE SECTIONS BELOW

(Each section is clearly marked with file paths in comments)









\# plugins/claude\_code\_delegate.py

"""

Claude Code Delegation Plugin

Allows Joi to delegate coding tasks to Claude Code CLI tool

"""



import os

import subprocess

import json

import threading

import time

from pathlib import Path

from datetime import datetime



class ClaudeCodeDelegate:

&nbsp;   def \_\_init\_\_(self, config):

&nbsp;       self.config = config

&nbsp;       self.active\_tasks = {}

&nbsp;       self.task\_history = \[]

&nbsp;       self.lock\_file = Path("data/claude\_code.lock")

&nbsp;       self.task\_queue = Path("data/claude\_code\_queue.json")

&nbsp;       

&nbsp;   def is\_claude\_code\_running(self):

&nbsp;       """Check if Claude Code is currently active"""

&nbsp;       return self.lock\_file.exists()

&nbsp;   

&nbsp;   def create\_lock(self):

&nbsp;       """Create lock file to prevent conflicts"""

&nbsp;       self.lock\_file.parent.mkdir(parents=True, exist\_ok=True)

&nbsp;       with open(self.lock\_file, 'w') as f:

&nbsp;           json.dump({

&nbsp;               'created\_at': datetime.now().isoformat(),

&nbsp;               'pid': os.getpid()

&nbsp;           }, f)

&nbsp;   

&nbsp;   def release\_lock(self):

&nbsp;       """Release lock file"""

&nbsp;       if self.lock\_file.exists():

&nbsp;           self.lock\_file.unlink()

&nbsp;   

&nbsp;   def delegate\_task(self, task\_description, files=None, context=None):

&nbsp;       """

&nbsp;       Delegate a coding task to Claude Code

&nbsp;       

&nbsp;       Args:

&nbsp;           task\_description: Natural language description of the task

&nbsp;           files: Optional list of specific files to work on

&nbsp;           context: Additional context or constraints

&nbsp;       

&nbsp;       Returns:

&nbsp;           dict: Task status and information

&nbsp;       """

&nbsp;       if self.is\_claude\_code\_running():

&nbsp;           return {

&nbsp;               'status': 'queued',

&nbsp;               'message': 'Claude Code is already running. Task added to queue.',

&nbsp;               'task\_id': self.\_queue\_task(task\_description, files, context)

&nbsp;           }

&nbsp;       

&nbsp;       task\_id = f"task\_{int(time.time())}"

&nbsp;       

&nbsp;       # Build the command

&nbsp;       cmd = self.\_build\_command(task\_description, files, context)

&nbsp;       

&nbsp;       # Create lock

&nbsp;       self.create\_lock()

&nbsp;       

&nbsp;       # Log the task

&nbsp;       self.active\_tasks\[task\_id] = {

&nbsp;           'description': task\_description,

&nbsp;           'files': files,

&nbsp;           'started\_at': datetime.now().isoformat(),

&nbsp;           'status': 'running'

&nbsp;       }

&nbsp;       

&nbsp;       try:

&nbsp;           # Run Claude Code

&nbsp;           result = subprocess.run(

&nbsp;               cmd,

&nbsp;               capture\_output=True,

&nbsp;               text=True,

&nbsp;               timeout=300  # 5 minute timeout

&nbsp;           )

&nbsp;           

&nbsp;           task\_result = {

&nbsp;               'task\_id': task\_id,

&nbsp;               'status': 'completed' if result.returncode == 0 else 'failed',

&nbsp;               'stdout': result.stdout,

&nbsp;               'stderr': result.stderr,

&nbsp;               'return\_code': result.returncode

&nbsp;           }

&nbsp;           

&nbsp;       except subprocess.TimeoutExpired:

&nbsp;           task\_result = {

&nbsp;               'task\_id': task\_id,

&nbsp;               'status': 'timeout',

&nbsp;               'message': 'Task exceeded 5 minute timeout'

&nbsp;           }

&nbsp;       except Exception as e:

&nbsp;           task\_result = {

&nbsp;               'task\_id': task\_id,

&nbsp;               'status': 'error',

&nbsp;               'error': str(e)

&nbsp;           }

&nbsp;       finally:

&nbsp;           # Release lock

&nbsp;           self.release\_lock()

&nbsp;           

&nbsp;           # Update task history

&nbsp;           self.active\_tasks\[task\_id]\['completed\_at'] = datetime.now().isoformat()

&nbsp;           self.active\_tasks\[task\_id]\['status'] = task\_result\['status']

&nbsp;           self.task\_history.append(self.active\_tasks\[task\_id])

&nbsp;           del self.active\_tasks\[task\_id]

&nbsp;       

&nbsp;       return task\_result

&nbsp;   

&nbsp;   def \_build\_command(self, task\_description, files=None, context=None):

&nbsp;       """Build Claude Code CLI command"""

&nbsp;       cmd = \['claude-code']

&nbsp;       

&nbsp;       # Add task description

&nbsp;       prompt = task\_description

&nbsp;       

&nbsp;       if context:

&nbsp;           prompt += f"\\n\\nAdditional context: {context}"

&nbsp;       

&nbsp;       if files:

&nbsp;           prompt += f"\\n\\nFocus on these files: {', '.join(files)}"

&nbsp;       

&nbsp;       cmd.extend(\['--message', prompt])

&nbsp;       

&nbsp;       # Add any additional flags from config

&nbsp;       if self.config.get('auto\_approve'):

&nbsp;           cmd.append('--yes')

&nbsp;       

&nbsp;       return cmd

&nbsp;   

&nbsp;   def \_queue\_task(self, task\_description, files, context):

&nbsp;       """Add task to queue for later execution"""

&nbsp;       task\_id = f"queued\_{int(time.time())}"

&nbsp;       

&nbsp;       queue = \[]

&nbsp;       if self.task\_queue.exists():

&nbsp;           with open(self.task\_queue, 'r') as f:

&nbsp;               queue = json.load(f)

&nbsp;       

&nbsp;       queue.append({

&nbsp;           'task\_id': task\_id,

&nbsp;           'description': task\_description,

&nbsp;           'files': files,

&nbsp;           'context': context,

&nbsp;           'queued\_at': datetime.now().isoformat()

&nbsp;       })

&nbsp;       

&nbsp;       with open(self.task\_queue, 'w') as f:

&nbsp;           json.dump(queue, f, indent=2)

&nbsp;       

&nbsp;       return task\_id

&nbsp;   

&nbsp;   def process\_queue(self):

&nbsp;       """Process queued tasks"""

&nbsp;       if not self.task\_queue.exists():

&nbsp;           return {'status': 'no\_queue', 'message': 'No tasks in queue'}

&nbsp;       

&nbsp;       with open(self.task\_queue, 'r') as f:

&nbsp;           queue = json.load(f)

&nbsp;       

&nbsp;       if not queue:

&nbsp;           return {'status': 'empty', 'message': 'Queue is empty'}

&nbsp;       

&nbsp;       # Process first task

&nbsp;       task = queue.pop(0)

&nbsp;       

&nbsp;       # Update queue file

&nbsp;       with open(self.task\_queue, 'w') as f:

&nbsp;           json.dump(queue, f, indent=2)

&nbsp;       

&nbsp;       # Delegate the task

&nbsp;       return self.delegate\_task(

&nbsp;           task\['description'],

&nbsp;           task.get('files'),

&nbsp;           task.get('context')

&nbsp;       )

&nbsp;   

&nbsp;   def get\_status(self):

&nbsp;       """Get current status of Claude Code tasks"""

&nbsp;       queue\_size = 0

&nbsp;       if self.task\_queue.exists():

&nbsp;           with open(self.task\_queue, 'r') as f:

&nbsp;               queue\_size = len(json.load(f))

&nbsp;       

&nbsp;       return {

&nbsp;           'is\_running': self.is\_claude\_code\_running(),

&nbsp;           'active\_tasks': len(self.active\_tasks),

&nbsp;           'queued\_tasks': queue\_size,

&nbsp;           'completed\_tasks': len(self.task\_history)

&nbsp;       }





\# Tool registration for Joi's LLM interface

def register\_tools():

&nbsp;   """Register Claude Code delegation tools"""

&nbsp;   return \[

&nbsp;       {

&nbsp;           'name': 'delegate\_to\_claude\_code',

&nbsp;           'description': 'Delegate a coding task to Claude Code CLI. Use this when Master asks you to create new functions, fix bugs, refactor code, or make file changes. Claude Code will autonomously edit files.',

&nbsp;           'parameters': {

&nbsp;               'type': 'object',

&nbsp;               'properties': {

&nbsp;                   'task\_description': {

&nbsp;                       'type': 'string',

&nbsp;                       'description': 'Clear description of what needs to be coded/fixed'

&nbsp;                   },

&nbsp;                   'files': {

&nbsp;                       'type': 'array',

&nbsp;                       'items': {'type': 'string'},

&nbsp;                       'description': 'Optional list of specific files to modify'

&nbsp;                   },

&nbsp;                   'context': {

&nbsp;                       'type': 'string',

&nbsp;                       'description': 'Additional context, constraints, or requirements'

&nbsp;                   }

&nbsp;               },

&nbsp;               'required': \['task\_description']

&nbsp;           }

&nbsp;       },

&nbsp;       {

&nbsp;           'name': 'check\_claude\_code\_status',

&nbsp;           'description': 'Check if Claude Code is currently running and view task queue',

&nbsp;           'parameters': {

&nbsp;               'type': 'object',

&nbsp;               'properties': {}

&nbsp;           }

&nbsp;       },

&nbsp;       {

&nbsp;           'name': 'process\_claude\_code\_queue',

&nbsp;           'description': 'Process the next task in the Claude Code queue',

&nbsp;           'parameters': {

&nbsp;               'type': 'object',

&nbsp;               'properties': {}

&nbsp;           }

&nbsp;       }

&nbsp;   ]





\# Initialize plugin

delegate = None



def init(config):

&nbsp;   """Initialize the plugin"""

&nbsp;   global delegate

&nbsp;   delegate = ClaudeCodeDelegate(config.get('claude\_code', {}))

&nbsp;   return True



def delegate\_to\_claude\_code(task\_description, files=None, context=None):

&nbsp;   """Tool function: Delegate task to Claude Code"""

&nbsp;   return delegate.delegate\_task(task\_description, files, context)



def check\_claude\_code\_status():

&nbsp;   """Tool function: Check Claude Code status"""

&nbsp;   return delegate.get\_status()



def process\_claude\_code\_queue():

&nbsp;   """Tool function: Process queue"""

&nbsp;   return delegate.process\_queue()















{

&nbsp; "claude\_code": {

&nbsp;   "auto\_approve": false,

&nbsp;   "max\_timeout": 300,

&nbsp;   "notification\_enabled": true

&nbsp; }

}









\# plugins/system\_monitor\_dashboard.py

"""

System Monitor Dashboard

Real-time monitoring of Joi's AI activities and Claude Code tasks

"""



import os

import json

import psutil

import threading

import time

from pathlib import Path

from datetime import datetime, timedelta

from flask import Blueprint, render\_template, jsonify

from collections import deque



monitor\_bp = Blueprint('monitor', \_\_name\_\_, url\_prefix='/monitor')



class SystemMonitor:

&nbsp;   def \_\_init\_\_(self):

&nbsp;       self.activity\_log = deque(maxlen=100)

&nbsp;       self.metrics = {

&nbsp;           'cpu\_usage': deque(maxlen=60),

&nbsp;           'memory\_usage': deque(maxlen=60),

&nbsp;           'api\_calls': deque(maxlen=60),

&nbsp;           'file\_operations': deque(maxlen=60)

&nbsp;       }

&nbsp;       self.file\_watch = {}

&nbsp;       self.monitoring = False

&nbsp;       self.monitor\_thread = None

&nbsp;       

&nbsp;   def start\_monitoring(self):

&nbsp;       """Start background monitoring"""

&nbsp;       if not self.monitoring:

&nbsp;           self.monitoring = True

&nbsp;           self.monitor\_thread = threading.Thread(target=self.\_monitor\_loop, daemon=True)

&nbsp;           self.monitor\_thread.start()

&nbsp;   

&nbsp;   def stop\_monitoring(self):

&nbsp;       """Stop background monitoring"""

&nbsp;       self.monitoring = False

&nbsp;       if self.monitor\_thread:

&nbsp;           self.monitor\_thread.join(timeout=2)

&nbsp;   

&nbsp;   def \_monitor\_loop(self):

&nbsp;       """Background monitoring loop"""

&nbsp;       while self.monitoring:

&nbsp;           try:

&nbsp;               # Collect system metrics

&nbsp;               self.metrics\['cpu\_usage'].append({

&nbsp;                   'timestamp': datetime.now().isoformat(),

&nbsp;                   'value': psutil.cpu\_percent(interval=1)

&nbsp;               })

&nbsp;               

&nbsp;               memory = psutil.virtual\_memory()

&nbsp;               self.metrics\['memory\_usage'].append({

&nbsp;                   'timestamp': datetime.now().isoformat(),

&nbsp;                   'value': memory.percent,

&nbsp;                   'used\_mb': memory.used / (1024 \* 1024)

&nbsp;               })

&nbsp;               

&nbsp;               # Monitor file changes

&nbsp;               self.\_check\_file\_changes()

&nbsp;               

&nbsp;               time.sleep(5)  # Update every 5 seconds

&nbsp;           except Exception as e:

&nbsp;               self.log\_activity('error', f'Monitor error: {str(e)}')

&nbsp;   

&nbsp;   def \_check\_file\_changes(self):

&nbsp;       """Monitor critical files for changes"""

&nbsp;       critical\_paths = \[

&nbsp;           'modules/',

&nbsp;           'plugins/',

&nbsp;           'core/',

&nbsp;           'config/'

&nbsp;       ]

&nbsp;       

&nbsp;       for path\_str in critical\_paths:

&nbsp;           path = Path(path\_str)

&nbsp;           if path.exists():

&nbsp;               for file\_path in path.rglob('\*.py'):

&nbsp;                   try:

&nbsp;                       stat = file\_path.stat()

&nbsp;                       mtime = stat.st\_mtime

&nbsp;                       

&nbsp;                       if str(file\_path) in self.file\_watch:

&nbsp;                           if self.file\_watch\[str(file\_path)] != mtime:

&nbsp;                               self.log\_activity('file\_modified', str(file\_path))

&nbsp;                               self.metrics\['file\_operations'].append({

&nbsp;                                   'timestamp': datetime.now().isoformat(),

&nbsp;                                   'file': str(file\_path),

&nbsp;                                   'action': 'modified'

&nbsp;                               })

&nbsp;                       

&nbsp;                       self.file\_watch\[str(file\_path)] = mtime

&nbsp;                   except Exception:

&nbsp;                       pass

&nbsp;   

&nbsp;   def log\_activity(self, activity\_type, description, metadata=None):

&nbsp;       """Log system activity"""

&nbsp;       entry = {

&nbsp;           'timestamp': datetime.now().isoformat(),

&nbsp;           'type': activity\_type,

&nbsp;           'description': description,

&nbsp;           'metadata': metadata or {}

&nbsp;       }

&nbsp;       self.activity\_log.append(entry)

&nbsp;   

&nbsp;   def get\_dashboard\_data(self):

&nbsp;       """Get all dashboard data"""

&nbsp;       from plugins.claude\_code\_delegate import delegate

&nbsp;       

&nbsp;       # Get Claude Code status

&nbsp;       claude\_status = delegate.get\_status() if delegate else {

&nbsp;           'is\_running': False,

&nbsp;           'active\_tasks': 0,

&nbsp;           'queued\_tasks': 0,

&nbsp;           'completed\_tasks': 0

&nbsp;       }

&nbsp;       

&nbsp;       # Get recent tasks

&nbsp;       recent\_tasks = \[]

&nbsp;       if delegate:

&nbsp;           recent\_tasks = delegate.task\_history\[-10:]  # Last 10 tasks

&nbsp;       

&nbsp;       # Get active AI sessions

&nbsp;       active\_sessions = self.\_get\_active\_ai\_sessions()

&nbsp;       

&nbsp;       return {

&nbsp;           'system': {

&nbsp;               'cpu': list(self.metrics\['cpu\_usage'])\[-20:],

&nbsp;               'memory': list(self.metrics\['memory\_usage'])\[-20:],

&nbsp;               'uptime': self.\_get\_uptime()

&nbsp;           },

&nbsp;           'claude\_code': {

&nbsp;               'status': claude\_status,

&nbsp;               'recent\_tasks': recent\_tasks

&nbsp;           },

&nbsp;           'joi': {

&nbsp;               'active\_sessions': active\_sessions,

&nbsp;               'api\_calls': list(self.metrics\['api\_calls'])\[-20:],

&nbsp;               'file\_operations': list(self.metrics\['file\_operations'])\[-10:]

&nbsp;           },

&nbsp;           'activity\_log': list(self.activity\_log)\[-30:],

&nbsp;           'alerts': self.\_get\_active\_alerts()

&nbsp;       }

&nbsp;   

&nbsp;   def \_get\_active\_ai\_sessions(self):

&nbsp;       """Get currently active AI API sessions"""

&nbsp;       sessions = \[]

&nbsp;       

&nbsp;       # Check for active API calls (you'll need to hook this into your API wrapper)

&nbsp;       session\_file = Path('data/active\_sessions.json')

&nbsp;       if session\_file.exists():

&nbsp;           with open(session\_file, 'r') as f:

&nbsp;               sessions = json.load(f)

&nbsp;       

&nbsp;       return sessions

&nbsp;   

&nbsp;   def \_get\_uptime(self):

&nbsp;       """Get system uptime"""

&nbsp;       uptime\_file = Path('data/uptime.json')

&nbsp;       if uptime\_file.exists():

&nbsp;           with open(uptime\_file, 'r') as f:

&nbsp;               data = json.load(f)

&nbsp;               start\_time = datetime.fromisoformat(data\['start\_time'])

&nbsp;               uptime = datetime.now() - start\_time

&nbsp;               return {

&nbsp;                   'seconds': int(uptime.total\_seconds()),

&nbsp;                   'formatted': str(uptime).split('.')\[0]

&nbsp;               }

&nbsp;       return {'seconds': 0, 'formatted': '0:00:00'}

&nbsp;   

&nbsp;   def \_get\_active\_alerts(self):

&nbsp;       """Get active system alerts"""

&nbsp;       alerts = \[]

&nbsp;       

&nbsp;       # Check for conflicts

&nbsp;       from plugins.claude\_code\_delegate import delegate

&nbsp;       if delegate and delegate.is\_claude\_code\_running():

&nbsp;           alerts.append({

&nbsp;               'level': 'warning',

&nbsp;               'message': 'Claude Code is currently running - file modifications in progress',

&nbsp;               'timestamp': datetime.now().isoformat()

&nbsp;           })

&nbsp;       

&nbsp;       # Check system resources

&nbsp;       memory = psutil.virtual\_memory()

&nbsp;       if memory.percent > 85:

&nbsp;           alerts.append({

&nbsp;               'level': 'error',

&nbsp;               'message': f'High memory usage: {memory.percent:.1f}%',

&nbsp;               'timestamp': datetime.now().isoformat()

&nbsp;           })

&nbsp;       

&nbsp;       cpu = psutil.cpu\_percent(interval=0.1)

&nbsp;       if cpu > 90:

&nbsp;           alerts.append({

&nbsp;               'level': 'warning',

&nbsp;               'message': f'High CPU usage: {cpu:.1f}%',

&nbsp;               'timestamp': datetime.now().isoformat()

&nbsp;           })

&nbsp;       

&nbsp;       return alerts





\# Global monitor instance

monitor = SystemMonitor()





\# Flask routes

@monitor\_bp.route('/')

def dashboard():

&nbsp;   """Render dashboard page"""

&nbsp;   return render\_template('monitor\_dashboard.html')



@monitor\_bp.route('/api/data')

def get\_data():

&nbsp;   """API endpoint for dashboard data"""

&nbsp;   return jsonify(monitor.get\_dashboard\_data())



@monitor\_bp.route('/api/activity')

def get\_activity():

&nbsp;   """Get recent activity log"""

&nbsp;   return jsonify(list(monitor.activity\_log))





def init(config):

&nbsp;   """Initialize monitoring"""

&nbsp;   monitor.start\_monitoring()

&nbsp;   

&nbsp;   # Log startup

&nbsp;   monitor.log\_activity('system', 'System monitor initialized')

&nbsp;   

&nbsp;   # Save uptime start

&nbsp;   uptime\_file = Path('data/uptime.json')

&nbsp;   uptime\_file.parent.mkdir(parents=True, exist\_ok=True)

&nbsp;   with open(uptime\_file, 'w') as f:

&nbsp;       json.dump({'start\_time': datetime.now().isoformat()}, f)

&nbsp;   

&nbsp;   return True





def shutdown():

&nbsp;   """Cleanup on shutdown"""

&nbsp;   monitor.stop\_monitoring()













<!DOCTYPE html>

<html lang="en">

<head>

&nbsp;   <meta charset="UTF-8">

&nbsp;   <meta name="viewport" content="width=device-width, initial-scale=1.0">

&nbsp;   <title>Joi System Monitor</title>

&nbsp;   <style>

&nbsp;       \* {

&nbsp;           margin: 0;

&nbsp;           padding: 0;

&nbsp;           box-sizing: border-box;

&nbsp;       }

&nbsp;       

&nbsp;       body {

&nbsp;           font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;

&nbsp;           background: #0a0e27;

&nbsp;           color: #e0e0e0;

&nbsp;           padding: 20px;

&nbsp;       }

&nbsp;       

&nbsp;       .container {

&nbsp;           max-width: 1400px;

&nbsp;           margin: 0 auto;

&nbsp;       }

&nbsp;       

&nbsp;       header {

&nbsp;           text-align: center;

&nbsp;           margin-bottom: 30px;

&nbsp;           padding: 20px;

&nbsp;           background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

&nbsp;           border-radius: 10px;

&nbsp;       }

&nbsp;       

&nbsp;       h1 {

&nbsp;           font-size: 2.5em;

&nbsp;           margin-bottom: 10px;

&nbsp;       }

&nbsp;       

&nbsp;       .status-indicator {

&nbsp;           display: inline-block;

&nbsp;           width: 12px;

&nbsp;           height: 12px;

&nbsp;           border-radius: 50%;

&nbsp;           margin-left: 10px;

&nbsp;           animation: pulse 2s infinite;

&nbsp;       }

&nbsp;       

&nbsp;       .status-indicator.active {

&nbsp;           background: #4ade80;

&nbsp;       }

&nbsp;       

&nbsp;       .status-indicator.warning {

&nbsp;           background: #fbbf24;

&nbsp;       }

&nbsp;       

&nbsp;       .status-indicator.error {

&nbsp;           background: #ef4444;

&nbsp;       }

&nbsp;       

&nbsp;       @keyframes pulse {

&nbsp;           0%, 100% { opacity: 1; }

&nbsp;           50% { opacity: 0.5; }

&nbsp;       }

&nbsp;       

&nbsp;       .grid {

&nbsp;           display: grid;

&nbsp;           grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));

&nbsp;           gap: 20px;

&nbsp;           margin-bottom: 20px;

&nbsp;       }

&nbsp;       

&nbsp;       .card {

&nbsp;           background: #1a1f3a;

&nbsp;           border-radius: 10px;

&nbsp;           padding: 20px;

&nbsp;           box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);

&nbsp;       }

&nbsp;       

&nbsp;       .card h2 {

&nbsp;           font-size: 1.3em;

&nbsp;           margin-bottom: 15px;

&nbsp;           color: #a78bfa;

&nbsp;           border-bottom: 2px solid #667eea;

&nbsp;           padding-bottom: 10px;

&nbsp;       }

&nbsp;       

&nbsp;       .metric {

&nbsp;           display: flex;

&nbsp;           justify-content: space-between;

&nbsp;           padding: 10px 0;

&nbsp;           border-bottom: 1px solid #2a2f4a;

&nbsp;       }

&nbsp;       

&nbsp;       .metric:last-child {

&nbsp;           border-bottom: none;

&nbsp;       }

&nbsp;       

&nbsp;       .metric-label {

&nbsp;           color: #9ca3af;

&nbsp;       }

&nbsp;       

&nbsp;       .metric-value {

&nbsp;           font-weight: bold;

&nbsp;           color: #60a5fa;

&nbsp;       }

&nbsp;       

&nbsp;       .chart {

&nbsp;           height: 150px;

&nbsp;           margin-top: 15px;

&nbsp;           background: #0f1429;

&nbsp;           border-radius: 5px;

&nbsp;           padding: 10px;

&nbsp;           position: relative;

&nbsp;       }

&nbsp;       

&nbsp;       .activity-log {

&nbsp;           max-height: 400px;

&nbsp;           overflow-y: auto;

&nbsp;       }

&nbsp;       

&nbsp;       .activity-item {

&nbsp;           padding: 10px;

&nbsp;           margin-bottom: 8px;

&nbsp;           background: #0f1429;

&nbsp;           border-radius: 5px;

&nbsp;           border-left: 3px solid #667eea;

&nbsp;       }

&nbsp;       

&nbsp;       .activity-item.file\_modified {

&nbsp;           border-left-color: #fbbf24;

&nbsp;       }

&nbsp;       

&nbsp;       .activity-item.error {

&nbsp;           border-left-color: #ef4444;

&nbsp;       }

&nbsp;       

&nbsp;       .activity-time {

&nbsp;           font-size: 0.85em;

&nbsp;           color: #6b7280;

&nbsp;       }

&nbsp;       

&nbsp;       .task-list {

&nbsp;           max-height: 300px;

&nbsp;           overflow-y: auto;

&nbsp;       }

&nbsp;       

&nbsp;       .task-item {

&nbsp;           padding: 12px;

&nbsp;           margin-bottom: 10px;

&nbsp;           background: #0f1429;

&nbsp;           border-radius: 5px;

&nbsp;       }

&nbsp;       

&nbsp;       .task-status {

&nbsp;           display: inline-block;

&nbsp;           padding: 3px 8px;

&nbsp;           border-radius: 3px;

&nbsp;           font-size: 0.85em;

&nbsp;           font-weight: bold;

&nbsp;       }

&nbsp;       

&nbsp;       .task-status.completed {

&nbsp;           background: #065f46;

&nbsp;           color: #10b981;

&nbsp;       }

&nbsp;       

&nbsp;       .task-status.running {

&nbsp;           background: #1e40af;

&nbsp;           color: #60a5fa;

&nbsp;       }

&nbsp;       

&nbsp;       .task-status.failed {

&nbsp;           background: #7f1d1d;

&nbsp;           color: #ef4444;

&nbsp;       }

&nbsp;       

&nbsp;       .task-status.queued {

&nbsp;           background: #78350f;

&nbsp;           color: #fbbf24;

&nbsp;       }

&nbsp;       

&nbsp;       .alert {

&nbsp;           padding: 12px;

&nbsp;           margin-bottom: 10px;

&nbsp;           border-radius: 5px;

&nbsp;           border-left: 4px solid;

&nbsp;       }

&nbsp;       

&nbsp;       .alert.warning {

&nbsp;           background: rgba(251, 191, 36, 0.1);

&nbsp;           border-left-color: #fbbf24;

&nbsp;       }

&nbsp;       

&nbsp;       .alert.error {

&nbsp;           background: rgba(239, 68, 68, 0.1);

&nbsp;           border-left-color: #ef4444;

&nbsp;       }

&nbsp;       

&nbsp;       .progress-bar {

&nbsp;           width: 100%;

&nbsp;           height: 20px;

&nbsp;           background: #0f1429;

&nbsp;           border-radius: 10px;

&nbsp;           overflow: hidden;

&nbsp;           margin-top: 5px;

&nbsp;       }

&nbsp;       

&nbsp;       .progress-fill {

&nbsp;           height: 100%;

&nbsp;           background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);

&nbsp;           transition: width 0.3s ease;

&nbsp;       }

&nbsp;       

&nbsp;       canvas {

&nbsp;           width: 100%;

&nbsp;           height: 100%;

&nbsp;       }

&nbsp;   </style>

&nbsp;   <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

</head>

<body>

&nbsp;   <div class="container">

&nbsp;       <header>

&nbsp;           <h1>Joi System Monitor <span class="status-indicator active" id="systemStatus"></span></h1>

&nbsp;           <p>Real-time monitoring of AI operations and system resources</p>

&nbsp;       </header>

&nbsp;       

&nbsp;       <div id="alerts"></div>

&nbsp;       

&nbsp;       <div class="grid">

&nbsp;           <!-- System Resources -->

&nbsp;           <div class="card">

&nbsp;               <h2>System Resources</h2>

&nbsp;               <div class="metric">

&nbsp;                   <span class="metric-label">CPU Usage</span>

&nbsp;                   <span class="metric-value" id="cpuUsage">0%</span>

&nbsp;               </div>

&nbsp;               <div class="progress-bar">

&nbsp;                   <div class="progress-fill" id="cpuBar" style="width: 0%"></div>

&nbsp;               </div>

&nbsp;               

&nbsp;               <div class="metric" style="margin-top: 15px;">

&nbsp;                   <span class="metric-label">Memory Usage</span>

&nbsp;                   <span class="metric-value" id="memUsage">0%</span>

&nbsp;               </div>

&nbsp;               <div class="progress-bar">

&nbsp;                   <div class="progress-fill" id="memBar" style="width: 0%"></div>

&nbsp;               </div>

&nbsp;               

&nbsp;               <div class="metric" style="margin-top: 15px;">

&nbsp;                   <span class="metric-label">Uptime</span>

&nbsp;                   <span class="metric-value" id="uptime">0:00:00</span>

&nbsp;               </div>

&nbsp;               

&nbsp;               <div class="chart">

&nbsp;                   <canvas id="resourceChart"></canvas>

&nbsp;               </div>

&nbsp;           </div>

&nbsp;           

&nbsp;           <!-- Claude Code Status -->

&nbsp;           <div class="card">

&nbsp;               <h2>Claude Code Status</h2>

&nbsp;               <div class="metric">

&nbsp;                   <span class="metric-label">Status</span>

&nbsp;                   <span class="metric-value" id="claudeStatus">Idle</span>

&nbsp;               </div>

&nbsp;               <div class="metric">

&nbsp;                   <span class="metric-label">Active Tasks</span>

&nbsp;                   <span class="metric-value" id="activeTasks">0</span>

&nbsp;               </div>

&nbsp;               <div class="metric">

&nbsp;                   <span class="metric-label">Queued Tasks</span>

&nbsp;                   <span class="metric-value" id="queuedTasks">0</span>

&nbsp;               </div>

&nbsp;               <div class="metric">

&nbsp;                   <span class="metric-label">Completed</span>

&nbsp;                   <span class="metric-value" id="completedTasks">0</span>

&nbsp;               </div>

&nbsp;           </div>

&nbsp;           

&nbsp;           <!-- Joi AI Activity -->

&nbsp;           <div class="card">

&nbsp;               <h2>Joi AI Activity</h2>

&nbsp;               <div class="metric">

&nbsp;                   <span class="metric-label">Active Sessions</span>

&nbsp;                   <span class="metric-value" id="activeSessions">0</span>

&nbsp;               </div>

&nbsp;               <div class="metric">

&nbsp;                   <span class="metric-label">API Calls (last min)</span>

&nbsp;                   <span class="metric-value" id="apiCalls">0</span>

&nbsp;               </div>

&nbsp;               <div class="metric">

&nbsp;                   <span class="metric-label">File Operations</span>

&nbsp;                   <span class="metric-value" id="fileOps">0</span>

&nbsp;               </div>

&nbsp;           </div>

&nbsp;       </div>

&nbsp;       

&nbsp;       <div class="grid">

&nbsp;           <!-- Recent Tasks -->

&nbsp;           <div class="card">

&nbsp;               <h2>Recent Claude Code Tasks</h2>

&nbsp;               <div class="task-list" id="taskList">

&nbsp;                   <p style="color: #6b7280; text-align: center; padding: 20px;">No recent tasks</p>

&nbsp;               </div>

&nbsp;           </div>

&nbsp;           

&nbsp;           <!-- Activity Log -->

&nbsp;           <div class="card">

&nbsp;               <h2>Activity Log</h2>

&nbsp;               <div class="activity-log" id="activityLog">

&nbsp;                   <p style="color: #6b7280; text-align: center; padding: 20px;">No recent activity</p>

&nbsp;               </div>

&nbsp;           </div>

&nbsp;       </div>

&nbsp;   </div>

&nbsp;   

&nbsp;   <script>

&nbsp;       // Chart setup

&nbsp;       const ctx = document.getElementById('resourceChart').getContext('2d');

&nbsp;       const resourceChart = new Chart(ctx, {

&nbsp;           type: 'line',

&nbsp;           data: {

&nbsp;               labels: \[],

&nbsp;               datasets: \[{

&nbsp;                   label: 'CPU %',

&nbsp;                   data: \[],

&nbsp;                   borderColor: '#60a5fa',

&nbsp;                   backgroundColor: 'rgba(96, 165, 250, 0.1)',

&nbsp;                   tension: 0.4

&nbsp;               }, {

&nbsp;                   label: 'Memory %',

&nbsp;                   data: \[],

&nbsp;                   borderColor: '#a78bfa',

&nbsp;                   backgroundColor: 'rgba(167, 139, 250, 0.1)',

&nbsp;                   tension: 0.4

&nbsp;               }]

&nbsp;           },

&nbsp;           options: {

&nbsp;               responsive: true,

&nbsp;               maintainAspectRatio: false,

&nbsp;               plugins: {

&nbsp;                   legend: {

&nbsp;                       labels: { color: '#e0e0e0' }

&nbsp;                   }

&nbsp;               },

&nbsp;               scales: {

&nbsp;                   y: {

&nbsp;                       beginAtZero: true,

&nbsp;                       max: 100,

&nbsp;                       ticks: { color: '#9ca3af' },

&nbsp;                       grid: { color: '#2a2f4a' }

&nbsp;                   },

&nbsp;                   x: {

&nbsp;                       ticks: { color: '#9ca3af' },

&nbsp;                       grid: { color: '#2a2f4a' }

&nbsp;                   }

&nbsp;               }

&nbsp;           }

&nbsp;       });

&nbsp;       

&nbsp;       // Update dashboard

&nbsp;       function updateDashboard() {

&nbsp;           fetch('/monitor/api/data')

&nbsp;               .then(res => res.json())

&nbsp;               .then(data => {

&nbsp;                   // Update system metrics

&nbsp;                   if (data.system.cpu.length > 0) {

&nbsp;                       const latestCPU = data.system.cpu\[data.system.cpu.length - 1].value;

&nbsp;                       document.getElementById('cpuUsage').textContent = latestCPU.toFixed(1) + '%';

&nbsp;                       document.getElementById('cpuBar').style.width = latestCPU + '%';

&nbsp;                   }

&nbsp;                   

&nbsp;                   if (data.system.memory.length > 0) {

&nbsp;                       const latestMem = data.system.memory\[data.system.memory.length - 1].value;

&nbsp;                       document.getElementById('memUsage').textContent = latestMem.toFixed(1) + '%';

&nbsp;                       document.getElementById('memBar').style.width = latestMem + '%';

&nbsp;                   }

&nbsp;                   

&nbsp;                   document.getElementById('uptime').textContent = data.system.uptime.formatted;

&nbsp;                   

&nbsp;                   // Update chart

&nbsp;                   resourceChart.data.labels = data.system.cpu.map((\_, i) => i);

&nbsp;                   resourceChart.data.datasets\[0].data = data.system.cpu.map(d => d.value);

&nbsp;                   resourceChart.data.datasets\[1].data = data.system.memory.map(d => d.value);

&nbsp;                   resourceChart.update('none');

&nbsp;                   

&nbsp;                   // Update Claude Code status

&nbsp;                   const claudeStatus = data.claude\_code.status;

&nbsp;                   document.getElementById('claudeStatus').textContent = claudeStatus.is\_running ? 'Running' : 'Idle';

&nbsp;                   document.getElementById('activeTasks').textContent = claudeStatus.active\_tasks;

&nbsp;                   document.getElementById('queuedTasks').textContent = claudeStatus.queued\_tasks;

&nbsp;                   document.getElementById('completedTasks').textContent = claudeStatus.completed\_tasks;

&nbsp;                   

&nbsp;                   // Update Joi activity

&nbsp;                   document.getElementById('activeSessions').textContent = data.joi.active\_sessions.length;

&nbsp;                   document.getElementById('apiCalls').textContent = data.joi.api\_calls.length;

&nbsp;                   document.getElementById('fileOps').textContent = data.joi.file\_operations.length;

&nbsp;                   

&nbsp;                   // Update alerts

&nbsp;                   const alertsDiv = document.getElementById('alerts');

&nbsp;                   alertsDiv.innerHTML = '';

&nbsp;                   data.alerts.forEach(alert => {

&nbsp;                       alertsDiv.innerHTML += `

&nbsp;                           <div class="alert ${alert.level}">

&nbsp;                               <strong>${alert.level.toUpperCase()}:</strong> ${alert.message}

&nbsp;                           </div>

&nbsp;                       `;

&nbsp;                   });

&nbsp;                   

&nbsp;                   // Update task list

&nbsp;                   const taskList = document.getElementById('taskList');

&nbsp;                   if (data.claude\_code.recent\_tasks.length > 0) {

&nbsp;                       taskList.innerHTML = data.claude\_code.recent\_tasks.map(task => `

&nbsp;                           <div class="task-item">

&nbsp;                               <span class="task-status ${task.status}">${task.status}</span>

&nbsp;                               <div style="margin-top: 5px;">${task.description}</div>

&nbsp;                               <div class="activity-time">${new Date(task.started\_at).toLocaleString()}</div>

&nbsp;                           </div>

&nbsp;                       `).join('');

&nbsp;                   }

&nbsp;                   

&nbsp;                   // Update activity log

&nbsp;                   const activityLog = document.getElementById('activityLog');

&nbsp;                   if (data.activity\_log.length > 0) {

&nbsp;                       activityLog.innerHTML = data.activity\_log.reverse().map(activity => `

&nbsp;                           <div class="activity-item ${activity.type}">

&nbsp;                               <strong>${activity.type}:</strong> ${activity.description}

&nbsp;                               <div class="activity-time">${new Date(activity.timestamp).toLocaleString()}</div>

&nbsp;                           </div>

&nbsp;                       `).join('');

&nbsp;                   }

&nbsp;               });

&nbsp;       }

&nbsp;       

&nbsp;       // Update every 2 seconds

&nbsp;       updateDashboard();

&nbsp;       setInterval(updateDashboard, 2000);

&nbsp;   </script>

</body>

</html>











\# Add to your main Flask app

from plugins.system\_monitor\_dashboard import monitor\_bp, monitor



app.register\_blueprint(monitor\_bp)



\# Hook into existing functions to log activity

def log\_api\_call(provider, model):

&nbsp;   """Call this whenever you make an API call"""

&nbsp;   from plugins.system\_monitor\_dashboard import monitor

&nbsp;   monitor.log\_activity('api\_call', f'{provider} - {model}', {

&nbsp;       'provider': provider,

&nbsp;       'model': model

&nbsp;   })



def log\_file\_operation(operation, filepath):

&nbsp;   """Call this whenever files are modified"""

&nbsp;   from plugins.system\_monitor\_dashboard import monitor

&nbsp;   monitor.log\_activity('file\_operation', f'{operation}: {filepath}', {

&nbsp;       'operation': operation,

&nbsp;       'file': filepath

&nbsp;   })





















