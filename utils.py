{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "52332436",
   "metadata": {
    "vscode": {
     "languageId": "plaintext"
    }
   },
   "outputs": [],
   "source": [
    "%%writefile utils.py\n",
    "\"\"\"\n",
    "Shared drawing / helper utilities.\n",
    "\"\"\"\n",
    "\n",
    "import cv2\n",
    "\n",
    "COLOR_MAP = {\n",
    "    \"Car\": (46, 204, 113),\n",
    "    \"Motorcycle\": (241, 196, 15),\n",
    "    \"Bus\": (230, 126, 34),\n",
    "    \"Truck\": (231, 76, 60),\n",
    "    \"Bicycle\": (155, 89, 182),\n",
    "    \"Person\": (52, 152, 219),\n",
    "    \"Traffic Light\": (149, 165, 166),\n",
    "    \"Stop Sign\": (192, 57, 43),\n",
    "}\n",
    "\n",
    "\n",
    "def draw_box(frame, bbox, label, track_id=None, extra_text=None):\n",
    "    x1, y1, x2, y2 = bbox\n",
    "    color = COLOR_MAP.get(label, (255, 255, 255))\n",
    "    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)\n",
    "\n",
    "    text = f\"{label}\"\n",
    "    if track_id is not None:\n",
    "        text += f\" ID:{track_id}\"\n",
    "    if extra_text:\n",
    "        text += f\" {extra_text}\"\n",
    "\n",
    "    (tw, th), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)\n",
    "    cv2.rectangle(frame, (x1, y1 - th - 6), (x1 + tw + 4, y1), color, -1)\n",
    "    cv2.putText(frame, text, (x1 + 2, y1 - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)\n",
    "    return frame\n",
    "\n",
    "\n",
    "def draw_hud(frame, fps, density_level, signal_status):\n",
    "    h, w = frame.shape[:2]\n",
    "    overlay_lines = [\n",
    "        f\"FPS: {fps:.1f}\",\n",
    "        f\"Density: {density_level}\",\n",
    "        f\"Signal: {signal_status['duration']}s (remaining {signal_status['remaining']}s)\",\n",
    "    ]\n",
    "    if signal_status.get(\"emergency_active\"):\n",
    "        overlay_lines.append(f\"EMERGENCY MODE - Lane {signal_status['emergency_lane']}\")\n",
    "\n",
    "    y = 25\n",
    "    for line in overlay_lines:\n",
    "        cv2.putText(frame, line, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)\n",
    "        y += 25\n",
    "    return frame"
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
