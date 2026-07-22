{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "d3302893",
   "metadata": {
    "vscode": {
     "languageId": "plaintext"
    }
   },
   "outputs": [],
   "source": [
    "%%writefile tracker.py\n",
    "\"\"\"\n",
    "Multi-object tracking wrapper using the 'supervision' library's ByteTrack\n",
    "implementation (avoids needing a separate ByteTrack repo/install).\n",
    "\"\"\"\n",
    "\n",
    "import numpy as np\n",
    "import supervision as sv\n",
    "\n",
    "\n",
    "class VehicleTracker:\n",
    "    def __init__(self, frame_rate: int = 30):\n",
    "        self.tracker = sv.ByteTrack(frame_rate=frame_rate)\n",
    "        self.track_history = {}   # track_id -> list of (cx, cy, frame_idx)\n",
    "\n",
    "    def update(self, detections: list, frame_idx: int):\n",
    "        if not detections:\n",
    "            empty = sv.Detections.empty()\n",
    "            tracked = self.tracker.update_with_detections(empty)\n",
    "            return []\n",
    "\n",
    "        xyxy = np.array([d[\"bbox\"] for d in detections], dtype=float)\n",
    "        confidence = np.array([d[\"conf\"] for d in detections], dtype=float)\n",
    "        class_id = np.array([d[\"class_id\"] for d in detections], dtype=int)\n",
    "\n",
    "        sv_detections = sv.Detections(xyxy=xyxy, confidence=confidence, class_id=class_id)\n",
    "        tracked = self.tracker.update_with_detections(sv_detections)\n",
    "\n",
    "        results = []\n",
    "        for i in range(len(tracked)):\n",
    "            x1, y1, x2, y2 = tracked.xyxy[i]\n",
    "            track_id = int(tracked.tracker_id[i])\n",
    "            cls_id = int(tracked.class_id[i])\n",
    "            cx, cy = (x1 + x2) / 2, (y1 + y2) / 2\n",
    "\n",
    "            self.track_history.setdefault(track_id, []).append((cx, cy, frame_idx))\n",
    "            if len(self.track_history[track_id]) > 50:\n",
    "                self.track_history[track_id].pop(0)\n",
    "\n",
    "            results.append({\n",
    "                \"track_id\": track_id,\n",
    "                \"bbox\": (int(x1), int(y1), int(x2), int(y2)),\n",
    "                \"class_id\": cls_id,\n",
    "                \"center\": (cx, cy),\n",
    "                \"path\": self.track_history[track_id],\n",
    "            })\n",
    "        return results\n",
    "\n",
    "    def get_history(self, track_id):\n",
    "        return self.track_history.get(track_id, [])"
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
