# A7DOv12 Sentience OS
# File: biology/L07_Growth.py
# Purpose: Absolute Mathematical Maturation Timeline with Organ Scaling.

import time

class MaturationEngine:
    """
    The Biological Clock for A7DOv12.
    Tracks physical growth, proportional shifting, and organ volume development.
    """
    def __init__(self, birth_scale=0.20):
        # Master Clock
        self.current_scale = birth_scale  # Starts at 20% of adult height
        self.target_scale = 1.0           # 100% Vitruvian Adult[cite: 17]
        self.growth_rate = 0.005          # Increment per tick[cite: 17]
        
        self.milestone_log = []
        self.last_recorded_stage = ""

        # Absolute Biological Thresholds (Height Scalars)[cite: 17]
        self.stages = {
            0.20: "NEONATAL",
            0.35: "INFANT",
            0.50: "TODDLER",
            0.70: "CHILD",
            0.85: "ADOLESCENT",
            1.00: "ADULT_SYNTHETIC"
        }

        # New: Organ Development Registry (Internal volume scaling)
        self.organs = {
            "HEART": {"growth_coef": 2.5, "base_efficiency": 0.4},
            "LUNGS": {"growth_coef": 3.0, "base_efficiency": 0.3}, # Square-Cube Law[cite: 17]
            "STOMACH": {"growth_coef": 2.8, "base_efficiency": 0.5}
        }

    def _get_current_stage_name(self):
        """Identifies the discrete biological stage based on the continuous scale[cite: 17]."""
        current_stage = "NEONATAL"
        for threshold, name in sorted(self.stages.items()):
            if self.current_scale >= threshold:
                current_stage = name
        return current_stage

    def _calculate_proportions(self):
        """
        Interpolation of Da Vinci Ratios.
        Maps the current scale (0.2 -> 1.0) to strict biological ratios[cite: 17].
        """
        progress = (self.current_scale - 0.2) / (1.0 - 0.2)
        progress = max(0.0, min(1.0, progress)) 
        
        # Head Ratio: Starts at 1/4 (0.25), ends at Da Vinci 1/8 (0.125)[cite: 17]
        current_head_ratio = 0.25 - (progress * (0.25 - 0.125))
        # Limb Ratio: Limbs are stubbier in infants (0.5x), full length in adults (1.0x)[cite: 17]
        current_limb_ratio = 0.5 + (progress * 0.5)
        
        return current_head_ratio, current_limb_ratio

    def trigger_growth_pulse(self):
        """Advances the biological clock[cite: 17]."""
        if self.current_scale < self.target_scale:
            self.current_scale = min(self.target_scale, self.current_scale + self.growth_rate)
            
            current_stage = self._get_current_stage_name()
            if current_stage != self.last_recorded_stage:
                self.milestone_log.append({
                    "timestamp": time.time(),
                    "stage": current_stage,
                    "height_scalar": round(self.current_scale, 3)
                })
                self.last_recorded_stage = current_stage
            return True
        return False

    def get_physics_state(self):
        """Generates state for physics and dashboard visualization[cite: 17]."""
        head_r, limb_r = self._calculate_proportions()
        
        # Calculate Allometric Organ Scaling
        organ_states = {}
        for name, stats in self.organs.items():
            # Organs scale exponentially relative to height
            organ_states[name] = {
                "capacity": round(self.current_scale ** stats["growth_coef"], 4),
                "efficiency": round(stats["base_efficiency"] + (0.5 * self.current_scale), 2)
            }
        
        return {
            "scale_x": round(self.current_scale, 4),           # Linear Height[cite: 17]
            "mass_x3": round(self.current_scale ** 3, 4),      # Volume/Weight[cite: 17]
            "head_ratio": round(head_r, 4),                    
            "limb_ratio": round(limb_r, 4),                    
            "stage": self._get_current_stage_name(),
            "organs": organ_states
        }
