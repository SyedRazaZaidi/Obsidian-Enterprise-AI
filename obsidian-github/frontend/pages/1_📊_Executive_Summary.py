import streamlit as st
import requests

st.set_page_config(page_title="Executive Summary", page_icon="📊", layout="wide")

# Security Check: Ensure user is logged in
if "access_token" not in st.session_state or not st.session_state["access_token"]:
    st.warning("🔒 Please authenticate on the main page to access this module.")
    st.stop()

st.title("📊 Enterprise Executive Summary")
st.markdown("Live metrics pulled securely from cloud data warehouse.")

headers = {"Authorization": f"Bearer {st.session_state['access_token']}"}

try:
    with st.spinner("Establishing secure handshake with API Gateway..."):
        # Hit your FastAPI endpoint securely
        response = requests.get("http://127.0.0.1:8000/api/v1/kpis", headers=headers)
        
    if response.status_code == 200:
        data = response.json()
        
        # Display massive KPI Cards
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(label="Total Delivered Orders", value=f"{data['total_delivered_orders']:,}")
            
        with col2:
            st.metric(label="Total Gross Revenue (BRL)", value=f"R$ {data['total_revenue_brl']:,.2f}")
            
        with col3:
            st.metric(label="System Status", value="OPTIMAL")
            
    elif response.status_code == 401:
        st.error("Session expired. Please log in again.")
        st.session_state["access_token"] = None
    else:
        error_detail = response.json().get('detail', 'Unknown error')
        st.error(f"🛑 API Error {response.status_code}: {error_detail}")
        st.info("Check if your Supabase password is correct in backend/main.py, or if you are experiencing a transient DNS drop.")
except Exception as e:
    st.error(f"Critical System Error: {e}")