%%writefile README.md
# 🚦 AI-Based Intelligent Traffic Monitoring and Smart Traffic Signal Management System

A final-year Smart City engineering project that combines **Computer Vision**, **Machine Learning**, and **real-time analytics** to monitor live traffic, dynamically manage signal timing, prioritize emergency vehicles, detect violations, and forecast short-term traffic volume — all through a professional Streamlit dashboard.

![Status](https://img.shields.io/badge/status-in--development-orange)
![Python](https://img.shields.io/badge/python-3.12-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 📌 Overview

Traditional traffic signals run on fixed timers regardless of actual road conditions, leading to unnecessary congestion, delayed emergency vehicle passage, and no automated way to catch violations. This system replaces that with an AI-driven pipeline that:

- Detects and tracks vehicles in real time using **YOLOv8** + **ByteTrack**
- Classifies traffic density per lane and **dynamically adjusts signal timing**
- Detects **emergency vehicles** and overrides the signal to give them priority
- Estimates vehicle **speed** and flags overspeeding
- Logs **red-light violations, wrong-lane driving, and illegal parking**
- Forecasts traffic volume 5–10 minutes ahead using **ML models** (Random Forest, XGBoost, Linear Regression)
- Presents everything through a **modern dark-themed Streamlit dashboard**

---

## 🖥️ Live Demo (Dashboard)

The dashboard currently runs on simulated/dummy data and is fully functional standalone — AI modules connect to it as a data source without changing the UI.

Run locally:
```bash
streamlit run app.py
```

Run from Google Colab (via tunnel):
```bash
!streamlit run app.py --server.port 8501 --server.headless true &
!npx localtunnel --port 8501
```

---

## 🏗️ System Architecture

```
Camera Feed
    │
    ▼
detector.py  (YOLOv8 — vehicle/person/traffic-light detection)
    │
    ▼
tracker.py  (ByteTrack — persistent unique IDs across frames)
    │
    ├──► density.py         → traffic density classification + lane assignment
    ├──► speed_estimator.py → vehicle speed from pixel displacement
    ├──► emergency_vehicle.py → ambulance/police/fire truck detection
    ├──► red_light_violation.py / wrong_lane.py / parking_detection.py
    │
    ▼
signal_controller.py  (adaptive signal timing + emergency override)
    │
    ▼
database.py  (SQLite — all events, logs, violations)
    │
    ▼
prediction.py  (ML forecasting — Random Forest / XGBoost / Linear Regression)
    │
    ▼
app.py  (Streamlit Dashboard — visualizes everything above)
```

---

## 📂 Project Structure

```
TrafficMonitoringSystem/
│
├── app.py                    # Main Streamlit dashboard (7 pages)
├── detector.py                # YOLOv8 detection wrapper
├── tracker.py                 # ByteTrack multi-object tracking
├── density.py                 # Density classification + lane assignment
├── signal_controller.py       # Adaptive signal timing logic
├── speed_estimator.py         # Pixel-displacement speed estimation
├── emergency_vehicle.py       # Emergency vehicle detection hook
├── lane_detection.py          # Virtual lane boundary logic
├── red_light_violation.py     # Red-light violation detection
├── wrong_lane.py               # Wrong-direction driving detection
├── parking_detection.py       # Illegal/stationary parking detection
├── analytics.py                # Report generation (CSV/Excel/PDF)
├── prediction.py               # ML traffic volume forecasting
├── database.py                 # SQLite schema + CRUD operations
├── config.py                   # Central configuration (thresholds, paths, timing)
├── utils.py                    # Drawing / HUD overlay helpers
├── requirements.txt
├── README.md
├── traffic.db                  # SQLite database (auto-created)
│
├── models/                     # YOLOv8 weights
├── videos/                     # Input traffic footage
├── datasets/                   # Training data (Metro Interstate Traffic Volume)
├── reports/                    # Generated CSV/Excel/PDF reports
├── charts/                     # Exported chart images
└── screenshots/                # Violation evidence screenshots
```

---

## ⚙️ Tech Stack

| Category | Technologies |
|---|---|
| **AI / Computer Vision** | YOLOv8 (Ultralytics), ByteTrack, OpenCV |
| **Backend / Logic** | Python 3.12, NumPy, Pandas |
| **Machine Learning** | Scikit-Learn, Random Forest, XGBoost, Linear Regression |
| **Database** | SQLite |
| **Dashboard / Visualization** | Streamlit, Plotly, Matplotlib |
| **Image Handling** | Pillow |

---

## 🧩 Module Reference

| File | Responsibility |
|---|---|
| `detector.py` | Runs pretrained YOLOv8 COCO model to detect cars, trucks, buses, motorcycles, bicycles, pedestrians, traffic lights, and stop signs. |
| `tracker.py` | Wraps ByteTrack to assign each detected vehicle a persistent ID and maintain its movement history across frames. |
| `density.py` | Classifies live traffic into **Low / Medium / High / Very High** bands and assigns each vehicle to one of 3 virtual lanes. |
| `signal_controller.py` | Calculates green-signal duration from current density band; supports emergency override to force a lane green. |
| `speed_estimator.py` | Estimates real-world speed (km/h) from tracked pixel displacement; flags vehicles exceeding the configured limit. |
| `emergency_vehicle.py` | Integration point for a fine-tuned classifier to detect ambulances, police vehicles, and fire trucks (COCO alone can't distinguish these). |
| `red_light_violation.py` | Flags vehicles crossing the stop line while the signal is red; stores a screenshot, timestamp, and vehicle ID. |
| `wrong_lane.py` | Detects vehicles moving against the expected traffic direction. |
| `parking_detection.py` | Flags vehicles that remain stationary beyond a configured time threshold. |
| `database.py` | Manages the SQLite schema and all read/write operations across 7 tables. |
| `analytics.py` | Generates downloadable CSV, Excel, and PDF traffic reports. |
| `prediction.py` | Trains and serves ML models on the Metro Interstate Traffic Volume dataset to forecast near-term traffic volume and recommend signal timing. |
| `utils.py` | Shared drawing utilities — bounding boxes, labels, and live HUD overlay (FPS, density, signal timer). |
| `config.py` | Single source of truth for thresholds, class mappings, signal timing rules, and file paths. |

---

## 🗄️ Database Schema

SQLite database (`traffic.db`) with 7 tables:

| Table | Stores |
|---|---|
| `vehicle_events` | Every counted vehicle — track ID, type, lane, timestamp |
| `density_log` | Vehicle count + density level over time |
| `speed_log` | Per-vehicle speed readings and overspeed flags |
| `violations` | Violation type, track ID, screenshot path, timestamp |
| `signal_log` | Signal duration decisions and their triggering density level |
| `prediction_log` | ML forecast outputs and horizon |
| `emergency_log` | Detected emergency vehicles and the lane they were given priority in |

---

## 📊 Dashboard Pages

The Streamlit dashboard (`app.py`) has a dark-themed sidebar with 7 pages:

1. **📊 Dashboard** — Live KPI cards (Total Vehicles, Cars, Bus, Truck, Bike, Avg Speed, Density, Signal Status, Emergency Status) plus Vehicle Distribution, Hourly Traffic, Density Trend, and Lane-wise Count charts.
2. **🎥 Live Detection** — Live camera feed panel with bounding boxes/tracking IDs (once AI modules are connected), frame stats, and a real-time detected-objects table.
3. **📈 Analytics** — Deeper breakdowns: vehicle distribution, hourly pattern with peak-hour detection, density trend, average speed vs. speed limit, lane-wise comparison, and a weekly traffic heatmap.
4. **📄 Reports** — Filterable violation log with CSV/Excel/PDF export and a report summary table.
5. **🔮 Prediction** — ML-based short-term traffic forecast, model selector (Random Forest / XGBoost / Linear Regression), and historical-vs-predicted comparison chart.
6. **⚙️ Settings** — Configure detection thresholds, YOLO model choice, class filters, signal timing rules, speed limit, calibration, and alert preferences.
7. **ℹ️ About** — Project summary and system architecture diagram.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.12
- pip

### Installation
```bash
git clone <repo-url>
cd TrafficMonitoringSystem
pip install -r requirements.txt
```

### Run the dashboard
```bash
streamlit run app.py
```

### Run detection on a video (core pipeline)
```bash
python -c "
from detector import VehicleDetector
from tracker import VehicleTracker
# See project notebook / main loop for full example
"
```

---

## 🔧 Configuration

All tunable parameters live in `config.py`:

- `CONFIDENCE_THRESHOLD`, `IOU_THRESHOLD` — YOLO detection sensitivity
- `DENSITY_THRESHOLDS` — vehicle-count ranges for Low/Medium/High/Very High
- `SIGNAL_TIMING` — green-light duration per density band
- `SPEED_LIMIT_KMPH`, `PIXELS_PER_METER` — speed estimation and overspeed threshold
- `LANE_BOUNDARIES_FRACTIONS` — virtual lane boundary positions

> ⚠️ **Calibration note:** `PIXELS_PER_METER` must be calibrated against your actual camera footage (e.g. using a known lane width) before speed readings are accurate.

---

## 🧠 Machine Learning

Traffic volume prediction is trained on the **Metro Interstate Traffic Volume Dataset**, comparing:

- Random Forest
- XGBoost
- Linear Regression

Outputs: predicted volume for the next 5 and 10 minutes, and a recommended signal duration.

---

## ⚠️ Known Limitations

- The pretrained YOLOv8 COCO model does **not** natively distinguish ambulances/police/fire trucks from regular cars/trucks — `emergency_vehicle.py` is an integration hook that needs a fine-tuned classifier for real emergency detection.
- Speed estimation accuracy depends entirely on correct `PIXELS_PER_METER` calibration per camera.
- Current signal logic is simplified for a single-approach demo; a full multi-approach intersection needs per-lane phase sequencing.

---

## 🛣️ Future Scope

- Multi-junction coordinated signal control
- Real CCTV/RTSP stream integration
- Mobile app for citizens and traffic police
- Fine-tuned emergency vehicle classifier
- Edge deployment (Jetson/Raspberry Pi) for on-site real-time processing

---

## 📜 License

This project is developed for academic purposes as a final-year university project.

---

## 🙌 Acknowledgements

- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)
- [ByteTrack](https://github.com/ifzhang/ByteTrack) / [Supervision](https://github.com/roboflow/supervision)
- Metro Interstate Traffic Volume Dataset (UCI Machine Learning Repository)
