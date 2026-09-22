
https://github.com/user-attachments/assets/3f0f5763-c341-4aff-b9d3-fa8558a75705
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





<img width="1347" height="639" alt="obsidian login" src="https://github.com/user-attachments/assets/a3ce7fd3-057b-4702-879c-e57e198e0e2c" />


<img width="1349" height="640" alt="obsidian homescreen" src="https://github.com/user-attachments/assets/31ce98eb-cd3f-4293-bb1a-3177e265922d" />


<img width="1350" height="637" alt="obsidian executive summary" src="https://github.com/user-attachments/assets/a5878057-3bbf-4b3b-aa0a-7cec8fc42f40" />


<img width="1357" height="640" alt="obsidian predictive churn 1" src="https://github.com/user-attachments/assets/b69081e6-ec11-4c59-8721-fe317cf46035" />


<img width="1357" height="640" alt="obsidian predictive churn 2" src="https://github.com/user-attachments/assets/d3b95c94-cdef-4f89-a13a-50d1c26da737" />


<img width="1350" height="635" alt="obsidian analyst agent 1" src="https://github.com/user-attachments/assets/06285ddf-9ca2-4591-8ee0-43efc8a84b41" />


<img width="1353" height="638" alt="obsidian analyst agent 2" src="https://github.com/user-attachments/assets/245f0b11-194f-49ca-8283-de3a417c662f" />


<img width="1352" height="638" alt="obsidian analytics hub 1" src="https://github.com/user-attachments/assets/52e17dbf-4303-4449-8d53-40d879d389b8" />


<img width="1014" height="508" alt="obsidian analytics hub 2" src="https://github.com/user-attachments/assets/f208d751-6b7b-4e6f-9190-77771e7fd016" />


<img width="1348" height="639" alt="obsidian analytics hub 3" src="https://github.com/user-attachments/assets/3eb47f4b-014b-4af4-a815-32889ad6d8c8" />


<img width="1352" height="639" alt="obsidian analytics hub 4" src="https://github.com/user-attachments/assets/29a35737-5c28-4c7c-acec-d8587b2f6318" />


<img width="450" height="469" alt="obsidian analytics hub 5" src="https://github.com/user-attachments/assets/cd4f0064-d2a6-4290-99a9-a38321381f20" />


<img width="501" height="390" alt="obsidian analytics hub 6" src="https://github.com/user-attachments/assets/f7fa139f-3701-4eb1-bfd5-6e3139ab9a5e" />


<img width="397" height="509" alt="obsidian analytics hub 7" src="https://github.com/user-attachments/assets/71c64c3c-c1ec-4d85-9182-96ac80074f9e" />


<img width="450" height="506" alt="obsidian analytics hub 8" src="https://github.com/user-attachments/assets/63c84ee6-c030-409e-b6c9-aa7529090a5a" />


<img width="974" height="559" alt="obsidian analytics hub 9" src="https://github.com/user-attachments/assets/48ccda5e-016f-4246-ba73-174f7b3a10ea" />


<img width="1352" height="639" alt="obsidian multi knowledge graph 1" src="https://github.com/user-attachments/assets/5e9e04cb-0390-462b-adbb-c6c2bb2c8f57" />


<img width="1340" height="636" alt="obsidian multi knowledge graph 2" src="https://github.com/user-attachments/assets/54ab3be8-ffd5-455f-b35f-009a60d8fcb2" />


<img width="878" height="573" alt="obsidian multi knowledge graph 3" src="https://github.com/user-attachments/assets/46615d65-0169-4b3f-83d8-65052b09dc94" />


Uploading Enterprise Knowledge Graph - Personal - Microsoft​ Edge 2026-09-22 14-52-36.mp4…
