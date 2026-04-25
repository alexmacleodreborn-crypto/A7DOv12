
# A7DOv12 Sentience OS
# File: biology/L07_Growth.py
# Purpose: Absolute Mathematical Maturation Timeline.
# Logic: Smooth interpolation of Da Vinci proportions and Square-Cube scaling.

import time

class MaturationEngine:
    """
    The Biological Clock for A7DOv12.
    Tracks physical growth, proportional shifting, and mass accumulation.
    """
    def __init__(self, birth_scale=0.20):
        # Master Clock
        self.current_scale = birth_scale  # Starts at 20% of adult height
        self.target_scale = 1.0           # 100% Vitruvian Adult
        self.growth_rate = 0.005          # Increment per tick
        
        # Sentience Log: Recording the physical experience of growing
        self.milestone_log = []
        self.last_recorded_stage = ""

        # Absolute Biological Thresholds (Height Scalars)
        self.stages = {
            0.20: "NEONATAL",
            0.35: "INFANT",
            0.50: "TODDLER",
            0.70: "CHILD",
            0.85: "ADOLESCENT",
            1.00: "ADULT_SYNTHETIC"
        }

    def _get_current_stage_name(self):
        """Identifies the discrete biological stage based on the continuous scale."""
        current_stage = "NEONATAL"
        for threshold, name in sorted(self.stages.items()):
            if self.current_scale >= threshold:
                current_stage = name
        return current_stage

    def _calculate_proportions(self):
        """
        Deterministic Interpolation of Da Vinci Ratios.
        Maps the current scale (0.2 -> 1.0) to strict biological ratios.
        """
        # Calculate how far along the timeline we are (0.0 to 1.0 progress)
        progress = (self.current_scale - 0.2) / (1.0 - 0.2)
        progress = max(0.0, min(1.0, progress)) # Clamp between 0 and 1
        
        # Head Ratio: Starts at 1/4 (0.25), ends at Da Vinci 1/8 (0.125)
        current_head_ratio = 0.25 - (progress * (0.25 - 0.125))
        
        # Limb Ratio: Limbs are stubbier in infants (0.5x), full length in adults (1.0x)
        current_limb_ratio = 0.5 + (progress * 0.5)
        
        return current_head_ratio, current_limb_ratio

    def trigger_growth_pulse(self):
        """
        Advances the biological clock. Returns True if actively growing.
        """
        if self.current_scale < self.target_scale:
            self.current_scale = min(self.target_scale, self.current_scale + self.growth_rate)
            
            # Check for developmental milestones
            current_stage = self._get_current_stage_name()
            if current_stage != self.last_recorded_stage:
                self.milestone_log.append({
                    "timestamp": time.time(),
                    "stage": current_stage,
                    "height_scalar": round(self.current_scale, 3),
                    "mass_scalar": round(self.current_scale ** 3, 3)
                })
                self.last_recorded_stage = current_stage
                
            return True
        return False

    def get_physics_state(self):
        """
        Generates the absolute mathematical state for L01, L02, and L05 to process.
        """
        head_r, limb_r = self._calculate_proportions()
        
        return {
            "scale_x": round(self.current_scale, 4),           # Linear Height
            "strength_x2": round(self.current_scale ** 2, 4),  # Muscle Cross-Section
            "mass_x3": round(self.current_scale ** 3, 4),      # Volume/Weight
            "head_ratio": round(head_r, 4),                    # Modifies L01 Cranium placement
            "limb_ratio": round(limb_r, 4),                    # Modifies L01 Femur/Humerus reach
            "stage": self._get_current_stage_name()
        }
