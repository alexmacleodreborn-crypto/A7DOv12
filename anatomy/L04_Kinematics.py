# anatomy/L04_Kinematics.py
# A7DOv12 Sentience OS - Layer 04: Kinematics Engine
# Connects muscle tension to bone rotation with better leg support for balance

class KinematicLink:
    """Maps a muscle to a joint rotation"""
    def __init__(self, actuator_id, target_bone, axis, max_flexion_angle):
        self.actuator_id = actuator_id
        self.target_bone = target_bone
        self.axis = axis
        self.max_angle = max_flexion_angle

class KinematicEngine:
    def __init__(self):
        self.mechanics = [
            # Arms
            KinematicLink("BICEPS_L", "RADIUS_ULNA_L", "pitch", -130.0),
            KinematicLink("BICEPS_R", "RADIUS_ULNA_R", "pitch", -130.0),
            KinematicLink("TRICEPS_L", "RADIUS_ULNA_L", "pitch", 30.0),   # Extension
            KinematicLink("TRICEPS_R", "RADIUS_ULNA_R", "pitch", 30.0),
            
            # Legs - Important for standing and balance
            KinematicLink("QUADRICEPS_L", "TIBIA_FIBULA_L", "pitch", -120.0),  # Knee extension
            KinematicLink("QUADRICEPS_R", "TIBIA_FIBULA_R", "pitch", -120.0),
            KinematicLink("HAMSTRINGS_L", "TIBIA_FIBULA_L", "pitch", 120.0),   # Knee flexion
            KinematicLink("HAMSTRINGS_R", "TIBIA_FIBULA_R", "pitch", 120.0),
            
            # Ankle (Calf muscles)
            KinematicLink("GASTROCNEMIUS_L", "FOOT_L", "pitch", -45.0),
            KinematicLink("GASTROCNEMIUS_R", "FOOT_R", "pitch", -45.0),
            
            # Neck
            KinematicLink("STERNOCLEIDOMASTOID_L", "CRANIUM", "pitch", 45.0),
            KinematicLink("STERNOCLEIDOMASTOID_R", "CRANIUM", "pitch", 45.0),
            
            # Core
            KinematicLink("RECTUS_ABDOMINIS", "THORACIC_SPINE", "pitch", 30.0),
        ]

    def apply_kinematics(self, musculature_registry, skeletal_registry):
        """
        Apply muscle tension to bone rotations.
        Resets dynamic rotations first, then applies controlled movement.
        """
        # Reset dynamic rotations (keep base posture for feet and clavicles)
        for bone_id, bone in skeletal_registry.items():
            if bone_id not in ["FOOT_L", "FOOT_R", "CLAVICLE_L", "CLAVICLE_R"]:
                bone.rotation = {"pitch": 0.0, "yaw": 0.0, "roll": 0.0}

        # Apply muscle-driven rotations
        for link in self.mechanics:
            muscle = musculature_registry.get(link.actuator_id)
            bone = skeletal_registry.get(link.target_bone)
            
            if muscle and bone:
                applied_angle = muscle.tension * link.max_angle
                if link.axis in bone.rotation:
                    bone.rotation[link.axis] += applied_angle