import os
import time
import pandas as pd
import xgboost as xgb
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pickle

# --- CLOUD DATABASE CONFIGURATION ---
# IMPORTANT: Replace [YOUR-PASSWORD] with your actual Supabase password
DB_URI = "postgresql://postgres.rtzrbsfxpwtnziyayyty:Syedzai7317@aws-0-ap-south-1.pooler.supabase.com:6543/postgres"

# Added connection timeout parameters
engine = create_engine(DB_URI, pool_pre_ping=True, connect_args={'connect_timeout': 15})

# --- DIRECTORY SETUP ---
MODEL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "saved_models"))
os.makedirs(MODEL_DIR, exist_ok=True)

def execute_query_with_retries(query: str, table_desc: str, max_retries: int = 5) -> pd.DataFrame:
    """Executes SQL extraction with resilient exponential backoff."""
    for attempt in range(1, max_retries + 1):
        try:
            return pd.read_sql(query, engine)
        except Exception as e:
            if attempt == max_retries:
                print(f"   ❌ FAILED to extract {table_desc} after {max_retries} attempts: {str(e)}")
                raise e
            
            wait_time = attempt * 4
            print(f"   ⚠️ Network hiccup on {table_desc}. Retrying ({attempt}/{max_retries}) in {wait_time}s...")
            time.sleep(wait_time)

def extract_and_engineer_features():
    print("📡 Extracting raw transactional data from Supabase Cloud...")
    
    # 1. Extract Orders, Deliveries & Payments
    orders_query = """
        SELECT 
            c.customer_unique_id,
            o.order_id,
            o.order_purchase_timestamp,
            o.order_delivered_customer_date,
            o.order_estimated_delivery_date,
            p.payment_value
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        LEFT JOIN order_payments p ON o.order_id = p.order_id
        WHERE o.order_status = 'delivered'
    """
    df_orders = execute_query_with_retries(orders_query, "Orders Data")
    
    print("⚙️ Engineering RFM and Logistics Features...")
    df_orders['order_purchase_timestamp'] = pd.to_datetime(df_orders['order_purchase_timestamp'])
    df_orders['order_delivered_customer_date'] = pd.to_datetime(df_orders['order_delivered_customer_date'])
    df_orders['order_estimated_delivery_date'] = pd.to_datetime(df_orders['order_estimated_delivery_date'])
    
    # Calculate Delivery Delay Penalty
    df_orders['delivery_delay'] = (df_orders['order_delivered_customer_date'] - df_orders['order_estimated_delivery_date']).dt.days
    df_orders['delivery_delay'] = df_orders['delivery_delay'].apply(lambda x: x if x > 0 else 0)

    # Aggregate Monetary, Frequency, and Logistics
    rfm = df_orders.groupby('customer_unique_id').agg(
        frequency=('order_id', 'nunique'),
        monetary=('payment_value', 'sum'),
        last_purchase=('order_purchase_timestamp', 'max'),
        max_delivery_delay=('delivery_delay', 'max')
    ).reset_index()

    # Calculate Recency (Days since last purchase relative to dataset's current state)
    max_date = rfm['last_purchase'].max()
    rfm['recency'] = (max_date - rfm['last_purchase']).dt.days

    # Define Churn Target (1 = One-Time Buyer [Churned], 0 = Repeat Buyer [Loyal])
    rfm['churn'] = (rfm['frequency'] == 1).astype(int)

    # 2. Extract Review Sentiment
    print("🧠 Extracting Customer Sentiment...")
    reviews_query = """
        SELECT 
            c.customer_unique_id,
            AVG(r.review_score) as avg_review_score
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        JOIN order_reviews r ON o.order_id = r.order_id
        GROUP BY c.customer_unique_id
    """
    df_reviews = execute_query_with_retries(reviews_query, "Review Sentiment Data")
    
    # Merge Features into Master Analytics Dataset
    final_df = pd.merge(rfm, df_reviews, on='customer_unique_id', how='left')
    
    # Impute missing reviews with the global median to prevent skewed training
    final_df['avg_review_score'] = final_df['avg_review_score'].fillna(final_df['avg_review_score'].median())
    
    return final_df

def train_xgboost_engine(df):
    print("\n🚀 Training XGBoost Predictive Engine...")
    
    X = df[['recency', 'monetary', 'max_delivery_delay', 'avg_review_score']]
    y = df['churn']

    # Stratified Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # Initialize XGBoost with scale_pos_weight
    imbalance_ratio = len(y_train[y_train == 0]) / len(y_train[y_train == 1])
    model = xgb.XGBClassifier(
        n_estimators=150, 
        learning_rate=0.1, 
        max_depth=5, 
        scale_pos_weight=imbalance_ratio,
        random_state=42,
        eval_metric='aucpr'
    )
    
    model.fit(X_train, y_train)

    # Evaluate Model
    predictions = model.predict(X_test)
    print("\n📊 Model Evaluation Metrics:")
    print(classification_report(y_test, predictions))

    # Export Model Artifact
    model_path = os.path.join(MODEL_DIR, "xgboost_churn_model.pkl")
    with open(model_path, "wb") as f:
        pickle.dump(model, f)
        
    print(f"\n✅ Production Model compiled and saved to: {model_path}")

if __name__ == "__main__":
    dataset = extract_and_engineer_features()
    train_xgboost_engine(dataset)