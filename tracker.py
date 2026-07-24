
"""
Multi-object tracking wrapper using the 'supervision' library's ByteTrack
implementation (avoids needing a separate ByteTrack repo/install).
"""

import numpy as np
import supervision as sv


class VehicleTracker:
    def __init__(self, frame_rate: int = 30):
        self.tracker = sv.ByteTrack(frame_rate=frame_rate)
        self.track_history = {}   # track_id -> list of (cx, cy, frame_idx)

    def update(self, detections: list, frame_idx: int):
        if not detections:
            empty = sv.Detections.empty()
            tracked = self.tracker.update_with_detections(empty)
            return []

        xyxy = np.array([d["bbox"] for d in detections], dtype=float)
        confidence = np.array([d["conf"] for d in detections], dtype=float)
        class_id = np.array([d["class_id"] for d in detections], dtype=int)

        sv_detections = sv.Detections(xyxy=xyxy, confidence=confidence, class_id=class_id)
        tracked = self.tracker.update_with_detections(sv_detections)

        results = []
        for i in range(len(tracked)):
            x1, y1, x2, y2 = tracked.xyxy[i]
            track_id = int(tracked.tracker_id[i])
            cls_id = int(tracked.class_id[i])
            cx, cy = (x1 + x2) / 2, (y1 + y2) / 2

            self.track_history.setdefault(track_id, []).append((cx, cy, frame_idx))
            if len(self.track_history[track_id]) > 50:
                self.track_history[track_id].pop(0)

            results.append({
                "track_id": track_id,
                "bbox": (int(x1), int(y1), int(x2), int(y2)),
                "class_id": cls_id,
                "center": (cx, cy),
                "path": self.track_history[track_id],
            })
        return results

    def get_history(self, track_id):
        return self.track_history.get(track_id, [])