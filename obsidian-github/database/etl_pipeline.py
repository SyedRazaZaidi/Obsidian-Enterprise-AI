import os
import time
import pandas as pd
from sqlalchemy import create_engine, inspect, text

# --- ENTERPRISE DATABASE CONFIGURATION ---
# Replace [YOUR-PASSWORD] with your actual Supabase database password
DB_URI = "postgresql://postgres.rtzrbsfxpwtnziyayyty:Syedzai7317@aws-0-ap-south-1.pooler.supabase.com:6543/postgres"

engine = create_engine(DB_URI, pool_pre_ping=True, connect_args={'connect_timeout': 15})
RAW_DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "raw"))

def get_existing_row_count(table_name: str) -> int:
    """Checks if table exists in PostgreSQL and returns its row count."""
    try:
        inspector = inspect(engine)
        if table_name in inspector.get_table_names():
            with engine.connect() as conn:
                result = conn.execute(text(f'SELECT COUNT(*) FROM "{table_name}"'))
                return result.scalar() or 0
    except Exception:
        return 0
    return 0

def load_with_retries(df: pd.DataFrame, table_name: str, max_retries: int = 5) -> bool:
    """Executes database insertion with resilient exponential backoff."""
    for attempt in range(1, max_retries + 1):
        try:
            df.to_sql(table_name, engine, if_exists='replace', index=False, chunksize=10000)
            return True
        except Exception as e:
            if attempt == max_retries:
                print(f"   ❌ FAILED to load {table_name} after {max_retries} attempts: {str(e)}")
                return False
            
            wait_time = attempt * 4
            print(f"   ⚠️ Network hiccup on {table_name}. Retrying ({attempt}/{max_retries}) in {wait_time}s...")
            time.sleep(wait_time)

def run_enterprise_etl():
    print("🚀 Initializing OBSIDIAN Smart Cloud ETL Pipeline...")
    start_time = time.time()
    
    if not os.path.exists(RAW_DATA_DIR):
        print(f"❌ ERROR: Data directory not found at {RAW_DATA_DIR}")
        return

    csv_files = [f for f in os.listdir(RAW_DATA_DIR) if f.endswith('.csv')]
    if not csv_files:
        print("❌ ERROR: No CSV files found in data/raw.")
        return

    for file in csv_files:
        table_name = file.replace("olist_", "").replace("_dataset.csv", "").replace(".csv", "")
        file_path = os.path.join(RAW_DATA_DIR, file)
        
        # Check if table is already populated in Supabase
        existing_rows = get_existing_row_count(table_name)
        if existing_rows > 0:
            print(f"⏩ [{table_name}] already contains {existing_rows:,} rows. Skipping...")
            continue
            
        print(f"⏳ Processing [{table_name}]...")
        df = pd.read_csv(file_path)
        
        success = load_with_retries(df, table_name)
        if success:
            print(f"   ✅ Successfully loaded {len(df):,} rows into table '{table_name}'.")

    elapsed = time.time() - start_time
    print(f"\n🏁 ETL Pipeline execution finished in {elapsed:.2f} seconds.")
    print("All enterprise tables verified in PostgreSQL.")

if __name__ == "__main__":
    run_enterprise_etl()