import os
import time
from sqlalchemy import create_engine
from langchain_groq import ChatGroq
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage

# --- ENTERPRISE CONFIGURATION ---
GROQ_API_KEY = "" 
DB_URI = "postgresql://postgres.rtzrbsfxpwtnziyayyty:Syedzai7317@aws-0-ap-south-1.pooler.supabase.com:6543/postgres"

# 0. Build the Resilient Engine Globally
engine = create_engine(DB_URI, pool_pre_ping=True, connect_args={'connect_timeout': 15})

# CRITICAL BYPASS: Define exact tables to prevent massive network payloads during DNS instability
TARGET_TABLES = [
    'customers', 'geolocation', 'orders', 'order_items', 
    'order_payments', 'order_reviews', 'products', 'sellers'
]

def get_obsidian_agent():
    """Initializes the LangGraph SQL Agent connected to Supabase."""
    
    # 1. Mount the Live Database and ONLY scan our target tables
    db = SQLDatabase(engine=engine, include_tables=TARGET_TABLES)
    
    # 2. Ignite the Groq Llama-3 Engine 
    # 2. Ignite the Groq Engine 
    llm = ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name="openai/gpt-oss-20b",
        temperature=0 
    )
    
    # 3. Equip the Agent with SQL Tools
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    tools = toolkit.get_tools()
    
    # 4. Define the Agent's Directive
    system_message = """You are OBSIDIAN, an elite AI data analyst for an e-commerce company.
    You have direct access to a PostgreSQL database containing Olist e-commerce data.
    When asked a question, you must:
    1. Check the available tables.
    2. Check the schemas of the relevant tables.
    3. Write and execute a PostgreSQL query to get the answer.
    4. If the query fails, rewrite it and try again.
    5. Present your final answer as a polished, professional executive summary. NEVER show the raw SQL query to the user.
    """
    
    return create_react_agent(llm, tools, prompt=system_message)

async def process_natural_language_query(user_query: str) -> str:
    """Invokes the LangGraph agent with Aggressive Enterprise Fault Tolerance."""
    max_retries = 5
    for attempt in range(1, max_retries + 1):
        try:
            agent = get_obsidian_agent()
            response = await agent.ainvoke({"messages": [HumanMessage(content=user_query)]})
            return response["messages"][-1].content
        except Exception as e:
            engine.dispose()
            
            if attempt == max_retries:
                raise e
            
            # Exponential backoff gives the OS DNS resolver time to recover
            wait_time = attempt * 4
            print(f"⚠️ Agent network drop caught. Rebuilding pool and retrying ({attempt}/{max_retries}) in {wait_time}s...")
            time.sleep(wait_time)