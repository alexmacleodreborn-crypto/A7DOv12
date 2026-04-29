# A7DOv12 Sentience OS
# File: biology/L09_Adaptation.py
# Purpose: Lightweight adaptation memory for repeated stimuli.

class AdaptationEngine:
    """Tracks exposures and converts them to adaptation scores."""

    def __init__(self):
        self.exposure_counts = {}

    def record_exposure(self, key):
        token = str(key)
        self.exposure_counts[token] = self.exposure_counts.get(token, 0) + 1
        return self.exposure_counts[token]

    def adaptation_score(self, key):
        return min(1.0, self.exposure_counts.get(str(key), 0) / 10.0)
