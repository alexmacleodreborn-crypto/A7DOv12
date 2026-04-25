
# A7DOv12 Sentience OS
# File: anatomy/L03_Articulations.py
# Purpose: The absolute mathematical hinges between skeletal segments.
# Logic: Fuses the Proximal end of a Child to the Distal end of a Parent.

class JointNode:
    """
    Mathematical definition of an articulation point.
    """
    def __init__(self, name, parent_bone, child_bone, joint_type="HINGE"):
        self.name = name
        self.parent_bone = parent_bone  # The bone closer to the core
        self.child_bone = child_bone    # The bone further from the core
        self.joint_type = joint_type    # HINGE (1-axis), BALL_SOCKET (3-axis), FIXED
        
        # Absolute 3D Location of the joint
        self.pos_3d = {"x": 0.0, "y": 0.0, "z": 0.0}

    def calculate_hinge_point(self, skeletal_geometry):
        """
        Finds the exact 3D coordinate where these two bones connect.
        It anchors to the Distal end of the Parent bone.
        """
        parent_node = skeletal_geometry.get(self.parent_bone)
        if parent_node:
            self.pos_3d = {
                "x": parent_node.pos_distal["x"],
                "y": parent_node.pos_distal["y"],
                "z": parent_node.pos_distal["z"]
            }

class ArticulationBlueprint:
    """The complete registry of A7DOv12 Joints."""
    def __init__(self):
        self.registry = {
            # --- UPPER BODY JOINTS ---
            "SHOULDER_L": JointNode("Left_Shoulder", "CLAVICLE_L", "HUMERUS_L", "BALL_SOCKET"),
            "SHOULDER_R": JointNode("Right_Shoulder", "CLAVICLE_R", "HUMERUS_R", "BALL_SOCKET"),
            "ELBOW_L": JointNode("Left_Elbow", "HUMERUS_L", "RADIUS_ULNA_L", "HINGE"),
            "ELBOW_R": JointNode("Right_Elbow", "HUMERUS_R", "RADIUS_ULNA_R", "HINGE"),
            
            # --- LOWER BODY JOINTS ---
            "HIP_L": JointNode("Left_Hip", "PELVIS", "FEMUR_L", "BALL_SOCKET"),
            "HIP_R": JointNode("Right_Hip", "PELVIS", "FEMUR_R", "BALL_SOCKET"),
            "KNEE_L": JointNode("Left_Knee", "FEMUR_L", "TIBIA_FIBULA_L", "HINGE"),
            "KNEE_R": JointNode("Right_Knee", "FEMUR_R", "TIBIA_FIBULA_R", "HINGE"),
            
            # --- SPINAL & CRANIAL JOINTS ---
            "ATLAS_AXIS": JointNode("Neck_Base", "CERVICAL_SPINE", "CRANIUM", "BALL_SOCKET"),
            "JAW_HINGE": JointNode("Jaw_Joint", "CRANIUM", "MANDIBLE", "HINGE")
        }

    def generate_current_joints(self, skeletal_geometry):
        """Calculates the 3D coordinates for every joint."""
        for joint_id, joint in self.registry.items():
            joint.calculate_hinge_point(skeletal_geometry)
        return self.registry

