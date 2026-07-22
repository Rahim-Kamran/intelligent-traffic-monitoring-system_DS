{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "3d022e19",
   "metadata": {
    "vscode": {
     "languageId": "plaintext"
    }
   },
   "outputs": [],
   "source": [
    "%%writefile signal_controller.py\n",
    "\"\"\"\n",
    "Smart signal timing logic, with emergency vehicle override.\n",
    "\"\"\"\n",
    "\n",
    "import time\n",
    "from config import SIGNAL_TIMING\n",
    "\n",
    "\n",
    "class SignalController:\n",
    "    def __init__(self):\n",
    "        self.current_density_level = \"Low\"\n",
    "        self.current_duration = SIGNAL_TIMING[\"Low\"]\n",
    "        self.timer_start = time.time()\n",
    "        self.emergency_active = False\n",
    "        self.emergency_lane = None\n",
    "\n",
    "    def update(self, density_level: str):\n",
    "        \"\"\"Call once per density evaluation cycle (not every frame).\"\"\"\n",
    "        if self.emergency_active:\n",
    "            return  # emergency override holds priority\n",
    "\n",
    "        self.current_density_level = density_level\n",
    "        self.current_duration = SIGNAL_TIMING.get(density_level, SIGNAL_TIMING[\"Low\"])\n",
    "        self.timer_start = time.time()\n",
    "\n",
    "    def trigger_emergency(self, lane: int):\n",
    "        self.emergency_active = True\n",
    "        self.emergency_lane = lane\n",
    "        self.timer_start = time.time()\n",
    "        self.current_duration = 30  # fixed clearance window, tune as needed\n",
    "\n",
    "    def clear_emergency(self):\n",
    "        self.emergency_active = False\n",
    "        self.emergency_lane = None\n",
    "\n",
    "    def time_remaining(self) -> int:\n",
    "        elapsed = time.time() - self.timer_start\n",
    "        remaining = max(0, int(self.current_duration - elapsed))\n",
    "        return remaining\n",
    "\n",
    "    def is_green_lane(self, lane: int) -> bool:\n",
    "        if self.emergency_active:\n",
    "            return lane == self.emergency_lane\n",
    "        return True  # simplified: single-approach demo; extend to per-lane phase logic for a full intersection\n",
    "\n",
    "    def status(self) -> dict:\n",
    "        return {\n",
    "            \"density_level\": self.current_density_level,\n",
    "            \"duration\": self.current_duration,\n",
    "            \"remaining\": self.time_remaining(),\n",
    "            \"emergency_active\": self.emergency_active,\n",
    "            \"emergency_lane\": self.emergency_lane,\n",
    "        }"
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
