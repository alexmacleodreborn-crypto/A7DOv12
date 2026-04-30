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
        self.pos_insertion_3d = {"x": 0.0, "y": 0.0, "z": 0.0}
        
        # Future Hill-Type properties
        self.fatigue = 1.0                    # 1.0 = fresh, decreases with use
        self.max_force = base_volume * 1000   # Rough estimate (will be refined)

    def _get_bone_point(self, bone_node, point_type):
        if point_type == "proximal":
            return bone_node.pos_proximal
        elif point_type == "distal":
            return bone_node.pos_distal
        else:
            return bone_node.pos_center

    def calculate_vector(self, skeletal_geometry):
        """Calculate current 3D length of the muscle"""
        origin_node = skeletal_geometry.get(self.origin_bone)
        insertion_node = skeletal_geometry.get(self.insertion_bone)
        
        if not origin_node or not insertion_node:
            self.current_length = 0.0
            return
            
        self.pos_origin_3d = self._get_bone_point(origin_node, self.origin_point)
        self.pos_insertion_3d = self._get_bone_point(insertion_node, self.insertion_point)
        
        dx = self.pos_insertion_3d["x"] - self.pos_origin_3d["x"]
        dy = self.pos_insertion_3d["y"] - self.pos_origin_3d["y"]
        dz = self.pos_insertion_3d["z"] - self.pos_origin_3d["z"]
        
        self.current_length = math.sqrt(dx**2 + dy**2 + dz**2)


class MuscularBlueprint:
    """Registry of all major muscles"""
    def __init__(self):
        self.registry = {
            # Neck
            "STERNOCLEIDOMASTOID_L": ActuatorNode("Neck_Flexor_L", "STERNUM", "proximal", "CRANIUM", "distal", base_volume=0.02),
            "STERNOCLEIDOMASTOID_R": ActuatorNode("Neck_Flexor_R", "STERNUM", "proximal", "CRANIUM", "distal", base_volume=0.02),
            
            # Torso
            "PECTORALIS_L": ActuatorNode("Chest_L", "STERNUM", "center", "HUMERUS_L", "proximal", base_volume=0.08),
            "PECTORALIS_R": ActuatorNode("Chest_R", "STERNUM", "center", "HUMERUS_R", "proximal", base_volume=0.08),
            "RECTUS_ABDOMINIS": ActuatorNode("Abs", "STERNUM", "distal", "PELVIS", "proximal", base_volume=0.06),
            
            # Arms
            "BICEPS_L": ActuatorNode("Bicep_L", "HUMERUS_L", "proximal", "RADIUS_ULNA_L", "proximal", base_volume=0.04),
            "BICEPS_R": ActuatorNode("Bicep_R", "HUMERUS_R", "proximal", "RADIUS_ULNA_R", "proximal", base_volume=0.04),
            "TRICEPS_L": ActuatorNode("Tricep_L", "HUMERUS_L", "proximal", "RADIUS_ULNA_L", "distal", base_volume=0.05),
            "TRICEPS_R": ActuatorNode("Tricep_R", "HUMERUS_R", "proximal", "RADIUS_ULNA_R", "distal", base_volume=0.05),
            
            # Legs - Important for standing/walking
            "QUADRICEPS_L": ActuatorNode("Quad_L", "PELVIS", "distal", "TIBIA_FIBULA_L", "proximal", base_volume=0.15),
            "QUADRICEPS_R": ActuatorNode("Quad_R", "PELVIS", "distal", "TIBIA_FIBULA_R", "proximal", base_volume=0.15),
            "HAMSTRINGS_L": ActuatorNode("Hamstring_L", "PELVIS", "distal", "TIBIA_FIBULA_L", "center", base_volume=0.12),
            "HAMSTRINGS_R": ActuatorNode("Hamstring_R", "PELVIS", "distal", "TIBIA_FIBULA_R", "center", base_volume=0.12),
            "GASTROCNEMIUS_L": ActuatorNode("Calf_L", "FEMUR_L", "distal", "FOOT_L", "proximal", base_volume=0.08),
            "GASTROCNEMIUS_R": ActuatorNode("Calf_R", "FEMUR_R", "distal", "FOOT_R", "proximal", base_volume=0.08),
        }

    def generate_current_musculature(self, skeletal_geometry):
        """Update all muscle vectors"""
        for muscle in self.registry.values():
            muscle.calculate_vector(skeletal_geometry)
        return self.registry