
"""
Smart signal timing logic, with emergency vehicle override.
"""

import time
from config import SIGNAL_TIMING


class SignalController:
    def __init__(self):
        self.current_density_level = "Low"
        self.current_duration = SIGNAL_TIMING["Low"]
        self.timer_start = time.time()
        self.emergency_active = False
        self.emergency_lane = None

    def update(self, density_level: str):
        """Call once per density evaluation cycle (not every frame)."""
        if self.emergency_active:
            return  # emergency override holds priority

        self.current_density_level = density_level
        self.current_duration = SIGNAL_TIMING.get(density_level, SIGNAL_TIMING["Low"])
        self.timer_start = time.time()

    def trigger_emergency(self, lane: int):
        self.emergency_active = True
        self.emergency_lane = lane
        self.timer_start = time.time()
        self.current_duration = 30  # fixed clearance window, tune as needed

    def clear_emergency(self):
        self.emergency_active = False
        self.emergency_lane = None

    def time_remaining(self) -> int:
        elapsed = time.time() - self.timer_start
        remaining = max(0, int(self.current_duration - elapsed))
        return remaining

    def is_green_lane(self, lane: int) -> bool:
        if self.emergency_active:
            return lane == self.emergency_lane
        return True  # simplified: single-approach demo; extend to per-lane phase logic for a full intersection

    def status(self) -> dict:
        return {
            "density_level": self.current_density_level,
            "duration": self.current_duration,
            "remaining": self.time_remaining(),
            "emergency_active": self.emergency_active,
            "emergency_lane": self.emergency_lane,
        }