# OBSIDIAN: Enterprise AI & Multi-Hop E-Commerce Analytics Engine

![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

## Executive Summary
OBSIDIAN is a fault-tolerant, production-ready AI pipeline designed to transition e-commerce data from passive, tabular dashboards into an active, multi-hop reasoning engine. Built over a 1.5M+ row synthetic dataset based on Olist, this architecture merges predictive machine learning (XGBoost) with autonomous agentic workflows (LangGraph/Groq) and interactive knowledge graphs (NetworkX/PyVis).

It is specifically engineered for high-latency, strictly firewalled network environments, featuring custom exponential backoff loops and Deep Packet Inspection (DPI) bypass routing to ensure uninterrupted cloud warehouse extraction.

## 🏗️ System Architecture

| Tier | Technology Stack | Functionality |
| :--- | :--- | :--- |
| **Data Warehouse** | Supabase (PostgreSQL) | Cloud-native relational database hosting 1.5M+ rows of customer, order, and seller data. |
| **AI / Inference** | LangGraph, Groq, XGBoost | Hierarchical ReAct agents for text-to-SQL synthesis and ML pipelines for multi-variable churn prediction. |
| **API Gateway** | FastAPI, Uvicorn, JWT | OAuth2 Password-Bearer secured backend managing asynchronous data streams and session state. |
| **Control Tower** | Streamlit, Plotly, PyVis | Hardware-accelerated UI rendering 3D business topography and physics-based neural networks. |
| **Deployment** | Docker Compose | Structurally mapped dual-service containerization for instant cloud deployment. |

## 🚀 Core Enterprise Features

* **Autonomous Agentic Analytics:** A LangGraph ReAct state machine powered by Groq's Llama 3 models dynamically writes, executes, and sanitizes SQL queries against the Supabase warehouse based on natural language prompts.
* **In-Memory Knowledge Graph (GraphRAG):** Bypasses traditional REST limitations by extracting relational tabular data and compiling it into a hardware-accelerated, interactive `NetworkX` physics engine, mapping the cascading relationships between toxic sellers and VIP customers.
* **Network-Resilient ETL Pipelines:** Engineered with custom connection-pooling and exponential backoff loops to actively detect and recover from dropped packets, DNS resolution failures, and ISP firewall interruptions.
* **Zero-Trust Security:** The entire frontend Control Tower is locked behind a FastAPI JWT authorization flow. The LangGraph agent is sandboxed with strictly defined SQL scopes to prevent prompt-injection or unauthorized database manipulation.
* **3D Behavioral Topography:** Utilizes `Plotly` to render multidimensional visualizations, including Customer Lifetime Value (CLV) elasticity surfaces, multi-stage conversion funnels, and VIP segment radar charts.

## ⚙️ Local Development Setup

OBSIDIAN utilizes a decoupled architecture requiring two concurrent terminals.

**1. Clone & Configure**
```bash
git clone [https://github.com/SyedRazaZaidi/obsidian-enterprise.git](https://github.com/SyedRazaZaidi/obsidian-enterprise.git)
cd obsidian-enterprise
python -m venv venv
source venv/Scripts/activate  # Windows: .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**2. Environment Variables (`.env`)**
```env
DB_URI=postgresql://[user]:[password]@[aws-0-ap-south-1.pooler.supabase.com:6543/postgres](https://aws-0-ap-south-1.pooler.supabase.com:6543/postgres)
GROQ_API_KEY=gsk_...
SECRET_KEY=your_secure_jwt_secret
```

**3. Ignite the API Gateway (Terminal 1)**
```bash
uvicorn backend.main:app --reload
```

**4. Launch the Control Tower (Terminal 2)**
```bash
streamlit run frontend/app.py
```

## 🐳 Containerization
For production deployment, the architecture is fully mapped via `docker-compose.yml`.
```bash
docker compose up --build -d
```

---
**Architected by Syed Raza Abbas Zaidi**  
*BS Artificial Intelligence | AI & Automation Engineer*  
[LinkedIn](https://www.linkedin.com/in/syedrazaabbaszaidi/) | [GitHub](https://github.com/SyedRazaZaidi)
