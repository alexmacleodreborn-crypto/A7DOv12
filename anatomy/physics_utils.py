# anatomy/physics_utils.py
import numpy as np

def calculate_com(skeleton_registry):
    """Calculate Center of Mass (CoM) weighted by bone mass"""
    total_mass = 0.0
    com = np.zeros(3)
    
    for bone_id, bone in skeleton_registry.items():
        mass = bone.mass if hasattr(bone, 'mass') else 1.0
        pos = np.array([
            bone.pos_center["x"],
            bone.pos_center["y"],
            bone.pos_center["z"]
        ])
        com += pos * mass
        total_mass += mass
    
    return com / total_mass if total_mass > 0 else np.zeros(3)


def calculate_base_of_support(skeleton_registry):
    """Simple Base of Support: area between both feet"""
    foot_l = skeleton_registry.get("FOOT_L")
    foot_r = skeleton_registry.get("FOOT_R")
    
    if not foot_l or not foot_r:
        return {"min_x": 0, "max_x": 0, "min_z": 0, "max_z": 0, "area": 0}
    
    min_x = min(foot_l.pos_center["x"], foot_r.pos_center["x"])
    max_x = max(foot_l.pos_center["x"], foot_r.pos_center["x"])
    min_z = min(foot_l.pos_center["z"], foot_r.pos_center["z"])
    max_z = max(foot_l.pos_center["z"], foot_r.pos_center["z"])
    
    area = (max_x - min_x) * (max_z - min_z)
    
    return {
        "min_x": min_x, "max_x": max_x,
        "min_z": min_z, "max_z": max_z,
        "area": round(area, 4)
    }


def calculate_stability(com, bos, height_scale=1.0):
    """Stability score: how well CoM is inside Base of Support"""
    if bos["area"] == 0:
        return 0.0
    
    com_x = com[0]
    com_z = com[2]
    
    # Normalized distance from center of BoS
    bos_center_x = (bos["min_x"] + bos["max_x"]) / 2
    bos_center_z = (bos["min_z"] + bos["max_z"]) / 2
    
    dx = abs(com_x - bos_center_x) / (bos["max_x"] - bos["min_x"] + 0.01)
    dz = abs(com_z - bos_center_z) / (bos["max_z"] - bos["min_z"] + 0.01)
    
    stability = max(0.0, 1.0 - (dx + dz))
    return round(stability, 4)


def apply_gravity_and_mass(skeleton_registry, growth_scale):
    """Apply Square-Cube Law mass and prepare for gravity effects"""
    for bone_id, bone in skeleton_registry.items():
        # Base mass at adult scale (x=1.0)
        base_mass = bone.dimensions.get("width", 0.05) * \
                    bone.dimensions.get("depth", 0.05) * \
                    bone.dimensions.get("length", 0.1) * 1000  # rough density
        
        # Apply Square-Cube Law
        bone.mass = base_mass * (growth_scale ** 3)
        bone.gravity_force = bone.mass * 9.81  # Newtons (downward)
