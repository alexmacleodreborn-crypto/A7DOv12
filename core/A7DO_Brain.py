
# A7DOv12 Sentience OS
# File 4: core/A7DO_Brain.py
# Purpose: The Central Nervous System.

import time

class A7DO_Brain:
    def __init__(self, skeleton_manifold, muscular_manifold, articulation_manifold, maturation_engine):
        self.skeleton = skeleton_manifold
        self.muscles = muscular_manifold
        self.joints = articulation_manifold
        self.growth = maturation_engine
        
        self.pulse_count = 0
        self.system_status = "INITIALIZED"

    def _apply_da_vinci_ratios(self, head_ratio, limb_ratio):
        cranium = self.skeleton.registry.get("CRANIUM")
        if cranium:
            cranium.dimensions["length"] = head_ratio * 0.85 
            cranium.offset["y"] = head_ratio * 0.4
            
        mandible = self.skeleton.registry.get("MANDIBLE")
        if mandible: mandible.dimensions["length"] = head_ratio * 0.4

        limb_bones = [
            ("HUMERUS_L", 0.18), ("HUMERUS_R", 0.18),
            ("RADIUS_ULNA_L", 0.15), ("RADIUS_ULNA_R", 0.15),
            ("FEMUR_L", 0.25), ("FEMUR_R", 0.25),
            ("TIBIA_FIBULA_L", 0.22), ("TIBIA_FIBULA_R", 0.22)
        ]
        for bone_id, original_len in limb_bones:
            bone = self.skeleton.registry.get(bone_id)
            if bone: bone.dimensions["length"] = original_len * limb_ratio

    def execute_system_pulse(self):
        self.pulse_count += 1
        
        # 1. TIME & GROWTH
        self.growth.trigger_growth_pulse()
        growth_stats = self.growth.get_physics_state()
        
        # 2. PROPORTIONAL OVERRIDE
        self._apply_da_vinci_ratios(growth_stats["head_ratio"], growth_stats["limb_ratio"])
        
        # 3. SKELETAL 3D CALCULATION
        self.skeleton.generate_current_geometry(growth_stats["scale_x"])
        
        # 4. JOINT 3D CALCULATION (New!)
        self.joints.generate_current_joints(self.skeleton.registry)
        
        # 5. MUSCULAR VECTOR CALCULATION
        self.muscles.generate_current_musculature(self.skeleton.registry)
        
        self.system_status = "SYNCHRONIZED"
        return self.export_unified_state(growth_stats)

    def export_unified_state(self, growth_stats):
        bone_data = {b_id: {"center": b.pos_center, "proximal": b.pos_proximal, "distal": b.pos_distal} for b_id, b in self.skeleton.registry.items()}
        muscle_data = {m_id: {"origin": m.pos_origin_3d, "insertion": m.pos_insertion_3d, "length": m.current_length} for m_id, m in self.muscles.registry.items()}
        joint_data = {j_id: {"pos": j.pos_3d, "type": j.joint_type} for j_id, j in self.joints.registry.items()}
            
        return {
            "status": self.system_status,
            "growth": growth_stats,
            "physics": {"skeleton": bone_data, "muscles": muscle_data, "joints": joint_data},
            "logs": self.growth.milestone_log
        }


