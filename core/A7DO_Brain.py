# core/A7DO_Brain.py
import numpy as np
from anatomy.physics_utils import calculate_com, calculate_base_of_support, calculate_stability, apply_gravity_and_mass

class A7DO_Brain:
    def __init__(self, skeleton_manifold, muscular_manifold, articulation_manifold, kinematic_engine, maturation_engine):
        self.skeleton = skeleton_manifold
        self.muscles = muscular_manifold
        self.joints = articulation_manifold
        self.kinematics = kinematic_engine
        self.growth = maturation_engine
        
        self.pulse_count = 0
        self.stability_history = []

    def set_muscle_tension(self, muscle_id, tension_value):
        muscle = self.muscles.registry.get(muscle_id)
        if muscle:
            muscle.tension = max(0.0, min(1.0, tension_value))

    def execute_system_pulse(self):
        self.pulse_count += 1
        
        # 1. Growth
        self.growth.trigger_growth_pulse()
        growth_stats = self.growth.get_physics_state()
        
        # 2. Apply proportions from growth
        self._apply_da_vinci_ratios(growth_stats["head_ratio"], growth_stats["limb_ratio"])
        
        # 3. Kinematics: Muscle tension → bone rotation
        self.kinematics.apply_kinematics(self.muscles.registry, self.skeleton.registry)
        
        # 4. Update skeleton geometry
        self.skeleton.generate_current_geometry(growth_stats["scale_x"])
        
        # 5. Update joints
        self.joints.generate_current_joints(self.skeleton.registry)
        
        # 6. Update muscle vectors
        self.muscles.generate_current_musculature(self.skeleton.registry)
        
        # 7. Physics: Mass, Gravity, CoM, Stability
        apply_gravity_and_mass(self.skeleton.registry, growth_stats["scale_x"])
        
        com = calculate_com(self.skeleton.registry)
        bos = calculate_base_of_support(self.skeleton.registry)
        stability = calculate_stability(com, bos)
        
        self.stability_history.append(stability)
        if len(self.stability_history) > 100:
            self.stability_history.pop(0)
        
        avg_stability = round(sum(self.stability_history) / len(self.stability_history), 4)

        # Detailed Console Log
        print(f"\n=== A7DO Pulse {self.pulse_count} | Stage: {growth_stats['stage']} ===")
        print(f"Height Scale: {growth_stats['scale_x']:.3f} | Mass: {sum(b.mass for b in self.skeleton.registry.values()):.1f} kg")
        print(f"CoM: ({com[0]:.4f}, {com[1]:.4f}, {com[2]:.4f})")
        print(f"BoS Area: {bos['area']:.4f} | Stability: {stability:.3f} (Avg: {avg_stability:.3f})")
        
        if stability < 0.4:
            print("*** HIGH FALL RISK - Agent is unstable! ***")
        elif stability < 0.65:
            print("Wobbly stance - Balance is challenged")

        return self.export_unified_state(growth_stats, com, bos, stability, avg_stability)

    def _apply_da_vinci_ratios(self, head_ratio, limb_ratio):
        # Simple proportion adjustment
        if "CRANIUM" in self.skeleton.registry:
            self.skeleton.registry["CRANIUM"].dimensions["length"] = 0.12 * head_ratio

    def export_unified_state(self, growth_stats, com, bos, stability, avg_stability):
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
                "joints": {jid: {"pos": j.pos_3d, "type": j.joint_type} for jid, j in self.joints.registry.items()},
                "com": {"x": round(float(com[0]),4), "y": round(float(com[1]),4), "z": round(float(com[2]),4)},
                "bos": bos,
                "stability": stability,
                "avg_stability": avg_stability
            }
        }