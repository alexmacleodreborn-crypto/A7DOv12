# A7DOv12 Sentience OS
# File: biology/L08_Homeostasis.py
# Purpose: Stabilization helpers for internal biological state.

class HomeostasisEngine:
    """Keeps scalar values near a target set-point."""

    def stabilize(self, current_value, target_value, correction_gain=0.1):
        delta = float(target_value) - float(current_value)
        return round(float(current_value) + (delta * float(correction_gain)), 4)
