
"""
Emergency vehicle detection heuristic.

NOTE: The pretrained COCO YOLOv8 model does NOT have "ambulance" / "police" /
"fire truck" classes — it only knows generic "car"/"truck"/"bus". A real
system needs a fine-tuned classifier (e.g. a second-stage CNN on cropped
detections) trained on labeled emergency vehicle images. This module provides
the integration point/interface for that model; wire in a trained classifier
here when you have one.
"""

from config import EMERGENCY_LABELS


class EmergencyVehicleDetector:
    def __init__(self, classifier=None):
        """
        classifier: optional callable(cropped_image) -> label:str
        If None, this module is a no-op stub (always returns False) —
        replace with a trained model for real emergency detection.
        """
        self.classifier = classifier

    def check(self, cropped_image) -> str | None:
        if self.classifier is None:
            return None
        label = self.classifier(cropped_image)
        if label and label.lower() in EMERGENCY_LABELS:
            return label
        return None