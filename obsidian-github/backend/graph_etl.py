import pandas as pd
import time
import requests
from sqlalchemy import create_engine

# --- ENTERPRISE CREDENTIALS ---
PG_URI = "postgresql://postgres.rtzrbsfxpwtnziyayyty:Syedzai7317@aws-0-ap-south-1.pooler.supabase.com:6543/postgres"

# HTTPS REST API Configuration (Bypassing Port 7687 Blocks)
NEO4J_HTTP_URL = "https://228a9df0.databases.neo4j.io/db/neo4j/tx/commit"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = ""

def extract_from_postgres():
    """Extracts relational data from Supabase with Enterprise Fault Tolerance."""
    print("🚀 Connecting to Supabase PostgreSQL...")
    engine = create_engine(PG_URI)
    
    query = """
        SELECT 
            c.customer_id, c.customer_state,
            o.order_id, o.order_status,
            oi.product_id, oi.seller_id, oi.price,
            r.review_score,
            s.seller_state
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN order_reviews r ON o.order_id = r.order_id
        JOIN sellers s ON oi.seller_id = s.seller_id
        LIMIT 5000;
    """
    
    max_retries = 5
    for attempt in range(1, max_retries + 1):
        try:
            df = pd.read_sql(query, engine)
            print(f"✅ Extracted {len(df)} rows from Supabase.")
            return df
        except Exception as e:
            engine.dispose()
            if attempt == max_retries:
                raise e
            wait_time = attempt * 4
            print(f"⚠️ Network drop caught during extraction. Retrying ({attempt}/{max_retries}) in {wait_time}s...")
            time.sleep(wait_time)

def load_into_neo4j_via_rest(df):
    """Transforms and loads data into Neo4j by tunneling through HTTPS."""
    print("🚀 Routing around ISP Port Blocks... Connecting to Neo4j via HTTPS REST API...")
    
    cypher_query = """
    UNWIND $batch AS row
    MERGE (c:Customer {id: row.customer_id}) SET c.state = row.customer_state
    MERGE (o:Order {id: row.order_id}) SET o.status = row.order_status
    MERGE (p:Product {id: row.product_id})
    MERGE (s:Seller {id: row.seller_id}) SET s.state = row.seller_state
    MERGE (r:Review {id: row.order_id + "_rev"}) SET r.score = row.review_score
    MERGE (c)-[:PLACED]->(o)
    MERGE (o)-[:CONTAINS {price: row.price}]->(p)
    MERGE (p)-[:SOLD_BY]->(s)
    MERGE (o)-[:RECEIVED]->(r)
    """
    
    records = df.to_dict('records')
    
    # Constructing the REST Transaction Payload
    payload = {
        "statements": [
            {"statement": "MATCH (n) DETACH DELETE n"}, # Clear existing graph
            {"statement": cypher_query, "parameters": {"batch": records}}
        ]
    }
    
    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.post(
                NEO4J_HTTP_URL,
                auth=(NEO4J_USER, NEO4J_PASSWORD),
                json=payload,
                timeout=45,
                headers={"Accept": "application/json", "Content-Type": "application/json"}
            )
            
            if response.status_code in [200, 201]:
                resp_data = response.json()
                if resp_data.get("errors"):
                    raise Exception(f"Neo4j Cypher Error: {resp_data['errors']}")
                print("✅ Graph topology successfully built via HTTPS REST API.")
                return
            else:
                raise Exception(f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            if attempt == max_retries:
                raise e
            print(f"⚠️ HTTPS Timeout caught. Retrying ({attempt}/{max_retries}) in 5s...")
            time.sleep(5)

if __name__ == "__main__":
    print("Initiating OBSIDIAN Graph ETL Process...")
    data = extract_from_postgres()
    load_into_neo4j_via_rest(data)
    print("🎉 ETL Complete. Knowledge Graph is live.")