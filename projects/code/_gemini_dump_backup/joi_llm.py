from __future__ import annotations
import os
import json
import time
from typing import Any, Dict, List, Optional, Tuple

import requests

SYSTEM_PROMPT = """You are Joi, an AI companion and developer assistant.
You can chat warmly, but you are also capable of using tools when helpful.
Rules:
- Be direct and practical.
- When you need to read/write project files, use the filesystem tools.
- For destructive operations, stage first and only apply when confirm=true.
- If a tool fails, explain the error and propose a fix.
"""

def _post(url: str, headers: Dict[str, str], payload: Dict[str, Any], timeout: int = 120) -> Dict[str, Any]:
    r = requests.post(url, headers=headers, json=payload, timeout=timeout)
    r.raise_for_status()
    return r.json()

def _provider_cfg():
    chat_provider = os.getenv("JOI_CHAT_PROVIDER", "local").lower()
    tool_provider = os.getenv("JOI_TOOL_PROVIDER", "openai").lower()

    local_base = os.getenv("JOI_LOCAL_BASE_URL", "http://localhost:1234/v1").rstrip("/")
    local_model = os.getenv("JOI_LOCAL_MODEL", "mistral")

    openai_key = os.getenv("OPENAI_API_KEY", "")
    openai_model = os.getenv("JOI_MODEL", "gpt-4o-mini")
    openai_tool_model = os.getenv("JOI_OPENAI_TOOL_MODEL", openai_model)

    return {
        "chat_provider": chat_provider,
        "tool_provider": tool_provider,
        "local_base": local_base,
        "local_model": local_model,
        "openai_key": openai_key,
        "openai_model": openai_model,
        "openai_tool_model": openai_tool_model,
    }

def _call_openai(messages: List[dict], model: str, tools: Optional[List[dict]] = None) -> Dict[str, Any]:
    cfg = _provider_cfg()
    if not cfg["openai_key"]:
        raise RuntimeError("OPENAI_API_KEY is missing")
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {cfg['openai_key']}", "Content-Type": "application/json"}
    payload: Dict[str, Any] = {"model": model, "messages": messages}
    if tools:
        payload["tools"] = tools
        payload["tool_choice"] = "auto"
    # modest defaults
    payload["temperature"] = 0.7
    payload["max_tokens"] = int(os.getenv("JOI_MAX_OUTPUT_TOKENS", "800"))
    return _post(url, headers, payload, timeout=180)

def _call_local(messages: List[dict], model: str, tools: Optional[List[dict]] = None) -> Dict[str, Any]:
    cfg = _provider_cfg()
    url = f"{cfg['local_base']}/chat/completions"
    headers = {"Content-Type": "application/json"}
    payload: Dict[str, Any] = {"model": model, "messages": messages, "temperature": 0.7}
    # Most local servers ignore tools; include anyway.
    if tools:
        payload["tools"] = tools
        payload["tool_choice"] = "auto"
    return _post(url, headers, payload, timeout=180)

def _extract_choice(resp: Dict[str, Any]) -> Dict[str, Any]:
    # OpenAI-compatible
    try:
        return resp["choices"][0]["message"]
    except Exception:
        raise RuntimeError(f"Unexpected response format: {resp}")

def run_conversation(messages: List[dict], tools: List[dict], tool_executors: Dict[str, Any]) -> str:
    """
    Runs a conversation with optional tool-calling. Works with OpenAI API or a local OpenAI-compatible server.
    """
    cfg = _provider_cfg()
    chat_provider = cfg["chat_provider"]
    model = cfg["local_model"] if chat_provider == "local" else cfg["openai_model"]

    # Decide which provider to use for tool-calling.
    # Many local models don't do tool_calls reliably; if tool_provider=openai and OPENAI_API_KEY is set,
    # we can run tool steps via OpenAI even if normal chat uses local.
    tool_provider = cfg["tool_provider"]

    def call(messages, with_tools: bool):
        if with_tools and tool_provider == "openai" and cfg["openai_key"]:
            return _call_openai(messages, cfg["openai_tool_model"], tools=tools)
        if chat_provider == "local":
            return _call_local(messages, model, tools=tools if with_tools else None)
        return _call_openai(messages, model, tools=tools if with_tools else None)

    # tool loop
    for _ in range(6):
        resp = call(messages, with_tools=True)
        msg = _extract_choice(resp)

        tool_calls = msg.get("tool_calls") or []
        if not tool_calls:
            return (msg.get("content") or "").strip()

        # Execute tools
        for tc in tool_calls:
            fn = (tc.get("function") or {}).get("name")
            arg_str = (tc.get("function") or {}).get("arguments") or "{}"
            try:
                args = json.loads(arg_str) if isinstance(arg_str, str) else (arg_str or {})
            except Exception:
                args = {}
            executor = tool_executors.get(fn)
            if not executor:
                result = {"ok": False, "error": f"Unknown tool: {fn}"}
            else:
                try:
                    result = executor(args)
                except Exception as e:
                    result = {"ok": False, "error": f"{type(e).__name__}: {e}"}

            messages.append({
                "role": "tool",
                "tool_call_id": tc.get("id", ""),
                "name": fn,
                "content": json.dumps(result, ensure_ascii=False),
            })

        # Continue loop with updated messages (assistant tool-call message included)
        messages.append({"role": "assistant", "content": "Tools executed. Continue."})

    return "I ran multiple tool steps but did not reach a final answer. Try again with a simpler request."
