import streamlit as st
import requests

st.set_page_config(page_title="Predictive Churn Engine", page_icon="🔮", layout="wide")

# Security Check: Ensure user is logged in
if "access_token" not in st.session_state or not st.session_state["access_token"]:
    st.warning("🔒 Please authenticate on the main page to access this module.")
    st.stop()

st.title("🔮 AI Predictive Churn Engine")
st.markdown("Run real-time inference on customer behavior using the OBSIDIAN XGBoost Model.")

# --- CUSTOMER FEATURE INPUTS ---
st.markdown("### Customer Profile Data")
with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        recency = st.number_input("Recency (Days since last purchase)", min_value=0, max_value=1000, value=45, help="Lower is better.")
        monetary = st.number_input("Monetary Value (Total Spend in BRL)", min_value=0.0, max_value=10000.0, value=350.00, step=10.0, help="Higher is better.")
        
    with col2:
        max_delivery_delay = st.number_input("Max Delivery Delay (Days)", min_value=0, max_value=100, value=0, help="0 means delivered on time.")
        avg_review_score = st.slider("Average Review Score", min_value=1.0, max_value=5.0, value=4.0, step=0.1, help="5.0 is perfect satisfaction.")

st.markdown("---")

# --- AI INFERENCE EXECUTION ---
if st.button("Run AI Inference", type="primary"):
    headers = {"Authorization": f"Bearer {st.session_state['access_token']}"}
    
    # We pass these as query parameters because our FastAPI endpoint expects them as direct arguments
    payload = {
        "recency": int(recency),
        "monetary": float(monetary),
        "max_delivery_delay": int(max_delivery_delay),
        "avg_review_score": float(avg_review_score)
    }
    
    try:
        with st.spinner("Processing data through XGBoost Engine..."):
            response = requests.post("http://127.0.0.1:8000/api/v1/predict_churn", headers=headers, params=payload)
            
        if response.status_code == 200:
            result = response.json()
            
            st.markdown("### Inference Results")
            r_col1, r_col2 = st.columns(2)
            
            with r_col1:
                status = result['status']
                if result['churn_prediction'] == 1:
                    st.error(f"**Classification:** {status}")
                    st.markdown("⚠️ **Action Required:** Trigger automated retention email sequence with a discount code.")
                else:
                    st.success(f"**Classification:** {status}")
                    st.markdown("✅ **Status Normal:** Customer exhibits strong brand loyalty.")
                    
            with r_col2:
                prob = result['churn_risk_probability']
                st.metric(label="Calculated Churn Risk", value=f"{prob}%")
                st.progress(prob / 100.0)
                
        elif response.status_code == 401:
            st.error("Session expired. Please log in again.")
            st.session_state["access_token"] = None
        else:
            st.error(f"🛑 API Error {response.status_code}: {response.text}")
            
    except Exception as e:
        st.error(f"Critical Connection Error: {e}")