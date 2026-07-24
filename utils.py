
"""
Shared drawing / helper utilities.
"""

import cv2

COLOR_MAP = {
    "Car": (46, 204, 113),
    "Motorcycle": (241, 196, 15),
    "Bus": (230, 126, 34),
    "Truck": (231, 76, 60),
    "Bicycle": (155, 89, 182),
    "Person": (52, 152, 219),
    "Traffic Light": (149, 165, 166),
    "Stop Sign": (192, 57, 43),
}


def draw_box(frame, bbox, label, track_id=None, extra_text=None):
    x1, y1, x2, y2 = bbox
    color = COLOR_MAP.get(label, (255, 255, 255))
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

    text = f"{label}"
    if track_id is not None:
        text += f" ID:{track_id}"
    if extra_text:
        text += f" {extra_text}"

    (tw, th), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    cv2.rectangle(frame, (x1, y1 - th - 6), (x1 + tw + 4, y1), color, -1)
    cv2.putText(frame, text, (x1 + 2, y1 - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    return frame


def draw_hud(frame, fps, density_level, signal_status):
    h, w = frame.shape[:2]
    overlay_lines = [
        f"FPS: {fps:.1f}",
        f"Density: {density_level}",
        f"Signal: {signal_status['duration']}s (remaining {signal_status['remaining']}s)",
    ]
    if signal_status.get("emergency_active"):
        overlay_lines.append(f"EMERGENCY MODE - Lane {signal_status['emergency_lane']}")

    y = 25
    for line in overlay_lines:
        cv2.putText(frame, line, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        y += 25
    return frame