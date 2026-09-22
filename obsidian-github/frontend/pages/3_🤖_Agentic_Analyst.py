import streamlit as st
import requests

st.set_page_config(page_title="Agentic Analyst", page_icon="🤖", layout="wide")

if "access_token" not in st.session_state or not st.session_state["access_token"]:
    st.warning("🔒 Please authenticate on the main page to access this module.")
    st.stop()

st.title("🤖 OBSIDIAN Agentic Analyst")
st.markdown("Ask natural language questions. OBSIDIAN will write the SQL, query the live Supabase warehouse, and analyze the results autonomously.")

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Display previous chat messages
for msg in st.session_state["chat_history"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_query = st.chat_input("E.g., What are the top 3 product categories by total revenue?")

if user_query:
    # 1. Display User Message
    with st.chat_message("user"):
        st.markdown(user_query)
    st.session_state["chat_history"].append({"role": "user", "content": user_query})
    
    # 2. Trigger Autonomous Agent
    with st.chat_message("assistant"):
        with st.spinner("OBSIDIAN is engineering SQL and analyzing data..."):
            headers = {"Authorization": f"Bearer {st.session_state['access_token']}"}
            
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/api/v1/ask_obsidian",
                    headers=headers,
                    json={"query": user_query} # Send as JSON body
                )
                
                if response.status_code == 200:
                    answer = response.json()["response"]
                    st.markdown(answer)
                    st.session_state["chat_history"].append({"role": "assistant", "content": answer})
                elif response.status_code == 401:
                    st.error("Session expired.")
                else:
                    st.error(f"Agent Error: {response.text}")
            except Exception as e:
                st.error(f"Connection Error: {e}")