"""
modules/core/meta_cognition.py

Layer 2 --- Cognitive Engine: Meta-Cognition Layer.
Analyzes task outcomes, adapts strategies, and maintains self-aware capability mapping.
"""
import time
import json
from typing import Dict, Any, List, Optional
from modules.core.cognition import graph
from modules.core.registry import update_routing_score, log_telemetry

class MetaCognitionEngine:
    """
    The 'Self-Reflective' brain.
    Periodically analyzes the Reasoning Graph to optimize future behavior.
    """
    def __init__(self):
        self.last_analysis_ts = 0.0
        self.analysis_interval = 300.0  # 5 minutes

    def run_analysis_cycle(self):
        """
        Main meta-cognitive loop.
        1. Analyze recent task outcomes.
        2. Update routing scores based on success/failure.
        3. Identify resource bottlenecks.
        4. Detect patterns in multi-agent orchestration.
        """
        now = time.time()
        if now - self.last_analysis_ts < self.analysis_interval:
            return

        print("  [META] Starting Meta-Cognitive Analysis Cycle...")
        
        # 1. Outcome Analysis
        outcomes = self._analyze_outcomes()
        
        # 2. Strategy Adaptation (Success-Weighted Routing)
        self._adapt_strategies(outcomes)
        
        # 3. Resource Optimization
        self._optimize_resources()
        
        self.last_analysis_ts = now
        log_telemetry("meta_analysis_cycles", 1)

    def _analyze_outcomes(self) -> List[Dict]:
        """Fetch and aggregate recent task outcomes from the graph."""
        # Query the graph for recent EXECUTION nodes with success scores
        # In a real implementation, this would be a SQL query on the 'nodes' table
        # For this pilot, we use the existing graph API
        try:
            stats = graph.get_model_performance_stats()
            return stats
        except Exception as e:
            print(f"  [META] Outcome analysis failed: {e}")
            return []

    def _adapt_strategies(self, outcomes: List[Dict]):
        """Update global routing weights based on observed performance."""
        for entry in outcomes:
            task_type = entry.get('task_type')
            model_id = entry.get('model_id')
            avg_success = entry.get('avg_success', 0.0)
            
            if task_type and model_id:
                # Update the registry's ROUTING_SCORES
                update_routing_score(task_type, model_id, avg_success)
                # print(f"  [META] Adapted Strategy: {task_type} -> {model_id} = {avg_success:.2f}")

    def _optimize_resources(self):
        """Check for resource bottlenecks and adjust concurrency limits."""
        from modules.core.regulator import regulator
        # If we are consistently hitting CPU limits, we might want to lower the hard cap temporarily
        # This is a placeholder for more advanced adaptive throttling logic
        pass

    def get_capability_report(self) -> Dict[str, Any]:
        """Generate a human-readable report of self-knowledge."""
        # Combine introspection data with performance metrics
        from modules.core.introspection import engine as intro_engine
        
        report = {
            "capabilities": intro_engine.capabilities,
            "performance": graph.get_capability_stats(),
            "routing_strategy": "Success-Weighted (Dynamic)"
        }
        return report

# Singleton
meta = MetaCognitionEngine()
