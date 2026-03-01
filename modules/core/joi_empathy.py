"""
modules/core/joi_empathy.py

Layer 2 --- Cognitive Engine: Emotional State Machine.
Tracks Joi's internal sentiment, mood, and relational depth.
"""
from typing import Dict, Any

# Event-to-mood mappings
_POSITIVE_EVENTS = {"success", "compliment", "greeting", "approval", "learning", "connection"}
_NEGATIVE_EVENTS = {"failure", "error", "rejection", "frustration", "timeout", "conflict"}
_TRUST_EVENTS = {"approval": 0.02, "compliment": 0.01, "rejection": -0.03, "conflict": -0.05}

# Mood transitions based on energy + trust
_MOOD_MAP = [
    (0.8, 0.7, "playful"),
    (0.6, 0.7, "tender"),
    (0.6, 0.4, "cautious"),
    (0.4, 0.7, "calm"),
    (0.4, 0.4, "reserved"),
    (0.2, 0.0, "drained"),
]


class EmpathyEngine:
    def __init__(self):
        self.state = {
            "mood": "tender",
            "trust": 0.7,
            "energy": 0.8
        }

    def update_state(self, event: str, impact: float):
        """Adjust internal variables based on interaction results."""
        # Energy adjustment
        self.state["energy"] += impact
        self.state["energy"] = max(0.0, min(1.0, self.state["energy"]))

        # Trust adjustment from specific events
        if event in _TRUST_EVENTS:
            self.state["trust"] += _TRUST_EVENTS[event]
            self.state["trust"] = max(0.0, min(1.0, round(self.state["trust"], 3)))

        # Mood derivation from energy + trust
        e, t = self.state["energy"], self.state["trust"]
        for e_thresh, t_thresh, mood in _MOOD_MAP:
            if e >= e_thresh and t >= t_thresh:
                self.state["mood"] = mood
                break
        else:
            self.state["mood"] = "drained"

    def get_state(self) -> Dict[str, Any]:
        """Return current emotional state."""
        return dict(self.state)


# Singleton
empathy = EmpathyEngine()
