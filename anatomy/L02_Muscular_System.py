
# A7DOv12 Sentience OS
# File: anatomy/L02_Muscular_System.py
# Purpose: The Absolute 3D Mathematical definition of Actuators (Muscles).
# Logic: Stringing vectors between L01 proximal/distal mathematical points.

import math

class ActuatorNode:
    """
    Strict mathematical definition of a Muscle/Tendon complex.
    Calculates its exact 3D length based on L01 skeletal geometry.
    """
    def __init__(self, name, origin_bone_id, origin_point, insertion_bone_id, insertion_point, base_volume):
        self.name = name
        
        # Attachment Logic
        self.origin_bone = origin_bone_id           # e.g., "FEMUR_L"
        self.origin_point = origin_point            # "proximal", "center", or "distal"
        self.insertion_bone = insertion_bone_id     # e.g., "TIBIA_FIBULA_L"
        self.insertion_point = insertion_point      # "proximal", "center", or "distal"
        
        # Physical Properties
        self.base_volume = base_volume              # Cross-sectional size
        self.tension = 0.0                          # 0.0 (Relaxed) to 1.0 (Max Flexion)
        
        # Calculated 3D State
        self.current_length = 0.0
        self.pos_origin_3d = {"x": 0.0, "y": 0.0, "z": 0.0}
        self.pos_insertion_3d = {"x": 0.0, "y": 0.0, "z": 0.0}

    def _get_bone_point(self, bone_node, point_type):
        """Extracts the exact 3D coordinate from the L01 AnatomicalNode."""
        if point_type == "proximal":
            return bone_node.pos_proximal
        elif point_type == "distal":
            return bone_node.pos_distal
        else:
            return bone_node.pos_center

    def calculate_vector(self, skeletal_geometry):
        """
        Calculates the true 3D vector line of the muscle based on the skeleton's current state.
        Uses Euclidean distance (Pythagorean theorem in 3D).
        """
        # 1. Fetch the exact Bones from L01
        origin_node = skeletal_geometry.get(self.origin_bone)
        insertion_node = skeletal_geometry.get(self.insertion_bone)
        
        if not origin_node or not insertion_node:
            return # Failsafe if skeleton is incomplete
            
        # 2. Extract specific mathematical anchor points
        self.pos_origin_3d = self._get_bone_point(origin_node, self.origin_point)
        self.pos_insertion_3d = self._get_bone_point(insertion_node, self.insertion_point)
        
        # 3. Calculate True 3D Euclidean Distance (Current Muscle Length)
        dx = self.pos_insertion_3d["x"] - self.pos_origin_3d["x"]
        dy = self.pos_insertion_3d["y"] - self.pos_origin_3d["y"]
        dz = self.pos_insertion_3d["z"] - self.pos_origin_3d["z"]
        
        self.current_length = math.sqrt(dx**2 + dy**2 + dz**2)


class MuscularBlueprint:
    """The complete registry of A7DOv12 Actuators."""
    def __init__(self):
        self.registry = {
            # --- NECK & CRANIAL ---
            "STERNOCLEIDOMASTOID_L": ActuatorNode("Neck_Flexor_L", "STERNUM", "proximal", "CRANIUM", "distal", base_volume=0.02),
            "STERNOCLEIDOMASTOID_R": ActuatorNode("Neck_Flexor_R", "STERNUM", "proximal", "CRANIUM", "distal", base_volume=0.02),
            "MASSETER": ActuatorNode("Jaw_Closer", "CRANIUM", "center", "MANDIBLE", "distal", base_volume=0.01),
            
            # --- CHEST & BACK ---
            "PECTORALIS_L": ActuatorNode("Chest_L", "STERNUM", "center", "HUMERUS_L", "proximal", base_volume=0.08),
            "PECTORALIS_R": ActuatorNode("Chest_R", "STERNUM", "center", "HUMERUS_R", "proximal", base_volume=0.08),
            "TRAPEZIUS": ActuatorNode("Upper_Back", "CERVICAL_SPINE", "proximal", "CLAVICLE_L", "center", base_volume=0.07), # Simplified anchor
            "LATISSIMUS_DORSI_L": ActuatorNode("Lats_L", "LUMBAR_SPINE", "center", "HUMERUS_L", "proximal", base_volume=0.09),
            "LATISSIMUS_DORSI_R": ActuatorNode("Lats_R", "LUMBAR_SPINE", "center", "HUMERUS_R", "proximal", base_volume=0.09),
            "RECTUS_ABDOMINIS": ActuatorNode("Abs", "STERNUM", "distal", "PELVIS", "proximal", base_volume=0.06),
            
            # --- ARMS ---
            "BICEPS_L": ActuatorNode("Bicep_L", "HUMERUS_L", "proximal", "RADIUS_ULNA_L", "proximal", base_volume=0.04),
            "BICEPS_R": ActuatorNode("Bicep_R", "HUMERUS_R", "proximal", "RADIUS_ULNA_R", "proximal", base_volume=0.04),
            "TRICEPS_L": ActuatorNode("Tricep_L", "HUMERUS_L", "proximal", "RADIUS_ULNA_L", "distal", base_volume=0.05),
            "TRICEPS_R": ActuatorNode("Tricep_R", "HUMERUS_R", "proximal", "RADIUS_ULNA_R", "distal", base_volume=0.05),
            
            # --- LEGS ---
            "QUADRICEPS_L": ActuatorNode("Quad_L", "PELVIS", "distal", "TIBIA_FIBULA_L", "proximal", base_volume=0.15),
            "QUADRICEPS_R": ActuatorNode("Quad_R", "PELVIS", "distal", "TIBIA_FIBULA_R", "proximal", base_volume=0.15),
            "HAMSTRINGS_L": ActuatorNode("Hamstring_L", "PELVIS", "distal", "TIBIA_FIBULA_L", "center", base_volume=0.12),
            "HAMSTRINGS_R": ActuatorNode("Hamstring_R", "PELVIS", "distal", "TIBIA_FIBULA_R", "center", base_volume=0.12),
            "GASTROCNEMIUS_L": ActuatorNode("Calf_L", "FEMUR_L", "distal", "FOOT_L", "proximal", base_volume=0.08),
            "GASTROCNEMIUS_R": ActuatorNode("Calf_R", "FEMUR_R", "distal", "FOOT_R", "proximal", base_volume=0.08)
        }

    def generate_current_musculature(self, skeletal_geometry):
        """
        Takes the calculated absolute 3D skeleton from L01 and calculates 
        every single muscle vector to drape over it perfectly.
        """
        for muscle_id, muscle in self.registry.items():
            muscle.calculate_vector(skeletal_geometry)
            
        return self.registry
