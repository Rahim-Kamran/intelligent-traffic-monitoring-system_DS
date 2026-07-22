{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "f38deda7",
   "metadata": {
    "vscode": {
     "languageId": "plaintext"
    }
   },
   "outputs": [],
   "source": [
    "%%writefile density.py\n",
    "\"\"\"\n",
    "Traffic density classification and lane assignment.\n",
    "\"\"\"\n",
    "\n",
    "from config import DENSITY_THRESHOLDS, DENSITY_COLORS, LANE_BOUNDARIES_FRACTIONS\n",
    "\n",
    "\n",
    "def classify_density(vehicle_count: int) -> str:\n",
    "    for level, (low, high) in DENSITY_THRESHOLDS.items():\n",
    "        if low <= vehicle_count <= high:\n",
    "            return level\n",
    "    return \"Very High\"\n",
    "\n",
    "\n",
    "def density_color(level: str) -> str:\n",
    "    return DENSITY_COLORS.get(level, \"#ffffff\")\n",
    "\n",
    "\n",
    "def assign_lane(cx: float, frame_width: int) -> int:\n",
    "    \"\"\"\n",
    "    Returns lane index (1-based) given a vehicle's x-center and frame width.\n",
    "    \"\"\"\n",
    "    fraction = cx / frame_width\n",
    "    boundaries = LANE_BOUNDARIES_FRACTIONS\n",
    "    for i in range(len(boundaries) - 1):\n",
    "        if boundaries[i] <= fraction < boundaries[i + 1]:\n",
    "            return i + 1\n",
    "    return len(boundaries) - 1\n",
    "\n",
    "\n",
    "def count_per_lane(tracked_objects: list, frame_width: int) -> dict:\n",
    "    counts = {}\n",
    "    for obj in tracked_objects:\n",
    "        lane = assign_lane(obj[\"center\"][0], frame_width)\n",
    "        counts[lane] = counts.get(lane, 0) + 1\n",
    "    return counts"
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
