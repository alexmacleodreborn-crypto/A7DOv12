class DecisionEngine:
    def evaluate(self, env, cog):
        if cog["focus"]:
            return {
                "action": "grab",
                "target": cog["focus"]
            }

        return {"action": "idle"}
