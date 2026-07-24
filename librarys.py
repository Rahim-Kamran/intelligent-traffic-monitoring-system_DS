# CELL 1: Install dependencies
# !pip install -q ultralytics opencv-python-headless supervision pandas numpy \
    plotly matplotlib scikit-learn pillow streamlit sqlalchemy openpyxl fpdf2

import os
os.makedirs("TrafficMonitoringSystem/models", exist_ok=True)
os.makedirs("TrafficMonitoringSystem/videos", exist_ok=True)
os.makedirs("TrafficMonitoringSystem/reports", exist_ok=True)
os.makedirs("TrafficMonitoringSystem/charts", exist_ok=True)
os.makedirs("TrafficMonitoringSystem/screenshots", exist_ok=True)
os.chdir("TrafficMonitoringSystem")
print("Project directory ready:", os.getcwd())

from google.colab import files
uploaded = files.upload()   # upload a short traffic clip (mp4)
video_path = list(uploaded.keys())[0]
print("Using video:", video_path)


import cv2
import time
from detector import VehicleDetector
from tracker import VehicleTracker
from density import classify_density, count_per_lane, assign_lane
from signal_controller import SignalController
from speed_estimator import estimate_speed, is_overspeed
from database import Database
from utils import draw_box, draw_hud
from config import VEHICLE_CLASSES

detector = VehicleDetector()
tracker = VehicleTracker()
signal_ctrl = SignalController()
db = Database()

cap = cv2.VideoCapture(video_path)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps_video = cap.get(cv2.CAP_PROP_FPS) or 30

out_path = "output_annotated.mp4"
writer = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*"mp4v"), fps_video, (frame_width, frame_height))

frame_idx = 0
counted_ids = set()
DENSITY_EVAL_INTERVAL = 15  # frames between density/signal re-evaluations

prev_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame_idx += 1

    detections = detector.detect(frame)
    tracked = tracker.update(detections, frame_idx)

    # --- Draw boxes + speed + logging ---
    for obj in tracked:
        label = VEHICLE_CLASSES.get(obj["class_id"], None)
        if label is None:
            continue  # skip person/traffic-light/stop-sign boxes for vehicle-only logic below (drawn separately if desired)

        speed = estimate_speed(obj["path"], frame_rate=fps_video)
        overspeed = is_overspeed(speed)
        extra = f"{speed:.0f}km/h" + (" OVERSPEED" if overspeed else "")
        draw_box(frame, obj["bbox"], label, obj["track_id"], extra)

        if obj["track_id"] not in counted_ids:
            counted_ids.add(obj["track_id"])
            lane = assign_lane(obj["center"][0], frame_width)
            db.log_vehicle_event(obj["track_id"], label, lane)

        if speed > 0:
            db.log_speed(obj["track_id"], label, speed, overspeed)

    # --- Density + signal update every N frames ---
    if frame_idx % DENSITY_EVAL_INTERVAL == 0:
        vehicle_count = len([o for o in tracked if o["class_id"] in VEHICLE_CLASSES])
        level = classify_density(vehicle_count)
        signal_ctrl.update(level)
        db.log_density(vehicle_count, level)
        db.log_signal(level, signal_ctrl.current_duration)

    # --- HUD ---
    now = time.time()
    fps_display = 1.0 / max(now - prev_time, 1e-6)
    prev_time = now
    draw_hud(frame, fps_display, signal_ctrl.current_density_level, signal_ctrl.status())

    writer.write(frame)

    if frame_idx % 50 == 0:
        print(f"Processed frame {frame_idx}")

cap.release()
writer.release()
print("Done. Annotated video saved to:", out_path)





import pandas as pd
import plotly.express as px

cols, rows = db.fetch_all("vehicle_events")
df = pd.DataFrame(rows, columns=cols)

if not df.empty:
    fig = px.pie(df, names="vehicle_type", title="Vehicle Type Distribution")
    fig.show()

    # Get the value counts and reset the index
    lane_counts_df = df["lane"].value_counts().reset_index()
    # Rename the columns to be explicit:
    # 'index' column contains the lane numbers
    # 'lane' column (from value_counts()) contains the vehicle counts
    lane_counts_df.columns = ['lane_number', 'vehicle_count']

    fig2 = px.bar(lane_counts_df, x="lane_number", y="vehicle_count",
                   labels={"lane_number": "Lane", "vehicle_count": "Vehicle Count"}, title="Vehicles per Lane")
    fig2.show()
else:
    print("No vehicle events logged yet — run Cell 12 on a video first.")


!pip install -q pyngrok
from pyngrok import ngrok

# Free account bana ke token lo: https://dashboard.ngrok.com/get-started/your-authtoken
ngrok.set_auth_token("3GktcP6XTOZJGETHsH3DPDemhCs_5QpAybvjq6YUYurCZhq9H")

# Kill any existing tunnels
ngrok.kill()

public_url = ngrok.connect(8501)
print("🚀 Dashboard live at:", public_url)


!kill -9 $(lsof -t -i:8501) 2>/dev/null
!streamlit run app.py --server.port 8501 --server.headless true > streamlit_log.txt 2>&1 &
import time
time.sleep(10)
!cat streamlit_log.txt


