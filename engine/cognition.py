class Cognition:
    def update(self, env):
        # minimal memory simulation
        return {
            "focus": env["objects"][0] if env["objects"] else None
        }
