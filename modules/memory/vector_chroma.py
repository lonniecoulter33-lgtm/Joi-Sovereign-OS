"""
ChromaDB Vector Store -- local persistent backend.
Storage: ./data/chroma/
"""

import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from modules.memory.vector_store_base import (
    VectorStoreBase, MemoryChunk, QueryResult, StoreStats,
)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
CHROMA_DIR = BASE_DIR / "data" / "chroma"
CHROMA_DIR.mkdir(parents=True, exist_ok=True)

COLLECTION_NAME = os.getenv("CHROMA_COLLECTION", "joi_memory")


def _get_embedder():
    """Return a local ONNX embedding function for Chroma (no API key needed)."""
    try:
        from chromadb.utils.embedding_functions import ONNXMiniLM_L6_V2
        return ONNXMiniLM_L6_V2()
    except Exception as e:
        print(f"  [VECTOR] ONNX embedder failed, using Chroma default: {e}")
    return None


class ChromaVectorStore(VectorStoreBase):

    def __init__(self):
        self._client = None
        self._collection = None
        self._last_write_time: Optional[str] = None
        self._last_write_ok: bool = True
        self._last_error: Optional[str] = None
        self._embedding_model = "chroma-default (all-MiniLM-L6-v2)"
        self._init_client()

    def _init_client(self):
        # Guard: detect google import shadowing early (prevents cryptic errors)
        try:
            from google.protobuf import __version__ as _pb_ver
        except ImportError as _shadow_err:
            import google as _g
            _gf = getattr(_g, '__file__', None)
            print(f"  [VECTOR] FATAL: 'from google.protobuf import ...' failed.\n"
                  f"           'google' resolves to: {_gf}\n"
                  f"           A local file/folder named 'google' is shadowing the real package.\n"
                  f"           Fix: rename that file to 'google_local.py' (or similar).")
            self._last_error = f"google.protobuf shadowed by {_gf}"
            return
        try:
            self._open_chroma()
        except Exception as e:
            err_str = str(e)
            # Schema mismatch from older ChromaDB version -- nuke and recreate
            if "no such column" in err_str or "no such table" in err_str:
                print(f"  [VECTOR] Stale ChromaDB schema detected -- rebuilding database...")
                self._rebuild_chroma_db()
            else:
                print(f"  [VECTOR] Chroma init FAILED: {e}")
                self._last_error = err_str

    def _open_chroma(self):
        """Open ChromaDB and get/create the collection."""
        import chromadb
        self._client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        ef = _get_embedder()
        kwargs = {
            "name": COLLECTION_NAME,
            "metadata": {"hnsw:space": "cosine"},
        }
        if ef:
            kwargs["embedding_function"] = ef
            self._embedding_model = "onnx:all-MiniLM-L6-v2 (local)"
        # Migrate: if collection exists with wrong distance metric, recreate it
        try:
            existing = self._client.get_collection(name=COLLECTION_NAME)
            meta = existing.metadata or {}
            if meta.get("hnsw:space") != "cosine":
                old_count = existing.count()
                print(f"  [VECTOR] Migrating collection from '{meta.get('hnsw:space', 'l2')}' to 'cosine' ({old_count} vectors will be re-indexed)")
                self._client.delete_collection(name=COLLECTION_NAME)
        except Exception:
            pass  # Collection doesn't exist yet -- fine
        self._collection = self._client.get_or_create_collection(**kwargs)
        count = self._collection.count()
        print(f"  [VECTOR] Chroma OK -- collection '{COLLECTION_NAME}', {count} vectors, "
              f"dir={CHROMA_DIR}")

    def _rebuild_chroma_db(self):
        """Delete stale ChromaDB files and create a fresh database."""
        import shutil
        self._client = None
        self._collection = None
        try:
            # Remove all files in chroma dir
            for item in CHROMA_DIR.iterdir():
                if item.is_file():
                    item.unlink()
                elif item.is_dir():
                    shutil.rmtree(item)
            print(f"  [VECTOR] Old database removed. Creating fresh database...")
            self._open_chroma()
        except Exception as e:
            print(f"  [VECTOR] Rebuild FAILED: {e}")
            self._last_error = f"Rebuild failed: {e}"

    # ── Interface ────────────────────────────────────────────────────────

    def upsert(self, chunks: List[MemoryChunk]) -> bool:
        if not self._collection:
            self._last_write_ok = False
            self._last_error = "Chroma not initialized"
            return False
        try:
            ids = [c.id for c in chunks]
            documents = [c.text for c in chunks]
            metadatas = [c.metadata for c in chunks]
            self._collection.upsert(ids=ids, documents=documents, metadatas=metadatas)
            self._last_write_time = datetime.now().isoformat()
            self._last_write_ok = True
            self._last_error = None
            for c in chunks:
                mtype = c.metadata.get("type", "?")
                print(f"  MEMORY_WRITE ok backend=chroma id={c.id} type={mtype}")
            return True
        except Exception as e:
            self._last_write_ok = False
            self._last_error = str(e)
            print(f"  MEMORY_WRITE fail backend=chroma reason={e}")
            return False

    def query(
        self,
        text: str,
        top_k: int = 5,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[QueryResult]:
        if not self._collection:
            return []
        try:
            kwargs: Dict[str, Any] = {
                "query_texts": [text],
                "n_results": min(top_k, self._collection.count() or 1),
            }
            if filters:
                kwargs["where"] = filters
            results = self._collection.query(**kwargs)
            out = []
            if results and results["ids"] and results["ids"][0]:
                for i, rid in enumerate(results["ids"][0]):
                    out.append(QueryResult(
                        id=rid,
                        text=results["documents"][0][i] if results["documents"] else "",
                        score=1.0 - (results["distances"][0][i] if results["distances"] else 0),
                        metadata=results["metadatas"][0][i] if results["metadatas"] else {},
                    ))
            return out
        except Exception as e:
            print(f"  [VECTOR] Chroma query error: {e}")
            return []

    def delete(
        self,
        ids: Optional[List[str]] = None,
        filters: Optional[Dict[str, Any]] = None,
    ) -> int:
        if not self._collection:
            return 0
        try:
            before = self._collection.count()
            if ids:
                self._collection.delete(ids=ids)
            elif filters:
                self._collection.delete(where=filters)
            after = self._collection.count()
            return before - after
        except Exception as e:
            print(f"  [VECTOR] Chroma delete error: {e}")
            return 0

    def healthcheck(self) -> bool:
        if not self._collection:
            return False
        try:
            self._collection.count()
            return True
        except Exception:
            return False

    def stats(self) -> StoreStats:
        count = 0
        if self._collection:
            try:
                count = self._collection.count()
            except Exception:
                pass
        return StoreStats(
            backend="chroma",
            collection=COLLECTION_NAME,
            vector_count=count,
            last_write_time=self._last_write_time,
            last_write_ok=self._last_write_ok,
            last_error=self._last_error,
            embedding_model=self._embedding_model,
            extra={"storage_dir": str(CHROMA_DIR)},
        )
