# engine/heartbeat.py

import time

class Heartbeat:
    def __init__(self, perception, cognition, decision, interaction):
        self.perception = perception
        self.cognition = cognition
        self.decision = decision
        self.interaction = interaction

        self.state = {
            "env": {},
            "cog": {},
            "decision": {},
            "interaction": {}
        }

    def tick(self):
        # 1. Perception
        env_data = self.perception.get_state()

        # 2. Cognitive update
        cog_state = self.cognition.update(env_data)

        # 3. Decision
        decision = self.decision.evaluate(env_data, cog_state)

        # 4. Interaction / Action
        interaction = self.interaction.update(env_data, decision)

        # 5. Store unified state
        self.state = {
            "env": env_data,
            "cog": cog_state,
            "decision": decision,
            "interaction": interaction
        }

        return self.state

    def run(self, hz=2):
        interval = 1.0 / hz

        while True:
            state = self.tick()

            print("\n--- A7DO STATE ---")
            print(state)

            time.sleep(interval)
