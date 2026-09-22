import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Analytics & Telemetry", page_icon="📈", layout="wide")

if "access_token" not in st.session_state or not st.session_state["access_token"]:
    st.warning("🔒 Please authenticate on the main page to access this module.")
    st.stop()

st.title("📈 Global Analytics & Telemetry Hub")
st.markdown("Real-time visual monitoring of system health and multi-dimensional e-commerce data.")
st.markdown("---")

# --- DATA GENERATION (Simulating massive Olist payloads for visuals) ---
np.random.seed(42)
dates = pd.date_range(start="2026-08-01", periods=30)
api_latency = np.random.normal(loc=45, scale=10, size=30)
active_sessions = np.random.randint(100, 500, size=30)

df_telemetry = pd.DataFrame({"Date": dates, "API Latency (ms)": api_latency, "Active Sessions": active_sessions})

df_products = pd.DataFrame({
    "Category": ["Health & Beauty", "Electronics", "Home & Garden", "Sports", "Automotive"],
    "Revenue": [450000, 890000, 320000, 210000, 150000],
    "Churn_Risk": [12, 45, 18, 8, 30]
})

# Generate 3D Surface Data (Customer Lifetime Value Elasticity)
x_val = np.linspace(-5, 5, 50)
y_val = np.linspace(-5, 5, 50)
x_grid, y_grid = np.meshgrid(x_val, y_val)
z_grid = np.sin(np.sqrt(x_grid**2 + y_grid**2)) * 1000 + 5000

# --- SECTION 1: SYSTEM TELEMETRY ---
st.subheader("⚙️ System Infrastructure")
col1, col2 = st.columns(2)

with col1:
    fig_telemetry = go.Figure()
    fig_telemetry.add_trace(go.Scatter(x=df_telemetry['Date'], y=df_telemetry['API Latency (ms)'], 
                                       mode='lines', name='Latency (ms)', line=dict(color='#00E5FF', width=3)))
    fig_telemetry.add_trace(go.Bar(x=df_telemetry['Date'], y=df_telemetry['Active Sessions'], 
                                   name='Active Sessions', yaxis='y2', marker_color='rgba(255, 0, 128, 0.4)'))
    
    fig_telemetry.update_layout(
        title="API Gateway Performance",
        template="plotly_dark",
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(title='Latency (ms)', side='left'),
        yaxis2=dict(title='Sessions', side='right', overlaying='y'),
        margin=dict(l=0, r=0, t=40, b=0)
    )
    st.plotly_chart(fig_telemetry, width='stretch')

with col2:
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = 72,
        title = {'text': "XGBoost Engine Load (%)", 'font': {'size': 18}},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
            'bar': {'color': "#00E5FF"},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [{'range': [0, 50], 'color': 'rgba(0, 255, 0, 0.1)'},
                      {'range': [50, 85], 'color': 'rgba(255, 255, 0, 0.1)'}],
            'threshold': {'line': {'color': "#FF0080", 'width': 4}, 'thickness': 0.75, 'value': 90}
        }
    ))
    fig_gauge.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', height=350, margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig_gauge, width='stretch')

st.markdown("---")

# --- SECTION 2: 3D MULTI-DIMENSIONAL ANALYSIS ---
st.subheader("🌌 3D Topography & Risk Matrices")
col3, col4 = st.columns(2)

with col3:
    fig_surface = go.Figure(data=[go.Surface(z=z_grid, x=x_val, y=y_val, colorscale='Turbo')])
    fig_surface.update_layout(
        title='CLV Elasticity Surface (Neural Topology)', 
        template="plotly_dark", 
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=40, b=0),
        height=500
    )
    st.plotly_chart(fig_surface, width='stretch')

with col4:
    fig_bubble = px.scatter_3d(df_products, x='Category', y='Revenue', z='Churn_Risk',
                               color='Churn_Risk', size='Revenue', 
                               color_continuous_scale='Inferno',
                               title="3D Churn Risk vs Category Revenue")
    fig_bubble.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=40, b=0), height=500)
    st.plotly_chart(fig_bubble, width='stretch')

st.markdown("---")

# --- SECTION 3: HIERARCHIES & BEHAVIORAL INTELLIGENCE ---
st.subheader("🧬 Behavioral Segmentation & Revenue Flow")
col5, col6, col7 = st.columns((1, 1, 1))

with col5:
    # Custom Hex Colors for Donut
    custom_cyan = ['#00E5FF', '#00CCFF', '#0099FF', '#0066FF', '#0033FF']
    fig_donut = px.pie(df_products, values='Revenue', names='Category', hole=0.7, 
                       title="Revenue Distribution", color_discrete_sequence=custom_cyan)
    fig_donut.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=40, b=0))
    fig_donut.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_donut, width='stretch')

with col6:
    # Conversion Funnel
    funnel_data = dict(
        number=[100000, 75000, 30000, 15000, 5000],
        stage=["Site Visits", "Cart Additions", "Checkout Initiated", "Purchase Completed", "Repeat VIPs"])
    fig_funnel = px.funnel(funnel_data, x='number', y='stage', title="Global Conversion Funnel")
    fig_funnel.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=40, b=0))
    fig_funnel.update_traces(marker=dict(color=['#00E5FF', '#00E5FF', '#00E5FF', '#FF0080', '#FF0080']))
    st.plotly_chart(fig_funnel, width='stretch')

with col7:
    # Behavioral Radar Chart
    categories = ['Recency', 'Frequency', 'Monetary', 'App Usage', 'Support Tickets']
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(r=[4, 5, 4, 5, 1], theta=categories, fill='toself', name='VIP Segment', line_color='#00E5FF'))
    fig_radar.add_trace(go.Scatterpolar(r=[1, 2, 1, 3, 5], theta=categories, fill='toself', name='High-Risk Segment', line_color='#FF0080'))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
        showlegend=True,
        title="Customer Segment Fingerprints",
        template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=20, r=20, t=40, b=20)
    )
    st.plotly_chart(fig_radar, width='stretch')