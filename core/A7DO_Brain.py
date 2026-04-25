
# A7DOv12 Sentience OS - Fresh Build
# File 4: core/A7DO_Brain.py
# Purpose: The Central Nervous System.
# Logic: Enforces the deterministic flow of data: Growth -> Skeleton -> Muscles.

import time

class A7DO_Brain:
    """
    The Master Coordinator for the A7DOv12 Manifold.
    Ensures absolute mathematical sync between Growth, Bones, and Actuators.
    """
    def __init__(self, skeleton_manifold, muscular_manifold, maturation_engine):
        # Attach the core biological systems
        self.skeleton = skeleton_manifold
        self.muscles = muscular_manifold
        self.growth = maturation_engine
        
        self.pulse_count = 0
        self.system_status = "INITIALIZED"

    def _apply_da_vinci_ratios(self, head_ratio, limb_ratio):
        """
        Dynamically alters the base blueprints of the skeleton 
        before 3D calculation, enforcing the baby-to-adult morphological shift.
        """
        # 1. Adjust Cranium (Head size shrinks relative to body as it grows)
        cranium = self.skeleton.segments.get("CRANIUM")
        if cranium:
            # Override base length to match exact Da Vinci head ratio
            cranium.base_length_ratio = head_ratio * 0.85 
            cranium.offset["y"] = head_ratio * 0.4
            
        mandible = self.skeleton.segments.get("MANDIBLE")
        if mandible:
            mandible.base_length_ratio = head_ratio * 0.4

        # 2. Adjust Limbs (Limbs lengthen relative to body as it grows)
        limb_bones = [
            ("HUMERUS_L", 0.18), ("HUMERUS_R", 0.18),
            ("RADIUS_ULNA_L", 0.15), ("RADIUS_ULNA_R", 0.15),
            ("FEMUR_L", 0.25), ("FEMUR_R", 0.25),
            ("TIBIA_FIBULA_L", 0.22), ("TIBIA_FIBULA_R", 0.22)
        ]
        
        for bone_id, original_base_ratio in limb_bones:
            bone = self.skeleton.segments.get(bone_id)
            if bone:
                # Apply the developmental limb_scalar to the adult base ratio
                bone.base_length_ratio = original_base_ratio * limb_ratio

    def execute_system_pulse(self):
        """
        The Master Heartbeat. 
        Executes the mathematical chain reaction in strict deterministic order.
        """
        self.pulse_count += 1
        
        # --- STEP 1: TIME & GROWTH ---
        # Advance the biological clock and retrieve current scaling physics
        self.growth.trigger_growth_pulse()
        growth_stats = self.growth.get_physics_state()
        
        total_height = growth_stats["scale_x"]
        
        # --- STEP 2: PROPORTIONAL OVERRIDE ---
        # Modify the skeletal blueprint using current Da Vinci ratios
        self._apply_da_vinci_ratios(
            head_ratio=growth_stats["head_ratio"], 
            limb_ratio=growth_stats["limb_ratio"]
        )
        
        # --- STEP 3: SKELETAL 3D CALCULATION ---
        # Resolve all center, proximal, and distal coordinates in absolute 3D space
        self.skeleton.calculate_current_posture(total_height)
        
        # --- STEP 4: MUSCULAR VECTOR CALCULATION ---
        # Snap the 640 muscles to the exact 3D proximal/distal points we just calculated
        self.muscles.generate_current_musculature(self.skeleton.segments)
        
        # --- STEP 5: EXPORT MANIFOLD ---
        self.system_status = "SYNCHRONIZED"
        return self.export_unified_state(growth_stats)

    def export_unified_state(self, growth_stats):
        """
        Packages the absolute 3D coordinates into a strict dictionary.
        The UI (app.py) will do NO math; it will only draw what this Brain outputs.
        """
        # Package Skeleton
        bone_data = {}
        for b_id, b_node in self.skeleton.segments.items():
            bone_data[b_id] = {
                "center": b_node.world_center,
                "proximal": b_node.end_proximal,
                "distal": b_node.end_distal
            }
            
        # Package Muscles
        muscle_data = {}
        for m_id, m_node in self.muscles.registry.items():
            muscle_data[m_id] = {
                "origin": m_node.pos_origin_3d,
                "insertion": m_node.pos_insertion_3d,
                "length": m_node.current_length,
                "tension": m_node.tension
            }
            
        return {
            "status": self.system_status,
            "pulse_count": self.pulse_count,
            "growth": growth_stats,
            "physics": {
                "skeleton": bone_data,
                "muscles": muscle_data
            },
            "logs": self.growth.milestone_log
        }
