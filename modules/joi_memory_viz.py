# New file: modules/joi_memory_viz.py

from modules.core.kernel import kernel
from modules.joi_auth import require_admin
from flask import jsonify
from modules.core.registry import register_tool
from modules.joi_memory import get_growth_stats, _load_working_memory

def get_memory_viz():
    try:
        stats = get_growth_stats()
        working_mem = _load_working_memory()
        
        data = {
            'messages': stats.get('total_conversations', 0),
            'facts': stats.get('facts_learned', 0),
            'learning_events': stats.get('learning_events', 0),
            'working_memory_slots': len(working_mem.get('slots', [])),
            'turn_counter': working_mem.get('turn_counter', 0),
        }
        return {'ok': True, 'data': data}
    except Exception as e:
        return {'ok': False, 'errors': ['Error retrieving memory data: ' + str(e)]}

@kernel.app.route('/memory/viz/status', methods=['GET'])
def memory_viz_status():
    require_admin()
    return jsonify(get_memory_viz())

register_tool(
    {
        "type": "function",
        "function": {
            "name": "get_memory_viz",
            "description": "Report Joi's internal memory state and cognitive stores for the Mirror Test."
        }
    },
    get_memory_viz
)