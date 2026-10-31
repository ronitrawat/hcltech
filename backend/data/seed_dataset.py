"""
Balanced Synthetic & Anonymized Enterprise Workforce Dataset Generator
======================================================================
Calibrated on:
1. O*NET 28.0 / ESCO Technical Skills Ontology (45 skills across 6 domains + adjacency edges)
2. Stack Overflow / GitHub Octoverse / WEF Future of Jobs 24-month demand velocity curves
3. Stratified Anonymized Employee Profiles (120 employees: 20 per department, balanced L1-L5)
   - Includes deliberate canary demographic attributes (age, gender, ethnicity) in raw intake
     ONLY so the Responsible AI Bias Guardrail (FR-10) can demonstrably strip and audit them.
4. RAG Knowledge Corpus (Market Intelligence Reports, Verified Learning Courses, Role Specs)
"""

from __future__ import annotations
import math
import random
from typing import Dict, List, Any

# Fixed deterministic seed for 100% reproducible training & evaluation
RNG = random.Random(42)

# ---------------------------------------------------------------------------
# 1. BALANCED SKILLS ONTOLOGY (45 Skills: 15 Emerging, 15 Core, 15 Legacy)
# ---------------------------------------------------------------------------
SKILLS_CATALOG: List[Dict[str, Any]] = [
    # --- EMERGING / HYPER-GROWTH SKILLS (15) ---
    {"id": "SK-001", "name": "LangGraph & Agentic AI", "domain": "AI & Data Science", "lifecycle": "EMERGING", "market_growth_yoy": 142.0, "contractor_hourly_usd": 165, "complexity": 4},
    {"id": "SK-002", "name": "RAG & Vector Databases", "domain": "AI & Data Science", "lifecycle": "EMERGING", "market_growth_yoy": 128.0, "contractor_hourly_usd": 155, "complexity": 4},
    {"id": "SK-003", "name": "LLM Guardrails & XAI", "domain": "AI & Data Science", "lifecycle": "EMERGING", "market_growth_yoy": 115.0, "contractor_hourly_usd": 160, "complexity": 4},
    {"id": "SK-004", "name": "Fine-Tuning & LoRA/PEFT", "domain": "AI & Data Science", "lifecycle": "EMERGING", "market_growth_yoy": 96.0, "contractor_hourly_usd": 150, "complexity": 5},
    {"id": "SK-005", "name": "Kubernetes Security (K8s Sec)", "domain": "Cloud & Platform", "lifecycle": "EMERGING", "market_growth_yoy": 88.0, "contractor_hourly_usd": 145, "complexity": 4},
    {"id": "SK-006", "name": "Cloud FinOps & Cost AI", "domain": "Cloud & Platform", "lifecycle": "EMERGING", "market_growth_yoy": 82.0, "contractor_hourly_usd": 135, "complexity": 3},
    {"id": "SK-007", "name": "Platform Engineering (IDP)", "domain": "Cloud & Platform", "lifecycle": "EMERGING", "market_growth_yoy": 79.0, "contractor_hourly_usd": 140, "complexity": 4},
    {"id": "SK-008", "name": "Rust Systems Programming", "domain": "Full-Stack Engineering", "lifecycle": "EMERGING", "market_growth_yoy": 74.0, "contractor_hourly_usd": 150, "complexity": 5},
    {"id": "SK-009", "name": "Next.js App Router & SSR", "domain": "Full-Stack Engineering", "lifecycle": "EMERGING", "market_growth_yoy": 68.0, "contractor_hourly_usd": 125, "complexity": 3},
    {"id": "SK-010", "name": "Zero-Trust Architecture", "domain": "Cybersecurity", "lifecycle": "EMERGING", "market_growth_yoy": 92.0, "contractor_hourly_usd": 155, "complexity": 4},
    {"id": "SK-011", "name": "AI Threat & Prompt Security", "domain": "Cybersecurity", "lifecycle": "EMERGING", "market_growth_yoy": 134.0, "contractor_hourly_usd": 165, "complexity": 4},
    {"id": "SK-012", "name": "Post-Quantum Cryptography", "domain": "Cybersecurity", "lifecycle": "EMERGING", "market_growth_yoy": 64.0, "contractor_hourly_usd": 170, "complexity": 5},
    {"id": "SK-013", "name": "Real-Time Streaming (Kafka/Flink)", "domain": "Data Engineering", "lifecycle": "EMERGING", "market_growth_yoy": 71.0, "contractor_hourly_usd": 140, "complexity": 4},
    {"id": "SK-014", "name": "Data Mesh & Lakehouse (Iceberg)", "domain": "Data Engineering", "lifecycle": "EMERGING", "market_growth_yoy": 84.0, "contractor_hourly_usd": 145, "complexity": 4},
    {"id": "SK-015", "name": "OpenTelemetry & AIOps", "domain": "Cloud & Platform", "lifecycle": "EMERGING", "market_growth_yoy": 89.0, "contractor_hourly_usd": 135, "complexity": 3},

    # --- CORE STABLE ENTERPRISE SKILLS (15) ---
    {"id": "SK-016", "name": "Python & FastAPI", "domain": "Full-Stack Engineering", "lifecycle": "CORE", "market_growth_yoy": 38.0, "contractor_hourly_usd": 115, "complexity": 3},
    {"id": "SK-017", "name": "React & TypeScript", "domain": "Full-Stack Engineering", "lifecycle": "CORE", "market_growth_yoy": 34.0, "contractor_hourly_usd": 110, "complexity": 3},
    {"id": "SK-018", "name": "Node.js & Express Microservices", "domain": "Full-Stack Engineering", "lifecycle": "CORE", "market_growth_yoy": 22.0, "contractor_hourly_usd": 105, "complexity": 3},
    {"id": "SK-019", "name": "Java Spring Boot", "domain": "Full-Stack Engineering", "lifecycle": "CORE", "market_growth_yoy": 18.0, "contractor_hourly_usd": 110, "complexity": 3},
    {"id": "SK-020", "name": "PostgreSQL & PgVector", "domain": "Data Engineering", "lifecycle": "CORE", "market_growth_yoy": 41.0, "contractor_hourly_usd": 115, "complexity": 3},
    {"id": "SK-021", "name": "Docker & Containerization", "domain": "Cloud & Platform", "lifecycle": "CORE", "market_growth_yoy": 29.0, "contractor_hourly_usd": 105, "complexity": 2},
    {"id": "SK-022", "name": "Kubernetes (EKS/AKS)", "domain": "Cloud & Platform", "lifecycle": "CORE", "market_growth_yoy": 44.0, "contractor_hourly_usd": 130, "complexity": 4},
    {"id": "SK-023", "name": "Terraform & IaC", "domain": "Cloud & Platform", "lifecycle": "CORE", "market_growth_yoy": 36.0, "contractor_hourly_usd": 125, "complexity": 3},
    {"id": "SK-024", "name": "AWS / Azure Cloud Architecture", "domain": "Cloud & Platform", "lifecycle": "CORE", "market_growth_yoy": 39.0, "contractor_hourly_usd": 135, "complexity": 4},
    {"id": "SK-025", "name": "Scikit-Learn & Classical ML", "domain": "AI & Data Science", "lifecycle": "CORE", "market_growth_yoy": 31.0, "contractor_hourly_usd": 125, "complexity": 3},
    {"id": "SK-026", "name": "PyTorch & Deep Learning", "domain": "AI & Data Science", "lifecycle": "CORE", "market_growth_yoy": 48.0, "contractor_hourly_usd": 140, "complexity": 4},
    {"id": "SK-027", "name": "OAuth 2.0, OIDC & IAM", "domain": "Cybersecurity", "lifecycle": "CORE", "market_growth_yoy": 27.0, "contractor_hourly_usd": 120, "complexity": 3},
    {"id": "SK-028", "name": "DevSecOps & SAST/DAST", "domain": "Cybersecurity", "lifecycle": "CORE", "market_growth_yoy": 42.0, "contractor_hourly_usd": 130, "complexity": 3},
    {"id": "SK-029", "name": "Apache Spark & PySpark", "domain": "Data Engineering", "lifecycle": "CORE", "market_growth_yoy": 25.0, "contractor_hourly_usd": 120, "complexity": 3},
    {"id": "SK-030", "name": "CI/CD (GitHub Actions / Azure DevOps)", "domain": "Cloud & Platform", "lifecycle": "CORE", "market_growth_yoy": 30.0, "contractor_hourly_usd": 110, "complexity": 2},

    # --- LEGACY / DECLINING SKILLS (15 - Prime Reskilling Source Pool) ---
    {"id": "SK-031", "name": "Monolithic J2EE & Struts", "domain": "Legacy Modernization", "lifecycle": "LEGACY", "market_growth_yoy": -28.0, "contractor_hourly_usd": 85, "complexity": 3},
    {"id": "SK-032", "name": "SOAP / XML Web Services", "domain": "Legacy Modernization", "lifecycle": "LEGACY", "market_growth_yoy": -34.0, "contractor_hourly_usd": 80, "complexity": 2},
    {"id": "SK-033", "name": "Manual Functional QA Testing", "domain": "Legacy Modernization", "lifecycle": "LEGACY", "market_growth_yoy": -41.0, "contractor_hourly_usd": 65, "complexity": 1},
    {"id": "SK-034", "name": "jQuery & Legacy Bootstrap UI", "domain": "Legacy Modernization", "lifecycle": "LEGACY", "market_growth_yoy": -36.0, "contractor_hourly_usd": 75, "complexity": 2},
    {"id": "SK-035", "name": "On-Prem Windows Server Admin", "domain": "Legacy Modernization", "lifecycle": "LEGACY", "market_growth_yoy": -24.0, "contractor_hourly_usd": 85, "complexity": 2},
    {"id": "SK-036", "name": "SVN / TFS Version Control", "domain": "Legacy Modernization", "lifecycle": "LEGACY", "market_growth_yoy": -48.0, "contractor_hourly_usd": 70, "complexity": 1},
    {"id": "SK-037", "name": "Classic ASP.NET WebForms", "domain": "Legacy Modernization", "lifecycle": "LEGACY", "market_growth_yoy": -39.0, "contractor_hourly_usd": 80, "complexity": 2},
    {"id": "SK-038", "name": "Legacy ETL (Informatica PowerCenter)", "domain": "Legacy Modernization", "lifecycle": "LEGACY", "market_growth_yoy": -22.0, "contractor_hourly_usd": 90, "complexity": 3},
    {"id": "SK-039", "name": "Perl & KornShell Scripting", "domain": "Legacy Modernization", "lifecycle": "LEGACY", "market_growth_yoy": -45.0, "contractor_hourly_usd": 75, "complexity": 2},
    {"id": "SK-040", "name": "Oracle Forms & PL/SQL Monoliths", "domain": "Legacy Modernization", "lifecycle": "LEGACY", "market_growth_yoy": -26.0, "contractor_hourly_usd": 90, "complexity": 3},
    {"id": "SK-041", "name": "Static Firewall Rule Management", "domain": "Legacy Modernization", "lifecycle": "LEGACY", "market_growth_yoy": -31.0, "contractor_hourly_usd": 85, "complexity": 2},
    {"id": "SK-042", "name": "Hadoop MapReduce v1", "domain": "Legacy Modernization", "lifecycle": "LEGACY", "market_growth_yoy": -52.0, "contractor_hourly_usd": 80, "complexity": 3},
    {"id": "SK-043", "name": "COBOL Mainframe Batch", "domain": "Legacy Modernization", "lifecycle": "LEGACY", "market_growth_yoy": -19.0, "contractor_hourly_usd": 95, "complexity": 3},
    {"id": "SK-044", "name": "Manual Release Runbooks", "domain": "Legacy Modernization", "lifecycle": "LEGACY", "market_growth_yoy": -44.0, "contractor_hourly_usd": 70, "complexity": 1},
    {"id": "SK-045", "name": "SPSS / Legacy Desktop BI", "domain": "Legacy Modernization", "lifecycle": "LEGACY", "market_growth_yoy": -33.0, "contractor_hourly_usd": 75, "complexity": 2},
]

# ---------------------------------------------------------------------------
# 2. SKILLS KNOWLEDGE GRAPH EDGES (Adjacency & Prerequisites)
# ---------------------------------------------------------------------------
SKILL_GRAPH_EDGES: List[Dict[str, Any]] = [
    # AI & Data Science progression
    {"source": "SK-016", "target": "SK-001", "relation": "PREREQUISITE_OF", "weight": 0.86, "rationale": "Python & FastAPI async patterns directly transfer to LangGraph agent state machines."},
    {"source": "SK-016", "target": "SK-002", "relation": "PREREQUISITE_OF", "weight": 0.84, "rationale": "Python API builders transition rapidly to RAG ingestion and vector retrieval pipelines."},
    {"source": "SK-025", "target": "SK-002", "relation": "ADJACENT_TO", "weight": 0.82, "rationale": "Scikit-learn vector space & cosine similarity concepts directly underpin Vector DBs."},
    {"source": "SK-025", "target": "SK-003", "relation": "ADJACENT_TO", "weight": 0.85, "rationale": "Classical ML feature attribution (SHAP/Gini) transfers directly to XAI & LLM Guardrails."},
    {"source": "SK-026", "target": "SK-004", "relation": "PREREQUISITE_OF", "weight": 0.90, "rationale": "PyTorch tensor & gradient fundamentals are the foundation of LoRA/PEFT fine-tuning."},
    {"source": "SK-002", "target": "SK-001", "relation": "ADJACENT_TO", "weight": 0.88, "rationale": "RAG retrieval is a core tool node inside multi-agent LangGraph architectures."},
    {"source": "SK-001", "target": "SK-003", "relation": "ADJACENT_TO", "weight": 0.83, "rationale": "Multi-agent workflows require output guardrails and policy validation nodes."},
    {"source": "SK-020", "target": "SK-002", "relation": "PREREQUISITE_OF", "weight": 0.87, "rationale": "PostgreSQL & PgVector directly bridge relational SQL engineers into vector search."},

    # Cloud & Platform progression
    {"source": "SK-021", "target": "SK-022", "relation": "PREREQUISITE_OF", "weight": 0.89, "rationale": "Docker containerization is the mandatory foundation for Kubernetes orchestration."},
    {"source": "SK-022", "target": "SK-005", "relation": "PREREQUISITE_OF", "weight": 0.85, "rationale": "Kubernetes cluster administration transitions naturally to K8s RBAC, Pod Security & eBPF."},
    {"source": "SK-023", "target": "SK-007", "relation": "PREREQUISITE_OF", "weight": 0.84, "rationale": "Terraform IaC modules form the self-service golden paths of Internal Developer Platforms."},
    {"source": "SK-024", "target": "SK-006", "relation": "ADJACENT_TO", "weight": 0.81, "rationale": "Cloud Architects understand compute/storage billing required for Cloud FinOps."},
    {"source": "SK-030", "target": "SK-007", "relation": "ADJACENT_TO", "weight": 0.83, "rationale": "CI/CD pipeline engineers can rapidly adopt Platform Engineering developer portals."},
    {"source": "SK-022", "target": "SK-015", "relation": "ADJACENT_TO", "weight": 0.80, "rationale": "Distributed Kubernetes workloads require OpenTelemetry tracing and AIOps correlation."},

    # Full-Stack progression
    {"source": "SK-017", "target": "SK-009", "relation": "PREREQUISITE_OF", "weight": 0.91, "rationale": "React & TypeScript developers can master Next.js App Router & Server Components in 2 weeks."},
    {"source": "SK-019", "target": "SK-016", "relation": "ADJACENT_TO", "weight": 0.76, "rationale": "Java Spring Boot REST/DI patterns map cleanly to Python FastAPI & Pydantic schemas."},
    {"source": "SK-018", "target": "SK-016", "relation": "ADJACENT_TO", "weight": 0.79, "rationale": "Async Node.js/Express microservice engineers easily adopt async Python FastAPI."},
    {"source": "SK-019", "target": "SK-008", "relation": "ADJACENT_TO", "weight": 0.68, "rationale": "Strong static typing and concurrency in Java help bridge into Rust systems programming."},

    # Cybersecurity progression
    {"source": "SK-027", "target": "SK-010", "relation": "PREREQUISITE_OF", "weight": 0.87, "rationale": "OAuth2/OIDC identity federation is the primary pillar of Zero-Trust Architecture."},
    {"source": "SK-028", "target": "SK-011", "relation": "ADJACENT_TO", "weight": 0.82, "rationale": "DevSecOps pipeline scanners extend directly to prompt-injection & AI red-teaming."},
    {"source": "SK-028", "target": "SK-005", "relation": "ADJACENT_TO", "weight": 0.80, "rationale": "Container image scanning in DevSecOps leads directly into runtime Kubernetes security."},
    {"source": "SK-010", "target": "SK-012", "relation": "ADJACENT_TO", "weight": 0.72, "rationale": "Zero-trust cryptographic transport naturally evolves to Post-Quantum TLS readiness."},

    # Data Engineering progression
    {"source": "SK-029", "target": "SK-014", "relation": "PREREQUISITE_OF", "weight": 0.86, "rationale": "Apache Spark distributed processing powers Apache Iceberg Data Lakehouses."},
    {"source": "SK-029", "target": "SK-013", "relation": "ADJACENT_TO", "weight": 0.83, "rationale": "Spark Structured Streaming engineers rapidly transition to Kafka & Apache Flink."},
    {"source": "SK-020", "target": "SK-014", "relation": "ADJACENT_TO", "weight": 0.75, "rationale": "Advanced SQL & partitioning in PostgreSQL transfer well to Data Mesh governance."},

    # Legacy Modernization Bridge Edges (Crucial for Internal Mobility FR-06!)
    {"source": "SK-031", "target": "SK-019", "relation": "PREREQUISITE_OF", "weight": 0.84, "rationale": "Monolithic J2EE/Struts Java engineers already know core JVM & OOP needed for Spring Boot."},
    {"source": "SK-032", "target": "SK-016", "relation": "ADJACENT_TO", "weight": 0.74, "rationale": "SOAP/XML schema designers understand strict API contracts used in FastAPI/OpenAPI."},
    {"source": "SK-033", "target": "SK-028", "relation": "ADJACENT_TO", "weight": 0.71, "rationale": "Manual QA testers with domain knowledge can upskill into automated DevSecOps test suites."},
    {"source": "SK-034", "target": "SK-017", "relation": "PREREQUISITE_OF", "weight": 0.78, "rationale": "jQuery/DOM frontend developers can modernize to component-based React & TypeScript."},
    {"source": "SK-035", "target": "SK-021", "relation": "ADJACENT_TO", "weight": 0.76, "rationale": "On-prem server administrators understand OS networking needed for Docker & Cloud IaC."},
    {"source": "SK-036", "target": "SK-030", "relation": "PREREQUISITE_OF", "weight": 0.80, "rationale": "SVN source control admins transition smoothly to GitHub Actions & modern GitOps."},
    {"source": "SK-037", "target": "SK-017", "relation": "ADJACENT_TO", "weight": 0.73, "rationale": "ASP.NET WebForms UI developers transition well to modern TypeScript & React SPAs."},
    {"source": "SK-038", "target": "SK-029", "relation": "PREREQUISITE_OF", "weight": 0.82, "rationale": "Informatica ETL pipeline designers already master data transformation logic used in PySpark."},
    {"source": "SK-039", "target": "SK-016", "relation": "ADJACENT_TO", "weight": 0.77, "rationale": "Perl/Shell automation scripters rapidly pick up Python backend & automation engineering."},
    {"source": "SK-040", "target": "SK-020", "relation": "PREREQUISITE_OF", "weight": 0.88, "rationale": "Oracle PL/SQL experts transfer 90% of their relational tuning skills to PostgreSQL & PgVector."},
    {"source": "SK-041", "target": "SK-010", "relation": "PREREQUISITE_OF", "weight": 0.79, "rationale": "Network firewall engineers understand perimeter segmentation needed for Zero-Trust."},
    {"source": "SK-042", "target": "SK-029", "relation": "PREREQUISITE_OF", "weight": 0.87, "rationale": "Hadoop MapReduce engineers transition directly to in-memory Apache Spark."},
    {"source": "SK-043", "target": "SK-019", "relation": "ADJACENT_TO", "weight": 0.70, "rationale": "COBOL enterprise transaction engineers understand banking domain logic for Java microservices."},
    {"source": "SK-044", "target": "SK-030", "relation": "PREREQUISITE_OF", "weight": 0.81, "rationale": "Manual release coordinators know deployment gates needed to automate CI/CD pipelines."},
    {"source": "SK-045", "target": "SK-025", "relation": "PREREQUISITE_OF", "weight": 0.83, "rationale": "SPSS statistical analysts already understand regression and hypothesis testing for Scikit-learn."},
]

# ---------------------------------------------------------------------------
# 3. TARGET ENTERPRISE ROLES & UPCOMING PROJECTS (12 Roles, 8 Projects)
# ---------------------------------------------------------------------------
TARGET_ROLES: List[Dict[str, Any]] = [
    {
        "id": "ROLE-AI-ARCH",
        "title": "Enterprise Agentic AI Architect",
        "department": "AI & Data Science",
        "grade": "L4 - Lead / Architect",
        "open_positions": 8,
        "external_hiring_cost_usd": 42000,
        "avg_time_to_hire_weeks": 14,
        "salary_band_usd": "$155,000 - $185,000",
        "required_skills": {"SK-001": 4, "SK-002": 4, "SK-003": 3, "SK-016": 4, "SK-020": 3},
        "description": "Designs multi-agent LangGraph systems, enterprise RAG pipelines, and Responsible AI guardrails."
    },
    {
        "id": "ROLE-RAG-ENG",
        "title": "GenAI & Vector Search Engineer",
        "department": "AI & Data Science",
        "grade": "L3 - Senior Engineer",
        "open_positions": 12,
        "external_hiring_cost_usd": 36000,
        "avg_time_to_hire_weeks": 12,
        "salary_band_usd": "$135,000 - $160,000",
        "required_skills": {"SK-002": 4, "SK-016": 4, "SK-020": 4, "SK-025": 3, "SK-001": 3},
        "description": "Builds high-precision semantic search, vector indexing, and grounded LLM retrieval services."
    },
    {
        "id": "ROLE-MLOPS-ENG",
        "title": "LLM Fine-Tuning & MLOps Specialist",
        "department": "AI & Data Science",
        "grade": "L3 - Senior Engineer",
        "open_positions": 6,
        "external_hiring_cost_usd": 38000,
        "avg_time_to_hire_weeks": 13,
        "salary_band_usd": "$140,000 - $168,000",
        "required_skills": {"SK-004": 4, "SK-026": 4, "SK-025": 4, "SK-021": 3, "SK-003": 3},
        "description": "Trains, fine-tunes, evaluates, and monitors domain-specific ML and foundation models."
    },
    {
        "id": "ROLE-PLAT-ENG",
        "title": "Cloud-Native Platform Engineer (IDP)",
        "department": "Cloud & Platform",
        "grade": "L3 - Senior Engineer",
        "open_positions": 10,
        "external_hiring_cost_usd": 34000,
        "avg_time_to_hire_weeks": 11,
        "salary_band_usd": "$130,000 - $155,000",
        "required_skills": {"SK-007": 4, "SK-022": 4, "SK-023": 4, "SK-030": 4, "SK-015": 3},
        "description": "Builds golden-path internal developer portals, Kubernetes automation, and OpenTelemetry observability."
    },
    {
        "id": "ROLE-FINOPS-ARCH",
        "title": "Cloud FinOps & AIOps Architect",
        "department": "Cloud & Platform",
        "grade": "L4 - Lead / Architect",
        "open_positions": 5,
        "external_hiring_cost_usd": 35000,
        "avg_time_to_hire_weeks": 12,
        "salary_band_usd": "$140,000 - $165,000",
        "required_skills": {"SK-006": 4, "SK-024": 4, "SK-015": 4, "SK-022": 3, "SK-023": 3},
        "description": "Optimizes multi-cloud infrastructure spend and implements AI-driven telemetry anomaly detection."
    },
    {
        "id": "ROLE-FULLSTACK-AI",
        "title": "AI-Native Full-Stack Principal Engineer",
        "department": "Full-Stack Engineering",
        "grade": "L3 - Senior Engineer",
        "open_positions": 14,
        "external_hiring_cost_usd": 32000,
        "avg_time_to_hire_weeks": 10,
        "salary_band_usd": "$125,000 - $150,000",
        "required_skills": {"SK-017": 4, "SK-009": 4, "SK-016": 4, "SK-002": 3, "SK-020": 3},
        "description": "Delivers responsive React/Next.js + FastAPI applications with embedded AI copilots and semantic search."
    },
    {
        "id": "ROLE-RUST-SYS",
        "title": "High-Performance Rust & Microservices Engineer",
        "department": "Full-Stack Engineering",
        "grade": "L3 - Senior Engineer",
        "open_positions": 6,
        "external_hiring_cost_usd": 39000,
        "avg_time_to_hire_weeks": 14,
        "salary_band_usd": "$140,000 - $170,000",
        "required_skills": {"SK-008": 4, "SK-019": 3, "SK-021": 4, "SK-013": 3},
        "description": "Re-architects high-throughput payment and telemetry engines using memory-safe Rust and microservices."
    },
    {
        "id": "ROLE-ZERO-TRUST",
        "title": "Zero-Trust & AI Security Architect",
        "department": "Cybersecurity",
        "grade": "L4 - Lead / Architect",
        "open_positions": 7,
        "external_hiring_cost_usd": 41000,
        "avg_time_to_hire_weeks": 15,
        "salary_band_usd": "$150,000 - $180,000",
        "required_skills": {"SK-010": 4, "SK-011": 4, "SK-005": 4, "SK-027": 4, "SK-028": 3},
        "description": "Secures enterprise AI deployments, Kubernetes clusters, and identity perimeters with Zero-Trust controls."
    },
    {
        "id": "ROLE-LAKEHOUSE-ARCH",
        "title": "Real-Time Data Mesh & Lakehouse Engineer",
        "department": "Data Engineering",
        "grade": "L3 - Senior Engineer",
        "open_positions": 9,
        "external_hiring_cost_usd": 35000,
        "avg_time_to_hire_weeks": 11,
        "salary_band_usd": "$132,000 - $158,000",
        "required_skills": {"SK-014": 4, "SK-013": 4, "SK-029": 4, "SK-020": 4},
        "description": "Builds streaming Kafka/Flink pipelines and Apache Iceberg lakehouses for enterprise analytics & AI."
    },
]

UPCOMING_PROJECTS: List[Dict[str, Any]] = [
    {
        "id": "PRJ-2026-Q3-01",
        "name": "Global Banking Autonomous Copilot & RAG Platform",
        "client_sector": "BFSI / Global Banking",
        "start_quarter": "Q3 2026",
        "budget_usd": 4800000,
        "priority": "CRITICAL",
        "required_headcount": {"SK-001": 14, "SK-002": 18, "SK-003": 10, "SK-016": 20, "SK-010": 8}
    },
    {
        "id": "PRJ-2026-Q3-02",
        "name": "Multi-Cloud Zero-Trust Kubernetes Modernization",
        "client_sector": "Healthcare & Life Sciences",
        "start_quarter": "Q3 2026",
        "budget_usd": 3600000,
        "priority": "HIGH",
        "required_headcount": {"SK-005": 12, "SK-010": 11, "SK-022": 18, "SK-007": 10, "SK-023": 15}
    },
    {
        "id": "PRJ-2026-Q4-01",
        "name": "Real-Time Supply Chain Lakehouse & Streaming Hub",
        "client_sector": "Manufacturing & Retail",
        "start_quarter": "Q4 2026",
        "budget_usd": 3100000,
        "priority": "HIGH",
        "required_headcount": {"SK-013": 14, "SK-014": 15, "SK-029": 16, "SK-006": 8, "SK-015": 9}
    },
    {
        "id": "PRJ-2026-Q4-02",
        "name": "Next-Gen Customer Portal & Rust Edge Gateway",
        "client_sector": "Telecom & Media",
        "start_quarter": "Q4 2026",
        "budget_usd": 2900000,
        "priority": "MODERATE",
        "required_headcount": {"SK-008": 8, "SK-009": 16, "SK-017": 22, "SK-011": 7, "SK-004": 6}
    }
]

# ---------------------------------------------------------------------------
# 4. RAG KNOWLEDGE BASE CORPUS (Market Intelligence + Learning Catalog)
# ---------------------------------------------------------------------------
RAG_DOCUMENTS: List[Dict[str, Any]] = [
    # --- Market Intelligence Documents (FR-03) ---
    {
        "doc_id": "MKT-2026-01",
        "category": "MARKET_INTELLIGENCE",
        "title": "Gartner & WEF 2026 Strategic Technology Workforce Report: Agentic AI & LangGraph Surge",
        "source": "Enterprise Tech Radar Q2-2026 (Gartner / WEF Calibrated)",
        "related_skills": ["SK-001", "SK-002", "SK-003", "SK-016"],
        "content": (
            "Enterprise demand for stateful Multi-Agent AI orchestration (LangGraph, Semantic Kernel) grew 142% YoY. "
            "Over 68% of Fortune 500 IT services RFPs in 2026 require Retrieval-Augmented Generation (RAG), vector databases, "
            "and Responsible AI Guardrails (XAI). Organizations that upskill existing Python/FastAPI and SQL engineers "
            "into Agentic AI reduce time-to-delivery by 58% and save $34,000 per seat compared to external hiring."
        )
    },
    {
        "doc_id": "MKT-2026-02",
        "category": "MARKET_INTELLIGENCE",
        "title": "CNCF Cloud-Native Workforce Survey: Kubernetes Security, Platform Engineering & FinOps",
        "source": "CNCF Annual Cloud Native Benchmark 2026",
        "related_skills": ["SK-005", "SK-006", "SK-007", "SK-015", "SK-022"],
        "content": (
            "As Kubernetes adoption stabilizes above 84%, severe talent shortages have shifted from basic container deployment "
            "to Kubernetes Runtime Security (K8s Sec, +88% YoY), Internal Developer Platforms (IDP, +79% YoY), OpenTelemetry AIOps (+89% YoY), "
            "and Cloud FinOps (+82% YoY). Legacy on-prem sysadmins and CI/CD engineers show an 83% transition success rate into Platform Engineering."
        )
    },
    {
        "doc_id": "MKT-2026-03",
        "category": "MARKET_INTELLIGENCE",
        "title": "Cybersecurity Threat Landscape: Zero-Trust, AI Prompt Security & Post-Quantum Readiness",
        "source": "NIST & Global CISO Workforce Outlook 2026",
        "related_skills": ["SK-010", "SK-011", "SK-012", "SK-027", "SK-028"],
        "content": (
            "Enterprise LLM deployments have created an urgent 134% demand spike for AI Threat & Prompt Security specialists "
            "capable of preventing prompt injection, data exfiltration, and PII leakage. Simultaneously, Zero-Trust Architecture (+92% YoY) "
            "and Post-Quantum Cryptography readiness (+64% YoY) are mandatory for banking and public-sector compliance."
        )
    },
    {
        "doc_id": "MKT-2026-04",
        "category": "MARKET_INTELLIGENCE",
        "title": "Legacy Obsolescence Alert: Monolithic J2EE, Manual QA, SOAP & Traditional ETL Decline",
        "source": "HCLTech Enterprise Modernization Index 2026",
        "related_skills": ["SK-031", "SK-032", "SK-033", "SK-038", "SK-040"],
        "content": (
            "Client demand for monolithic J2EE/Struts (-28% YoY), manual functional QA (-41% YoY), SOAP XML services (-34% YoY), "
            "and legacy Informatica ETL (-22% YoY) continues to contract sharply. However, engineers holding these legacy skills "
            "possess deep enterprise domain knowledge and achieve an 85% retention rate when guided through structured 6-to-10 week "
            "bridge curricula into Spring Boot, FastAPI, PySpark Lakehouses, and Automated DevSecOps."
        )
    },
    {
        "doc_id": "MKT-2026-05",
        "category": "MARKET_INTELLIGENCE",
        "title": "Data Architecture Evolution: Apache Iceberg Lakehouses & Real-Time Kafka/Flink Streaming",
        "source": "Modern Data Stack Workforce Report 2026",
        "related_skills": ["SK-013", "SK-014", "SK-029", "SK-020"],
        "content": (
            "Real-time event streaming with Kafka/Flink (+71% YoY) and open table formats like Apache Iceberg Data Mesh/Lakehouse (+84% YoY) "
            "are replacing batch Hadoop MapReduce (-52% YoY) and legacy ETL. Oracle PL/SQL and Spark engineers represent the highest-ROI "
            "internal talent pool for Lakehouse and PgVector modernization."
        )
    },

    # --- Verified Learning Catalog Documents (FR-05) ---
    {
        "doc_id": "CRS-AI-101",
        "category": "LEARNING_COURSE",
        "title": "Production Agentic AI with LangGraph, Tool Calling & Stateful Workflows",
        "provider": "DeepLearning.AI / LangChain Academy",
        "certification": "Certified Agentic AI Architect (CAAI)",
        "duration_hours": 28,
        "difficulty": "Intermediate-Advanced",
        "related_skills": ["SK-001", "SK-016"],
        "content": (
            "Hands-on engineering certification covering cyclic state graphs, multi-agent supervisor coordination, human-in-the-loop "
            "approval checkpoints, persistent memory, and hybrid local/cloud LLM routing using Python and FastAPI."
        )
    },
    {
        "doc_id": "CRS-AI-102",
        "category": "LEARNING_COURSE",
        "title": "Enterprise RAG, FAISS/Chroma Vector Databases & Grounded Evaluation",
        "provider": "AWS & DeepLearning.AI",
        "certification": "Enterprise RAG & Vector Search Specialist",
        "duration_hours": 24,
        "difficulty": "Intermediate",
        "related_skills": ["SK-002", "SK-020", "SK-025"],
        "content": (
            "Covers semantic chunking, dense/sparse hybrid embeddings, FAISS & PgVector indexing, citation traceability, "
            "and hallucination/groundedness evaluation metrics."
        )
    },
    {
        "doc_id": "CRS-AI-103",
        "category": "LEARNING_COURSE",
        "title": "Responsible AI, Explainable AI (SHAP/LIME) & LLM Safety Guardrails",
        "provider": "Linux Foundation / AI Governance Institute",
        "certification": "Responsible & Explainable AI Practitioner",
        "duration_hours": 18,
        "difficulty": "Intermediate",
        "related_skills": ["SK-003", "SK-025", "SK-011"],
        "content": (
            "Teaches demographic bias stripping, fairness auditing, feature importance attribution, prompt injection defense, "
            "and EU AI Act / NIST AI RMF governance compliance."
        )
    },
    {
        "doc_id": "CRS-AI-104",
        "category": "LEARNING_COURSE",
        "title": "Parameter-Efficient LLM Fine-Tuning (LoRA, QLoRA & PyTorch Distributed)",
        "provider": "HuggingFace & PyTorch Foundation",
        "certification": "PyTorch LLM Fine-Tuning Specialist",
        "duration_hours": 32,
        "difficulty": "Advanced",
        "related_skills": ["SK-004", "SK-026"],
        "content": (
            "Deep dive into instruction tuning, LoRA/PEFT adapters, quantization, RLHF/DPO alignment, and MLflow experiment tracking."
        )
    },
    {
        "doc_id": "CRS-CLD-201",
        "category": "LEARNING_COURSE",
        "title": "Certified Kubernetes Security Specialist (CKS) & Runtime Defense",
        "provider": "Cloud Native Computing Foundation (CNCF)",
        "certification": "CNCF CKS - Kubernetes Security Specialist",
        "duration_hours": 36,
        "difficulty": "Advanced",
        "related_skills": ["SK-005", "SK-022", "SK-028"],
        "content": (
            "Covers Kubernetes cluster hardening, network policies, mTLS, admission controllers, container supply-chain signing, and runtime eBPF threat detection."
        )
    },
    {
        "doc_id": "CRS-CLD-202",
        "category": "LEARNING_COURSE",
        "title": "Platform Engineering: Building Internal Developer Portals with Terraform & GitOps",
        "provider": "CNCF & HashiCorp Academy",
        "certification": "Certified Platform Engineering Architect",
        "duration_hours": 26,
        "difficulty": "Intermediate",
        "related_skills": ["SK-007", "SK-023", "SK-030"],
        "content": (
            "Blueprints for self-service developer workflows, golden-path Terraform templates, ArgoCD GitOps, and automated environment provisioning."
        )
    },
    {
        "doc_id": "CRS-CLD-203",
        "category": "LEARNING_COURSE",
        "title": "FinOps Certified Practitioner & OpenTelemetry Cloud Observability",
        "provider": "FinOps Foundation & CNCF",
        "certification": "FinOps & AIOps Certified Engineer",
        "duration_hours": 22,
        "difficulty": "Intermediate",
        "related_skills": ["SK-006", "SK-015", "SK-024"],
        "content": (
            "Combines unit-economics cloud cost optimization across AWS/Azure/GCP with OpenTelemetry distributed tracing and Prometheus metrics."
        )
    },
    {
        "doc_id": "CRS-FS-301",
        "category": "LEARNING_COURSE",
        "title": "Modern Full-Stack AI Engineering: React 18, Next.js SSR, TypeScript & FastAPI",
        "provider": "Frontend Masters & FastAPI Official Track",
        "certification": "Full-Stack AI Application Developer",
        "duration_hours": 30,
        "difficulty": "Intermediate",
        "related_skills": ["SK-009", "SK-017", "SK-016"],
        "content": (
            "End-to-end architecture for type-safe React/Next.js frontends paired with async Python FastAPI + Pydantic backends."
        )
    },
    {
        "doc_id": "CRS-FS-302",
        "category": "LEARNING_COURSE",
        "title": "Rust for Enterprise Java & C# Backend Engineers",
        "provider": "Rust Foundation Enterprise Track",
        "certification": "Enterprise Rust Systems Developer",
        "duration_hours": 40,
        "difficulty": "Advanced",
        "related_skills": ["SK-008", "SK-019"],
        "content": (
            "Ownership, borrow checker, Tokio async runtime, WebAssembly, and building high-throughput memory-safe microservices."
        )
    },
    {
        "doc_id": "CRS-SEC-401",
        "category": "LEARNING_COURSE",
        "title": "Zero-Trust Network & Identity Architecture (NIST SP 800-207) + Post-Quantum Crypto",
        "provider": "SANS / Cloud Security Alliance",
        "certification": "Certified Zero-Trust & Quantum-Safe Architect",
        "duration_hours": 30,
        "difficulty": "Advanced",
        "related_skills": ["SK-010", "SK-012", "SK-027"],
        "content": (
            "Continuous identity verification, OAuth2/OIDC policy engines, micro-segmentation, and NIST post-quantum lattice cryptography migration."
        )
    },
    {
        "doc_id": "CRS-DAT-501",
        "category": "LEARNING_COURSE",
        "title": "Real-Time Data Lakehouses with Apache Iceberg, Spark & Kafka/Flink",
        "provider": "Confluent & Databricks Academy",
        "certification": "Certified Lakehouse & Streaming Architect",
        "duration_hours": 34,
        "difficulty": "Intermediate-Advanced",
        "related_skills": ["SK-013", "SK-014", "SK-029"],
        "content": (
            "Transitions traditional SQL/ETL engineers into streaming event architectures, ACID Lakehouse tables, and federated Data Mesh governance."
        )
    },
]


# ---------------------------------------------------------------------------
# 5. BALANCED SYNTHETIC EMPLOYEE GENERATOR (120 Employees, 20 per Dept)
# ---------------------------------------------------------------------------
DEPARTMENTS = [
    "AI & Data Science",
    "Cloud & Platform",
    "Full-Stack Engineering",
    "Cybersecurity",
    "Data Engineering",
    "Legacy Modernization",
]

SENIORITY_TIERS = [
    ("L1 - Associate Engineer", 1.5),
    ("L2 - Software Engineer", 3.5),
    ("L3 - Senior Engineer", 6.5),
    ("L4 - Lead / Architect", 10.0),
    ("L5 - Principal Technologist", 14.0),
]

FIRST_NAMES = [
    "Aarav", "Vivaan", "Aditya", "Ananya", "Diya", "Isha", "Rohan", "Priya", "Vikram", "Neha",
    "Arjun", "Kavya", "Siddharth", "Meera", "Karan", "Pooja", "Rahul", "Sneha", "Nikhil", "Tanvi",
    "Dev", "Riya", "Akash", "Nisha", "Varun", "Shreya", "Gaurav", "Aditi", "Harsh", "Kritika"
]
LAST_NAMES = [
    "Sharma", "Verma", "Patel", "Nair", "Iyer", "Reddy", "Gupta", "Mehta", "Joshi", "Rao",
    "Kulkarni", "Chatterjee", "Menon", "kapoor", "Malhotra", "Desai", "Bhatia", "Saxena", "banerjee", "Chopra"
]


def generate_balanced_employees() -> List[Dict[str, Any]]:
    """
    Generates 120 balanced, anonymized employee records (20 per department, 4 per seniority tier in each dept).
    Includes deliberate 'canary' sensitive demographic fields (age, gender, ethnicity) in raw storage
    so the Responsible AI Guardrail (FR-10) can strip them and prove 0.0% demographic influence.
    """
    employees: List[Dict[str, Any]] = []

    dept_core_skills = {
        "AI & Data Science": ["SK-016", "SK-025", "SK-026", "SK-020", "SK-002", "SK-001", "SK-003", "SK-004"],
        "Cloud & Platform": ["SK-021", "SK-022", "SK-023", "SK-024", "SK-030", "SK-005", "SK-006", "SK-007", "SK-015"],
        "Full-Stack Engineering": ["SK-016", "SK-017", "SK-018", "SK-019", "SK-020", "SK-009", "SK-008"],
        "Cybersecurity": ["SK-027", "SK-028", "SK-021", "SK-010", "SK-011", "SK-005", "SK-012"],
        "Data Engineering": ["SK-020", "SK-029", "SK-016", "SK-013", "SK-014", "SK-025"],
        "Legacy Modernization": [
            "SK-031", "SK-032", "SK-033", "SK-034", "SK-035", "SK-036", "SK-037", "SK-038",
            "SK-039", "SK-040", "SK-019", "SK-016", "SK-020", "SK-021", "SK-017"
        ],
    }

    dept_role_titles = {
        "AI & Data Science": "Data Scientist / ML Engineer",
        "Cloud & Platform": "Cloud & DevOps Engineer",
        "Full-Stack Engineering": "Full-Stack Software Engineer",
        "Cybersecurity": "Information Security Engineer",
        "Data Engineering": "Data & ETL Platform Engineer",
        "Legacy Modernization": "Enterprise Systems & Modernization Engineer",
    }

    emp_counter = 101
    for dept in DEPARTMENTS:
        for tier_idx, (tier_label, base_exp) in enumerate(SENIORITY_TIERS):
            # 4 employees per seniority tier per department = 20 per department = 120 total
            for slot in range(4):
                emp_id = f"EMP-{emp_counter}"
                fname = FIRST_NAMES[(emp_counter - 101) % len(FIRST_NAMES)]
                lname = LAST_NAMES[((emp_counter - 101) * 3) % len(LAST_NAMES)].capitalize()

                # Skill assignment: strong in core/legacy, scarcer in emerging (creating realistic measurable gaps!)
                pool = dept_core_skills[dept]
                emp_skills: Dict[str, int] = {}

                for sk_id in pool:
                    sk_meta = next(s for s in SKILLS_CATALOG if s["id"] == sk_id)
                    if sk_meta["lifecycle"] == "LEGACY":
                        if RNG.random() < 0.72:
                            emp_skills[sk_id] = min(5, max(2, tier_idx + RNG.randint(1, 2)))
                    elif sk_meta["lifecycle"] == "CORE":
                        if RNG.random() < 0.78:
                            emp_skills[sk_id] = min(5, max(2, tier_idx + RNG.randint(1, 2)))
                    else:  # EMERGING skills are intentionally scarcer to create realistic gaps & bus-factors
                        if RNG.random() < 0.24:
                            emp_skills[sk_id] = min(4, max(1, tier_idx + RNG.randint(0, 1)))

                # Ensure every employee has at least 4 skills
                while len(emp_skills) < 4:
                    pick = RNG.choice(pool)
                    emp_skills[pick] = min(5, max(2, tier_idx + 1))

                # Give Legacy Modernization engineers strong bridgeable foundations (e.g., Python/Java/SQL/Docker)
                if dept == "Legacy Modernization" and slot % 2 == 0:
                    emp_skills["SK-016"] = max(emp_skills.get("SK-016", 0), 3)
                    emp_skills["SK-020"] = max(emp_skills.get("SK-020", 0), 4)

                learning_velocity = round(RNG.uniform(0.68, 0.96), 2)
                attrition_risk = round(RNG.uniform(0.08, 0.42), 2)

                employees.append({
                    "id": emp_id,
                    "anonymized_code": f"HCL-ANON-{emp_counter}",
                    "display_name": f"{fname} {lname} ({emp_id})",
                    "department": dept,
                    "current_role": dept_role_titles[dept],
                    "seniority_tier": tier_label,
                    "years_experience": round(base_exp + RNG.uniform(-0.5, 1.5), 1),
                    "learning_velocity_index": learning_velocity,
                    "completed_certifications_count": RNG.randint(1, 5),
                    "attrition_probability": attrition_risk,
                    "availability_percent": RNG.choice([40, 60, 80, 100]),
                    "skills": emp_skills,
                    # Canary sensitive fields (STRIPPED by BiasGuardrail before any ML/Graph/Agent execution!)
                    "sensitive_canary_attributes": {
                        "age": RNG.randint(23, 56),
                        "gender": RNG.choice(["Female", "Male", "Non-Binary"]),
                        "ethnicity": RNG.choice(["Group_A", "Group_B", "Group_C", "Group_D"]),
                        "marital_status": RNG.choice(["Single", "Married"]),
                    }
                })
                emp_counter += 1

    return employees


# ---------------------------------------------------------------------------
# 6. 24-MONTH HISTORICAL DEMAND TIME-SERIES (1,080 Rows = 45 Skills x 24 Months)
# ---------------------------------------------------------------------------
def generate_historical_skill_timeseries(employees: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Generates 24 months (M-24 to M-01) of historical monthly skill supply & project demand
    calibrated to each skill's lifecycle (EMERGING, CORE, LEGACY) for training our
    Scikit-learn / NumPy Autoregressive Time-Series Forecasting Model (FR-04).
    """
    records: List[Dict[str, Any]] = []
    # Compute current internal supply (proficiency >= 3) per skill
    current_supply_map: Dict[str, int] = {s["id"]: 0 for s in SKILLS_CATALOG}
    for emp in employees:
        for sk_id, prof in emp["skills"].items():
            if prof >= 3:
                current_supply_map[sk_id] = current_supply_map.get(sk_id, 0) + 1

    for sk in SKILLS_CATALOG:
        sk_id = sk["id"]
        lifecycle = sk["lifecycle"]
        yoy_rate = sk["market_growth_yoy"] / 100.0
        monthly_growth = yoy_rate / 12.0
        curr_supply = max(2, current_supply_map.get(sk_id, 4))

        # Determine base demand 24 months ago
        if lifecycle == "EMERGING":
            base_demand = max(4.0, curr_supply * 0.65)
        elif lifecycle == "CORE":
            base_demand = max(8.0, curr_supply * 0.90)
        else:  # LEGACY
            base_demand = max(10.0, curr_supply * 1.35)

        for month_idx in range(1, 25):  # 1 .. 24
            # Seasonal wave + trend growth
            seasonality = 1.0 + 0.06 * math.sin((2 * math.pi * month_idx) / 6.0)
            trend_factor = max(0.25, 1.0 + monthly_growth * month_idx)
            noise = RNG.uniform(-0.6, 0.6)
            demand_val = max(1, round(base_demand * trend_factor * seasonality + noise))

            # Supply grows much slower than emerging demand
            if lifecycle == "EMERGING":
                supply_val = max(1, round(curr_supply * (0.75 + 0.25 * (month_idx / 24.0))))
            elif lifecycle == "CORE":
                supply_val = max(2, round(curr_supply * (0.92 + 0.08 * (month_idx / 24.0))))
            else:
                supply_val = max(2, round(curr_supply * (1.10 - 0.10 * (month_idx / 24.0))))

            records.append({
                "skill_id": sk_id,
                "month_index": month_idx,
                "month_label": f"M-{25 - month_idx:02d}",
                "internal_supply": int(supply_val),
                "project_demand": int(demand_val),
                "market_momentum_score": round(min(100.0, max(10.0, 50.0 + sk["market_growth_yoy"] * 0.35)), 1),
            })

    return records
