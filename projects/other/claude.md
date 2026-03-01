\# CLAUDE.md — Joi Development Guidelines



\## 🌟 Project North Star

Transition Joi to a fully autonomous, agentic system capable of self-healing and code generation.



\## 🛠 Build \& Run Commands

\- Start Flask Server: `python joi\_companion.py`

\- Run Market Module: `python modules/joi\_market.py`

\- Check Evolution Logs: `cat evolution\_log.json`



\## 📝 Coding Standards

\- \*\*Errors First:\*\* Always check `logs/system.log` before proposing a fix.

\- \*\*Atomic Patches:\*\* Use the `joi\_patching.py` logic to propose changes before applying them.

\- \*\*Memory Preservation:\*\* Never overwrite `joi\_memory.db` or `learned\_patterns.json` without a backup.



\## 🚀 Super AI Directives

1\. Use `joi\_evolution.py` to identify the "propose\_upgrade" TypeError and fix it first.

2\. Automate the "Market Watcher" to alert the UI when XRP hits the buy/sell ladders.

