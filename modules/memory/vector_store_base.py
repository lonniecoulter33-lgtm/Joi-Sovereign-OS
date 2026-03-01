"""
Vector Store Interface
======================
Abstract base for all vector backends (Chroma, Pinecone, etc).
Every backend must implement these methods.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class MemoryChunk:
    """A single piece of memory to store."""
    id: str
    text: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    # metadata should include: type (fact/decision/summary/message), timestamp, source


@dataclass
class QueryResult:
    """A single search result."""
    id: str
    text: str
    score: float
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StoreStats:
    """Health/status snapshot of a vector store."""
    backend: str
    collection: str
    vector_count: int
    last_write_time: Optional[str] = None
    last_write_ok: bool = True
    last_error: Optional[str] = None
    embedding_model: str = ""
    extra: Dict[str, Any] = field(default_factory=dict)


class VectorStoreBase(ABC):
    """Abstract vector store interface."""

    @abstractmethod
    def upsert(self, chunks: List[MemoryChunk]) -> bool:
        """Insert or update memory chunks. Returns True on success."""
        ...

    @abstractmethod
    def query(
        self,
        text: str,
        top_k: int = 5,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[QueryResult]:
        """Semantic search. Returns top_k results sorted by relevance."""
        ...

    @abstractmethod
    def delete(
        self,
        ids: Optional[List[str]] = None,
        filters: Optional[Dict[str, Any]] = None,
    ) -> int:
        """Delete by IDs or metadata filters. Returns count deleted."""
        ...

    @abstractmethod
    def healthcheck(self) -> bool:
        """Returns True if the backend is reachable and functional."""
        ...

    @abstractmethod
    def stats(self) -> StoreStats:
        """Return current status/stats snapshot."""
        ...
