
"""
Simple speed estimation from tracked pixel displacement.

IMPORTANT CALIBRATION NOTE:
Pixel-to-meter conversion (PIXELS_PER_METER) must be calibrated per camera
by measuring a known real-world distance (e.g. lane width ~3.5m, or distance
between two road markings) in pixels in your actual video. The default value
is a placeholder and will NOT give accurate real-world speeds until calibrated.
"""

from config import PIXELS_PER_METER, FRAME_RATE_ASSUMED, SPEED_LIMIT_KMPH


def estimate_speed(path: list, frame_rate: int = FRAME_RATE_ASSUMED,
                    pixels_per_meter: float = PIXELS_PER_METER) -> float:
    """
    path: list of (cx, cy, frame_idx) tuples from tracker history.
    Returns speed in km/h based on displacement over the last N frames.
    """
    if len(path) < 2:
        return 0.0

    (x1, y1, f1) = path[0]
    (x2, y2, f2) = path[-1]
    frame_diff = f2 - f1
    if frame_diff <= 0:
        return 0.0

    pixel_dist = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    meters = pixel_dist / pixels_per_meter
    seconds = frame_diff / frame_rate
    if seconds <= 0:
        return 0.0

    mps = meters / seconds
    kmph = mps * 3.6
    return round(kmph, 1)


def is_overspeed(speed_kmph: float, limit: float = SPEED_LIMIT_KMPH) -> bool:
    return speed_kmph > limit