# plugins/system_monitor_dashboard.py
"""
System Monitor Dashboard
Real-time monitoring of Joi's AI activities and Claude Code tasks
"""

import os
import json
import psutil
import threading
import time
from pathlib import Path
from datetime import datetime, timedelta
from flask import Blueprint, render_template, jsonify
from collections import deque

monitor_bp = Blueprint('monitor', __name__, url_prefix='/monitor')

class SystemMonitor:
    def __init__(self):
        self.activity_log = deque(maxlen=100)
        self.metrics = {
            'cpu_usage': deque(maxlen=60),
            'memory_usage': deque(maxlen=60),
            'api_calls': deque(maxlen=60),
            'file_operations': deque(maxlen=60)
        }
        self.file_watch = {}
        self.monitoring = False
        self.monitor_thread = None
        
    def start_monitoring(self):
        """Start background monitoring"""
        if not self.monitoring:
            self.monitoring = True
            self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self.monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop background monitoring"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2)
    
    def _monitor_loop(self):
        """Background monitoring loop"""
        while self.monitoring:
            try:
                # Collect system metrics
                self.metrics['cpu_usage'].append({
                    'timestamp': datetime.now().isoformat(),
                    'value': psutil.cpu_percent(interval=1)
                })
                
                memory = psutil.virtual_memory()
                self.metrics['memory_usage'].append({
                    'timestamp': datetime.now().isoformat(),
                    'value': memory.percent,
                    'used_mb': memory.used / (1024 * 1024)
                })
                
                # Monitor file changes
                self._check_file_changes()
                
                time.sleep(5)  # Update every 5 seconds
            except Exception as e:
                self.log_activity('error', f'Monitor error: {str(e)}')
    
    def _check_file_changes(self):
        """Monitor critical files for changes"""
        critical_paths = [
            'modules/',
            'plugins/',
            'core/',
            'config/'
        ]
        
        for path_str in critical_paths:
            path = Path(path_str)
            if path.exists():
                for file_path in path.rglob('*.py'):
                    try:
                        stat = file_path.stat()
                        mtime = stat.st_mtime
                        
                        if str(file_path) in self.file_watch:
                            if self.file_watch[str(file_path)] != mtime:
                                self.log_activity('file_modified', str(file_path))
                                self.metrics['file_operations'].append({
                                    'timestamp': datetime.now().isoformat(),
                                    'file': str(file_path),
                                    'action': 'modified'
                                })
                        
                        self.file_watch[str(file_path)] = mtime
                    except Exception:
                        pass
    
    def log_activity(self, activity_type, description, metadata=None):
        """Log system activity"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'type': activity_type,
            'description': description,
            'metadata': metadata or {}
        }
        self.activity_log.append(entry)
    
    def get_dashboard_data(self):
        """Get all dashboard data"""
        from plugins.claude_code_delegate import delegate
        
        # Get Claude Code status
        claude_status = delegate.get_status() if delegate else {
            'is_running': False,
            'active_tasks': 0,
            'queued_tasks': 0,
            'completed_tasks': 0
        }
        
        # Get recent tasks
        recent_tasks = []
        if delegate:
            recent_tasks = delegate.task_history[-10:]  # Last 10 tasks
        
        # Get active AI sessions
        active_sessions = self._get_active_ai_sessions()
        
        return {
            'system': {
                'cpu': list(self.metrics['cpu_usage'])[-20:],
                'memory': list(self.metrics['memory_usage'])[-20:],
                'uptime': self._get_uptime()
            },
            'claude_code': {
                'status': claude_status,
                'recent_tasks': recent_tasks
            },
            'joi': {
                'active_sessions': active_sessions,
                'api_calls': list(self.metrics['api_calls'])[-20:],
                'file_operations': list(self.metrics['file_operations'])[-10:]
            },
            'activity_log': list(self.activity_log)[-30:],
            'alerts': self._get_active_alerts()
        }
    
    def _get_active_ai_sessions(self):
        """Get currently active AI API sessions"""
        sessions = []
        
        # Check for active API calls (you'll need to hook this into your API wrapper)
        session_file = Path('data/active_sessions.json')
        if session_file.exists():
            with open(session_file, 'r') as f:
                sessions = json.load(f)
        
        return sessions
    
    def _get_uptime(self):
        """Get system uptime"""
        uptime_file = Path('data/uptime.json')
        if uptime_file.exists():
            with open(uptime_file, 'r') as f:
                data = json.load(f)
                start_time = datetime.fromisoformat(data['start_time'])
                uptime = datetime.now() - start_time
                return {
                    'seconds': int(uptime.total_seconds()),
                    'formatted': str(uptime).split('.')[0]
                }
        return {'seconds': 0, 'formatted': '0:00:00'}
    
    def _get_active_alerts(self):
        """Get active system alerts"""
        alerts = []
        
        # Check for conflicts
        from plugins.claude_code_delegate import delegate
        if delegate and delegate.is_claude_code_running():
            alerts.append({
                'level': 'warning',
                'message': 'Claude Code is currently running - file modifications in progress',
                'timestamp': datetime.now().isoformat()
            })
        
        # Check system resources
        memory = psutil.virtual_memory()
        if memory.percent > 85:
            alerts.append({
                'level': 'error',
                'message': f'High memory usage: {memory.percent:.1f}%',
                'timestamp': datetime.now().isoformat()
            })
        
        cpu = psutil.cpu_percent(interval=0.1)
        if cpu > 90:
            alerts.append({
                'level': 'warning',
                'message': f'High CPU usage: {cpu:.1f}%',
                'timestamp': datetime.now().isoformat()
            })
        
        return alerts


# Global monitor instance
monitor = SystemMonitor()


# Flask routes
@monitor_bp.route('/')
def dashboard():
    """Render dashboard page"""
    return render_template('monitor_dashboard.html')

@monitor_bp.route('/api/data')
def get_data():
    """API endpoint for dashboard data"""
    return jsonify(monitor.get_dashboard_data())

@monitor_bp.route('/api/activity')
def get_activity():
    """Get recent activity log"""
    return jsonify(list(monitor.activity_log))


def init(config):
    """Initialize monitoring"""
    monitor.start_monitoring()
    
    # Log startup
    monitor.log_activity('system', 'System monitor initialized')
    
    # Save uptime start
    uptime_file = Path('data/uptime.json')
    uptime_file.parent.mkdir(parents=True, exist_ok=True)
    with open(uptime_file, 'w') as f:
        json.dump({'start_time': datetime.now().isoformat()}, f)
    
    return True


def shutdown():
    """Cleanup on shutdown"""
    monitor.stop_monitoring()