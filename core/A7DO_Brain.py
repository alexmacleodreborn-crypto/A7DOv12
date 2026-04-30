# core/A7DO_Brain.py
import numpy as np

class A7DO_Brain:
    def __init__(self, skeleton_manifold, muscular_manifold, articulation_manifold, kinematic_engine, maturation_engine):
        self.skeleton = skeleton_manifold
        self.muscles = muscular_manifold
        self.joints = articulation_manifold
        self.kinematics = kinematic_engine
        self.growth = maturation_engine
        
        self.pulse_count = 0
        self.stability_history = []
        # Learning Parameters
        self.balance_coefficient = 0.1  # Start low, increase as he "learns"

    def set_muscle_tension(self, muscle_id, tension_value):
        """Sets the tension for a specific muscle in the registry."""
        muscle = self.muscles.registry.get(muscle_id)
        if muscle:
            muscle.tension = max(0.0, min(1.0, tension_value))

    def learn_to_stand(self, com, bos):
        """
        Calculates necessary muscle tension to keep CoM over the BoS.
        This is the 'Proprioception' layer[cite: 18].
        """
        if bos['area'] == 0: return

        # Calculate the offset from the center of the feet
        center_x = (bos['min_x'] + bos['max_x']) / 2
        error_x = com[0] - center_x

        # Calculate reactive adjustment based on learning coefficient
        adjustment = abs(error_x) * self.balance_coefficient
        
        # Target specific muscles for balance[cite: 18]
        self.set_muscle_tension("GASTROCNEMIUS_L", adjustment)
        self.set_muscle_tension("GASTROCNEMIUS_R", adjustment)
        self.set_muscle_tension("RECTUS_ABDOMINIS", adjustment * 0.5)

    def _apply_da_vinci_ratios(self, head_ratio, limb_ratio):
        """Adjusts cranium size based on maturation stage[cite: 18]."""
        if "CRANIUM" in self.skeleton.registry:
            self.skeleton.registry["CRANIUM"].dimensions["length"] = 0.12 * head_ratio

    def execute_system_pulse(self):
        """Main biological and physical loop[cite: 18]."""
        self.pulse_count += 1
        
        # 1. Growth & Proportions[cite: 17, 18]
        self.growth.trigger_growth_pulse()
        growth_stats = self.growth.get_physics_state()
        self._apply_da_vinci_ratios(growth_stats["head_ratio"], growth_stats["limb_ratio"])
        
        # 2. Geometry Update[cite: 1, 18]
        self.skeleton.generate_current_geometry(growth_stats["scale_x"])
        
        # 3. Stability Check (Proprioception)
        # These functions come from your physics_utils
        from anatomy.physics_utils import calculate_com, calculate_base_of_support, calculate_stability, apply_gravity_and_mass
        
        apply_gravity_and_mass(self.skeleton.registry, growth_stats["scale_x"])
        com = calculate_com(self.skeleton.registry)
        bos = calculate_base_of_support(self.skeleton.registry)
        stability = calculate_stability(com, bos)
        
        # 4. LEARN: Adjust muscles based on the stability check[cite: 18]
        self.learn_to_stand(com, bos)
        
        # 5. Apply Kinematics[cite: 2, 3, 4, 18]
        self.kinematics.apply_kinematics(self.muscles.registry, self.skeleton.registry)
        self.joints.generate_current_joints(self.skeleton.registry)
        self.muscles.generate_current_musculature(self.skeleton.registry)
        
        self.stability_history.append(stability)
        if len(self.stability_history) > 100: self.stability_history.pop(0)
        
        return self.export_unified_state(growth_stats, com, bos, stability, np.mean(self.stability_history))

    def export_unified_state(self, growth_stats, com, bos, stability, avg_stability):
        """Packages data for the Streamlit dashboard[cite: 18]."""
        bone_data = {bid: {
            "center": b.pos_center,
            "proximal": b.pos_proximal,
            "distal": b.pos_distal,
            "rotation": b.rotation,
            "mass": getattr(b, 'mass', 1.0)
        } for bid, b in self.skeleton.registry.items()}

        muscle_data = {mid: {
            "origin": m.pos_origin_3d,
            "insertion": m.pos_insertion_3d,
            "length": m.current_length,
            "tension": m.tension
        } for mid, m in self.muscles.registry.items()}

        return {
            "status": "PHYSICS_ACTIVE",
            "growth": growth_stats,
            "physics": {
                "skeleton": bone_data,
                "muscles": muscle_data,
                "com": {"x": round(float(com[0]),4), "y": round(float(com[1]),4), "z": round(float(com[2]),4)},
                "bos": bos,
                "stability": stability,
                "avg_stability": avg_stability
            }
        }
