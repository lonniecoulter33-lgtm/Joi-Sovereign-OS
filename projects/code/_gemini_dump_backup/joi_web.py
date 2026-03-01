from __future__ import annotations
from typing import Any, Dict
from joi_registry import register_tool

def _tool_web_search(args: Dict[str, Any]) -> Dict[str, Any]:
    # Placeholder: implement with your preferred search API.
    q = (args.get("query") or "").strip()
    if not q:
        return {"ok": False, "error": "query required"}
    return {"ok": False, "error": "Web search not configured. Add a search API key and implement joi_web.py."}

register_tool({
  "type":"function",
  "function":{
    "name":"web_search",
    "description":"(Placeholder) Web search. Requires configuration.",
    "parameters":{"type":"object","properties":{"query":{"type":"string"}}, "required":["query"]}
  }
}, _tool_web_search)
