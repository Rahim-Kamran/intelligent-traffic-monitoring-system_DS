{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "60f583f8",
   "metadata": {
    "vscode": {
     "languageId": "plaintext"
    }
   },
   "outputs": [],
   "source": [
    "%%writefile emergency_vehicle.py\n",
    "\"\"\"\n",
    "Emergency vehicle detection heuristic.\n",
    "\n",
    "NOTE: The pretrained COCO YOLOv8 model does NOT have \"ambulance\" / \"police\" /\n",
    "\"fire truck\" classes — it only knows generic \"car\"/\"truck\"/\"bus\". A real\n",
    "system needs a fine-tuned classifier (e.g. a second-stage CNN on cropped\n",
    "detections) trained on labeled emergency vehicle images. This module provides\n",
    "the integration point/interface for that model; wire in a trained classifier\n",
    "here when you have one.\n",
    "\"\"\"\n",
    "\n",
    "from config import EMERGENCY_LABELS\n",
    "\n",
    "\n",
    "class EmergencyVehicleDetector:\n",
    "    def __init__(self, classifier=None):\n",
    "        \"\"\"\n",
    "        classifier: optional callable(cropped_image) -> label:str\n",
    "        If None, this module is a no-op stub (always returns False) —\n",
    "        replace with a trained model for real emergency detection.\n",
    "        \"\"\"\n",
    "        self.classifier = classifier\n",
    "\n",
    "    def check(self, cropped_image) -> str | None:\n",
    "        if self.classifier is None:\n",
    "            return None\n",
    "        label = self.classifier(cropped_image)\n",
    "        if label and label.lower() in EMERGENCY_LABELS:\n",
    "            return label\n",
    "        return None"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "vscode": {
     "languageId": "plaintext"
    }
   },
   "outputs": [],
   "source": []
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
