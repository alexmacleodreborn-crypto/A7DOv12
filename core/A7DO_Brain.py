# core/A7DO_Brain.py

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

    def learn_to_stand(self, com, bos):
        """
        Calculates necessary muscle tension to keep CoM over the BoS.
        This is the 'Proprioception' layer.
        """
        if bos['area'] == 0: return

        # Calculate the offset from the center of the feet
        center_x = (bos['min_x'] + bos['max_x']) / 2
        error_x = com[0] - center_x

        # If leaning too far forward or back, activate calves/shins
        # This tension is fed back into the Kinematic Engine
        adjustment = abs(error_x) * self.balance_coefficient
        
        # Target specific muscles for balance
        self.set_muscle_tension("GASTROCNEMIUS_L", adjustment)
        self.set_muscle_tension("GASTROCNEMIUS_R", adjustment)
        self.set_muscle_tension("RECTUS_ABDOMINIS", adjustment * 0.5)

    def execute_system_pulse(self):
        self.pulse_count += 1
        
        # 1. Growth & Proportions
        self.growth.trigger_growth_pulse()[cite: 17]
        growth_stats = self.growth.get_physics_state()[cite: 17]
        self._apply_da_vinci_ratios(growth_stats["head_ratio"], growth_stats["limb_ratio"])[cite: 18]
        
        # 2. Physics & Gravity
        # Higher scale = higher mass = harder to stand (Square-Cube Law)
        apply_gravity_and_mass(self.skeleton.registry, growth_stats["scale_x"])[cite: 5]
        
        # 3. Geometry Update
        self.skeleton.generate_current_geometry(growth_stats["scale_x"])[cite: 1, 18]
        
        # 4. Stability Check (Proprioception)
        com = calculate_com(self.skeleton.registry)[cite: 5]
        bos = calculate_base_of_support(self.skeleton.registry)[cite: 5]
        stability = calculate_stability(com, bos)[cite: 5]
        
        # 5. LEARN: Adjust muscles based on the stability check
        self.learn_to_stand(com, bos)
        
        # 6. Apply Kinematics (Move the bones based on new tension)
        self.kinematics.apply_kinematics(self.muscles.registry, self.skeleton.registry)[cite: 4, 18]
        self.joints.generate_current_joints(self.skeleton.registry)[cite: 3]
        self.muscles.generate_current_musculature(self.skeleton.registry)[cite: 2]
        
        self.stability_history.append(stability)
        if len(self.stability_history) > 100: self.stability_history.pop(0)
        
        return self.export_unified_state(growth_stats, com, bos, stability, np.mean(self.stability_history))
