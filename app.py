"""
OLA Ride Insights — Streamlit Application (CSV version for Streamlit Cloud)
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
import numpy as np
import warnings
warnings.filterwarnings("ignore")

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="OLA Ride Insights",
    page_icon="🚕",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CUSTOM CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&display=swap');
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    .main { background-color: #0f0f14; }
    .block-container { padding-top: 1.5rem; }
    .ola-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        border-radius: 16px; padding: 2rem 2.5rem; margin-bottom: 1.5rem;
        border: 1px solid rgba(0,180,216,0.2); position: relative; overflow: hidden;
    }
    .ola-header h1 {
        font-family: 'Syne', sans-serif; font-size: 2.2rem; font-weight: 800;
        color: #ffffff; margin: 0 0 0.3rem 0;
    }
    .ola-header p { color: #94a3b8; margin: 0; font-size: 0.95rem; }
    .ola-badge {
        display: inline-block; background: rgba(0,180,216,0.15); color: #00b4d8;
        border: 1px solid rgba(0,180,216,0.3); border-radius: 20px;
        padding: 3px 12px; font-size: 0.78rem; font-weight: 500; margin-top: 0.6rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #1e1e2e, #252535);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 12px; padding: 1.2rem 1.5rem; text-align: center;
    }
    .metric-value {
        font-family: 'Syne', sans-serif; font-size: 1.8rem; font-weight: 700;
        color: #00b4d8; line-height: 1.1;
    }
    .metric-label {
        font-size: 0.78rem; color: #64748b; margin-top: 0.3rem;
        text-transform: uppercase; letter-spacing: 0.05em;
    }
    .section-title {
        font-family: 'Syne', sans-serif; font-size: 1.1rem; font-weight: 700;
        color: #e2e8f0; padding: 0.5rem 0; border-bottom: 2px solid #00b4d8;
        margin-bottom: 1rem;
    }
    section[data-testid="stSidebar"] {
        background: #13131f; border-right: 1px solid rgba(255,255,255,0.06);
    }
    .sidebar-logo {
        font-family: 'Syne', sans-serif; font-size: 1.4rem; font-weight: 800;
        color: #00b4d8; padding: 0.5rem 0 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ── LOAD DATA ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("ola_clean.csv")
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["DateOnly"] = df["Date"].dt.date
    for col in ["Booking_Value", "Ride_Distance", "Driver_Ratings", "Customer_Rating"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df

@st.cache_resource
def get_conn(_df):
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    _df.to_sql("rides", conn, if_exists="replace", index=False)
    return conn

df = load_data()
conn = get_conn(df)

def run_query(sql):
    return pd.read_sql(sql, conn)

# ── PLOTLY THEME ──────────────────────────────────────────────────────────────
PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans", color="#94a3b8"),
    xaxis=dict(gridcolor="rgba(255,255,255,0.05)", showline=False),
    yaxis=dict(gridcolor="rgba(255,255,255,0.05)", showline=False),
    margin=dict(l=20, r=20, t=40, b=20),
)
COLOR_SEQ = ["#00b4d8", "#0077b6", "#48cae4", "#90e0ef", "#ade8f4", "#caf0f8", "#023e8a", "#03045e"]

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-logo">🚕OLA Insights</div>', unsafe_allow_html=True)
    section = st.radio(
        "Navigate to",
        ["📊 Overall", "🚗 Vehicle Type", "💰 Revenue", "❌ Cancellation", "⭐ Ratings", "🔍 SQL Explorer"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown("**Dataset**")
    st.caption("OLA Rides · July 2024")
    st.caption(f"{len(df):,} records")

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="ola-header">
  <h1>🚖 OLA Ride Insights</h1>
  <p>Ride-Sharing & Mobility Analytics · July 2024</p>
  <span class="ola-badge">Power BI • SQL • Streamlit</span>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  SECTION 1 — OVERALL
# ═══════════════════════════════════════════════════════════════════════════════
if section == "📊 Overall":

    total     = len(df)
    success   = len(df[df["Booking_Status"] == "Success"])
    c_cancel  = len(df[df["Booking_Status"] == "Canceled by Customer"])
    d_cancel  = len(df[df["Booking_Status"] == "Canceled by Driver"])
    no_driver = len(df[df["Booking_Status"] == "Driver Not Found"])
    revenue   = df[df["Booking_Status"] == "Success"]["Booking_Value"].sum()

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    for col, val, label in [
        (c1, f"{total:,}",          "Total Rides"),
        (c2, f"{success:,}",        "Successful"),
        (c3, f"{c_cancel:,}",       "Customer Cancels"),
        (c4, f"{d_cancel:,}",       "Driver Cancels"),
        (c5, f"{no_driver:,}",      "No Driver Found"),
        (c6, f"₹{revenue:,.0f}",    "Total Revenue"),
    ]:
        col.markdown(
            f'<div class="metric-card"><div class="metric-value">{val}</div>'
            f'<div class="metric-label">{label}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_l, col_r = st.columns([2, 1])

    with col_l:
        st.markdown('<div class="section-title">Ride Volume Over Time</div>', unsafe_allow_html=True)
        daily = df.groupby("DateOnly").size().reset_index(name="Rides")
        fig = px.area(daily, x="DateOnly", y="Rides", color_discrete_sequence=["#00b4d8"])
        fig.update_traces(fill='tozeroy', line_color='#00b4d8', fillcolor='rgba(0,180,216,0.15)')
        fig.update_layout(**PLOT_LAYOUT, height=300)
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.markdown('<div class="section-title">Booking Status Breakdown</div>', unsafe_allow_html=True)
        status = df["Booking_Status"].value_counts().reset_index()
        status.columns = ["Booking_Status", "Count"]
        fig2 = px.pie(status, names="Booking_Status", values="Count",
                      color_discrete_sequence=COLOR_SEQ, hole=0.55)
        fig2.update_layout(**PLOT_LAYOUT, height=300)
        st.plotly_chart(fig2, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  SECTION 2 — VEHICLE TYPE
# ═══════════════════════════════════════════════════════════════════════════════
elif section == "🚗 Vehicle Type":

    st.markdown('<div class="section-title">Vehicle Type Analytics</div>', unsafe_allow_html=True)

    df_veh = df.groupby("Vehicle_Type").agg(
        Total_Bookings=("Booking_ID", "count"),
        Successful=("Booking_Status", lambda x: (x == "Success").sum()),
        Total_Distance_km=("Ride_Distance", "sum"),
        Avg_Distance_km=("Ride_Distance", "mean"),
        Total_Booking_Value=("Booking_Value", "sum"),
    ).reset_index().round(2).sort_values("Total_Distance_km", ascending=False)

    st.dataframe(df_veh, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-title">Top 5 by Total Ride Distance</div>', unsafe_allow_html=True)
        top5 = df_veh.nlargest(5, "Total_Distance_km")
        fig = px.bar(top5, x="Vehicle_Type", y="Total_Distance_km",
                     color="Vehicle_Type", color_discrete_sequence=COLOR_SEQ)
        fig.update_layout(**PLOT_LAYOUT, height=320, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-title">Average Distance per Vehicle Type</div>', unsafe_allow_html=True)
        fig2 = px.bar(df_veh.sort_values("Avg_Distance_km"),
                      x="Avg_Distance_km", y="Vehicle_Type", orientation="h",
                      color="Avg_Distance_km", color_continuous_scale="Blues")
        fig2.update_layout(**PLOT_LAYOUT, height=320, coloraxis_showscale=False)
        st.plotly_chart(fig2, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  SECTION 3 — REVENUE
# ═══════════════════════════════════════════════════════════════════════════════
elif section == "💰 Revenue":

    st.markdown('<div class="section-title">Revenue Analytics</div>', unsafe_allow_html=True)
    df_success = df[df["Booking_Status"] == "Success"]

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Revenue by Payment Method**")
        pay = df_success.groupby("Payment_Method")["Booking_Value"].sum().reset_index()
        pay.columns = ["Payment_Method", "Revenue"]
        fig = px.bar(pay.sort_values("Revenue", ascending=False),
                     x="Payment_Method", y="Revenue",
                     color="Payment_Method", color_discrete_sequence=COLOR_SEQ)
        fig.update_layout(**PLOT_LAYOUT, height=320, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("**Top 5 Customers by Booking Value**")
        cust = df_success.groupby("Customer_ID")["Booking_Value"].sum().nlargest(5).reset_index()
        cust.columns = ["Customer_ID", "Total_Value"]
        fig2 = px.bar(cust, x="Customer_ID", y="Total_Value",
                      color="Total_Value", color_continuous_scale="Blues")
        fig2.update_layout(**PLOT_LAYOUT, height=320, coloraxis_showscale=False)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("**Daily Ride Distance**")
    daily_dist = df_success.groupby("DateOnly").agg(
        Total_Distance=("Ride_Distance", "sum"),
        Avg_Distance=("Ride_Distance", "mean")
    ).reset_index()
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=daily_dist["DateOnly"], y=daily_dist["Total_Distance"],
                              name="Total Distance", fill='tozeroy',
                              line_color="#00b4d8", fillcolor="rgba(0,180,216,0.1)"))
    fig3.add_trace(go.Scatter(x=daily_dist["DateOnly"], y=daily_dist["Avg_Distance"],
                              name="Avg Distance", line_color="#90e0ef", yaxis="y2"))
    fig3.update_layout(**PLOT_LAYOUT, height=300,
                       yaxis2=dict(overlaying="y", side="right", gridcolor="rgba(255,255,255,0.03)"))
    st.plotly_chart(fig3, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  SECTION 4 — CANCELLATION
# ═══════════════════════════════════════════════════════════════════════════════
elif section == "❌ Cancellation":

    st.markdown('<div class="section-title">Cancellation Analysis</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    by_cust = len(df[df["Booking_Status"] == "Canceled by Customer"])
    by_drv  = len(df[df["Booking_Status"] == "Canceled by Driver"])
    no_drv  = len(df[df["Booking_Status"] == "Driver Not Found"])

    for col, val, label in [
        (c1, f"{by_cust:,}", "Cancelled by Customer"),
        (c2, f"{by_drv:,}",  "Cancelled by Driver"),
        (c3, f"{no_drv:,}",  "Driver Not Found"),
    ]:
        col.markdown(
            f'<div class="metric-card"><div class="metric-value" style="color:#ef4444">{val}</div>'
            f'<div class="metric-label">{label}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_l, col_r = st.columns(2)

    with col_l:
        st.markdown("**Customer Cancellation Reasons**")
        cc = df[df["Booking_Status"] == "Canceled by Customer"]["Canceled_Rides_by_Customer"].value_counts().reset_index()
        cc.columns = ["Reason", "Count"]
        fig = px.bar(cc, x="Count", y="Reason", orientation="h",
                     color="Count", color_continuous_scale="Reds")
        fig.update_layout(**PLOT_LAYOUT, height=300, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.markdown("**Driver Cancellation Reasons**")
        dc = df[df["Booking_Status"] == "Canceled by Driver"]["Canceled_Rides_by_Driver"].value_counts().reset_index()
        dc.columns = ["Reason", "Count"]
        fig2 = px.bar(dc, x="Count", y="Reason", orientation="h",
                      color="Count", color_continuous_scale="Oranges")
        fig2.update_layout(**PLOT_LAYOUT, height=300, coloraxis_showscale=False)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("**Cancellation Trend Over Time**")
    cancel_df = df[df["Booking_Status"].isin(["Canceled by Customer", "Canceled by Driver", "Driver Not Found"])]
    trend = cancel_df.groupby(["DateOnly", "Booking_Status"]).size().reset_index(name="Count")
    fig3 = px.line(trend, x="DateOnly", y="Count", color="Booking_Status",
                   color_discrete_sequence=["#ef4444", "#f97316", "#eab308"])
    fig3.update_layout(**PLOT_LAYOUT, height=280)
    st.plotly_chart(fig3, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  SECTION 5 — RATINGS
# ═══════════════════════════════════════════════════════════════════════════════
elif section == "⭐ Ratings":

    st.markdown('<div class="section-title">Ratings Analysis</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Driver Ratings Distribution**")
        drv = df["Driver_Ratings"].dropna().round(1).value_counts().reset_index()
        drv.columns = ["Rating", "Count"]
        drv = drv.sort_values("Rating")
        fig = px.bar(drv, x="Rating", y="Count", color="Count", color_continuous_scale="Blues")
        fig.update_layout(**PLOT_LAYOUT, height=320, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("**Customer Ratings Distribution**")
        cust = df["Customer_Rating"].dropna().round(1).value_counts().reset_index()
        cust.columns = ["Rating", "Count"]
        cust = cust.sort_values("Rating")
        fig2 = px.bar(cust, x="Rating", y="Count", color="Count", color_continuous_scale="Purples")
        fig2.update_layout(**PLOT_LAYOUT, height=320, coloraxis_showscale=False)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("**Average Ratings by Vehicle Type**")
    ratings = df.groupby("Vehicle_Type").agg(
        Avg_Driver_Rating=("Driver_Ratings", "mean"),
        Avg_Customer_Rating=("Customer_Rating", "mean")
    ).reset_index().dropna().round(2)
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(name="Driver Rating",   x=ratings["Vehicle_Type"], y=ratings["Avg_Driver_Rating"],   marker_color="#00b4d8"))
    fig3.add_trace(go.Bar(name="Customer Rating", x=ratings["Vehicle_Type"], y=ratings["Avg_Customer_Rating"], marker_color="#90e0ef"))
    fig3.update_layout(**PLOT_LAYOUT, height=320, barmode="group",
                       legend=dict(orientation="h", yanchor="bottom", y=1.02))
    st.plotly_chart(fig3, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  SECTION 6 — SQL EXPLORER
# ═══════════════════════════════════════════════════════════════════════════════
elif section == "🔍 SQL Explorer":

    st.markdown('<div class="section-title">SQL Query Explorer</div>', unsafe_allow_html=True)
    st.markdown("Run any of the 10 project queries or write your own.")

    QUERIES = {
        "Q1 — All successful bookings":
            "SELECT * FROM rides WHERE Booking_Status = 'Success' LIMIT 500",
        "Q2 — Avg ride distance per vehicle type":
            "SELECT Vehicle_Type, ROUND(AVG(Ride_Distance), 2) AS Avg_Ride_Distance_km FROM rides GROUP BY Vehicle_Type ORDER BY Avg_Ride_Distance_km DESC",
        "Q3 — Total customer cancellations":
            "SELECT COUNT(*) AS Total_Customer_Cancellations FROM rides WHERE Booking_Status = 'Canceled by Customer'",
        "Q4 — Top 5 customers by ride count":
            "SELECT Customer_ID, COUNT(*) AS Total_Rides FROM rides GROUP BY Customer_ID ORDER BY Total_Rides DESC LIMIT 5",
        "Q5 — Driver cancels: personal/car issues":
            "SELECT COUNT(*) AS Driver_Cancel_Personal_Car FROM rides WHERE Canceled_Rides_by_Driver = 'Personal & Car related issue'",
        "Q6 — Max & min driver ratings (Prime Sedan)":
            "SELECT MAX(Driver_Ratings) AS Max_Rating, MIN(Driver_Ratings) AS Min_Rating FROM rides WHERE Vehicle_Type = 'Prime Sedan' AND Driver_Ratings IS NOT NULL",
        "Q7 — Rides paid via UPI":
            "SELECT * FROM rides WHERE Payment_Method = 'UPI' LIMIT 500",
        "Q8 — Avg customer rating per vehicle type":
            "SELECT Vehicle_Type, ROUND(AVG(Customer_Rating), 2) AS Avg_Customer_Rating FROM rides WHERE Customer_Rating IS NOT NULL GROUP BY Vehicle_Type ORDER BY Avg_Customer_Rating DESC",
        "Q9 — Total revenue from successful rides":
            "SELECT ROUND(SUM(Booking_Value), 2) AS Total_Successful_Booking_Value FROM rides WHERE Booking_Status = 'Success'",
        "Q10 — All incomplete rides with reason":
            "SELECT Booking_ID, Customer_ID, Vehicle_Type, Pickup_Location, Drop_Location, Booking_Value, Incomplete_Rides_Reason FROM rides WHERE Incomplete_Rides = 'Yes'",
        "✏️ Custom Query": "",
    }

    selected = st.selectbox("Choose a query", list(QUERIES.keys()))
    if selected == "✏️ Custom Query":
        sql = st.text_area("Write your SQL:", height=120, placeholder="SELECT * FROM rides LIMIT 10")
    else:
        sql = st.text_area("SQL (editable):", value=QUERIES[selected], height=120)

    if st.button("▶ Run Query", type="primary"):
        if sql.strip():
            try:
                with st.spinner("Running query…"):
                    df_result = run_query(sql)
                st.success(f"✓ {len(df_result):,} row(s) returned")
                st.dataframe(df_result, use_container_width=True)
                if len(df_result.columns) == 2:
                    num_cols = df_result.select_dtypes("number").columns.tolist()
                    cat_cols = df_result.select_dtypes("object").columns.tolist()
                    if num_cols and cat_cols:
                        fig = px.bar(df_result, x=cat_cols[0], y=num_cols[0],
                                     color_discrete_sequence=["#00b4d8"])
                        fig.update_layout(**PLOT_LAYOUT, height=300)
                        st.plotly_chart(fig, use_container_width=True)
                csv = df_result.to_csv(index=False).encode("utf-8")
                st.download_button("⬇ Download CSV", csv, file_name="query_result.csv", mime="text/csv")
            except Exception as e:
                st.error(f"Query error: {e}")
        else:
            st.warning("Please enter a SQL query.")
