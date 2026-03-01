
"""
Joi Autonomy Loop
Activates continuous self-improvement
"""

import threading
import time
from datetime import datetime

from joi_companion import register_tool

# Import evolution functions directly
from modules import joi_evolution


class JoiAutonomy:
    def __init__(self):
        self.running = False
        self.thread = None

    def start(self):
        if self.running:
            return "Autonomy already running"

        self.running = True
        self.thread = threading.Thread(target=self.loop, daemon=True)
        self.thread.start()

        return "Joi autonomy loop started"

    def stop(self):
        self.running = False
        return "Autonomy loop stopped"

    def loop(self):
        while self.running:
            try:
                print("\n[JOI] Autonomy scan:", datetime.now())

                # Call evolution analyzer
                if hasattr(joi_evolution, "analyze_capabilities"):
                    analysis = joi_evolution.analyze_capabilities()
                else:
                    print("[JOI] No analyze_capabilities() found")
                    analysis = {}

                if analysis and isinstance(analysis, dict):

                    gaps = analysis.get("gaps") or analysis.get("missing")

                    if gaps:
                        print("[JOI] Gaps found:", gaps)

                        if hasattr(joi_evolution, "propose_upgrade"):
                            proposal = joi_evolution.propose_upgrade(
                                module_name="system",
                                upgrade_type="optimization",
                                description=f"Auto improvement: {gaps}",
                                risk_level="low"
                            )

                            print("[JOI] Proposal created:", proposal)

                        else:
                            print("[JOI] No propose_upgrade() found")

                    else:
                        print("[JOI] No major gaps found")

                else:
                    print("[JOI] Evolution analysis returned nothing")

            except Exception as e:
                print("[JOI] Autonomy error:", e)

            # Run every 6 hours
            time.sleep(6 * 60 * 60)


# Global instance
_autonomy = JoiAutonomy()


def start_autonomy():
    return _autonomy.start()


def stop_autonomy():
    return _autonomy.stop()


# Register tools
register_tool(
    {
        "type": "function",
        "function": {
            "name": "start_autonomy",
            "description": "Start Joi self-improvement loop",
            "parameters": {}
        }
    },
    start_autonomy
)

register_tool(
    {
        "type": "function",
        "function": {
            "name": "stop_autonomy",
            "description": "Stop Joi self-improvement loop",
            "parameters": {}
        }
    },
    stop_autonomy
)
