# SkillPulse AI — Skill Gap & Workforce Evolution Predictor
**HCLTech | AI Future Ready FullStack Web Engineer — Problem Statement 4**

An AI-Powered Workforce Intelligence Platform combining an **Interactive Skills Knowledge Graph**, **Hybrid Dense-SVD + TF-IDF Vector RAG**, **Autoregressive Ridge ML Demand Forecasting**, **5-Agent Stateful Orchestration**, **Explainable AI (XAI)**, and **Responsible AI Bias Guardrails + Human-in-the-Loop HR Governance**.

---

## ⚡ Quick Start (1-Command Local Execution)

### 1. Start the Full-Stack Platform (Frontend + FastAPI Backend + SQLite + Vector RAG)
```powershell
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```
- **Web Application Portal:** Open `http://127.0.0.1:8000`
- **Interactive OpenAPI / Swagger Docs:** Open `http://127.0.0.1:8000/docs`

### 2. Run Automated Verification Test Suite (`FR-01` to `FR-10`)
```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

---

## ✅ 100% Functional Requirement Coverage (`FR-01` to `FR-10`)

| ID | Capability | Implementation Module | API Endpoint |
| :--- | :--- | :--- | :--- |
| **FR-01** | **Skill Inventory Assessment** | `backend/data/seed_dataset.py` & `backend/main.py` | `GET /api/v1/employees` & `POST /api/v1/profile/extract-skills` |
| **FR-02** | **Skill Gap Detection** | `backend/engines/knowledge_graph.py` | `GET /api/v1/graph/skills-network` & `POST /api/v1/agents/analyze-employee` |
| **FR-03** | **Market Intelligence (RAG)** | `backend/engines/rag_vector_store.py` | `GET /api/v1/rag/search` |
| **FR-04** | **Demand Forecasting (6/12/24m)** | `backend/engines/ml_forecaster.py` | `GET /api/v1/forecast/dashboard` |
| **FR-05** | **Personalized Learning Paths** | `backend/agents/orchestrator.py` (Agent 3) | `POST /api/v1/agents/analyze-employee` |
| **FR-06** | **Internal Mobility Analysis** | `backend/agents/orchestrator.py` (Agent 4) | `GET /api/v1/mobility/match` |
| **FR-07** | **Workforce Risk Assessment** | `backend/engines/ml_forecaster.py` | `GET /api/v1/forecast/dashboard` |
| **FR-08** | **Career Path Recommendations** | `backend/agents/orchestrator.py` (Agent 3) | `POST /api/v1/agents/analyze-employee` |
| **FR-09** | **Explainable AI (XAI)** | `backend/agents/orchestrator.py` (Agent 5) | `POST /api/v1/agents/analyze-employee` |
| **FR-10** | **Human Review & Bias Guardrail** | `backend/engines/bias_guardrail.py` & `backend/main.py` | `GET /api/v1/governance/queue`, `POST /api/v1/governance/decision`, `POST /api/v1/guardrail/test` |

---

## 📚 Documentation & Evaluation Deliverables
- **Architecture & End-to-End Blueprint:** [`docs/ARCHITECTURE_BLUEPRINT.md`](docs/ARCHITECTURE_BLUEPRINT.md)
- **Technical Documentation:** [`docs/TECHNICAL_DOCUMENTATION.md`](docs/TECHNICAL_DOCUMENTATION.md)
- **Model & Workforce Evaluation Report:** [`docs/EVALUATION_REPORT.md`](docs/EVALUATION_REPORT.md)
