# A7DOv12 Sentience OS
# File: anatomy/L01_Anatomical_Manifold.py
# Purpose: The Absolute 3D Mathematical Blueprint of the Human Anatomy with Physics

import math
import numpy as np

class AnatomicalNode:
    """
    Enhanced AnatomicalNode with mass and gravity support for real physics.
    """
    def __init__(self, name, category, anchor, length, width, depth, 
                 offset_x=0.0, offset_y=0.0, offset_z=0.0):
        self.name = name
        self.category = category  # BONE, ORGAN, NEURAL
        self.anchor = anchor      # C0 to C5 Vitruvian Anchor
        
        # 3D Shape
        self.dimensions = {"length": length, "width": width, "depth": depth}
        
        # Local offset from anchor
        self.offset = {"x": offset_x, "y": offset_y, "z": offset_z}
        
        # Rotation
        self.rotation = {"pitch": 0.0, "yaw": 0.0, "roll": 0.0}
        
        # 3D Positions
        self.pos_center = {"x": 0.0, "y": 0.0, "z": 0.0}
        self.pos_proximal = {"x": 0.0, "y": 0.0, "z": 0.0}
        self.pos_distal = {"x": 0.0, "y": 0.0, "z": 0.0}
        
        # Physics properties
        self.mass = 1.0
        self.gravity_force = 0.0

    def _rotate_3d(self, vx, vy, vz):
        """Apply pitch, yaw, roll rotations"""
        p, y, r = map(math.radians, (self.rotation["pitch"], self.rotation["yaw"], self.rotation["roll"]))
        
        # Pitch (X)
        vy_p = vy * math.cos(p) - vz * math.sin(p)
        vz_p = vy * math.sin(p) + vz * math.cos(p)
        # Yaw (Y)
        vx_y = vx * math.cos(y) + vz_p * math.sin(y)
        vz_y = -vx * math.sin(y) + vz_p * math.cos(y)
        # Roll (Z)
        vx_r = vx_y * math.cos(r) - vy_p * math.sin(r)
        vy_r = vx_y * math.sin(r) + vy_p * math.cos(r)
        
        return vx_r, vy_r, vz_y

    def calculate_geometry(self, total_height, vitruvian_centers):
        """Calculate absolute 3D positions"""
        anchor_y = vitruvian_centers[self.anchor] * total_height
        
        # Center position
        self.pos_center["x"] = self.offset["x"] * total_height
        self.pos_center["y"] = anchor_y + (self.offset["y"] * total_height)
        self.pos_center["z"] = self.offset["z"] * total_height
        
        # Half length for proximal/distal
        half_len = (self.dimensions["length"] * total_height) / 2.0
        
        # Apply rotation
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
    """Master Anatomical Registry with Vitruvian Centers"""
    def __init__(self):
        self.v_centers = {
            "C3_HEAD": 0.875, 
            "C2_HEART": 0.75, 
            "C4_HANDS": 0.625,
            "C0_NAVEL": 0.60, 
            "C1_GROIN": 0.50, 
            "C5_FEET": 0.05
        }
        
        self.registry = {
            # Head & Neck
            "CRANIUM": AnatomicalNode("Skull", "BONE", "C3_HEAD", length=0.12, width=0.08, depth=0.10, offset_y=0.04),
            "MANDIBLE": AnatomicalNode("Jaw", "BONE", "C3_HEAD", length=0.05, width=0.06, depth=0.04, offset_y=-0.04, offset_z=0.03),
            "CERVICAL_SPINE": AnatomicalNode("Neck_Spine", "BONE", "C3_HEAD", length=0.08, width=0.02, depth=0.02, offset_y=-0.08),
            
            # Torso
            "THORACIC_SPINE": AnatomicalNode("Upper_Spine", "BONE", "C2_HEART", length=0.15, width=0.03, depth=0.03, offset_z=-0.04),
            "STERNUM": AnatomicalNode("Breastbone", "BONE", "C2_HEART", length=0.10, width=0.03, depth=0.01, offset_z=0.05),
            "LUMBAR_SPINE": AnatomicalNode("Lower_Spine", "BONE", "C0_NAVEL", length=0.10, width=0.03, depth=0.03, offset_z=-0.03),
            "PELVIS": AnatomicalNode("Pelvis", "BONE", "C1_GROIN", length=0.12, width=0.15, depth=0.10, offset_y=0.02),
            
            # Arms
            "CLAVICLE_L": AnatomicalNode("Collarbone_L", "BONE", "C2_HEART", length=0.08, width=0.01, depth=0.01, offset_x=-0.06, offset_y=0.09),
            "CLAVICLE_R": AnatomicalNode("Collarbone_R", "BONE", "C2_HEART", length=0.08, width=0.01, depth=0.01, offset_x=0.06, offset_y=0.09),
            "HUMERUS_L": AnatomicalNode("Upper_Arm_L", "BONE", "C4_HANDS", length=0.18, width=0.03, depth=0.03, offset_x=-0.12, offset_y=0.12),
            "HUMERUS_R": AnatomicalNode("Upper_Arm_R", "BONE", "C4_HANDS", length=0.18, width=0.03, depth=0.03, offset_x=0.12, offset_y=0.12),
            "RADIUS_ULNA_L": AnatomicalNode("Forearm_L", "BONE", "C4_HANDS", length=0.15, width=0.02, depth=0.02, offset_x=-0.12, offset_y=-0.06),
            "RADIUS_ULNA_R": AnatomicalNode("Forearm_R", "BONE", "C4_HANDS", length=0.15, width=0.02, depth=0.02, offset_x=0.12, offset_y=-0.06),
            
            # Legs
            "FEMUR_L": AnatomicalNode("Thigh_L", "BONE", "C1_GROIN", length=0.25, width=0.04, depth=0.04, offset_x=-0.06, offset_y=-0.10),
            "FEMUR_R": AnatomicalNode("Thigh_R", "BONE", "C1_GROIN", length=0.25, width=0.04, depth=0.04, offset_x=0.06, offset_y=-0.10),
            "TIBIA_FIBULA_L": AnatomicalNode("Calf_L", "BONE", "C5_FEET", length=0.22, width=0.03, depth=0.03, offset_x=-0.06, offset_y=0.20),
            "TIBIA_FIBULA_R": AnatomicalNode("Calf_R", "BONE", "C5_FEET", length=0.22, width=0.03, depth=0.03, offset_x=0.06, offset_y=0.20),
            "FOOT_L": AnatomicalNode("Foot_L", "BONE", "C5_FEET", length=0.08, width=0.04, depth=0.08, offset_x=-0.06, offset_z=0.03),
            "FOOT_R": AnatomicalNode("Foot_R", "BONE", "C5_FEET", length=0.08, width=0.04, depth=0.08, offset_x=0.06, offset_z=0.03),
        }

        # Initial resting posture
        self.registry["CLAVICLE_L"].rotation["roll"] = 90.0
        self.registry["CLAVICLE_R"].rotation["roll"] = -90.0
        self.registry["FOOT_L"].rotation["pitch"] = 90.0
        self.registry["FOOT_R"].rotation["pitch"] = 90.0

    def generate_current_geometry(self, total_height):
        """Update all bone positions"""
        for node in self.registry.values():
            node.calculate_geometry(total_height, self.v_centers)
        return self.registry
