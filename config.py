
"""
Central configuration for the Traffic Monitoring System.
"""

# --- Model settings ---
YOLO_MODEL_PATH = "yolov8n.pt"   # nano model — fast, good enough for demo; swap for yolov8m.pt for accuracy
CONFIDENCE_THRESHOLD = 0.35
IOU_THRESHOLD = 0.45

# COCO class IDs relevant to traffic
VEHICLE_CLASSES = {
    2: "Car",
    3: "Motorcycle",
    5: "Bus",
    7: "Truck",
    1: "Bicycle",
}
PERSON_CLASS = {0: "Person"}
TRAFFIC_LIGHT_CLASS = {9: "Traffic Light"}
STOP_SIGN_CLASS = {11: "Stop Sign"}

ALL_TRACKED_CLASSES = {**VEHICLE_CLASSES, **PERSON_CLASS, **TRAFFIC_LIGHT_CLASS, **STOP_SIGN_CLASS}

# --- Density thresholds (vehicles currently in frame / ROI) ---
DENSITY_THRESHOLDS = {
    "Low": (0, 10),
    "Medium": (11, 25),
    "High": (26, 40),
    "Very High": (41, 10_000),
}
DENSITY_COLORS = {
    "Low": "#2ecc71",       # green
    "Medium": "#f1c40f",    # yellow
    "High": "#e67e22",      # orange
    "Very High": "#e74c3c", # red
}

# --- Signal timing map (seconds) keyed by density band ---
SIGNAL_TIMING = {
    "Low": 20,
    "Medium": 40,
    "High": 60,
    "Very High": 90,
}

# --- Speed estimation ---
SPEED_LIMIT_KMPH = 60
PIXELS_PER_METER = 8.0     # calibrate this per camera/video — see speed_estimator.py notes
FRAME_RATE_ASSUMED = 30

# --- Emergency vehicle keywords (used with a secondary classifier/heuristic — see emergency_vehicle.py) ---
EMERGENCY_LABELS = ["ambulance", "police", "fire truck"]

# --- Database ---
DB_PATH = "traffic.db"

# --- Lanes (as fraction of frame width, left->right boundaries) ---
LANE_BOUNDARIES_FRACTIONS = [0.0, 0.33, 0.66, 1.0]  # 3 lanes