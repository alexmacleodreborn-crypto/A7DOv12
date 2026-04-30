# anatomy/L01_Anatomical_Manifold.py
# A7DOv12 Sentience OS - Layer 01: Skeletal Chassis with Physics

import math

class AnatomicalNode:
    """
    Enhanced with mass and gravity support for real physics simulation.
    """
    def __init__(self, name, category, anchor, length, width, depth, 
                 offset_x=0.0, offset_y=0.0, offset_z=0.0):
        self.name = name
        self.category = category
        self.anchor = anchor
        
        self.dimensions = {"length": length, "width": width, "depth": depth}
        self.offset = {"x": offset_x, "y": offset_y, "z": offset_z}
        
        self.rotation = {"pitch": 0.0, "yaw": 0.0, "roll": 0.0}
        
        self.pos_center = {"x": 0.0, "y": 0.0, "z": 0.0}
        self.pos_proximal = {"x": 0.0, "y": 0.0, "z": 0.0}
        self.pos_distal = {"x": 0.0, "y": 0.0, "z": 0.0}
        
        # Physics
        self.mass = 1.0
        self.gravity_force = 0.0

    def _rotate_3d(self, vx, vy, vz):
        p, y, r = map(math.radians, (self.rotation["pitch"], self.rotation["yaw"], self.rotation["roll"]))
        
        vy_p = vy * math.cos(p) - vz * math.sin(p)
        vz_p = vy * math.sin(p) + vz * math.cos(p)
        
        vx_y = vx * math.cos(y) + vz_p * math.sin(y)
        vz_y = -vx * math.sin(y) + vz_p * math.cos(y)
        
        vx_r = vx_y * math.cos(r) - vy_p * math.sin(r)
        vy_r = vx_y * math.sin(r) + vy_p * math.cos(r)
        
        return vx_r, vy_r, vz_y

    def calculate_geometry(self, total_height, vitruvian_centers):
        anchor_y = vitruvian_centers[self.anchor] * total_height
        
        self.pos_center = {
            "x": self.offset["x"] * total_height,
            "y": anchor_y + (self.offset["y"] * total_height),
            "z": self.offset["z"] * total_height
        }
        
        half_len = (self.dimensions["length"] * total_height) / 2.0
        
        dx_p, dy_p, dz_p = self._rotate_3d(0, half_len, 0)
        dx_d, dy_d, dz_d = self._rotate_3d(0, -half_len, 0)
        
        self.pos_proximal = {
            "x": self.pos_center["x"] + dx_p,
            "y": self.pos_center["y"] + dy_p,
            "z": self.pos_center["z"] + dz_p
        }
        self.pos_distal = {
            "x": self.pos_center["x"] + dx_d,
            "y": self.pos_center["y"] + dy_d,
            "z": self.pos_center["z"] + dz_d
        }


class BiomechanicalBlueprint:
    def __init__(self):
        self.v_centers = {
            "C3_HEAD": 0.875, "C2_HEART": 0.75, "C4_HANDS": 0.625,
            "C0_NAVEL": 0.60, "C1_GROIN": 0.50, "C5_FEET": 0.05
        }
        
        self.registry = {
            "CRANIUM": AnatomicalNode("Skull", "BONE", "C3_HEAD", 0.12, 0.08, 0.10, offset_y=0.04),
            "MANDIBLE": AnatomicalNode("Jaw", "BONE", "C3_HEAD", 0.05, 0.06, 0.04, offset_y=-0.04, offset_z=0.03),
            "CERVICAL_SPINE": AnatomicalNode("Neck_Spine", "BONE", "C3_HEAD", 0.08, 0.02, 0.02, offset_y=-0.08),
            "THORACIC_SPINE": AnatomicalNode("Upper_Spine", "BONE", "C2_HEART", 0.15, 0.03, 0.03, offset_z=-0.04),
            "STERNUM": AnatomicalNode("Breastbone", "BONE", "C2_HEART", 0.10, 0.03, 0.01, offset_z=0.05),
            "LUMBAR_SPINE": AnatomicalNode("Lower_Spine", "BONE", "C0_NAVEL", 0.10, 0.03, 0.03, offset_z=-0.03),
            "PELVIS": AnatomicalNode("Pelvis", "BONE", "C1_GROIN", 0.12, 0.15, 0.10, offset_y=0.02),
            
            "CLAVICLE_L": AnatomicalNode("Collarbone_L", "BONE", "C2_HEART", 0.08, 0.01, 0.01, offset_x=-0.06, offset_y=0.09),
            "CLAVICLE_R": AnatomicalNode("Collarbone_R", "BONE", "C2_HEART", 0.08, 0.01, 0.01, offset_x=0.06, offset_y=0.09),
            "HUMERUS_L": AnatomicalNode("Upper_Arm_L", "BONE", "C4_HANDS", 0.18, 0.03, 0.03, offset_x=-0.12, offset_y=0.12),
            "HUMERUS_R": AnatomicalNode("Upper_Arm_R", "BONE", "C4_HANDS", 0.18, 0.03, 0.03, offset_x=0.12, offset_y=0.12),
            "RADIUS_ULNA_L": AnatomicalNode("Forearm_L", "BONE", "C4_HANDS", 0.15, 0.02, 0.02, offset_x=-0.12, offset_y=-0.06),
            "RADIUS_ULNA_R": AnatomicalNode("Forearm_R", "BONE", "C4_HANDS", 0.15, 0.02, 0.02, offset_x=0.12, offset_y=-0.06),
            
            "FEMUR_L": AnatomicalNode("Thigh_L", "BONE", "C1_GROIN", 0.25, 0.04, 0.04, offset_x=-0.06, offset_y=-0.10),
            "FEMUR_R": AnatomicalNode("Thigh_R", "BONE", "C1_GROIN", 0.25, 0.04, 0.04, offset_x=0.06, offset_y=-0.10),
            "TIBIA_FIBULA_L": AnatomicalNode("Calf_L", "BONE", "C5_FEET", 0.22, 0.03, 0.03, offset_x=-0.06, offset_y=0.20),
            "TIBIA_FIBULA_R": AnatomicalNode("Calf_R", "BONE", "C5_FEET", 0.22, 0.03, 0.03, offset_x=0.06, offset_y=0.20),
            "FOOT_L": AnatomicalNode("Foot_L", "BONE", "C5_FEET", 0.08, 0.04, 0.08, offset_x=-0.06, offset_z=0.03),
            "FOOT_R": AnatomicalNode("Foot_R", "BONE", "C5_FEET", 0.08, 0.04, 0.08, offset_x=0.06, offset_z=0.03),
        }

        # Resting posture
        self.registry["CLAVICLE_L"].rotation["roll"] = 90.0
        self.registry["CLAVICLE_R"].rotation["roll"] = -90.0
        self.registry["FOOT_L"].rotation["pitch"] = 90.0
        self.registry["FOOT_R"].rotation["pitch"] = 90.0

    def generate_current_geometry(self, total_height):
        for node in self.registry.values():
            node.calculate_geometry(total_height, self.v_centers)
        return self.registry