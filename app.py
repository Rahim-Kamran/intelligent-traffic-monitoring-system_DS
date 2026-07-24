
"""
AI-Based Intelligent Traffic Monitoring and Smart Traffic Signal Management System
Main Streamlit Dashboard

Currently running on dummy/simulated data. Live AI modules (detector.py,
tracker.py, density.py, etc.) will be wired into the "Live Detection" page
and the dummy-data generators below will be swapped for database.py reads
in a later pass.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import random

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Smart Traffic Control System",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# DARK THEME CSS
# ============================================================
CUSTOM_CSS = """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .stApp {
        background: linear-gradient(180deg, #0b0f19 0%, #0d1220 100%);
        color: #e6e9f0;
    }

    section[data-testid="stSidebar"] {
        background: #0a0e17;
        border-right: 1px solid #1c2333;
    }
    section[data-testid="stSidebar"] .stRadio label {
        font-size: 15px;
    }

    h1, h2, h3, h4 {
        color: #f2f4f8 !important;
        font-family: 'Segoe UI', sans-serif;
    }

    /* KPI card */
    .kpi-card {
        background: linear-gradient(145deg, #131a2b, #0f1524);
        border: 1px solid #232b40;
        border-radius: 14px;
        padding: 18px 20px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.35);
        transition: transform 0.15s ease;
    }
    .kpi-card:hover {
        transform: translateY(-3px);
        border-color: #3b82f6;
    }
    .kpi-label {
        font-size: 13px;
        color: #8b94ab;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 30px;
        font-weight: 700;
        color: #f2f4f8;
    }
    .kpi-icon {
        font-size: 26px;
        margin-bottom: 4px;
    }
    .kpi-sub {
        font-size: 12px;
        color: #5fd68a;
        margin-top: 4px;
    }

    .status-pill {
        display: inline-block;
        padding: 6px 16px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 14px;
    }

    .section-title {
        font-size: 20px;
        font-weight: 700;
        margin-top: 10px;
        margin-bottom: 14px;
        color: #f2f4f8;
        border-left: 4px solid #3b82f6;
        padding-left: 10px;
    }

    .panel {
        background: #0f1524;
        border: 1px solid #1c2333;
        border-radius: 14px;
        padding: 18px;
    }

    div[data-testid="stMetricValue"] {
        color: #f2f4f8;
    }

    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
    }

    .footer-tag {
        text-align: center;
        color: #4b5470;
        font-size: 12px;
        margin-top: 40px;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ============================================================
# PLOTLY DARK TEMPLATE
# ============================================================
PLOTLY_TEMPLATE = "plotly_dark"
PLOT_BG = "#0f1524"
PAPER_BG = "#0f1524"
GRID_COLOR = "#1c2333"

def style_fig(fig, height=350):
    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        plot_bgcolor=PLOT_BG,
        paper_bgcolor=PAPER_BG,
        font=dict(color="#c8cede", family="Segoe UI"),
        height=height,
        margin=dict(l=10, r=10, t=45, b=10),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    fig.update_xaxes(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR)
    fig.update_yaxes(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR)
    return fig

DENSITY_COLORS = {
    "Low": "#2ecc71",
    "Medium": "#f1c40f",
    "High": "#e67e22",
    "Very High": "#e74c3c",
}
VEHICLE_COLORS = {
    "Car": "#3b82f6",
    "Bike": "#f1c40f",
    "Bus": "#e67e22",
    "Truck": "#e74c3c",
}

# ============================================================
# DUMMY DATA GENERATORS
# (These are the integration points — later swapped for database.py reads)
# ============================================================

@st.cache_data(ttl=5)
def generate_kpis():
    cars = random.randint(120, 220)
    bikes = random.randint(60, 140)
    bus = random.randint(5, 25)
    truck = random.randint(10, 40)
    total = cars + bikes + bus + truck
    avg_speed = round(random.uniform(28, 58), 1)
    density = random.choice(["Low", "Medium", "High", "Very High"])
    signal = random.choice(["GREEN", "YELLOW", "RED"])
    emergency = random.choice([False, False, False, False, True])
    return {
        "total": total, "cars": cars, "bikes": bikes, "bus": bus, "truck": truck,
        "avg_speed": avg_speed, "density": density, "signal": signal, "emergency": emergency,
    }

@st.cache_data(ttl=30)
def generate_hourly_traffic():
    hours = [f"{h:02d}:00" for h in range(24)]
    base = [30, 20, 15, 12, 18, 35, 80, 150, 190, 160, 130, 140,
            150, 145, 135, 150, 175, 200, 210, 170, 120, 90, 60, 40]
    values = [max(5, b + random.randint(-20, 20)) for b in base]
    return pd.DataFrame({"Hour": hours, "Vehicles": values})

@st.cache_data(ttl=30)
def generate_density_trend():
    now = datetime.now()
    times = [(now - timedelta(minutes=5 * i)).strftime("%H:%M") for i in range(30)][::-1]
    counts = np.clip(np.cumsum(np.random.randn(30)) * 3 + 25, 2, 60).astype(int)
    levels = []
    for c in counts:
        if c <= 10: levels.append("Low")
        elif c <= 25: levels.append("Medium")
        elif c <= 40: levels.append("High")
        else: levels.append("Very High")
    return pd.DataFrame({"Time": times, "VehicleCount": counts, "Density": levels})

@st.cache_data(ttl=30)
def generate_speed_data():
    now = datetime.now()
    times = [(now - timedelta(minutes=2 * i)).strftime("%H:%M") for i in range(20)][::-1]
    speeds = np.clip(np.random.normal(45, 10, 20), 15, 90)
    return pd.DataFrame({"Time": times, "AvgSpeed": speeds.round(1)})

@st.cache_data(ttl=30)
def generate_lane_counts():
    lanes = ["Lane 1", "Lane 2", "Lane 3"]
    counts = [random.randint(15, 60) for _ in lanes]
    return pd.DataFrame({"Lane": lanes, "VehicleCount": counts})

@st.cache_data(ttl=30)
def generate_vehicle_distribution(kpis):
    return pd.DataFrame({
        "Type": ["Car", "Bike", "Bus", "Truck"],
        "Count": [kpis["cars"], kpis["bikes"], kpis["bus"], kpis["truck"]],
    })

@st.cache_data(ttl=60)
def generate_violation_log():
    types = ["Red Light Violation", "Wrong Lane", "Illegal Parking", "Overspeed"]
    rows = []
    now = datetime.now()
    for i in range(15):
        rows.append({
            "ID": f"V{1000+i}",
            "Type": random.choice(types),
            "Vehicle ID": random.randint(1, 300),
            "Time": (now - timedelta(minutes=random.randint(1, 500))).strftime("%Y-%m-%d %H:%M:%S"),
            "Location": random.choice(["Junction A", "Junction B", "Main St", "Ring Rd"]),
        })
    return pd.DataFrame(rows).sort_values("Time", ascending=False)

@st.cache_data(ttl=60)
def generate_prediction_data():
    now = datetime.now()
    future_times = [(now + timedelta(minutes=5 * i)).strftime("%H:%M") for i in range(1, 7)]
    predicted = np.clip(np.cumsum(np.random.randn(6)) * 4 + 90, 20, 220).astype(int)
    return pd.DataFrame({"Time": future_times, "PredictedVolume": predicted})

# ============================================================
# SIDEBAR NAVIGATION
# ============================================================
with st.sidebar:
    st.markdown("## 🚦 TrafficAI")
    st.markdown("###### Smart Traffic Control System")
    st.markdown("---")
    page = st.radio(
        "Navigation",
        ["📊 Dashboard", "🎥 Live Detection", "📈 Analytics", "📄 Reports", "🔮 Prediction", "⚙️ Settings", "ℹ️ About"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown("###### System Status")
    st.markdown("🟢 **Online** — Simulated Feed")
    st.caption(f"Last sync: {datetime.now().strftime('%H:%M:%S')}")
    st.markdown("---")
    auto_refresh = st.checkbox("Auto-refresh (5s)", value=False)

# ============================================================
# REUSABLE KPI CARD COMPONENT
# ============================================================
def kpi_card(col, icon, label, value, sub=None, color="#3b82f6"):
    with col:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">{icon}</div>
            <div class="kpi-label">{label}</div>
            <div class="kpi-value" style="color:{color}">{value}</div>
            {f'<div class="kpi-sub">{sub}</div>' if sub else ''}
        </div>
        """, unsafe_allow_html=True)


# ============================================================
# PAGE: DASHBOARD
# ============================================================
if page == "📊 Dashboard":
    st.markdown("# Traffic Control Dashboard")
    st.caption(f"Real-time overview • {datetime.now().strftime('%A, %d %B %Y — %H:%M:%S')}")

    kpis = generate_kpis()

    st.markdown('<div class="section-title">Live Metrics</div>', unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns(5)
    kpi_card(c1, "🚗", "Total Vehicles", kpis["total"], "Last 5 min", "#3b82f6")
    kpi_card(c2, "🚘", "Cars", kpis["cars"], color="#5fa8f5")
    kpi_card(c3, "🚌", "Bus", kpis["bus"], color="#e67e22")
    kpi_card(c4, "🚚", "Truck", kpis["truck"], color="#e74c3c")
    kpi_card(c5, "🏍️", "Bike", kpis["bikes"], color="#f1c40f")

    st.write("")
    c6, c7, c8, c9 = st.columns(4)
    kpi_card(c6, "⚡", "Average Speed", f'{kpis["avg_speed"]} km/h', color="#2ecc71")

    density_color = DENSITY_COLORS[kpis["density"]]
    with c7:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">🚦</div>
            <div class="kpi-label">Current Density</div>
            <div class="status-pill" style="background:{density_color}22; color:{density_color}; border:1px solid {density_color};">
                {kpis["density"]}
            </div>
        </div>
        """, unsafe_allow_html=True)

    signal_color = {"GREEN": "#2ecc71", "YELLOW": "#f1c40f", "RED": "#e74c3c"}[kpis["signal"]]
    with c8:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">🚥</div>
            <div class="kpi-label">Signal Status</div>
            <div class="status-pill" style="background:{signal_color}22; color:{signal_color}; border:1px solid {signal_color};">
                {kpis["signal"]}
            </div>
        </div>
        """, unsafe_allow_html=True)

    emergency_text = "ACTIVE 🚨" if kpis["emergency"] else "NORMAL"
    emergency_color = "#e74c3c" if kpis["emergency"] else "#2ecc71"
    with c9:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">🆘</div>
            <div class="kpi-label">Emergency Status</div>
            <div class="status-pill" style="background:{emergency_color}22; color:{emergency_color}; border:1px solid {emergency_color};">
                {emergency_text}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.markdown('<div class="section-title">Traffic Overview</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns([1, 1])
    with col_a:
        dist_df = generate_vehicle_distribution(kpis)
        fig = px.pie(dist_df, names="Type", values="Count", hole=0.55,
                     color="Type", color_discrete_map=VEHICLE_COLORS,
                     title="Vehicle Distribution")
        fig.update_traces(textinfo="percent+label")
        st.plotly_chart(style_fig(fig), use_container_width=True)

    with col_b:
        hourly_df = generate_hourly_traffic()
        fig2 = px.area(hourly_df, x="Hour", y="Vehicles", title="Hourly Traffic Volume")
        fig2.update_traces(line_color="#3b82f6", fillcolor="rgba(59,130,246,0.25)")
        st.plotly_chart(style_fig(fig2), use_container_width=True)

    col_c, col_d = st.columns([1, 1])
    with col_c:
        density_df = generate_density_trend()
        fig3 = px.line(density_df, x="Time", y="VehicleCount", title="Density Trend (last 2.5 hrs)",
                        markers=True)
        fig3.update_traces(line_color="#e67e22")
        st.plotly_chart(style_fig(fig3), use_container_width=True)

    with col_d:
        lane_df = generate_lane_counts()
        fig4 = px.bar(lane_df, x="Lane", y="VehicleCount", title="Lane-wise Vehicle Count",
                       color="VehicleCount", color_continuous_scale="Blues")
        st.plotly_chart(style_fig(fig4), use_container_width=True)


# ============================================================
# PAGE: LIVE DETECTION
# ============================================================
elif page == "🎥 Live Detection":
    st.markdown("# Live Detection Feed")
    st.caption("Simulated feed — connects to detector.py + tracker.py in the AI integration pass")

    col_video, col_info = st.columns([2, 1])

    with col_video:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown("#### 📹 Camera Feed — Junction A")
        st.image(
            "https://placehold.co/960x540/0f1524/3b82f6?text=Live+Camera+Feed+%28Simulated%29",
            use_container_width=True,
        )
        b1, b2, b3 = st.columns(3)
        b1.button("▶️ Start Feed", use_container_width=True)
        b2.button("⏸️ Pause", use_container_width=True)
        b3.button("⏹️ Stop", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_info:
        kpis = generate_kpis()
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown("#### Frame Stats")
        st.metric("FPS", f"{random.randint(24, 30)}")
        st.metric("Vehicles in Frame", kpis["total"] % 40 + 5)
        st.metric("Current Density", kpis["density"])
        st.metric("Signal Timer", f"{random.randint(5, 60)}s")
        if kpis["emergency"]:
            st.error("🚨 Emergency Vehicle Detected — Lane 2")
        else:
            st.success("✅ No Emergency Vehicles")
        st.markdown('</div>', unsafe_allow_html=True)

    st.write("")
    st.markdown('<div class="section-title">Detected Objects (current frame)</div>', unsafe_allow_html=True)
    obj_rows = []
    for i in range(random.randint(6, 12)):
        obj_rows.append({
            "Track ID": random.randint(100, 999),
            "Type": random.choice(["Car", "Bike", "Bus", "Truck", "Person"]),
            "Lane": random.choice([1, 2, 3]),
            "Speed (km/h)": round(random.uniform(10, 75), 1),
            "Confidence": f"{random.uniform(0.75, 0.98):.2f}",
        })
    st.dataframe(pd.DataFrame(obj_rows), use_container_width=True, hide_index=True)


# ============================================================
# PAGE: ANALYTICS
# ============================================================
elif page == "📈 Analytics":
    st.markdown("# Traffic Analytics")
    st.caption("Historical trends and breakdowns")

    kpis = generate_kpis()

    col1, col2 = st.columns(2)
    with col1:
        dist_df = generate_vehicle_distribution(kpis)
        fig = px.bar(dist_df, x="Type", y="Count", color="Type",
                     color_discrete_map=VEHICLE_COLORS, title="Vehicle Type Distribution")
        st.plotly_chart(style_fig(fig), use_container_width=True)

    with col2:
        hourly_df = generate_hourly_traffic()
        fig2 = px.line(hourly_df, x="Hour", y="Vehicles", title="Hourly Traffic Pattern", markers=True)
        fig2.update_traces(line_color="#3b82f6")
        peak_hour = hourly_df.loc[hourly_df["Vehicles"].idxmax(), "Hour"]
        st.plotly_chart(style_fig(fig2), use_container_width=True)
        st.info(f"📌 Peak Hour: **{peak_hour}**")

    col3, col4 = st.columns(2)
    with col3:
        density_df = generate_density_trend()
        fig3 = px.bar(density_df, x="Time", y="VehicleCount", color="Density",
                       color_discrete_map=DENSITY_COLORS, title="Density Trend")
        st.plotly_chart(style_fig(fig3), use_container_width=True)

    with col4:
        speed_df = generate_speed_data()
        fig4 = px.line(speed_df, x="Time", y="AvgSpeed", title="Average Speed Over Time", markers=True)
        fig4.add_hline(y=60, line_dash="dash", line_color="#e74c3c",
                        annotation_text="Speed Limit (60 km/h)")
        fig4.update_traces(line_color="#2ecc71")
        st.plotly_chart(style_fig(fig4), use_container_width=True)

    st.markdown('<div class="section-title">Lane-wise Analysis & Heatmap</div>', unsafe_allow_html=True)
    col5, col6 = st.columns(2)
    with col5:
        lane_df = generate_lane_counts()
        fig5 = px.bar(lane_df, x="Lane", y="VehicleCount", color="Lane", title="Lane-wise Count")
        st.plotly_chart(style_fig(fig5), use_container_width=True)

    with col6:
        heat_data = np.random.randint(5, 60, size=(7, 24))
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        hours = [f"{h}:00" for h in range(24)]
        fig6 = go.Figure(data=go.Heatmap(z=heat_data, x=hours, y=days, colorscale="Blues"))
        fig6.update_layout(title="Weekly Traffic Heatmap")
        st.plotly_chart(style_fig(fig6), use_container_width=True)


# ============================================================
# PAGE: REPORTS
# ============================================================
elif page == "📄 Reports":
    st.markdown("# Reports & Violations")
    st.caption("Generate and export traffic reports")

    tab1, tab2 = st.tabs(["📋 Violation Log", "📦 Export Reports"])

    with tab1:
        viol_df = generate_violation_log()
        f1, f2 = st.columns([1, 3])
        with f1:
            type_filter = st.selectbox("Filter by type", ["All"] + list(viol_df["Type"].unique()))
        if type_filter != "All":
            viol_df = viol_df[viol_df["Type"] == type_filter]
        st.dataframe(viol_df, use_container_width=True, hide_index=True)

        c1, c2, c3 = st.columns(3)
        c1.metric("Total Violations (24h)", len(viol_df))
        c2.metric("Most Common", viol_df["Type"].mode()[0] if not viol_df.empty else "-")
        c3.metric("Locations Monitored", viol_df["Location"].nunique() if not viol_df.empty else 0)

    with tab2:
        st.markdown("#### Export current data")
        colf1, colf2, colf3 = st.columns(3)
        with colf1:
            st.markdown("**CSV Export**")
            csv_data = generate_violation_log().to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Download CSV", csv_data, "traffic_report.csv", "text/csv",
                                use_container_width=True)
        with colf2:
            st.markdown("**Excel Export**")
            st.button("⬇️ Download Excel", use_container_width=True,
                       help="Wired to analytics.py export function in the AI integration pass")
        with colf3:
            st.markdown("**PDF Export**")
            st.button("⬇️ Download PDF", use_container_width=True,
                       help="Wired to analytics.py export function in the AI integration pass")

        st.markdown("---")
        st.markdown("#### Report Preview")
        summary_df = pd.DataFrame({
            "Metric": ["Total Vehicles", "Total Violations", "Average Speed", "Peak Hour", "Most Congested Lane"],
            "Value": [random.randint(1000, 3000), random.randint(20, 80),
                      f"{random.uniform(35, 55):.1f} km/h", "18:00", "Lane 2"],
        })
        st.table(summary_df)


# ============================================================
# PAGE: PREDICTION
# ============================================================
elif page == "🔮 Prediction":
    st.markdown("# Traffic Prediction")
    st.caption("ML-based short-term forecasting — will connect to prediction.py (Random Forest / XGBoost / Linear Regression)")

    col1, col2 = st.columns([2, 1])
    with col1:
        pred_df = generate_prediction_data()
        fig = px.line(pred_df, x="Time", y="PredictedVolume", markers=True,
                       title="Predicted Traffic Volume (Next 30 min)")
        fig.update_traces(line_color="#8b5cf6")
        st.plotly_chart(style_fig(fig), use_container_width=True)

    with col2:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown("#### Model Info")
        model_choice = st.selectbox("Active Model", ["Random Forest", "XGBoost", "Linear Regression"])
        st.metric("Model Accuracy (R²)", f"{random.uniform(0.82, 0.95):.2f}")
        st.metric("Next 5 min", f"{random.randint(60, 200)} vehicles")
        st.metric("Next 10 min", f"{random.randint(60, 200)} vehicles")
        recommended = random.choice(["20s", "40s", "60s", "90s"])
        st.metric("Recommended Signal Timing", recommended)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Historical vs Predicted</div>', unsafe_allow_html=True)
    hourly_df = generate_hourly_traffic()
    hist_hours = hourly_df["Hour"].tolist()[-6:]
    hist_vals = hourly_df["Vehicles"].tolist()[-6:]
    combined = pd.DataFrame({
        "Time": hist_hours + pred_df["Time"].tolist(),
        "Vehicles": hist_vals + pred_df["PredictedVolume"].tolist(),
        "Type": ["Historical"] * 6 + ["Predicted"] * len(pred_df),
    })
    fig2 = px.line(combined, x="Time", y="Vehicles", color="Type", markers=True,
                    color_discrete_map={"Historical": "#3b82f6", "Predicted": "#8b5cf6"})
    st.plotly_chart(style_fig(fig2), use_container_width=True)


# ============================================================
# PAGE: SETTINGS
# ============================================================
elif page == "⚙️ Settings":
    st.markdown("# Settings")
    st.caption("System configuration")

    tab1, tab2, tab3 = st.tabs(["🎯 Detection", "🚦 Signal Timing", "🔔 Alerts"])

    with tab1:
        st.markdown("#### Detection Parameters")
        st.slider("Confidence Threshold", 0.0, 1.0, 0.35, 0.05)
        st.slider("IOU Threshold", 0.0, 1.0, 0.45, 0.05)
        st.selectbox("YOLO Model", ["yolov8n.pt", "yolov8s.pt", "yolov8m.pt", "yolov8l.pt"])
        st.multiselect("Classes to Detect",
                        ["Car", "Truck", "Bus", "Motorcycle", "Bicycle", "Person", "Traffic Light", "Stop Sign"],
                        default=["Car", "Truck", "Bus", "Motorcycle", "Bicycle"])

    with tab2:
        st.markdown("#### Signal Timing Rules (seconds)")
        c1, c2, c3, c4 = st.columns(4)
        c1.number_input("Low density", value=20)
        c2.number_input("Medium density", value=40)
        c3.number_input("High density", value=60)
        c4.number_input("Very High density", value=90)
        st.number_input("Speed Limit (km/h)", value=60)
        st.number_input("Pixels per Meter (calibration)", value=8.0)

    with tab3:
        st.markdown("#### Alert Preferences")
        st.checkbox("Emergency vehicle sound alert", value=True)
        st.checkbox("Red light violation alerts", value=True)
        st.checkbox("Overspeed alerts", value=True)
        st.checkbox("Illegal parking alerts", value=False)
        st.text_input("Alert notification email")

    st.markdown("---")
    st.button("💾 Save Settings", type="primary")


# ============================================================
# PAGE: ABOUT
# ============================================================
elif page == "ℹ️ About":
    st.markdown("# About This System")
    st.markdown("""
    <div class="panel">
    <h4>AI-Based Intelligent Traffic Monitoring and Smart Traffic Signal Management System</h4>
    <p>A final-year Smart City project combining computer vision, machine learning, and
    real-time analytics to monitor traffic, manage adaptive signal timing, and detect
    violations automatically.</p>
    <p><b>Core Modules:</b> YOLOv8 Detection • ByteTrack Multi-Object Tracking • Density Classification
    • Adaptive Signal Control • Speed Estimation • Emergency Vehicle Priority • Violation Detection
    • ML-based Traffic Prediction</p>
    <p><b>Tech Stack:</b> Python, YOLOv8, OpenCV, Streamlit, SQLite, Plotly, Scikit-Learn</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### System Architecture")
    st.graphviz_chart("""
    digraph {
        rankdir=LR;
        bgcolor="transparent";
        node [shape=box, style="rounded,filled", fillcolor="#131a2b", fontcolor="#e6e9f0", color="#3b82f6"];
        edge [color="#8b94ab"];
        Camera -> Detector [label="frames"];
        Detector -> Tracker;
        Tracker -> Density;
        Density -> SignalController;
        Tracker -> SpeedEstimator;
        Tracker -> ViolationModules;
        SignalController -> Dashboard;
        SpeedEstimator -> Dashboard;
        ViolationModules -> Dashboard;
        Density -> Dashboard;
        Dashboard -> Database;
        Database -> Prediction;
        Prediction -> Dashboard;
    }
    """)


# ============================================================
# FOOTER
# ============================================================
st.markdown('<div class="footer-tag">Smart Traffic Control System • Running on simulated data • v0.1</div>',
            unsafe_allow_html=True)

if auto_refresh:
    time.sleep(5)
    st.rerun()