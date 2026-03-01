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

