#!/usr/bin/env python3
"""
scripts/check_system_health.py

Conflict Resolver Audit: Parse joi_router.py and joi_llm.py for system-prompt text,
then use a fast-tier LLM to compare for contradictions (e.g. "Agent A: be concise"
vs "Agent B: be verbose"). Outputs a Conflict Report for pruning redundant instructions.

Usage:
  python scripts/check_system_health.py
  # Writes data/conflict_report.txt and prints to stdout.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
CONFLICT_REPORT_PATH = DATA_DIR / "conflict_report.txt"

ROUTER_PATH = BASE_DIR / "modules" / "joi_router.py"
LLM_PATH = BASE_DIR / "modules" / "joi_llm.py"


def extract_triple_quoted_blocks(content: str, label: str) -> list[tuple[str, str]]:
    """Extract ''' or \"\"\" blocks of at least min_len chars. Returns [(label, block), ...]."""
    blocks: list[tuple[str, str]] = []
    # Match """ ... """ or ''' ... '''
    pattern = re.compile(
        r'''(?s)("""|''')(.*?)\1''',
        re.DOTALL,
    )
    for m in pattern.finditer(content):
        block = (m.group(2) or "").strip()
        if len(block) >= 120:  # skip tiny strings
            blocks.append((label, block))
    return blocks


def collect_prompts_from_llm() -> list[tuple[str, str]]:
    """Collect system-prompt-like strings from joi_llm.py."""
    out: list[tuple[str, str]] = []
    if not LLM_PATH.exists():
        return out
    # Prefer runtime build so we get the actual prompt (with soul/identity)
    try:
        sys.path.insert(0, str(BASE_DIR))
        from modules.joi_llm import _build_system_prompt
        built = _build_system_prompt()
        if built and len(built) > 200:
            out.append(("joi_llm.SYSTEM_PROMPT (runtime)", built[:8000]))
            return out
    except Exception:
        pass
    # Fallback: extract by line range (identity_block in _build_system_prompt)
    text = LLM_PATH.read_text(encoding="utf-8")
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if "identity_block = f" in line and '"""' in line:
            start = i
            break
        if "CORE IDENTITY -- WHO YOU ARE" in line:
            start = i
            break
    if start is not None:
        end = start + 1
        while end < len(lines) and "return identity_block" not in lines[end]:
            end += 1
        block = "\n".join(lines[start:min(end, start + 200)])
        if len(block) > 200:
            out.append(("joi_llm.SYSTEM_PROMPT (source excerpt)", block[:8000]))
    return out


def collect_prompts_from_router() -> list[tuple[str, str]]:
    """Collect planning / constraint prompt strings from joi_router.py."""
    out: list[tuple[str, str]] = []
    if not ROUTER_PATH.exists():
        return out
    text = ROUTER_PATH.read_text(encoding="utf-8")
    # planning_prompt base string (multi-line in source)
    m = re.search(
        r'\[PLANNING\].*?Output ONLY a JSON array.*?Format:.*?\[.*?\]',
        text,
        re.DOTALL,
    )
    if m:
        base = m.group(0)[:1500]
        if len(base) > 50:
            out.append(("joi_router.planning_prompt (Architect)", base))
    # get_coding_constraints_block: look for MUST_FOLLOW text
    m2 = re.search(
        r'\[MUST_FOLLOW_CONSTRAINTS[^\]]+\].*?skill library',
        text,
    )
    if m2:
        out.append(("joi_router.get_coding_constraints_block", m2.group(0)[:600]))
    # Docstrings that describe behavior
    for m in re.finditer(r'def (planning_prompt|get_coding_constraints_block)\s*\([^)]*\)\s*->[^:]+:\s*"""([^"]{80,600})"""', text):
        out.append((f"joi_router.{m.group(1)} (docstring)", m.group(2)))
    return out


def build_document(blocks: list[tuple[str, str]]) -> str:
    """Turn (label, text) list into one document for the LLM."""
    lines = []
    for i, (label, text) in enumerate(blocks, 1):
        lines.append(f"--- BLOCK {i}: {label} ---")
        lines.append(text[:6000])  # cap per block
        lines.append("")
    return "\n".join(lines)


def call_fast_llm_for_conflict_report(prompt_doc: str) -> str:
    """Use a fast-tier LLM to compare prompts and return a conflict report."""
    if not prompt_doc.strip():
        return "No prompt blocks found to compare."
    try:
        from openai import OpenAI
    except ImportError:
        return "openai not installed; cannot run LLM conflict check. Install with: pip install openai"

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model = os.getenv("JOI_CONFLICT_CHECK_MODEL", "gpt-4o-mini")
    user_content = (
        "The following blocks are system prompts or instruction strings used in the same AI product (Joi). "
        "They are sent to different models or at different stages (e.g. main system prompt vs planning phase).\n\n"
        "Compare them for CONTRADICTIONS or CONFLICTS. Examples:\n"
        "- One block says 'be concise' and another says 'be verbose' or 'give detailed explanations'.\n"
        "- One says 'never ask questions' and another says 'ask clarifying questions'.\n"
        "- One says 'use tools' and another implies 'respond with text only'.\n\n"
        "Output a short CONFLICT REPORT (bullet list). For each conflict: which blocks, what the conflict is, "
        "and a one-line suggestion to resolve (e.g. 'Prune redundant instruction from Block 2'). "
        "If there are no clear contradictions, say 'No contradictions found.'\n\n"
        "PROMPT BLOCKS:\n\n" + prompt_doc
    )
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an expert at reviewing AI system prompts for consistency. Output only the conflict report, no preamble."},
                {"role": "user", "content": user_content[:120000]},
            ],
            max_tokens=1500,
        )
        if resp.choices and resp.choices[0].message.content:
            return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"LLM call failed: {e}"
    return "No response from LLM."


def main() -> int:
    blocks: list[tuple[str, str]] = []
    blocks.extend(collect_prompts_from_llm())
    blocks.extend(collect_prompts_from_router())
    if not blocks:
        report = "No system-prompt blocks could be extracted from joi_llm.py and joi_router.py. Check paths."
    else:
        doc = build_document(blocks)
        report = call_fast_llm_for_conflict_report(doc)
    CONFLICT_REPORT_PATH.write_text(report, encoding="utf-8")
    print("Conflict Report (saved to data/conflict_report.txt):")
    print("=" * 60)
    print(report)
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
