# JOI.md — System Laws

## Environment
- Python: venv311 (C:\Users\user\Desktop\AI Joi\venv311\Scripts\python.exe)
- System Python fallback: C:\Users\user\AppData\Local\Programs\Python\Python311\python.exe
- Flask port: 5001
- Project root: C:\Users\user\Desktop\AI Joi

## Critical Rules
- NEVER write Python files directly to modules/. Always stage to staging/ first.
- Run `python -m py_compile <file>` after every write. Exit code must be 0.
- Required imports in every orchestrator-generated module: re, ast, json, os, threading
- Staging dir: staging/ (must exist — create if missing)
- All git operations use array-format subprocess (no shell=True with interpolation)

## Active Models (March 2026)
- Architect: gpt-5 (fallback: gemini-2.5-pro)
- Coder: gpt-5 (fallback: gpt-5-mini)
- Validator: o4-mini
- Auto-approve plans with ≤3 subtasks

## Port 5001 Safety
- Before running a new Flask process, check: netstat -ano | grep :5001
- Kill stale processes before restart
