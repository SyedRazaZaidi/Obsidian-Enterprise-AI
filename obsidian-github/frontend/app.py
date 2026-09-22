import streamlit as st
import requests

# --- ENTERPRISE UI CONFIGURATION ---
st.set_page_config(
    page_title="OBSIDIAN | Control Tower",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS INJECTION ---
st.markdown("""
    <style>
    .main { background-color: #0E1117; }
    h1, h2, h3 { color: #00E5FF; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .stButton>button { width: 100%; border-radius: 4px; background-color: #00E5FF; color: black; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if "access_token" not in st.session_state:
    st.session_state["access_token"] = None

# --- AUTHENTICATION UI ---
if not st.session_state["access_token"]:
    st.title("💠 OBSIDIAN")
    st.markdown("### Enterprise Commerce Intelligence")
    
    with st.form("login_form"):
        st.write("Secure Gateway Authentication")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Authenticate")
        
        if submit:
            try:
                # Call our FastAPI Secure Token Endpoint
                response = requests.post(
                    "http://127.0.0.1:8000/token",
                    data={"username": username, "password": password}
                )
                if response.status_code == 200:
                    st.session_state["access_token"] = response.json().get("access_token")
                    st.success("Authentication successful. Initializing Control Tower...")
                    st.rerun()
                else:
                    st.error("Access Denied: Invalid credentials.")
            except Exception as e:
                st.error(f"API Connection Failed. Is your FastAPI server running? Error: {e}")

else:
    st.title("💠 OBSIDIAN Control Tower")
    st.success("Secure connection established.")
    st.markdown("---")
    st.markdown("""
    ### Welcome to the Autonomous Unified Revenue & Analytics system.
    Please select a module from the sidebar to begin.
    * **📊 Executive Summary**: View high-level metrics and financial health.
    * **🔮 Predictive Churn**: Run real-time AI inference on customer loyalty.
    """)
    
    if st.button("Terminate Session"):
        st.session_state["access_token"] = None
        st.rerun()