class Perception:
    def get_state(self):
        # fake object detection
        return {
            "objects": [
                {"id": "obj_1", "type": "cube"}
            ]
        }
