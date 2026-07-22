{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "77c91754",
   "metadata": {
    "vscode": {
     "languageId": "plaintext"
    }
   },
   "outputs": [],
   "source": [
    "%%writefile config.py\n",
    "\"\"\"\n",
    "Central configuration for the Traffic Monitoring System.\n",
    "\"\"\"\n",
    "\n",
    "# --- Model settings ---\n",
    "YOLO_MODEL_PATH = \"yolov8n.pt\"   # nano model — fast, good enough for demo; swap for yolov8m.pt for accuracy\n",
    "CONFIDENCE_THRESHOLD = 0.35\n",
    "IOU_THRESHOLD = 0.45\n",
    "\n",
    "# COCO class IDs relevant to traffic\n",
    "VEHICLE_CLASSES = {\n",
    "    2: \"Car\",\n",
    "    3: \"Motorcycle\",\n",
    "    5: \"Bus\",\n",
    "    7: \"Truck\",\n",
    "    1: \"Bicycle\",\n",
    "}\n",
    "PERSON_CLASS = {0: \"Person\"}\n",
    "TRAFFIC_LIGHT_CLASS = {9: \"Traffic Light\"}\n",
    "STOP_SIGN_CLASS = {11: \"Stop Sign\"}\n",
    "\n",
    "ALL_TRACKED_CLASSES = {**VEHICLE_CLASSES, **PERSON_CLASS, **TRAFFIC_LIGHT_CLASS, **STOP_SIGN_CLASS}\n",
    "\n",
    "# --- Density thresholds (vehicles currently in frame / ROI) ---\n",
    "DENSITY_THRESHOLDS = {\n",
    "    \"Low\": (0, 10),\n",
    "    \"Medium\": (11, 25),\n",
    "    \"High\": (26, 40),\n",
    "    \"Very High\": (41, 10_000),\n",
    "}\n",
    "DENSITY_COLORS = {\n",
    "    \"Low\": \"#2ecc71\",       # green\n",
    "    \"Medium\": \"#f1c40f\",    # yellow\n",
    "    \"High\": \"#e67e22\",      # orange\n",
    "    \"Very High\": \"#e74c3c\", # red\n",
    "}\n",
    "\n",
    "# --- Signal timing map (seconds) keyed by density band ---\n",
    "SIGNAL_TIMING = {\n",
    "    \"Low\": 20,\n",
    "    \"Medium\": 40,\n",
    "    \"High\": 60,\n",
    "    \"Very High\": 90,\n",
    "}\n",
    "\n",
    "# --- Speed estimation ---\n",
    "SPEED_LIMIT_KMPH = 60\n",
    "PIXELS_PER_METER = 8.0     # calibrate this per camera/video — see speed_estimator.py notes\n",
    "FRAME_RATE_ASSUMED = 30\n",
    "\n",
    "# --- Emergency vehicle keywords (used with a secondary classifier/heuristic — see emergency_vehicle.py) ---\n",
    "EMERGENCY_LABELS = [\"ambulance\", \"police\", \"fire truck\"]\n",
    "\n",
    "# --- Database ---\n",
    "DB_PATH = \"traffic.db\"\n",
    "\n",
    "# --- Lanes (as fraction of frame width, left->right boundaries) ---\n",
    "LANE_BOUNDARIES_FRACTIONS = [0.0, 0.33, 0.66, 1.0]  # 3 lanes"
   ]
  }
 ],
 "metadata": {
  "language_info": {
   "name": "python"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
