# engine/interaction_engine.py

class InteractionEngine:
    def __init__(self):
        self.state = {
            "active_action": None,
            "target_object": None,
            "grip_strength": 0.0,
            "holding": False
        }

    def update(self, perception, decision):
        """
        perception: dict with detected objects
        decision: dict with chosen action
        """

        if decision["action"] == "grab":
            target = decision.get("target")

            if target:
                self.state["active_action"] = "grab"
                self.state["target_object"] = target

                # simple grip logic
                self.state["grip_strength"] += 0.1

                if self.state["grip_strength"] > 0.5:
                    self.state["holding"] = True

        else:
            self.reset()

        return self.state

    def reset(self):
        self.state = {
            "active_action": None,
            "target_object": None,
            "grip_strength": 0.0,
            "holding": False
        }
