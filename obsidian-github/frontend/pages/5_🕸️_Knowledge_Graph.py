import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
import time
from sqlalchemy import create_engine

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Enterprise Knowledge Graph", page_icon="🕸️", layout="wide")

if "access_token" not in st.session_state or not st.session_state["access_token"]:
    st.warning("🔒 Please authenticate on the main page to access the Knowledge Graph.")
    st.stop()

st.title("🕸️ OBSIDIAN Multi-Hop Knowledge Graph")
st.markdown("Real-time, in-memory network topology traversing Customer-Seller-Product relationships.")
st.markdown("---")

# --- ENTERPRISE CREDENTIALS ---
PG_URI = "postgresql://postgres.rtzrbsfxpwtnziyayyty:Syedzai7317@aws-0-ap-south-1.pooler.supabase.com:6543/postgres"

@st.cache_data(ttl=3600)
def build_in_memory_graph():
    """Extracts relational data and compiles a NetworkX graph topology."""
    engine = create_engine(PG_URI)
    query = """
        SELECT 
            c.customer_id, c.customer_state,
            o.order_id, o.order_status,
            oi.product_id, oi.seller_id, oi.price,
            r.review_score
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN order_reviews r ON o.order_id = r.order_id
        LIMIT 400; -- Optimized for real-time physics rendering in the browser
    """
    
    # Fault Tolerance Loop
    max_retries = 5
    df = None
    for attempt in range(1, max_retries + 1):
        try:
            df = pd.read_sql(query, engine)
            break
        except Exception as e:
            engine.dispose()
            if attempt == max_retries:
                st.error("Failed to extract topology from AWS. Check network.")
                return None
            time.sleep(attempt * 2)
            
    if df is None or df.empty:
        return None

    # Compile the Multi-Hop Network
    G = nx.Graph()
    for _, row in df.iterrows():
        # Nodes
        cust_node = f"Cust: {str(row['customer_id'])[:6]}"
        order_node = f"Ord: {str(row['order_id'])[:6]}"
        prod_node = f"Prod: {str(row['product_id'])[:6]}"
        seller_node = f"Sell: {str(row['seller_id'])[:6]}"
        
        G.add_node(cust_node, group=1, title=f"Customer\nState: {row['customer_state']}", color="#00E5FF")
        G.add_node(order_node, group=2, title=f"Order\nStatus: {row['order_status']}\nReview: {row['review_score']}★", color="#FF0080")
        G.add_node(prod_node, group=3, title="Product", color="#7000FF")
        G.add_node(seller_node, group=4, title="Seller", color="#00FF9D")
        
        # Edges
        G.add_edge(cust_node, order_node, value=1)
        G.add_edge(order_node, prod_node, value=row['price'])
        G.add_edge(prod_node, seller_node, value=1)
        
    return G

with st.spinner("Extracting multi-hop topology from AWS & compiling physics engine..."):
    G = build_in_memory_graph()

if G:
    # Build the PyVis Interactive Network
    net = Network(height='700px', width='100%', bgcolor='#0E1117', font_color='white')
    net.from_nx(G)
    
    # Inject Enterprise Physics settings for smooth dragging
    net.set_options("""
    var options = {
      "physics": {
        "forceAtlas2Based": {
          "gravitationalConstant": -100,
          "centralGravity": 0.01,
          "springLength": 100,
          "springConstant": 0.08
        },
        "minVelocity": 0.75,
        "solver": "forceAtlas2Based"
      }
    }
    """)
    
    # Generate and serve the HTML rendering
    path = "frontend/knowledge_graph.html"
    net.save_graph(path)
    
    HtmlFile = open(path, 'r', encoding='utf-8')
    source_code = HtmlFile.read() 
    components.html(source_code, height=750, scrolling=True)
    
    st.success("✅ Neural Topology successfully rendered in local memory. Drag nodes to interact.")