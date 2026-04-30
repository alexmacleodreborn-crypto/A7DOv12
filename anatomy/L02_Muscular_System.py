# anatomy/L02_Muscular_System.py
# A7DOv12 Sentience OS - Layer 02: Muscular Actuators (Hill-Type Ready)

import math

class ActuatorNode:
    """
    Muscle/Tendon complex with tension and basic Hill-Type properties.
    """
    def __init__(self, name, origin_bone_id, origin_point, insertion_bone_id, insertion_point, base_volume):
        self.name = name
        
        self.origin_bone = origin_bone_id
        self.origin_point = origin_point      # "proximal", "center", or "distal"
        self.insertion_bone = insertion_bone_id
        self.insertion_point = insertion_point
        
        self.base_volume = base_volume        # Used for force calculation later
        self.tension = 0.0                    # 0.0 = relaxed, 1.0 = max contraction
        
        # Calculated state
        self.current_length = 0.0
        self.pos_origin_3d = {"x": 0.0, "y": 0.0, "z": 0.0}