# app.py
# A7DOv12 Sentience OS - Main Runner
# Runs full organism loop: growth → kinematics → physics → stability

import time

# --- IMPORT YOUR SYSTEM ---
from core.A7DO_Brain import A7DO_Brain

# Anatomy Layers (adjust paths if needed)
from anatomy.L01_Skeleton import SkeletonManifold
from anatomy.L02_Musculature import MusculatureManifold
from anatomy.L03_Articulation import ArticulationManifold
from anatomy.L04_Kinematics import KinematicEngine
from anatomy.L00_Maturation import MaturationEngine


# --- INITIALISE SYSTEM ---

def build_a7do():
    print("Initializing A7DO System...")

    skeleton = SkeletonManifold()
    muscles = MusculatureManifold()
    joints = ArticulationManifold()
    kinematics = KinematicEngine()
    growth = MaturationEngine()

    brain = A7DO_Brain(
        skeleton_manifold=skeleton,
        muscular_manifold=muscles,
        articulation_manifold=joints,
        kinematic_engine=kinematics,
        maturation_engine=growth
    )

    print("A7DO Initialized Successfully\n")
    return brain


# --- SIMPLE MOTOR PATTERNS (so it actually moves) ---

def apply_basic_motor_pattern(brain, pulse):
    """
    Simple oscillating muscle inputs to test balance + kinematics
    """

    import math

    # Arms swing
    brain.set_muscle_tension("BICEPS_L", (math.sin(pulse * 0.1) + 1) / 2)
    brain.set_muscle_tension("BICEPS_R", (math.cos(pulse * 0.1) + 1) / 2)

    # Legs (basic alternating pattern)
    brain.set_muscle_tension("QUADRICEPS_L", (math.sin(pulse * 0.08) + 1) / 2)
    brain.set_muscle_tension("QUADRICEPS_R", (math.cos(pulse * 0.08) + 1) / 2)

    brain.set_muscle_tension("HAMSTRINGS_L", (math.cos(pulse * 0.08) + 1) / 2)
    brain.set_muscle_tension("HAMSTRINGS_R", (math.sin(pulse * 0.08) + 1) / 2)

    # Core stabilisation
    brain.set_muscle_tension("RECTUS_ABDOMINIS", 0.3)


# --- MAIN LOOP ---

def run_simulation():
    brain = build_a7do()

    MAX_PULSES = 500
    DELAY = 0.1  # seconds

    print("Starting simulation...\n")

    for pulse in range(MAX_PULSES):

        # 1. Apply motor inputs
        apply_basic_motor_pattern(brain, pulse)

        # 2. Run full system
        state = brain.execute_system_pulse()

        # 3. Optional: access structured data
        stability = state["physics"]["stability"]
        com = state["physics"]["com"]

        # Lightweight output (you already get detailed logs from brain)
        print(f"[Pulse {pulse}] Stability: {stability:.3f} | CoM Y: {com['y']:.3f}")

        # 4. Slow it down so you can observe
        time.sleep(DELAY)

    print("\nSimulation complete.")


# --- ENTRY POINT ---

if __name__ == "__main__":
    run_simulation()