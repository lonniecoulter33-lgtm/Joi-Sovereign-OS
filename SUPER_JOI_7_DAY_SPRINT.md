# SUPER JOI - 7 DAY SPRINT CHECKLIST

## 🚨 CRITICAL PRIORITY - DAY 1

### Fix Evolution System TypeError
**File**: `modules/joi_evolution.py`
**Error**: `TypeError: propose_upgrade() got an unexpected keyword argument 'capability'`

- [ ] **Step 1**: Open `modules/joi_evolution.py`
- [ ] **Step 2**: Locate the `propose_upgrade()` function definition
- [ ] **Step 3**: Update function signature to:
```python
def propose_upgrade(self, module_name, upgrade_type, description, 
                   risk_level="medium", affected_files=None, 
                   rollback_plan=None, test_steps=None):
```
- [ ] **Step 4**: Search for all calls to `propose_upgrade()` in the codebase
- [ ] **Step 5**: Remove any `capability=` parameter from calls
- [ ] **Step 6**: Test the evolution system:
```bash
python joi_companion.py
# Then in Joi interface: "Joi, review your current architecture and propose 3 incremental upgrades."
```

### Fix Database Cursor Issues
**File**: `modules/joi_memory.py`

- [ ] **Step 1**: Create database context manager class
- [ ] **Step 2**: Replace all direct sqlite3.connect() calls with context manager
- [ ] **Step 3**: Test database operations:
```python
# Test script:
python -c "from modules.joi_memory import JoiMemory; mem = JoiMemory(); mem.save_conversation('test', 'test message')"
```

---

## 📋 DAY 2 - Imports & Authentication

### Resolve Circular Imports

- [ ] **Step 1**: Map all module dependencies:
```bash
python -c "import sys; sys.path.append('modules'); import joi_companion"
# Note any ImportError messages
```

- [ ] **Step 2**: Create `modules/joi_container.py` (dependency injection)
- [ ] **Step 3**: Refactor modules to use lazy imports where needed
- [ ] **Step 4**: Test that all modules load:
```python
python joi_companion.py --test-imports
```

### Fix Login System

- [ ] **Step 1**: Check `modules/joi_db.py` authentication functions
- [ ] **Step 2**: Verify session token generation
- [ ] **Step 3**: Test login flow:
```bash
# Start Joi
python joi_companion.py

# Try logging in through Electron UI
# Check Flask logs for any errors
```
- [ ] **Step 4**: Add session recovery if needed

---

## 🔌 DAY 3 - IPC Communication

### Fix Electron-Flask IPC

- [ ] **Step 1**: Review `main.js` IPC handlers
- [ ] **Step 2**: Review `preload.js` IPC channels  
- [ ] **Step 3**: Test each IPC channel:
```javascript
// In Electron console
window.electronAPI.sendMessage({type: 'test', content: 'hello'})
```
- [ ] **Step 4**: Fix any broken channels
- [ ] **Step 5**: Test avatar state synchronization
- [ ] **Step 6**: Test voice interaction through IPC

---

## 🧪 DAY 4 - System Testing

### Comprehensive System Test

- [ ] **Module Loading Test**
```bash
python -m pytest modules/test_module_loading.py -v
```

- [ ] **API Connection Test**
  - [ ] Test OpenAI connection
  - [ ] Test Claude connection  
  - [ ] Test Gemini connection
  - [ ] Test Stock Exchange API 1
  - [ ] Test Stock Exchange API 2

- [ ] **Feature Test**
  - [ ] Test file management
  - [ ] Test web search
  - [ ] Test voice input/output
  - [ ] Test conversation memory
  - [ ] Test project management

- [ ] **Market Intelligence Test**
  - [ ] Test crypto price fetching
  - [ ] Test technical analysis (RSI, trends)
  - [ ] Test price predictions
  - [ ] Test notifications

---

## 📊 DAY 5 - Market Intelligence Verification

### Crypto Analysis

- [ ] **Test Current Features**:
```python
# In Joi interface
"Analyze Bitcoin (BTC) and give me entry/exit recommendations"
"What's the current sentiment for Ethereum?"
"Alert me when XRP reaches $1.50"
```

- [ ] **Verify Data Sources**:
  - [ ] Check API rate limits
  - [ ] Verify data accuracy
  - [ ] Test historical data access

### Stock Analysis

- [ ] **Test Stock Features**:
```python
# In Joi interface  
"Analyze Tesla (TSLA) fundamentals"
"What are the top performing tech stocks today?"
"Track AAPL and notify me of significant moves"
```

### Trading Integration

- [ ] **Verify Exchange Connections**:
  - [ ] Test read-only access (balances, positions)
  - [ ] Test order placement (paper trading mode)
  - [ ] Verify safety limits are enforced

---

## 🔄 DAY 6 - Evolution System Setup

### Design New Evolution Workflow

- [ ] **Step 1**: Create upgrade proposal template:
```python
# Example upgrade proposal format:
{
    "module_name": "joi_market.py",
    "upgrade_type": "feature",
    "description": "Add Bollinger Bands indicator",
    "risk_level": "low",
    "affected_files": ["modules/joi_market.py"],
    "rollback_plan": "Restore from backup",
    "test_steps": ["Test BB calculation", "Verify plotting"]
}
```

- [ ] **Step 2**: Implement safety validation:
  - [ ] Syntax checking
  - [ ] Import validation  
  - [ ] Security scanning
  - [ ] Resource estimation

- [ ] **Step 3**: Create test framework:
```python
# modules/joi_testing.py
class JoiTestRunner:
    def run_module_tests(self, module_name):
        # Run all tests for module
        pass
```

- [ ] **Step 4**: Test upgrade workflow:
```python
# In Joi interface
"Joi, propose an upgrade to add multi-timeframe analysis to your market module"
# Review proposal
"Joi, implement the approved upgrade"
# Verify upgrade success
```

---

## 📝 DAY 7 - Documentation & Wrap-up

### Create Documentation

- [ ] **User Guide**:
  - [ ] Getting started
  - [ ] Feature overview
  - [ ] Market intelligence guide
  - [ ] Voice commands
  - [ ] Troubleshooting

- [ ] **Developer Documentation**:
  - [ ] Architecture overview
  - [ ] Module descriptions
  - [ ] API documentation
  - [ ] Adding new modules
  - [ ] Upgrade system guide

### Final Testing

- [ ] Run full test suite
- [ ] Verify all critical bugs fixed
- [ ] Test on clean Python environment
- [ ] Create backup of stable version

### Prepare for Phase 2

- [ ] Review Phase 2 tasks
- [ ] Order any needed resources
- [ ] Set up development branch for Phase 2
- [ ] Create Phase 2 task breakdown

---

## 🎯 SUCCESS CRITERIA FOR WEEK 1

By end of Day 7, you should have:

✅ **Zero Critical Errors**
- Evolution system working without TypeErrors
- Database operations stable
- No circular import issues
- Login system functional
- IPC communication reliable

✅ **All Core Features Working**
- Multi-AI routing functioning
- Market intelligence operational  
- File management working
- Voice interaction active
- Project management accessible

✅ **System Stability**
- Can run for 24+ hours without crashes
- All API connections stable
- Memory usage under control
- Response times acceptable

✅ **Foundation for Self-Evolution**
- Upgrade proposal system working
- Safety validation implemented
- Test framework in place
- Code analysis functional

---

## 🆘 TROUBLESHOOTING GUIDE

### If Evolution System Still Failing:

1. Check Python version: `python --version` (should be 3.12+)
2. Check all imports: Look for missing dependencies
3. Check function calls: Search for outdated parameter names
4. Check logs: `tail -f logs/joi_evolution.log`

### If Database Issues Persist:

1. Check database file: `ls -lh joi_memory.db`
2. Test database: `sqlite3 joi_memory.db ".tables"`
3. Check permissions: Should be read/write
4. Consider database rebuild if corrupted

### If IPC Not Working:

1. Check Electron version: `npm list electron`
2. Check console: Open DevTools in Electron (Ctrl+Shift+I)
3. Check Flask logs: Should show incoming IPC requests
4. Test with simple message first

### If APIs Failing:

1. Check API keys: Verify they're loaded correctly
2. Check rate limits: May need to wait or upgrade plan
3. Check network: Test API directly with curl
4. Check API status pages

---

## 📞 COMMANDS FOR TESTING

### Quick System Health Check:
```bash
cd "C:\Users\user\Desktop\AI Joi"
python joi_companion.py --health-check
```

### Test Specific Module:
```bash
python -m modules.joi_market test
python -m modules.joi_evolution test
python -m modules.joi_llm test
```

### Run All Tests:
```bash
python -m pytest tests/ -v --tb=short
```

### Check Logs:
```bash
# View today's logs
type logs\joi_%date:~-4,4%-%date:~-10,2%-%date:~-7,2%.log

# Watch logs in real-time (PowerShell)
Get-Content logs\joi_latest.log -Wait
```

---

## 💡 TIPS FOR SUCCESS

1. **Work Incrementally** - Fix one thing at a time, test thoroughly
2. **Backup Before Changes** - Always backup before major modifications  
3. **Use Git** - Commit after each successful fix
4. **Read Error Messages** - They usually tell you exactly what's wrong
5. **Test Immediately** - Don't pile up changes without testing
6. **Document As You Go** - Note what you changed and why
7. **Ask for Help** - If stuck for >30 minutes, seek assistance

---

## 📅 DAILY STANDUP FORMAT

Each day, review:
1. **What did I complete yesterday?**
2. **What am I working on today?**
3. **What blockers do I have?**
4. **Do I need help with anything?**

---

## 🎉 CELEBRATION CHECKPOINTS

- [ ] 🎊 First critical bug fixed
- [ ] 🎊 All modules loading successfully
- [ ] 🎊 First successful self-upgrade
- [ ] 🎊 24 hours of stable operation
- [ ] 🎊 All tests passing
- [ ] 🎊 Week 1 complete!

**You've got this! Let's make Joi super! 💪**

