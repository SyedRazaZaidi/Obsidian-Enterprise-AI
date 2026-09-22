import os
import time
import pickle
import pandas as pd
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import create_engine, text
from backend.auth import create_access_token, get_current_user, verify_password, FAKE_USER_DB, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
from backend.agent import process_natural_language_query
from pydantic import BaseModel

app = FastAPI(title="OBSIDIAN Enterprise API", version="1.0.0")

# --- CLOUD DATABASE & MODEL CONFIG ---
# IMPORTANT: Replace [YOUR-PASSWORD] with your actual Supabase password
DB_URI = "postgresql://postgres.rtzrbsfxpwtnziyayyty:Syedzai7317@aws-0-ap-south-1.pooler.supabase.com:6543/postgres"

engine = create_engine(DB_URI, pool_pre_ping=True, connect_args={'connect_timeout': 15})

MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "ml_engine", "saved_models", "xgboost_churn_model.pkl"))

# Load the AI Model into memory on startup
try:
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    print("✅ XGBoost Model successfully loaded into API memory.")
except Exception as e:
    print(f"❌ ERROR loading model: {e}")
    model = None

# --- AUTHENTICATION ENDPOINT ---
@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = FAKE_USER_DB.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user["username"]}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# --- SECURE DATA ENDPOINTS ---
@app.get("/api/v1/kpis")
async def get_dashboard_kpis(current_user: dict = Depends(get_current_user)):
    """Fetches high-level executive metrics from PostgreSQL with Pool Disposal."""
    max_retries = 5
    for attempt in range(1, max_retries + 1):
        try:
            with engine.connect() as conn:
                # Get Total Revenue
                rev_result = conn.execute(text("SELECT SUM(payment_value) FROM order_payments"))
                total_revenue = rev_result.scalar() or 0
                
                # Get Total Delivered Orders
                order_result = conn.execute(text("SELECT COUNT(order_id) FROM orders WHERE order_status = 'delivered'"))
                total_orders = order_result.scalar() or 0

            return {
                "total_revenue_brl": round(total_revenue, 2),
                "total_delivered_orders": total_orders
            }
        except Exception as e:
            # CRITICAL FIX: Destroy the corrupted connection pool so it doesn't get reused
            engine.dispose()
            
            if attempt == max_retries:
                raise HTTPException(status_code=500, detail=str(e))
            
            print(f"⚠️ Network drop caught. Rebuilding pool and retrying ({attempt}/{max_retries})...")
            time.sleep(3)

@app.post("/api/v1/predict_churn")
async def predict_customer_churn(recency: int, monetary: float, max_delivery_delay: int, avg_review_score: float, current_user: dict = Depends(get_current_user)):
    """Runs live real-time inference using the XGBoost Model."""
    if model is None:
        raise HTTPException(status_code=500, detail="AI Model not loaded.")
    
    input_df = pd.DataFrame([{
        'recency': recency,
        'monetary': monetary,
        'max_delivery_delay': max_delivery_delay,
        'avg_review_score': avg_review_score
    }])
    
    prediction = model.predict(input_df)[0]
    probability = model.predict_proba(input_df)[0][1]
    
    return {
        "churn_prediction": int(prediction),
        "churn_risk_probability": round(float(probability) * 100, 2),
        "status": "High Risk (One-Time Buyer)" if prediction == 1 else "Loyal (Repeat Buyer)"
    }
class AgentQuery(BaseModel):
    query: str

@app.post("/api/v1/ask_obsidian")
async def ask_obsidian_agent(payload: AgentQuery, current_user: dict = Depends(get_current_user)):
    """Routes natural language to the LangGraph autonomous reasoning engine."""
    try:
        answer = await process_natural_language_query(payload.query)
        return {"response": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))