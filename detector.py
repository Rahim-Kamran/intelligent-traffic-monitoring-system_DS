
"""
YOLOv8-based object detector wrapper.
"""

from ultralytics import YOLO
from config import YOLO_MODEL_PATH, CONFIDENCE_THRESHOLD, IOU_THRESHOLD, ALL_TRACKED_CLASSES


class VehicleDetector:
    def __init__(self, model_path: str = YOLO_MODEL_PATH):
        self.model = YOLO(model_path)
        self.class_names = ALL_TRACKED_CLASSES

    def detect(self, frame):
        """
        Runs detection on a single frame.
        Returns list of dicts: {bbox, conf, class_id, label}
        """
        results = self.model.predict(
            frame,
            conf=CONFIDENCE_THRESHOLD,
            iou=IOU_THRESHOLD,
            classes=list(self.class_names.keys()),
            verbose=False,
        )[0]

        detections = []
        for box in results.boxes:
            cls_id = int(box.cls[0])
            if cls_id not in self.class_names:
                continue
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            conf = float(box.conf[0])
            detections.append({
                "bbox": (int(x1), int(y1), int(x2), int(y2)),
                "conf": conf,
                "class_id": cls_id,
                "label": self.class_names[cls_id],
            })
        return detections