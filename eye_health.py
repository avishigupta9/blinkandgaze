"""
Eye health scoring using blink + gaze history.
"""

import numpy as np

class EyeHealthModel:
    """
    Combines blink and gaze metrics into an eye strain risk score.
    """

    def __init__(self, baseline):
        """
        baseline: dict with mean/std for each metric
        """
        self.baseline = baseline

    def z(self, value, mean, std):
        return (value - mean) / (std + 1e-6)

    def compute_risk(self, metrics):
        """
        Computes eye strain risk score.

        Higher score = higher strain risk.
        """
        z_blink = self.z(metrics["blink_rate"],
                         self.baseline["blink_rate_mean"],
                         self.baseline["blink_rate_std"])

        z_incomplete = self.z(metrics["incomplete_ratio"],
                              self.baseline["incomplete_ratio_mean"],
                              self.baseline["incomplete_ratio_std"])

        z_fixation = self.z(metrics["fixation_ratio"],
                            self.baseline["fixation_ratio_mean"],
                            self.baseline["fixation_ratio_std"])

        # Blink rate decreases → strain, so invert sign
        risk = (-z_blink) + z_incomplete + z_fixation
        return risk
