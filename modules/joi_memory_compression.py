"""
modules/joi_memory_compression.py

Joi v4.0 — Memory Compression Intelligence (Upgrade III)
=========================================================
Prevents context bloat while preserving semantic integrity.

Hierarchical Memory Tiers:
  ACTIVE    — hot working memory (immediate conversation context)
  EPISODIC  — recent multi-turn memories (last session batch)
  LONG_TERM — vector-accessed long-term memory
  ARCHIVE   — compressed historical nodes (never deleted, summarized)

Features:
  - Time-weighted decay function (exponential, configurable half-life)
  - Epistemic certainty scoring per memory entry (0.0–1.0)
  - Compression: clusters of episodic memory → single compressed MemoryNode
  - Context Budget Optimizer: ranks by relevance × certainty × recency
  - Memory health telemetry endpoint

This module is additive — joi_memory.py is NOT modified.
It exposes optimize_context_budget() which joi_memory.py can call
via try/except at prompt assembly time.
"""

import json
import math
import time
import hashlib
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

BASE_DIR   = Path(__file__).resolve().parent.parent
DATA_DIR   = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

TIERS_PATH  = DATA_DIR / "memory_tiers.json"
ARCHIVE_PATH = DATA_DIR / "memory_archive.json"

# Time-decay half-lives per tier (hours)
HALFLIFE_ACTIVE   = 1.0
HALFLIFE_EPISODIC = 24.0
HALFLIFE_LONGTERM = 168.0   # 7 days
HALFLIFE_ARCHIVE  = 8760.0  # 1 year (essentially permanent)

# Token estimation: rough chars-to-tokens ratio
CHARS_PER_TOKEN = 4
DEFAULT_BUDGET_TOKENS = 4000  # default context budget for memory selection


class MemoryTier(str, Enum):
    ACTIVE    = "ACTIVE"
    EPISODIC  = "EPISODIC"
    LONG_TERM = "LONG_TERM"
    ARCHIVE   = "ARCHIVE"


@dataclass
class MemoryNode:
    """A single memory entry with tier, certainty, and decay metadata."""
    id:                   str
    content:              str
    tier:                 MemoryTier = MemoryTier.EPISODIC
    confidence:           float = 0.7          # 0.0–1.0 source confidence
    epistemic_certainty:  float = 0.7          # 0.0–1.0 how certain we are this is true
    source_type:          str   = "retrieved"  # retrieved | inferred | speculative
    created_at:           str   = ""
    last_accessed:        str   = ""
    access_count:         int   = 0
    compressed_from:      List[str] = field(default_factory=list)  # source node IDs
    tags:                 List[str] = field(default_factory=list)

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now(timezone.utc).isoformat()
        if not self.last_accessed:
            self.last_accessed = self.created_at


# ── Decay Functions ────────────────────────────────────────────────────────────

def _tier_halflife(tier: MemoryTier) -> float:
    return {
        MemoryTier.ACTIVE:    HALFLIFE_ACTIVE,
        MemoryTier.EPISODIC:  HALFLIFE_EPISODIC,
        MemoryTier.LONG_TERM: HALFLIFE_LONGTERM,
        MemoryTier.ARCHIVE:   HALFLIFE_ARCHIVE,
    }.get(tier, HALFLIFE_EPISODIC)


def compute_recency_score(node: MemoryNode) -> float:
    """
    Exponential time-decay recency score (0.0–1.0).
    More recent = higher score. Tier half-life controls decay rate.
    """
    try:
        last = datetime.fromisoformat(node.last_accessed)
        if last.tzinfo is None:
            last = last.replace(tzinfo=timezone.utc)
        age_hours = (datetime.now(timezone.utc) - last).total_seconds() / 3600
        halflife = _tier_halflife(node.tier)
        return math.exp(-0.693 * age_hours / halflife)
    except Exception:
        return 0.5


def compute_relevance_score(node: MemoryNode, query: str) -> float:
    """
    Simple keyword overlap relevance score (0.0–1.0).
    No embedding required — suitable for fast pre-filtering.
    """
    if not query or not node.content:
        return 0.0
    query_tokens = set(query.lower().split())
    content_tokens = set(node.content.lower().split())
    if not query_tokens:
        return 0.0
    overlap = len(query_tokens & content_tokens)
    return min(1.0, overlap / len(query_tokens))


def composite_score(node: MemoryNode, query: str = "") -> float:
    """relevance × epistemic_certainty × recency_score"""
    rec = compute_recency_score(node)
    rel = compute_relevance_score(node, query) if query else 0.5
    cert = node.epistemic_certainty
    return rec * cert * (rel if rel > 0 else 0.5)


# ── Compression ────────────────────────────────────────────────────────────────

def _generate_node_id(content: str) -> str:
    return "mem_" + hashlib.md5(content.encode("utf-8")).hexdigest()[:12]


def compress_episodic_cluster(nodes: List[MemoryNode], summary_hint: str = "") -> MemoryNode:
    """
    Merge a cluster of episodic nodes into one ARCHIVE MemoryNode.

    Preserves:
      - Summary of all content (concatenated, deduplicated)
      - Source references (compressed_from IDs)
      - Lower epistemic certainty (conservative — compressed info is less certain)
      - Original creation date (oldest in cluster)
    """
    if not nodes:
        raise ValueError("Cannot compress empty cluster")

    contents = []
    seen = set()
    for n in nodes:
        snippet = n.content[:200].strip()
        if snippet not in seen:
            contents.append(snippet)
            seen.add(snippet)

    combined = " | ".join(contents)
    summary = summary_hint or f"[Compressed {len(nodes)} memories] {combined[:400]}"

    oldest_created = min((n.created_at for n in nodes if n.created_at), default="")
    avg_certainty = sum(n.epistemic_certainty for n in nodes) / len(nodes)
    # Compression slightly lowers certainty (information loss)
    compressed_certainty = max(0.2, avg_certainty * 0.85)

    compressed = MemoryNode(
        id=_generate_node_id(summary),
        content=summary,
        tier=MemoryTier.ARCHIVE,
        confidence=avg_certainty,
        epistemic_certainty=compressed_certainty,
        source_type="retrieved",
        created_at=oldest_created,
        last_accessed=datetime.now(timezone.utc).isoformat(),
        compressed_from=[n.id for n in nodes],
        tags=["compressed", f"cluster_{len(nodes)}"],
    )
    return compressed


# ── Context Budget Optimizer ───────────────────────────────────────────────────

def estimate_token_cost(nodes: List[MemoryNode]) -> int:
    """Estimate total tokens for a list of memory nodes."""
    total_chars = sum(len(n.content) for n in nodes)
    return max(1, total_chars // CHARS_PER_TOKEN)


def optimize_context_budget(
    query: str,
    available_nodes: List[MemoryNode],
    token_budget: int = DEFAULT_BUDGET_TOKENS,
) -> Tuple[List[MemoryNode], Dict]:
    """
    Select the best memory nodes within a token budget.

    Ranking: composite_score (relevance × certainty × recency)
    Strategy:
      1. Score all nodes
      2. Sort descending
      3. Greedily add until budget exhausted
      4. Return selected nodes + budget report

    This replaces blind 1M context escalation for cases where
    memory compression + selection can solve the problem.
    """
    scored = []
    for node in available_nodes:
        score = composite_score(node, query)
        tokens = max(1, len(node.content) // CHARS_PER_TOKEN)
        scored.append((score, tokens, node))

    scored.sort(key=lambda x: -x[0])  # highest score first

    selected = []
    used_tokens = 0
    for score, tokens, node in scored:
        if used_tokens + tokens <= token_budget:
            selected.append(node)
            used_tokens += tokens
        # Stop if over budget and we have something
        if used_tokens >= token_budget * 0.95 and selected:
            break

    report = {
        "budget_tokens": token_budget,
        "used_tokens": used_tokens,
        "selected_nodes": len(selected),
        "available_nodes": len(available_nodes),
        "coverage_pct": round(100 * used_tokens / token_budget, 1) if token_budget else 0,
    }
    return selected, report


# ── MemoryCompressor ───────────────────────────────────────────────────────────

class MemoryCompressor:
    """
    Main interface to compression intelligence.

    Persists tier metadata to TIERS_PATH (data/memory_tiers.json).
    Archive to ARCHIVE_PATH (data/memory_archive.json).
    """

    def __init__(self):
        self._nodes: Dict[str, MemoryNode] = {}
        self._load()

    def _load(self):
        if TIERS_PATH.exists():
            try:
                raw = json.loads(TIERS_PATH.read_text(encoding="utf-8"))
                for nid, ndata in raw.items():
                    try:
                        ndata["tier"] = MemoryTier(ndata.get("tier", "EPISODIC"))
                        self._nodes[nid] = MemoryNode(**ndata)
                    except Exception:
                        pass
            except Exception:
                pass

    def _save(self):
        out = {}
        for nid, node in self._nodes.items():
            d = asdict(node)
            d["tier"] = node.tier.value
            out[nid] = d
        TIERS_PATH.write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")

    def add_node(self, node: MemoryNode):
        """Register or update a memory node."""
        self._nodes[node.id] = node
        self._save()

    def promote_tier(self, node_id: str, new_tier: MemoryTier):
        """Move a node to a different tier."""
        if node_id in self._nodes:
            self._nodes[node_id].tier = new_tier
            self._save()

    def compress_old_episodic(self, max_age_hours: float = 48.0) -> Optional[MemoryNode]:
        """
        Find episodic nodes older than max_age_hours and compress them into one archive node.
        Returns the compressed node (or None if nothing to compress).
        """
        cutoff = (datetime.now(timezone.utc) - timedelta(hours=max_age_hours)).isoformat()
        old_nodes = [
            n for n in self._nodes.values()
            if n.tier == MemoryTier.EPISODIC and n.created_at < cutoff
        ]
        if len(old_nodes) < 2:
            return None

        compressed = compress_episodic_cluster(old_nodes)

        # Archive the compressed node
        archive_data = {}
        if ARCHIVE_PATH.exists():
            try:
                archive_data = json.loads(ARCHIVE_PATH.read_text(encoding="utf-8"))
            except Exception:
                pass
        d = asdict(compressed)
        d["tier"] = compressed.tier.value
        archive_data[compressed.id] = d
        ARCHIVE_PATH.write_text(json.dumps(archive_data, indent=2, default=str), encoding="utf-8")

        # Remove originals from active tier store (they're archived)
        for n in old_nodes:
            self._nodes.pop(n.id, None)
        self._nodes[compressed.id] = compressed
        self._save()
        return compressed

    def get_health_telemetry(self) -> Dict[str, Any]:
        """Memory health metrics."""
        all_nodes = list(self._nodes.values())
        compressed = [n for n in all_nodes if n.compressed_from]
        stale_cutoff = (datetime.now(timezone.utc) - timedelta(hours=72)).isoformat()
        stale = [n for n in all_nodes if n.last_accessed < stale_cutoff]

        # Redundancy: nodes with very similar short content
        seen_prefixes = {}
        redundant = 0
        for n in all_nodes:
            prefix = n.content[:50].strip().lower()
            if prefix in seen_prefixes:
                redundant += 1
            else:
                seen_prefixes[prefix] = n.id

        total = len(all_nodes)
        compressed_ratio = round(len(compressed) / max(1, total), 3)

        return {
            "total_memory_nodes": total,
            "compressed_nodes": len(compressed),
            "compressed_ratio": compressed_ratio,
            "stale_node_count": len(stale),
            "redundancy_score": round(redundant / max(1, total), 3),
            "tier_breakdown": {
                tier.value: sum(1 for n in all_nodes if n.tier == tier)
                for tier in MemoryTier
            },
        }

    def optimize_for_query(
        self, query: str, token_budget: int = DEFAULT_BUDGET_TOKENS
    ) -> Tuple[List[MemoryNode], Dict]:
        """Select best nodes within budget for a given query."""
        all_nodes = list(self._nodes.values())
        return optimize_context_budget(query, all_nodes, token_budget)


# ── Singleton ──────────────────────────────────────────────────────────────────
_compressor: Optional[MemoryCompressor] = None


def get_memory_compressor() -> MemoryCompressor:
    global _compressor
    if _compressor is None:
        _compressor = MemoryCompressor()
    return _compressor


# ── Tool Functions ─────────────────────────────────────────────────────────────

def get_memory_health(**kwargs) -> Dict:
    """Get memory compression health telemetry."""
    return {"ok": True, **get_memory_compressor().get_health_telemetry()}


def compress_memory_archive(**kwargs) -> Dict:
    """Trigger compression of old episodic memories into archive nodes."""
    hours = float(kwargs.get("max_age_hours", 48.0))
    node = get_memory_compressor().compress_old_episodic(hours)
    if node:
        return {"ok": True, "compressed": True, "archive_node_id": node.id,
                "sources_compressed": len(node.compressed_from)}
    return {"ok": True, "compressed": False, "message": "No episodic memories old enough to compress."}


# ── Tool + Route Registration ──────────────────────────────────────────────────
try:
    import joi_companion
    joi_companion.register_tool(
        {"type": "function", "function": {
            "name": "get_memory_health",
            "description": (
                "Get Joi's memory compression telemetry: total nodes, compressed ratio, "
                "stale count, redundancy score, and tier breakdown."
            ),
            "parameters": {"type": "object", "properties": {}, "required": []}
        }},
        get_memory_health
    )
    joi_companion.register_tool(
        {"type": "function", "function": {
            "name": "compress_memory_archive",
            "description": "Compress old episodic memories into archive nodes to free context space.",
            "parameters": {"type": "object", "properties": {
                "max_age_hours": {"type": "number",
                                   "description": "Archive episodic nodes older than this many hours (default 48)."}
            }, "required": []}
        }},
        compress_memory_archive
    )
    print("  [OK] joi_memory_compression loaded (MemoryCompressor active)")
except Exception as _e:
    print(f"  [WARN] joi_memory_compression: tool registration skipped ({_e})")

try:
    import joi_companion

    def _mc_route():
        from flask import jsonify
        return jsonify(get_memory_health())

    joi_companion.register_route(
        "/memory/compression/status", ["GET"], _mc_route, "memory_compression_route"
    )
except Exception:
    pass
