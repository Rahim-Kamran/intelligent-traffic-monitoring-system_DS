{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "fb045c82",
   "metadata": {
    "vscode": {
     "languageId": "plaintext"
    }
   },
   "outputs": [],
   "source": [
    "%%writefile speed_estimator.py\n",
    "\"\"\"\n",
    "Simple speed estimation from tracked pixel displacement.\n",
    "\n",
    "IMPORTANT CALIBRATION NOTE:\n",
    "Pixel-to-meter conversion (PIXELS_PER_METER) must be calibrated per camera\n",
    "by measuring a known real-world distance (e.g. lane width ~3.5m, or distance\n",
    "between two road markings) in pixels in your actual video. The default value\n",
    "is a placeholder and will NOT give accurate real-world speeds until calibrated.\n",
    "\"\"\"\n",
    "\n",
    "from config import PIXELS_PER_METER, FRAME_RATE_ASSUMED, SPEED_LIMIT_KMPH\n",
    "\n",
    "\n",
    "def estimate_speed(path: list, frame_rate: int = FRAME_RATE_ASSUMED,\n",
    "                    pixels_per_meter: float = PIXELS_PER_METER) -> float:\n",
    "    \"\"\"\n",
    "    path: list of (cx, cy, frame_idx) tuples from tracker history.\n",
    "    Returns speed in km/h based on displacement over the last N frames.\n",
    "    \"\"\"\n",
    "    if len(path) < 2:\n",
    "        return 0.0\n",
    "\n",
    "    (x1, y1, f1) = path[0]\n",
    "    (x2, y2, f2) = path[-1]\n",
    "    frame_diff = f2 - f1\n",
    "    if frame_diff <= 0:\n",
    "        return 0.0\n",
    "\n",
    "    pixel_dist = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5\n",
    "    meters = pixel_dist / pixels_per_meter\n",
    "    seconds = frame_diff / frame_rate\n",
    "    if seconds <= 0:\n",
    "        return 0.0\n",
    "\n",
    "    mps = meters / seconds\n",
    "    kmph = mps * 3.6\n",
    "    return round(kmph, 1)\n",
    "\n",
    "\n",
    "def is_overspeed(speed_kmph: float, limit: float = SPEED_LIMIT_KMPH) -> bool:\n",
    "    return speed_kmph > limit"
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
