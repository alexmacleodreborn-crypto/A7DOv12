# anatomy/L03_Articulations.py
# A7DOv12 Sentience OS - Layer 03: Joint Definitions

class JointNode:
    """
    Defines connection points between bones.
    """
    def __init__(self, name, parent_bone, child_bone, joint_type="HINGE"):
        self.name = name
        self.parent_bone = parent_bone
        self.child_bone = child_bone
        self.joint_type = joint_type  # HINGE, BALL_SOCKET, FIXED
        
        self.pos_3d = {"x": 0.0, "y": 0.0, "z": 0.0}

    def calculate_hinge_point(self, skeletal_geometry):
        """Joint position = Distal end of parent bone"""
        parent_node = skeletal_geometry.get(self.parent_bone)
        if parent_node:
            self.pos_3d = {
                "x": parent_node.pos_distal["x"],
                "y": parent_node.pos_distal["y"],
                "z": parent_node.pos_distal["z"]
            }


class ArticulationBlueprint:
    """Complete joint registry"""
    def __init__(self):
        self.registry = {
            # Upper body
            "SHOULDER_L": JointNode("Left_Shoulder", "CLAVICLE_L", "HUMERUS_L", "BALL_SOCKET"),
            "SHOULDER_R": JointNode("Right_Shoulder", "CLAVICLE_R", "HUMERUS_R", "BALL_SOCKET"),
            "ELBOW_L": JointNode("Left_Elbow", "HUMERUS_L", "RADIUS_ULNA_L", "HINGE"),
            "ELBOW_R": JointNode("Right_Elbow", "HUMERUS_R", "RADIUS_ULNA_R", "HINGE"),
            
            # Lower body - Critical for standing/walking
            "HIP_L": JointNode("Left_Hip", "PELVIS", "FEMUR_L", "BALL_SOCKET"),
            "HIP_R": JointNode("Right_Hip", "PELVIS", "FEMUR_R", "BALL_SOCKET"),
            "KNEE_L": JointNode("Left_Knee", "FEMUR_L", "TIBIA_FIBULA_L", "HINGE"),
            "KNEE_R": JointNode("Right_Knee", "FEMUR_R", "TIBIA_FIBULA_R", "HINGE"),
            
            # Head & Neck
            "ATLAS_AXIS": JointNode("Neck_Base", "CERVICAL_SPINE", "CRANIUM", "BALL_SOCKET"),
            "JAW_HINGE": JointNode("Jaw_Joint", "CRANIUM", "MANDIBLE", "HINGE")
        }

    def generate_current_joints(self, skeletal_geometry):
        for joint in self.registry.values():
            joint.calculate_hinge_point(skeletal_geometry)
        return self.registry