# SUPER JOI - CRITICAL FIXES CODE TEMPLATES

## 🔧 IMMEDIATE FIX #1: Evolution System TypeError

### File: `modules/joi_evolution.py`

**Find and replace this function:**

```python
# OLD (BROKEN) - Remove this
def propose_upgrade(self, module_name, upgrade_type, description, capability=None):
    # ... old code
```

**Replace with:**

```python
# NEW (FIXED) - Use this
def propose_upgrade(self, module_name, upgrade_type, description, 
                   risk_level="medium", affected_files=None, 
                   rollback_plan=None, test_steps=None):
    """
    Propose a system upgrade with comprehensive metadata
    
    Args:
        module_name (str): Name of module to upgrade (e.g., 'joi_market.py')
        upgrade_type (str): Type of upgrade - 'feature', 'bugfix', 'optimization', 'security'
        description (str): Detailed description of what the upgrade does
        risk_level (str): Risk assessment - 'low', 'medium', 'high', 'critical'
        affected_files (list): List of file paths that will be modified
        rollback_plan (str): Description of how to undo this upgrade
        test_steps (list): List of test steps to verify upgrade success
        
    Returns:
        dict: Upgrade proposal with ID and metadata
    """
    import time
    import json
    from datetime import datetime
    
    # Generate unique ID for this proposal
    proposal_id = f"upgrade_{module_name}_{int(time.time())}"
    
    # Create proposal object
    proposal = {
        'id': proposal_id,
        'module_name': module_name,
        'upgrade_type': upgrade_type,
        'description': description,
        'risk_level': risk_level,
        'affected_files': affected_files or [],
        'rollback_plan': rollback_plan or "Restore from backup",
        'test_steps': test_steps or ["Manual verification required"],
        'status': 'pending',
        'proposed_at': datetime.now().isoformat(),
        'proposed_by': 'joi_evolution'
    }
    
    # Save proposal to database
    try:
        self.save_proposal(proposal)
        print(f"✅ Upgrade proposal created: {proposal_id}")
        return proposal
    except Exception as e:
        print(f"❌ Failed to save proposal: {e}")
        return None
```

**Also add this helper method:**

```python
def save_proposal(self, proposal):
    """Save proposal to database"""
    import sqlite3
    import json
    
    conn = sqlite3.connect('joi_memory.db')
    cursor = conn.cursor()
    
    # Create table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS upgrade_proposals (
            id TEXT PRIMARY KEY,
            module_name TEXT,
            upgrade_type TEXT,
            description TEXT,
            risk_level TEXT,
            affected_files TEXT,
            rollback_plan TEXT,
            test_steps TEXT,
            status TEXT,
            proposed_at TEXT,
            proposed_by TEXT
        )
    ''')
    
    # Insert proposal
    cursor.execute('''
        INSERT INTO upgrade_proposals VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        proposal['id'],
        proposal['module_name'],
        proposal['upgrade_type'],
        proposal['description'],
        proposal['risk_level'],
        json.dumps(proposal['affected_files']),
        proposal['rollback_plan'],
        json.dumps(proposal['test_steps']),
        proposal['status'],
        proposal['proposed_at'],
        proposal['proposed_by']
    ))
    
    conn.commit()
    conn.close()
```

**Find all calls and update them:**

Search your codebase for: `propose_upgrade(`

**Old call (remove `capability=`):**
```python
self.propose_upgrade(
    module_name="joi_market.py",
    upgrade_type="feature",
    description="Add Bollinger Bands",
    capability="technical_analysis"  # ❌ REMOVE THIS
)
```

**New call:**
```python
self.propose_upgrade(
    module_name="joi_market.py",
    upgrade_type="feature",
    description="Add Bollinger Bands indicator for volatility analysis",
    risk_level="low",
    affected_files=["modules/joi_market.py"],
    rollback_plan="Restore joi_market.py from backup",
    test_steps=[
        "Test BB calculation with sample data",
        "Verify upper/middle/lower bands",
        "Test with real market data"
    ]
)
```

---

## 🔧 IMMEDIATE FIX #2: Database Context Manager

### File: `modules/joi_memory.py`

**Add this class at the top of the file:**

```python
import sqlite3
from contextlib import contextmanager

class DatabaseManager:
    """Context manager for safe database operations"""
    
    def __init__(self, db_path='joi_memory.db'):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
    
    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        return self.cursor
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            # If there was an error, rollback
            print(f"Database error: {exc_val}")
            self.conn.rollback()
        else:
            # If successful, commit
            self.conn.commit()
        
        # Always close
        self.cursor.close()
        self.conn.close()
        
        # Don't suppress exceptions
        return False

# Alternative: Use as a decorator
@contextmanager
def db_transaction(db_path='joi_memory.db'):
    """Context manager for database transactions"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Transaction failed: {e}")
        raise
    finally:
        cursor.close()
        conn.close()
```

**Replace all database operations like this:**

**OLD (BROKEN):**
```python
def save_conversation(self, user_id, message):
    conn = sqlite3.connect('joi_memory.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO conversations VALUES (?, ?)", (user_id, message))
    conn.commit()
    # ❌ Missing: cursor.close(), conn.close()
    # ❌ Missing: Error handling
```

**NEW (FIXED):**
```python
def save_conversation(self, user_id, message):
    with DatabaseManager() as cursor:
        cursor.execute(
            "INSERT INTO conversations VALUES (?, ?)", 
            (user_id, message)
        )
    # ✅ Automatically commits and closes
    # ✅ Automatically rolls back on error

# Or using the decorator:
def save_conversation(self, user_id, message):
    with db_transaction() as cursor:
        cursor.execute(
            "INSERT INTO conversations VALUES (?, ?)", 
            (user_id, message)
        )
```

**Find and fix all database operations:**

1. Search for: `sqlite3.connect(`
2. For each match, wrap in context manager
3. Remove manual `commit()`, `close()` calls

---

## 🔧 IMMEDIATE FIX #3: Dependency Injection Container

### Create new file: `modules/joi_container.py`

```python
"""
Dependency Injection Container for Joi
Resolves circular dependencies and manages module lifecycle
"""

class JoiContainer:
    """Simple dependency injection container"""
    
    def __init__(self):
        self._services = {}
        self._singletons = {}
        self._initializing = set()
    
    def register_singleton(self, name, factory):
        """
        Register a singleton service
        
        Args:
            name (str): Service name (e.g., 'llm', 'memory')
            factory (callable): Function that creates the service
                               Should accept container as parameter
        """
        self._services[name] = ('singleton', factory)
    
    def register_transient(self, name, factory):
        """
        Register a transient service (new instance each time)
        
        Args:
            name (str): Service name
            factory (callable): Function that creates the service
        """
        self._services[name] = ('transient', factory)
    
    def resolve(self, name):
        """
        Resolve a service by name
        
        Args:
            name (str): Service name to resolve
            
        Returns:
            Service instance
        """
        if name not in self._services:
            raise ValueError(f"Service '{name}' not registered in container")
        
        # Check for circular dependencies
        if name in self._initializing:
            raise RuntimeError(f"Circular dependency detected: {name}")
        
        service_type, factory = self._services[name]
        
        if service_type == 'singleton':
            # Return cached instance if exists
            if name not in self._singletons:
                self._initializing.add(name)
                try:
                    self._singletons[name] = factory(self)
                finally:
                    self._initializing.remove(name)
            return self._singletons[name]
        else:
            # Create new instance each time
            self._initializing.add(name)
            try:
                return factory(self)
            finally:
                self._initializing.remove(name)
    
    def has(self, name):
        """Check if service is registered"""
        return name in self._services
    
    def clear_singletons(self):
        """Clear all singleton instances (for testing)"""
        self._singletons.clear()


# Global container instance
_container = None

def get_container():
    """Get global container instance"""
    global _container
    if _container is None:
        _container = JoiContainer()
        register_services(_container)
    return _container

def register_services(container):
    """Register all Joi services"""
    
    # Core services (no dependencies)
    container.register_singleton('config', lambda c: load_config())
    
    # LLM service
    container.register_singleton('llm', lambda c: create_llm(c.resolve('config')))
    
    # Memory service (uses database)
    container.register_singleton('memory', lambda c: create_memory())
    
    # File service (uses memory)
    container.register_singleton('files', lambda c: create_files(
        memory=c.resolve('memory')
    ))
    
    # Market service (uses llm and memory)
    container.register_singleton('market', lambda c: create_market(
        llm=c.resolve('llm'),
        memory=c.resolve('memory')
    ))
    
    # Evolution service (uses many services)
    container.register_singleton('evolution', lambda c: create_evolution(
        llm=c.resolve('llm'),
        memory=c.resolve('memory'),
        files=c.resolve('files')
    ))
    
    # ... register other services


def load_config():
    """Load configuration"""
    import json
    with open('.env', 'r') as f:
        # Parse .env file
        config = {}
        for line in f:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                config[key] = value
        return config

def create_llm(config):
    """Create LLM service"""
    from joi_llm import JoiLLM
    return JoiLLM(
        openai_key=config.get('OPENAI_API_KEY'),
        claude_key=config.get('CLAUDE_API_KEY'),
        gemini_key=config.get('GEMINI_API_KEY')
    )

def create_memory():
    """Create memory service"""
    from joi_memory import JoiMemory
    return JoiMemory()

def create_files(memory):
    """Create files service with memory dependency"""
    from joi_files import JoiFiles
    return JoiFiles(memory=memory)

def create_market(llm, memory):
    """Create market service"""
    from joi_market import JoiMarket
    return JoiMarket(llm=llm, memory=memory)

def create_evolution(llm, memory, files):
    """Create evolution service"""
    from joi_evolution import JoiEvolution
    return JoiEvolution(llm=llm, memory=memory, files=files)
```

### Update `joi_companion.py` to use container:

**OLD (BROKEN):**
```python
# joi_companion.py
from joi_llm import JoiLLM
from joi_memory import JoiMemory
from joi_files import JoiFiles  # ❌ Circular import if JoiFiles imports JoiMemory

class JoiCompanion:
    def __init__(self):
        self.llm = JoiLLM()
        self.memory = JoiMemory()
        self.files = JoiFiles(self.memory)
```

**NEW (FIXED):**
```python
# joi_companion.py
from joi_container import get_container

class JoiCompanion:
    def __init__(self):
        self.container = get_container()
    
    @property
    def llm(self):
        return self.container.resolve('llm')
    
    @property
    def memory(self):
        return self.container.resolve('memory')
    
    @property
    def files(self):
        return self.container.resolve('files')
    
    @property
    def market(self):
        return self.container.resolve('market')
```

---

## 🔧 IMMEDIATE FIX #4: IPC Communication

### File: `main.js` (Electron)

**Add error handling to IPC:**

```javascript
const { app, BrowserWindow, ipcMain } = require('electron');
const axios = require('axios');

const FLASK_URL = 'http://127.0.0.1:5001';

// Store window reference
let mainWindow = null;

// IPC handler with error handling
ipcMain.handle('send-message', async (event, data) => {
    try {
        console.log('📤 Sending to Flask:', data);
        
        const response = await axios.post(`${FLASK_URL}/api/chat`, data, {
            headers: { 'Content-Type': 'application/json' },
            timeout: 30000 // 30 second timeout
        });
        
        console.log('📥 Received from Flask:', response.data);
        return { success: true, data: response.data };
        
    } catch (error) {
        console.error('❌ IPC Error:', error.message);
        
        // Send error to renderer
        if (mainWindow && !mainWindow.isDestroyed()) {
            mainWindow.webContents.send('flask-error', {
                message: error.message,
                type: 'connection'
            });
        }
        
        return { 
            success: false, 
            error: error.message,
            details: error.response?.data || null
        };
    }
});

// Avatar state sync
ipcMain.handle('update-avatar', async (event, avatarState) => {
    try {
        console.log('🎭 Avatar state:', avatarState);
        
        const response = await axios.post(`${FLASK_URL}/api/avatar`, avatarState);
        return { success: true, data: response.data };
        
    } catch (error) {
        console.error('❌ Avatar update failed:', error.message);
        return { success: false, error: error.message };
    }
});

// Voice state sync
ipcMain.handle('voice-input', async (event, audioData) => {
    try {
        const response = await axios.post(`${FLASK_URL}/api/voice`, {
            audio: audioData,
            format: 'wav'
        });
        return { success: true, data: response.data };
    } catch (error) {
        console.error('❌ Voice input failed:', error.message);
        return { success: false, error: error.message };
    }
});

// Health check
ipcMain.handle('health-check', async () => {
    try {
        const response = await axios.get(`${FLASK_URL}/api/health`, {
            timeout: 5000
        });
        return { success: true, healthy: true };
    } catch (error) {
        return { success: false, healthy: false, error: error.message };
    }
});

// Create window
function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1200,
        height: 800,
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            preload: path.join(__dirname, 'preload.js')
        }
    });
    
    mainWindow.loadFile('joi_ui.html');
    
    // Check Flask connection on startup
    setTimeout(async () => {
        const health = await checkFlaskHealth();
        if (!health) {
            mainWindow.webContents.send('flask-error', {
                message: 'Cannot connect to Flask backend. Please start joi_companion.py',
                type: 'startup'
            });
        }
    }, 2000);
}

async function checkFlaskHealth() {
    try {
        const response = await axios.get(`${FLASK_URL}/api/health`, {
            timeout: 5000
        });
        return response.status === 200;
    } catch (error) {
        return false;
    }
}

app.whenReady().then(createWindow);
```

### File: `preload.js`

```javascript
const { contextBridge, ipcRenderer } = require('electron');

// Expose protected methods to renderer
contextBridge.exposeInMainWorld('electronAPI', {
    // Send message to Flask
    sendMessage: async (message) => {
        return await ipcRenderer.invoke('send-message', message);
    },
    
    // Update avatar state
    updateAvatar: async (state) => {
        return await ipcRenderer.invoke('update-avatar', state);
    },
    
    // Send voice input
    sendVoice: async (audioData) => {
        return await ipcRenderer.invoke('voice-input', audioData);
    },
    
    // Check backend health
    checkHealth: async () => {
        return await ipcRenderer.invoke('health-check');
    },
    
    // Listen for errors from main process
    onFlaskError: (callback) => {
        ipcRenderer.on('flask-error', (event, error) => {
            callback(error);
        });
    }
});
```

### File: `joi_routes.py` (Flask)

**Add health check endpoint:**

```python
from flask import Flask, request, jsonify
from joi_companion import JoiCompanion

app = Flask(__name__)
joi = JoiCompanion()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint for Electron"""
    return jsonify({
        'status': 'healthy',
        'modules_loaded': joi.get_loaded_modules(),
        'apis_connected': joi.check_api_connections()
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    """Main chat endpoint"""
    try:
        data = request.json
        message = data.get('content', '')
        user_id = data.get('user_id', 'default')
        
        # Process message
        response = joi.process_message(message, user_id)
        
        return jsonify({
            'success': True,
            'response': response
        })
        
    except Exception as e:
        print(f"❌ Chat error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/avatar', methods=['POST'])
def update_avatar():
    """Update avatar state"""
    try:
        data = request.json
        # Update avatar in database
        joi.memory.save_avatar_state(data)
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)
```

---

## 🧪 TESTING SCRIPTS

### Test Evolution System:

```python
# test_evolution.py
from modules.joi_evolution import JoiEvolution

def test_propose_upgrade():
    evolution = JoiEvolution()
    
    proposal = evolution.propose_upgrade(
        module_name="joi_market.py",
        upgrade_type="feature",
        description="Add moving average indicators (SMA, EMA, WMA)",
        risk_level="low",
        affected_files=["modules/joi_market.py"],
        rollback_plan="Restore from backup/joi_market_backup.py",
        test_steps=[
            "Test SMA calculation with sample data",
            "Test EMA calculation with sample data",
            "Verify crossover detection",
            "Test with real-time market data"
        ]
    )
    
    assert proposal is not None
    assert proposal['status'] == 'pending'
    print("✅ Evolution system working!")
    return proposal

if __name__ == '__main__':
    test_propose_upgrade()
```

### Test Database:

```python
# test_database.py
from modules.joi_memory import DatabaseManager

def test_database():
    # Test basic operation
    with DatabaseManager() as cursor:
        cursor.execute('SELECT 1')
        result = cursor.fetchone()
        assert result[0] == 1
    
    print("✅ Database context manager working!")
    
    # Test error handling
    try:
        with DatabaseManager() as cursor:
            cursor.execute('INVALID SQL')
    except Exception as e:
        print(f"✅ Error handling working: {e}")

if __name__ == '__main__':
    test_database()
```

### Test IPC:

```javascript
// test_ipc.js (run in Electron console)
async function testIPC() {
    console.log('Testing IPC...');
    
    // Test health check
    const health = await window.electronAPI.checkHealth();
    console.log('Health:', health);
    
    // Test message
    const response = await window.electronAPI.sendMessage({
        content: 'Hello Joi, this is a test message',
        user_id: 'test_user'
    });
    console.log('Response:', response);
    
    // Test avatar
    const avatar = await window.electronAPI.updateAvatar({
        personality: 'professional',
        mood: 'focused'
    });
    console.log('Avatar:', avatar);
}

testIPC();
```

---

## 📋 VERIFICATION CHECKLIST

After applying all fixes, verify:

- [ ] `python joi_companion.py` starts without errors
- [ ] Evolution system: `python test_evolution.py` passes
- [ ] Database: `python test_database.py` passes
- [ ] All modules import successfully
- [ ] Login works through Electron UI
- [ ] Chat messages send and receive
- [ ] Avatar state syncs
- [ ] Voice input/output works
- [ ] Market data loads
- [ ] No TypeErrors in logs
- [ ] No circular import errors

---

## 🚀 QUICK START COMMANDS

```bash
# 1. Backup current system
xcopy /E /I /Y "C:\Users\user\Desktop\AI Joi" "C:\Users\user\Desktop\AI Joi_Backup"

# 2. Apply fixes (manually edit files as shown above)

# 3. Test evolution system
cd "C:\Users\user\Desktop\AI Joi"
python test_evolution.py

# 4. Test database
python test_database.py

# 5. Start Flask backend
python joi_companion.py

# 6. Start Electron (in new terminal)
npm start

# 7. Test in Joi UI
"Joi, propose an upgrade to add RSI indicator to your market analysis"
```

**Good luck! You've got this! 💪**

