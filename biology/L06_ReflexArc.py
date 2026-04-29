# A7DOv12 Sentience OS
# File: biology/L06_ReflexArc.py
# Purpose: Minimal reflex mapping utilities.

class ReflexArc:
    """Stores reflex response strengths by trigger label."""

    def __init__(self):
        self.registry = {}

    def set_response(self, trigger, strength):
        self.registry[str(trigger)] = max(0.0, min(1.0, float(strength)))

    def get_response(self, trigger, default=0.0):
        return self.registry.get(str(trigger), float(default))
