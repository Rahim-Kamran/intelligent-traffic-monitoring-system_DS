
"""
Traffic density classification and lane assignment.
"""

from config import DENSITY_THRESHOLDS, DENSITY_COLORS, LANE_BOUNDARIES_FRACTIONS


def classify_density(vehicle_count: int) -> str:
    for level, (low, high) in DENSITY_THRESHOLDS.items():
        if low <= vehicle_count <= high:
            return level
    return "Very High"


def density_color(level: str) -> str:
    return DENSITY_COLORS.get(level, "#ffffff")


def assign_lane(cx: float, frame_width: int) -> int:
    """
    Returns lane index (1-based) given a vehicle's x-center and frame width.
    """
    fraction = cx / frame_width
    boundaries = LANE_BOUNDARIES_FRACTIONS
    for i in range(len(boundaries) - 1):
        if boundaries[i] <= fraction < boundaries[i + 1]:
            return i + 1
    return len(boundaries) - 1


def count_per_lane(tracked_objects: list, frame_width: int) -> dict:
    counts = {}
    for obj in tracked_objects:
        lane = assign_lane(obj["center"][0], frame_width)
        counts[lane] = counts.get(lane, 0) + 1
    return counts