"""
Document Reader -- Ingest large documents into ChromaDB for semantic search.
"""
import os
import uuid
import datetime
from pathlib import Path
from typing import Any, Dict

import joi_companion
from modules.memory.vector_chroma import ChromaVectorStore
from modules.memory.vector_store_base import MemoryChunk

# Instantiate vector store singleton for this module
vector_store = ChromaVectorStore()

def ingest_long_document(**kwargs) -> Dict[str, Any]:
    """Ingest a large document (txt, md) by chunking and sending to vector DB."""
    file_path = kwargs.get("file_path", "").strip()
    if not file_path:
        return {"ok": False, "error": "file_path is required"}
    
    path = Path(file_path)
    if not path.is_absolute():
        path = Path(joi_companion.BASE_DIR) / file_path
        
    if not path.exists():
        return {"ok": False, "error": f"File not found: {path}"}
        
    try:
        content = path.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        return {"ok": False, "error": f"Failed to read file: {e}"}
        
    # Simple chunking (~1000 words per chunk, 100 overlap)
    words = content.split()
    chunk_size = 1000
    overlap = 100
    
    chunks = []
    for i in range(0, len(words), max(1, chunk_size - overlap)):
        chunk_words = words[i:i + chunk_size]
        if not chunk_words:
            break
        chunk_text = " ".join(chunk_words)
        
        chunk = MemoryChunk(
            id=f"{path.name}_{uuid.uuid4()}",
            text=chunk_text,
            metadata={
                "type": "document",
                "source": str(path),
                "filename": path.name,
                "timestamp": datetime.datetime.now().isoformat()
            }
        )
        chunks.append(chunk)

    if not chunks:
        return {"ok": False, "error": "File was empty"}

    success = vector_store.upsert(chunks)
    
    if success:
        return {
            "ok": True, 
            "message": f"Successfully ingested {path.name} into {len(chunks)} chunks.",
            "chunk_count": len(chunks)
        }
    else:
        return {"ok": False, "error": "Failed to upsert chunks into ChromaDB."}


def query_document(**kwargs) -> Dict[str, Any]:
    """Search for relevant context within ingested documents."""
    query = kwargs.get("query", "").strip()
    filename = kwargs.get("filename", "").strip()
    top_k = kwargs.get("top_k", 5)
    
    if not query:
        return {"ok": False, "error": "query is required"}
        
    filters = None
    if filename:
        filters = {"filename": filename}
        
    results = vector_store.query(text=query, top_k=top_k, filters=filters)
    
    if not results:
        return {"ok": True, "results": [], "message": "No relevant context found."}
        
    formatted_results = []
    for r in results:
        formatted_results.append({
            "text": r.text,
            "source": r.metadata.get("filename", "unknown"),
            "score": round(r.score, 3)
        })
        
    return {"ok": True, "results": formatted_results}


# Register tools with Joi's core
joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "ingest_long_document",
        "description": "Read a massive document (book, manual, codebase file) and safely chunk it into Joi's vector memory. Use this before answering questions about huge files to avoid token limits.",
        "parameters": {"type": "object", "properties": {
            "file_path": {"type": "string", "description": "Absolute or relative path to the text file"}
        }, "required": ["file_path"]}
    }},
    ingest_long_document
)

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "query_document",
        "description": "Ask a semantic question about previously ingested long documents. Retrieves the exact paragraphs containing the answer.",
        "parameters": {"type": "object", "properties": {
            "query": {"type": "string", "description": "The specific question or topic to search for"},
            "filename": {"type": "string", "description": "Optional: Filter search to a specific filename"},
            "top_k": {"type": "integer", "description": "Number of paragraphs to retrieve (default 5)"}
        }, "required": ["query"]}
    }},
    query_document
)

print("  [OK] joi_document_reader -- RAG Document Ingestion loaded")
