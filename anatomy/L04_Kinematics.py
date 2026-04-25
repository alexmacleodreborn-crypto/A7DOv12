
# A7DOv12 Sentience OS
# File 6: anatomy/L04_Kinematics.py
# Purpose: Absolute translation of Muscle Tension to Bone Rotation.
# Logic: Tension (0.0 to 1.0) * Max Range of Motion = Exact Angle.

class KinematicLink:
    """Mathematical mapping between an actuator, a joint axis, and a bone."""
    def __init__(self, actuator_id, target_bone, axis, max_flexion_angle):
        self.actuator_id = actuator_id          # e.g., "BICEPS_L"
        self.target_bone = target_bone          # e.g., "RADIUS_ULNA_L"
        self.axis = axis                        # "pitch", "yaw", "roll"
        self.max_angle = max_flexion_angle      # Maximum degrees of rotation

class KinematicEngine:
    """The deterministic gear-system of A7DOv12."""
    def __init__(self):
        # The absolute mapping of cause-and-effect
        self.mechanics = [
            # ARMS (Flexing the elbow)
            KinematicLink("BICEPS_L", "RADIUS_ULNA_L", "pitch", -130.0),
            KinematicLink("BICEPS_R", "RADIUS_ULNA_R", "pitch", -130.0),
            
            # LEGS (Bending the knee)
            KinematicLink("HAMSTRINGS_L", "TIBIA_FIBULA_L", "pitch", 120.0),
            KinematicLink("HAMSTRINGS_R", "TIBIA_FIBULA_R", "pitch", 120.0),
            
            # HEAD/NECK (Nodding via Sternocleidomastoid)
            KinematicLink("STERNOCLEIDOMASTOID_L", "CRANIUM", "pitch", 45.0),
            KinematicLink("STERNOCLEIDOMASTOID_R", "CRANIUM", "pitch", 45.0),
            
            # CORE (Crunches via Abs)
            KinematicLink("RECTUS_ABDOMINIS", "THORACIC_SPINE", "pitch", 30.0)
        ]

    def apply_kinematics(self, musculature_registry, skeletal_registry):
        """
        Reads all muscle tensions and physically rotates the target bones.
        This runs BEFORE the skeleton calculates its 3D coordinates.
        """
        # 1. Reset dynamic rotations to 0 (so limbs don't spin infinitely)
        # We skip feet and clavicles to preserve their base Vitruvian resting posture
        for bone_id, bone in skeletal_registry.items():
            if bone_id not in ["FOOT_L", "FOOT_R", "CLAVICLE_L", "CLAVICLE_R"]:
                bone.rotation = {"pitch": 0.0, "yaw": 0.0, "roll": 0.0}

        # 2. Apply deterministic rotation based on tension
        for link in self.mechanics:
            muscle = musculature_registry.get(link.actuator_id)
            bone = skeletal_registry.get(link.target_bone)
            
            if muscle and bone:
                # Math: Tension (0 to 1) * Max Angle (e.g., 130) = Current Angle
                applied_angle = muscle.tension * link.max_angle
                bone.rotation[link.axis] += applied_angle
