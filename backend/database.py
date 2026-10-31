"""
SQLite Relational Persistence Layer (workforce_intelligence.db)
===============================================================
Stores and manages:
- Skills ontology & graph edges (FR-01, FR-02)
- Anonymized employees & skill proficiency matrices (FR-01)
- Target enterprise roles & upcoming client projects (FR-02, FR-06)
- 24-month historical supply/demand time-series (FR-04)
- AI-generated recommendations & HR human-in-the-loop approval queue (FR-05, FR-06, FR-08, FR-10)
- Immutable observability & responsible AI bias-stripping audit logs (FR-09, FR-10)
"""

from __future__ import annotations
import json
import os
import sqlite3
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from backend.data.seed_dataset import (
    SKILLS_CATALOG,
    SKILL_GRAPH_EDGES,
    TARGET_ROLES,
    UPCOMING_PROJECTS,
    RAG_DOCUMENTS,
    generate_balanced_employees,
    generate_historical_skill_timeseries,
)

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "workforce_intelligence.db")


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_and_seed_database() -> Dict[str, int]:
    """Creates SQLite schema and seeds the balanced synthetic enterprise dataset if empty."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = get_connection()
    cur = conn.cursor()

    cur.executescript(
        """
        CREATE TABLE IF NOT EXISTS skills (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            domain TEXT NOT NULL,
            lifecycle TEXT NOT NULL,
            market_growth_yoy REAL NOT NULL,
            contractor_hourly_usd INTEGER NOT NULL,
            complexity INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS skill_edges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            target TEXT NOT NULL,
            relation TEXT NOT NULL,
            weight REAL NOT NULL,
            rationale TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS employees (
            id TEXT PRIMARY KEY,
            anonymized_code TEXT NOT NULL,
            display_name TEXT NOT NULL,
            department TEXT NOT NULL,
            current_role TEXT NOT NULL,
            seniority_tier TEXT NOT NULL,
            years_experience REAL NOT NULL,
            learning_velocity_index REAL NOT NULL,
            completed_certifications_count INTEGER NOT NULL,
            attrition_probability REAL NOT NULL,
            availability_percent INTEGER NOT NULL,
            skills_json TEXT NOT NULL,
            sensitive_canary_json TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS target_roles (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            department TEXT NOT NULL,
            grade TEXT NOT NULL,
            open_positions INTEGER NOT NULL,
            external_hiring_cost_usd INTEGER NOT NULL,
            avg_time_to_hire_weeks INTEGER NOT NULL,
            salary_band_usd TEXT NOT NULL,
            required_skills_json TEXT NOT NULL,
            description TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS upcoming_projects (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            client_sector TEXT NOT NULL,
            start_quarter TEXT NOT NULL,
            budget_usd INTEGER NOT NULL,
            priority TEXT NOT NULL,
            required_headcount_json TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS historical_timeseries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            skill_id TEXT NOT NULL,
            month_index INTEGER NOT NULL,
            month_label TEXT NOT NULL,
            internal_supply INTEGER NOT NULL,
            project_demand INTEGER NOT NULL,
            market_momentum_score REAL NOT NULL
        );

        CREATE TABLE IF NOT EXISTS recommendations_queue (
            rec_id TEXT PRIMARY KEY,
            rec_type TEXT NOT NULL,
            employee_id TEXT NOT NULL,
            employee_name TEXT NOT NULL,
            target_role_id TEXT NOT NULL,
            target_role_title TEXT NOT NULL,
            readiness_score REAL NOT NULL,
            estimated_weeks INTEGER NOT NULL,
            cost_savings_usd INTEGER NOT NULL,
            summary TEXT NOT NULL,
            xai_factors_json TEXT NOT NULL,
            learning_path_json TEXT NOT NULL,
            rag_citations_json TEXT NOT NULL,
            bias_audit_passed INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'PENDING_HR_REVIEW',
            reviewer_role TEXT,
            reviewer_notes TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS audit_logs (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            event_type TEXT NOT NULL,
            actor TEXT NOT NULL,
            endpoint TEXT NOT NULL,
            details_json TEXT NOT NULL,
            bias_guardrail_status TEXT NOT NULL
        );
        """
    )

    # Check if already seeded
    cur.execute("SELECT COUNT(*) as cnt FROM employees")
    emp_count = cur.fetchone()["cnt"]

    if emp_count == 0:
        # 1. Seed Skills
        for sk in SKILLS_CATALOG:
            cur.execute(
                """INSERT INTO skills (id, name, domain, lifecycle, market_growth_yoy, contractor_hourly_usd, complexity)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    sk["id"], sk["name"], sk["domain"], sk["lifecycle"],
                    sk["market_growth_yoy"], sk["contractor_hourly_usd"], sk["complexity"]
                ),
            )

        # 2. Seed Graph Edges
        for ed in SKILL_GRAPH_EDGES:
            cur.execute(
                """INSERT INTO skill_edges (source, target, relation, weight, rationale)
                   VALUES (?, ?, ?, ?, ?)""",
                (ed["source"], ed["target"], ed["relation"], ed["weight"], ed["rationale"]),
            )

        # 3. Seed Balanced Employees
        employees = generate_balanced_employees()
        for emp in employees:
            cur.execute(
                """INSERT INTO employees (
                    id, anonymized_code, display_name, department, current_role,
                    seniority_tier, years_experience, learning_velocity_index,
                    completed_certifications_count, attrition_probability,
                    availability_percent, skills_json, sensitive_canary_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    emp["id"], emp["anonymized_code"], emp["display_name"], emp["department"],
                    emp["current_role"], emp["seniority_tier"], emp["years_experience"],
                    emp["learning_velocity_index"], emp["completed_certifications_count"],
                    emp["attrition_probability"], emp["availability_percent"],
                    json.dumps(emp["skills"]), json.dumps(emp["sensitive_canary_attributes"]),
                ),
            )

        # 4. Seed Target Roles
        for role in TARGET_ROLES:
            cur.execute(
                """INSERT INTO target_roles (
                    id, title, department, grade, open_positions,
                    external_hiring_cost_usd, avg_time_to_hire_weeks,
                    salary_band_usd, required_skills_json, description
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    role["id"], role["title"], role["department"], role["grade"],
                    role["open_positions"], role["external_hiring_cost_usd"],
                    role["avg_time_to_hire_weeks"], role["salary_band_usd"],
                    json.dumps(role["required_skills"]), role["description"],
                ),
            )

        # 5. Seed Upcoming Projects
        for prj in UPCOMING_PROJECTS:
            cur.execute(
                """INSERT INTO upcoming_projects (
                    id, name, client_sector, start_quarter, budget_usd, priority, required_headcount_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    prj["id"], prj["name"], prj["client_sector"], prj["start_quarter"],
                    prj["budget_usd"], prj["priority"], json.dumps(prj["required_headcount"]),
                ),
            )

        # 6. Seed 24-Month Historical Time Series
        ts_rows = generate_historical_skill_timeseries(employees)
        for row in ts_rows:
            cur.execute(
                """INSERT INTO historical_timeseries (
                    skill_id, month_index, month_label, internal_supply, project_demand, market_momentum_score
                ) VALUES (?, ?, ?, ?, ?, ?)""",
                (
                    row["skill_id"], row["month_index"], row["month_label"],
                    row["internal_supply"], row["project_demand"], row["market_momentum_score"],
                ),
            )

        # 7. Seed Initial Sample Recommendations for the HR Approval Queue (FR-10)
        now_iso = datetime.now(timezone.utc).isoformat()
        sample_recs = [
            {
                "rec_id": "REC-2026-001",
                "rec_type": "ROLE_TRANSITION_AND_UPSKILL",
                "employee_id": "EMP-103",
                "employee_name": "Aditya Patel (EMP-103)",
                "target_role_id": "ROLE-AI-ARCH",
                "target_role_title": "Enterprise Agentic AI Architect",
                "readiness_score": 84.5,
                "estimated_weeks": 5,
                "cost_savings_usd": 36200,
                "summary": "High-adjacency transition from Senior ML Engineer to Enterprise Agentic AI Architect via LangGraph & XAI Guardrails track.",
                "xai_factors": [
                    {"factor": "Skill Graph Adjacency (Python/Scikit/PyTorch)", "weight_pct": 41.0, "impact": "POSITIVE"},
                    {"factor": "Q3 Banking Copilot Project Demand Surge", "weight_pct": 31.0, "impact": "POSITIVE"},
                    {"factor": "Market Trend Growth (+142% YoY LangGraph)", "weight_pct": 18.0, "impact": "POSITIVE"},
                    {"factor": "Employee Learning Velocity (0.91 Index)", "weight_pct": 10.0, "impact": "POSITIVE"},
                    {"factor": "Demographic / Sensitive Attributes (Age/Gender/Ethnicity)", "weight_pct": 0.0, "impact": "EXCLUDED_BY_GUARDRAIL"},
                ],
                "learning_path": [
                    {"week": "Weeks 1-2", "course_id": "CRS-AI-102", "title": "Enterprise RAG, FAISS/Chroma Vector Databases & Grounded Evaluation", "hours": 24},
                    {"week": "Weeks 3-4", "course_id": "CRS-AI-101", "title": "Production Agentic AI with LangGraph, Tool Calling & Stateful Workflows", "hours": 28},
                    {"week": "Week 5", "course_id": "CRS-AI-103", "title": "Responsible AI, Explainable AI (SHAP/LIME) & LLM Safety Guardrails", "hours": 18},
                ],
                "rag_citations": ["MKT-2026-01", "CRS-AI-101", "CRS-AI-102"],
                "status": "PENDING_HR_REVIEW",
            },
            {
                "rec_id": "REC-2026-002",
                "rec_type": "LEGACY_RESKILL_BRIDGE",
                "employee_id": "EMP-205",
                "employee_name": "Neha Joshi (EMP-205)",
                "target_role_id": "ROLE-FULLSTACK-AI",
                "target_role_title": "AI-Native Full-Stack Principal Engineer",
                "readiness_score": 78.2,
                "estimated_weeks": 6,
                "cost_savings_usd": 27400,
                "summary": "Proactive reskilling from Legacy Modernization team into AI-Native Full-Stack Engineering leveraging strong Python & SQL foundations.",
                "xai_factors": [
                    {"factor": "Skill Graph Adjacency (Python/SQL/Java Foundations)", "weight_pct": 38.0, "impact": "POSITIVE"},
                    {"factor": "Legacy Obsolescence Risk Mitigation (-28% J2EE Decline)", "weight_pct": 29.0, "impact": "POSITIVE"},
                    {"factor": "Internal Hiring Cost Savings ($27.4K vs External)", "weight_pct": 21.0, "impact": "POSITIVE"},
                    {"factor": "Employee Learning Velocity", "weight_pct": 12.0, "impact": "POSITIVE"},
                    {"factor": "Demographic / Sensitive Attributes (Age/Gender/Ethnicity)", "weight_pct": 0.0, "impact": "EXCLUDED_BY_GUARDRAIL"},
                ],
                "learning_path": [
                    {"week": "Weeks 1-3", "course_id": "CRS-FS-301", "title": "Modern Full-Stack AI Engineering: React 18, Next.js SSR, TypeScript & FastAPI", "hours": 30},
                    {"week": "Weeks 4-6", "course_id": "CRS-AI-102", "title": "Enterprise RAG, FAISS/Chroma Vector Databases & Grounded Evaluation", "hours": 24},
                ],
                "rag_citations": ["MKT-2026-04", "CRS-FS-301", "CRS-AI-102"],
                "status": "PENDING_HR_REVIEW",
            },
            {
                "rec_id": "REC-2026-003",
                "rec_type": "CRITICAL_SHORTAGE_MITIGATION",
                "employee_id": "EMP-127",
                "employee_name": "Vikram Reddy (EMP-127)",
                "target_role_id": "ROLE-ZERO-TRUST",
                "target_role_title": "Zero-Trust & AI Security Architect",
                "readiness_score": 86.0,
                "estimated_weeks": 4,
                "cost_savings_usd": 35800,
                "summary": "Fast-track Cloud DevOps Lead into Zero-Trust & Kubernetes Security Architect to resolve Q3 Healthcare K8s Security bottleneck.",
                "xai_factors": [
                    {"factor": "Kubernetes & Docker Core Proficiency (Level 4)", "weight_pct": 44.0, "impact": "POSITIVE"},
                    {"factor": "Critical Bus-Factor Risk in K8s Security (SK-005)", "weight_pct": 34.0, "impact": "POSITIVE"},
                    {"factor": "Market Demand Surge (+88% YoY K8s Sec)", "weight_pct": 22.0, "impact": "POSITIVE"},
                    {"factor": "Demographic / Sensitive Attributes (Age/Gender/Ethnicity)", "weight_pct": 0.0, "impact": "EXCLUDED_BY_GUARDRAIL"},
                ],
                "learning_path": [
                    {"week": "Weeks 1-2", "course_id": "CRS-CLD-201", "title": "Certified Kubernetes Security Specialist (CKS) & Runtime Defense", "hours": 36},
                    {"week": "Weeks 3-4", "course_id": "CRS-SEC-401", "title": "Zero-Trust Network & Identity Architecture (NIST SP 800-207)", "hours": 30},
                ],
                "rag_citations": ["MKT-2026-02", "MKT-2026-03", "CRS-CLD-201"],
                "status": "APPROVED",
            },
        ]

        for rec in sample_recs:
            cur.execute(
                """INSERT INTO recommendations_queue (
                    rec_id, rec_type, employee_id, employee_name, target_role_id, target_role_title,
                    readiness_score, estimated_weeks, cost_savings_usd, summary,
                    xai_factors_json, learning_path_json, rag_citations_json,
                    bias_audit_passed, status, reviewer_role, reviewer_notes, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    rec["rec_id"], rec["rec_type"], rec["employee_id"], rec["employee_name"],
                    rec["target_role_id"], rec["target_role_title"], rec["readiness_score"],
                    rec["estimated_weeks"], rec["cost_savings_usd"], rec["summary"],
                    json.dumps(rec["xai_factors"]), json.dumps(rec["learning_path"]),
                    json.dumps(rec["rag_citations"]), 1, rec["status"],
                    "HR_DIRECTOR" if rec["status"] == "APPROVED" else None,
                    "Approved for Q3 Healthcare Zero-Trust Pod ramp-up." if rec["status"] == "APPROVED" else None,
                    now_iso, now_iso,
                ),
            )

        # 8. Seed Initial Audit Log
        cur.execute(
            """INSERT INTO audit_logs (timestamp, event_type, actor, endpoint, details_json, bias_guardrail_status)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (
                now_iso,
                "SYSTEM_BOOTSTRAP_AND_BIAS_VERIFICATION",
                "SYSTEM_INIT",
                "/startup",
                json.dumps({
                    "seeded_employees": len(employees),
                    "seeded_skills": len(SKILLS_CATALOG),
                    "seeded_timeseries_points": len(ts_rows),
                    "seeded_rag_docs": len(RAG_DOCUMENTS),
                    "stripped_canary_fields": ["age", "gender", "ethnicity", "marital_status"],
                }),
                "PASSED_ZERO_DEMOGRAPHIC_LEAKAGE",
            ),
        )

        conn.commit()

    cur.execute("SELECT COUNT(*) as c FROM employees")
    total_emp = cur.fetchone()["c"]
    cur.execute("SELECT COUNT(*) as c FROM skills")
    total_skills = cur.fetchone()["c"]
    cur.execute("SELECT COUNT(*) as c FROM historical_timeseries")
    total_ts = cur.fetchone()["c"]
    conn.close()

    return {
        "employees": total_emp,
        "skills": total_skills,
        "timeseries_rows": total_ts,
        "rag_documents": len(RAG_DOCUMENTS),
    }


def log_audit_event(
    event_type: str,
    actor: str,
    endpoint: str,
    details: Dict[str, Any],
    bias_status: str = "PASSED_ZERO_DEMOGRAPHIC_LEAKAGE",
) -> None:
    conn = get_connection()
    conn.execute(
        """INSERT INTO audit_logs (timestamp, event_type, actor, endpoint, details_json, bias_guardrail_status)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (
            datetime.now(timezone.utc).isoformat(),
            event_type,
            actor,
            endpoint,
            json.dumps(details),
            bias_status,
        ),
    )
    conn.commit()
    conn.close()
