"""
modules/core/cognition.py

Layer 2 --- Cognitive Engine: Reasoning Graph Store.
Handles the persistence and relationship mapping of Joi's internal loops.
"""
import sqlite3
import json
import time
import uuid
from dataclasses import dataclass, asdict, field
from typing import List, Optional, Dict, Any
from modules.core.config import config

@dataclass
class CognitiveNode:
    node_id: str
    loop_type: str  # PERCEPTION, DELIBERATION, EXECUTION, REFLECTION
    content: Dict[str, Any]
    parent_id: Optional[str] = None
    session_id: Optional[str] = None
    timestamp: float = field(default_factory=time.time)

    def to_json(self):
        return json.dumps(asdict(self))

class ReasoningGraph:
    def __init__(self):
        self.db_path = config.DATA_DIR / "joi_cognition.db"
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS nodes (
                node_id TEXT PRIMARY KEY,
                loop_type TEXT,
                parent_id TEXT,
                session_id TEXT,
                capability_id TEXT,
                content TEXT,
                tags TEXT,
                success_score REAL DEFAULT 0.0,
                latency_ms INTEGER DEFAULT 0,
                timestamp REAL
            )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_session ON nodes(session_id)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_cap_success ON nodes(capability_id, success_score)")
        conn.commit()
        conn.close()

    def add_node(self, loop_type: str, content: Dict[str, Any], 
                 parent_id: str = None, session_id: str = None, 
                 capability_id: str = None, tags: List[str] = None, 
                 success_score: float = 0.0, latency_ms: int = 0) -> str:
        """Record a cognitive event with capability tracking and telemetry."""
        node_id = str(uuid.uuid4())
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            "INSERT INTO nodes (node_id, loop_type, parent_id, session_id, capability_id, content, tags, success_score, latency_ms, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (node_id, loop_type, parent_id, session_id, capability_id, json.dumps(content), json.dumps(tags or []), success_score, latency_ms, time.time())
        )
        conn.commit()
        conn.close()
        return node_id

    def update_score(self, node_id: str, score: float):
        """Update the success score of a reasoning node (Loop 4)."""
        conn = sqlite3.connect(self.db_path)
        conn.execute("UPDATE nodes SET success_score = ? WHERE node_id = ?", (score, node_id))
        conn.commit()
        conn.close()

    def get_successful_strategies(self, limit: int = 3) -> List[Dict]:
        """Retrieve historical reasoning chains that had high success scores."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        # Find successful DELIBERATION nodes (the plans)
        rows = conn.execute(
            "SELECT * FROM nodes WHERE loop_type = 'DELIBERATION' AND success_score > 0.7 ORDER BY success_score DESC, timestamp DESC LIMIT ?", 
            (limit,)
        ).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_model_performance_stats(self) -> List[Dict]:
        """Aggregate success rates per task_type and model."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        # We look for nodes that have both a model_id (in content) and a success_score
        # For this pilot, we assume Loop 4 Reflection nodes store the final outcome
        rows = conn.execute("""
            SELECT 
                json_extract(content, '$.task_type') as task_type,
                json_extract(content, '$.model_id') as model_id,
                AVG(success_score) as avg_success
            FROM nodes 
            WHERE loop_type = 'REFLECTION'
            GROUP BY task_type, model_id
            HAVING task_type IS NOT NULL AND model_id IS NOT NULL
        """).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_chain(self, session_id: str) -> List[Dict]:
        """Retrieve all nodes for a given session, ordered by timestamp."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT * FROM nodes WHERE session_id = ? ORDER BY timestamp ASC",
            (session_id,)
        ).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_capability_stats(self) -> List[Dict]:
        """Aggregate performance metrics per capability (module)."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        rows = conn.execute("""
            SELECT 
                capability_id,
                AVG(success_score) as success_rate,
                AVG(latency_ms) as avg_latency,
                COUNT(*) as usage_count
            FROM nodes 
            WHERE capability_id IS NOT NULL AND capability_id != 'unknown'
            GROUP BY capability_id
        """).fetchall()
        conn.close()
        return [dict(r) for r in rows]

# Singleton graph store
graph = ReasoningGraph()
