"""
Gaze analysis module using MediaPipe Face Mesh.

Computes relative gaze direction and stability metrics suitable for
long-term eye strain monitoring using a standard webcam.
"""

import numpy as np
from collections import deque
import time

class GazeAnalyzer:
    """
    Computes relative gaze metrics from iris and eye landmarks.
    """

    def __init__(self, window_size=300):
        """
        Args:
            window_size (int): Number of frames used for rolling analysis
        """
        self.window_size = window_size
        self.h_buffer = deque(maxlen=window_size)
        self.v_buffer = deque(maxlen=window_size)
        self.timestamps = deque(maxlen=window_size)

    def compute_normalized_gaze(self, iris, eye_inner, eye_outer, eye_top, eye_bottom):
        """
        Normalizes iris position within the eye region.

        Returns:
            (h, v): normalized horizontal and vertical gaze (0–1)
        """
        h = (iris[0] - eye_inner[0]) / (eye_outer[0] - eye_inner[0] + 1e-6)
        v = (iris[1] - eye_top[1]) / (eye_bottom[1] - eye_top[1] + 1e-6)
        return h, v

    def update(self, h, v):
        """Add gaze sample to rolling buffer."""
        self.h_buffer.append(h)
        self.v_buffer.append(v)
        self.timestamps.append(time.time())

    def get_metrics(self):
        """
        Returns rolling gaze metrics.

        Metrics:
            - gaze_variance
            - fixation_ratio
            - off_center_ratio
        """
        if len(self.h_buffer) < 30:
            return None

        h = np.array(self.h_buffer)
        v = np.array(self.v_buffer)

        gaze_var = np.var(h) + np.var(v)

        center_dist = np.sqrt((h - 0.5)**2 + (v - 0.5)**2)
        fixation_ratio = np.mean(center_dist < 0.05)
        off_center_ratio = np.mean(center_dist > 0.15)

        return {
            "gaze_variance": gaze_var,
            "fixation_ratio": fixation_ratio,
            "off_center_ratio": off_center_ratio
        }
