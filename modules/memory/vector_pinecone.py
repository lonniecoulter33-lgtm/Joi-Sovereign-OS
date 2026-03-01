"""
Pinecone Vector Store -- optional cloud backend.
Enable via VECTOR_BACKEND=pinecone + PINECONE_API_KEY.
Falls back to Chroma on failure (never crashes).
"""

import os
import time
from datetime import datetime
from typing import Any, Dict, List, Optional

from modules.memory.vector_store_base import (
    VectorStoreBase, MemoryChunk, QueryResult, StoreStats,
)

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "").strip()
PINECONE_INDEX = os.getenv("PINECONE_INDEX", "joi-memory").strip()
PINECONE_REGION = os.getenv("PINECONE_REGION", "").strip()
PINECONE_HOST = os.getenv("PINECONE_HOST", "").strip()
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")


def _get_openai_embedding(texts: List[str]) -> List[List[float]]:
    """Get embeddings via OpenAI API."""
    from openai import OpenAI
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        return []
    client = OpenAI(api_key=api_key)
    resp = client.embeddings.create(model=EMBEDDING_MODEL, input=texts)
    return [d.embedding for d in resp.data]


class PineconeVectorStore(VectorStoreBase):

    def __init__(self):
        self._index = None
        self._last_write_time: Optional[str] = None
        self._last_write_ok: bool = True
        self._last_error: Optional[str] = None
        self._init_client()

    def _init_client(self):
        if not PINECONE_API_KEY:
            self._last_error = "PINECONE_API_KEY not set"
            print("  [VECTOR] Pinecone skipped -- no API key")
            return
        try:
            from pinecone import Pinecone
            pc = Pinecone(api_key=PINECONE_API_KEY)
            if PINECONE_HOST:
                self._index = pc.Index(host=PINECONE_HOST)
            else:
                self._index = pc.Index(PINECONE_INDEX)
            stats = self._index.describe_index_stats()
            print(f"  [VECTOR] Pinecone OK -- index '{PINECONE_INDEX}', "
                  f"{stats.total_vector_count} vectors")
        except Exception as e:
            self._last_error = str(e)
            print(f"  [VECTOR] Pinecone init FAILED: {e}")

    # ── Interface ────────────────────────────────────────────────────────

    def upsert(self, chunks: List[MemoryChunk]) -> bool:
        if not self._index:
            self._last_write_ok = False
            self._last_error = "Pinecone not initialized"
            return False
        try:
            texts = [c.text for c in chunks]
            embeddings = _get_openai_embedding(texts)
            if not embeddings:
                self._last_write_ok = False
                self._last_error = "Embedding generation failed"
                return False

            vectors = []
            for i, c in enumerate(chunks):
                meta = dict(c.metadata)
                meta["text"] = c.text[:1000]  # Pinecone metadata limit
                vectors.append({
                    "id": c.id,
                    "values": embeddings[i],
                    "metadata": meta,
                })
            self._index.upsert(vectors=vectors)
            self._last_write_time = datetime.now().isoformat()
            self._last_write_ok = True
            self._last_error = None
            for c in chunks:
                mtype = c.metadata.get("type", "?")
                print(f"  MEMORY_WRITE ok backend=pinecone id={c.id} type={mtype}")
            return True
        except Exception as e:
            self._last_write_ok = False
            self._last_error = str(e)
            print(f"  MEMORY_WRITE fail backend=pinecone reason={e}")
            return False

    def query(
        self,
        text: str,
        top_k: int = 5,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[QueryResult]:
        if not self._index:
            return []
        try:
            embeddings = _get_openai_embedding([text])
            if not embeddings:
                return []
            kwargs: Dict[str, Any] = {
                "vector": embeddings[0],
                "top_k": top_k,
                "include_metadata": True,
            }
            if filters:
                kwargs["filter"] = filters
            results = self._index.query(**kwargs)
            out = []
            for match in results.get("matches", []):
                meta = match.get("metadata", {})
                out.append(QueryResult(
                    id=match["id"],
                    text=meta.pop("text", ""),
                    score=match.get("score", 0.0),
                    metadata=meta,
                ))
            return out
        except Exception as e:
            print(f"  [VECTOR] Pinecone query error: {e}")
            return []

    def delete(
        self,
        ids: Optional[List[str]] = None,
        filters: Optional[Dict[str, Any]] = None,
    ) -> int:
        if not self._index:
            return 0
        try:
            if ids:
                self._index.delete(ids=ids)
                return len(ids)
            elif filters:
                self._index.delete(filter=filters)
                return -1  # Pinecone doesn't return count
            return 0
        except Exception as e:
            print(f"  [VECTOR] Pinecone delete error: {e}")
            return 0

    def healthcheck(self) -> bool:
        if not self._index:
            return False
        try:
            self._index.describe_index_stats()
            return True
        except Exception:
            return False

    def stats(self) -> StoreStats:
        count = 0
        if self._index:
            try:
                s = self._index.describe_index_stats()
                count = s.total_vector_count
            except Exception:
                pass
        return StoreStats(
            backend="pinecone",
            collection=PINECONE_INDEX,
            vector_count=count,
            last_write_time=self._last_write_time,
            last_write_ok=self._last_write_ok,
            last_error=self._last_error,
            embedding_model=EMBEDDING_MODEL,
            extra={"region": PINECONE_REGION, "host": PINECONE_HOST},
        )
