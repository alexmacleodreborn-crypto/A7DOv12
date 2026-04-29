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

    def execute_system_pulse(self):
        self.pulse_count += 1
        
        # 1. Growth Pulse
        self.growth.trigger_growth_pulse()
        growth_stats = self.growth.get_physics_state()
        
        # 2. Apply Da Vinci proportions
        self._apply_da_vinci_ratios(growth_stats["head_ratio"], growth_stats["limb_ratio"])
        
        # 3. Kinematics (Muscle tension → rotation)
        self.kinematics.apply_kinematics(self.muscles.registry, self.skeleton.registry)
        
        # 4. Update 3D Geometry
        self.skeleton.generate_current_geometry(growth_stats["scale_x"])
        
        # 5. Joint positions
        self.joints.generate_current_joints(self.skeleton.registry)
        
        # 6. Muscle vectors
        self.muscles.generate_current_musculature(self.skeleton.registry)
        
        # === NEW: REAL PHYSICS ===
        apply_gravity_and_mass(self.skeleton.registry, growth_stats["scale_x"])
        
        com = calculate_com(self.skeleton.registry)
        bos = calculate_base_of_support(self.skeleton.registry)
        stability = calculate_stability(com, bos)
        
        self.stability_history.append(stability)
        if len(self.stability_history) > 50:
            self.stability_history.pop(0)
        
        avg_stability = round(sum(self.stability_history) / len(self.stability_history), 4)

        # Detailed Log
        print(f"\n=== A7DO Pulse {self.pulse_count} ===")
        print(f"Growth Stage: {growth_stats['stage']} | Scale: {growth_stats['scale_x']:.3f}")
        print(f"Center of Mass: ({com[0]:.4f}, {com[1]:.4f}, {com[2]:.4f})")
        print(f"Base of Support Area: {bos['area']:.4f}")
        print(f"Instant Stability: {stability:.4f} | Avg Stability: {avg_stability:.4f}")
        print(f"Total Body Mass: {sum(b.mass for b in self.skeleton.registry.values()):.2f} kg")
        
        if stability < 0.3:
            print("WARNING: HIGH RISK OF FALLING!")
        elif stability < 0.6:
            print("Wobbly - Balance challenged")

        return self.export_unified_state(growth_stats, com, bos, stability, avg_stability)

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
            "status": "PHYSICS_ENABLED",
            "growth": growth_stats,
            "physics": {
                "skeleton": bone_data,
                "muscles": muscle_data,
                "joints": {jid: {"pos": j.pos_3d, "type": j.joint_type} for jid, j in self.joints.registry.items()},
                "com": {"x": round(com[0],4), "y": round(com[1],4), "z": round(com[2],4)},
                "bos": bos,
                "stability": stability,
                "avg_stability": avg_stability
            }
        }        # Muscles stretch or compress to match the newly moved bones
        self.muscles.generate_current_musculature(self.skeleton.registry)
        
        self.system_status = "SYNCHRONIZED"
        return self.export_unified_state(growth_stats)

    def export_unified_state(self, growth_stats):
        bone_data = {b_id: {"center": b.pos_center, "proximal": b.pos_proximal, "distal": b.pos_distal, "rotation": b.rotation} for b_id, b in self.skeleton.registry.items()}
        muscle_data = {m_id: {"origin": m.pos_origin_3d, "insertion": m.pos_insertion_3d, "length": m.current_length, "tension": m.tension} for m_id, m in self.muscles.registry.items()}
        joint_data = {j_id: {"pos": j.pos_3d, "type": j.joint_type} for j_id, j in self.joints.registry.items()}
            
        return {
            "status": self.system_status,
            "growth": growth_stats,
            "physics": {"skeleton": bone_data, "muscles": muscle_data, "joints": joint_data},
            "logs": self.growth.milestone_log
        }


