"""
modules/core/topology.py

Layer 3 --- Capability System: Topology Manager.
Manages awareness of the physical runtime environment and available compute nodes.
"""
import platform
import psutil
import socket
import os
from typing import Dict, Any, List
from dataclasses import dataclass, field

@dataclass
class ComputeNode:
    node_id: str
    type: str # 'local_primary', 'local_worker', 'cloud_worker'
    status: str # 'active', 'busy', 'offline'
    capabilities: List[str]
    load: float = 0.0

class TopologyManager:
    def __init__(self):
        self.local_node = self._scan_local_environment()
        self.workers = {} # node_id -> ComputeNode

    def _scan_local_environment(self) -> ComputeNode:
        """Discover local hardware capabilities."""
        return ComputeNode(
            node_id=socket.gethostname(),
            type="local_primary",
            status="active",
            capabilities=self._detect_capabilities()
        )

    def _detect_capabilities(self) -> List[str]:
        caps = ["python_execution", "file_io"]
        # Basic heuristic for "heavy" capabilities
        mem = psutil.virtual_memory()
        if mem.total > 16 * 1024 * 1024 * 1024: # >16GB RAM
            caps.append("heavy_compute")
        
        # Check for GPU (naive check for NVIDIA)
        try:
            import subprocess
            res = subprocess.run(['nvidia-smi'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if res.returncode == 0:
                caps.append("gpu_acceleration")
        except: pass
        
        return caps

    def get_topology_snapshot(self) -> Dict[str, Any]:
        """Return a serializable view of the cognitive network."""
        return {
            "primary": self.local_node.__dict__,
            "workers": {k: v.__dict__ for k, v in self.workers.items()},
            "os": f"{platform.system()} {platform.release()}"
        }

# Singleton
topology = TopologyManager()
