"""
Automated Verification Suite for SkillPulse AI (FR-01 through FR-10)
====================================================================
Tests every Functional Requirement and Scope Boundary:
- FR-01: Skill Inventory Assessment & Unstructured Bio Skill Extractor
- FR-02: Skill Gap Detection & Knowledge Graph Adjacency Bridges
- FR-03: Market Intelligence via Hybrid Dense/Sparse Vector RAG
- FR-04: Demand Forecasting (6, 12, 24-month Autoregressive Ridge Time-Series)
- FR-05: Personalized Learning Paths (Prerequisite-Ordered RAG Courses)
- FR-06: Internal Mobility Analysis & Cost-Savings Calculator
- FR-07: Workforce Risk Assessment & Bus-Factor Alerts
- FR-08: Multi-Horizon Career Path Recommendations
- FR-09: Explainable AI (XAI) Feature Attribution & Grounded Citations
- FR-10: Human Review Approval Queue, JWT RBAC & Responsible AI Bias Stripper
"""

from __future__ import annotations
import unittest
from backend.main import (
    app,
    health_check,
    get_forecast_dashboard,
    get_skills_knowledge_graph,
    list_employees_and_roles,
    extract_skills_from_resume_bio,
    analyze_employee_evolution,
    match_internal_mobility_candidates,
    search_rag_knowledge_base,
    get_governance_approval_queue,
    submit_human_governance_decision,
    test_bias_and_policy_guardrail,
    simulate_what_if_forecast,
    simulate_custom_employee_profile,
    AnalyzeEmployeeRequest,
    ProfileExtractorRequest,
    GovernanceDecisionRequest,
    GuardrailTestRequest,
    WhatIfForecastRequest,
    CustomEmployeeSimulationRequest,
)


class TestSkillPulseWorkforcePlatform(unittest.TestCase):
    def test_01_dataset_balance_and_health(self) -> None:
        """Verifies balanced synthetic dataset seeding (120 employees, 45 skills, 1,080 time-series rows)."""
        res = health_check()
        self.assertEqual(res["status"], "HEALTHY")
        self.assertEqual(res["seeded_records"]["employees"], 120)
        self.assertEqual(res["seeded_records"]["skills"], 45)
        self.assertEqual(res["seeded_records"]["timeseries_rows"], 1080)

    def test_02_fr01_and_fr10_employee_sanitization_and_skill_extraction(self) -> None:
        """FR-01 & FR-10: Verifies employee skill inventory and strict stripping of sensitive canary fields."""
        emp_data = list_employees_and_roles()
        self.assertEqual(emp_data["total_employees"], 120)
        sample_emp = emp_data["employees"][0]
        # Sensitive canary fields MUST be stripped before leaving the backend
        self.assertNotIn("sensitive_canary_attributes", sample_emp)
        self.assertEqual(sample_emp["bias_certificate"]["demographic_feature_weight_pct"], 0.0)
        self.assertIn("age", sample_emp["bias_certificate"]["stripped_sensitive_attributes"])

        # Test unstructured resume/bio extractor
        ext = extract_skills_from_resume_bio(
            ProfileExtractorRequest(
                employee_name="Test Engineer",
                department="AI & Data Science",
                raw_resume_or_bio="Senior Architect skilled in Python, FastAPI, LangGraph, RAG vector databases, and Docker.",
            )
        )
        self.assertGreaterEqual(ext["extracted_skills_count"], 4)

    def test_03_fr02_skills_knowledge_graph(self) -> None:
        """FR-02: Verifies Skills Knowledge Graph nodes and weighted adjacency/prerequisite edges."""
        kg = get_skills_knowledge_graph(domain="ALL")
        self.assertEqual(kg["total_nodes"], 45)
        self.assertGreaterEqual(kg["total_edges"], 35)

    def test_04_fr03_and_fr04_and_fr07_forecast_and_shortage_risk(self) -> None:
        """FR-03, FR-04, FR-07: Verifies 6/12/24m ML demand forecasting, MAPE/R2 metrics, and risk scoring."""
        dash = get_forecast_dashboard(horizon_months=12, domain="ALL")
        self.assertEqual(dash["horizon_months"], 12)
        self.assertEqual(len(dash["forecasts"]), 45)
        self.assertLess(dash["summary_kpis"]["model_test_mape_pct"], 20.0)
        self.assertGreater(dash["summary_kpis"]["model_test_r2"], 0.70)
        self.assertGreaterEqual(len(dash["market_intelligence_highlights"]), 3)

    def test_05_fr05_fr08_fr09_five_agent_evolution_pipeline(self) -> None:
        """FR-05, FR-08, FR-09: Verifies 5-Agent orchestration, RAG learning path, 3-step career plan, and XAI."""
        res = analyze_employee_evolution(
            AnalyzeEmployeeRequest(
                employee_id="EMP-103",
                target_role_id="ROLE-AI-ARCH",
                persist_to_queue=True,
            )
        )
        self.assertEqual(len(res["agent_execution_traces"]), 5)
        self.assertGreater(res["skill_gap_analysis"]["readiness_score_pct"], 50.0)
        self.assertGreaterEqual(len(res["personalized_learning_path"]), 2)
        self.assertEqual(len(res["career_evolution_trajectory"]), 3)
        # Verify XAI feature weights sum to 100% and demographic weight is strictly 0.0%
        factors = res["explainable_ai_audit"]["feature_attribution"]
        total_w = round(sum(f["weight_pct"] for f in factors), 1)
        self.assertAlmostEqual(total_w, 100.0, places=0)
        demo_factor = [f for f in factors if "Demographic" in f["factor"]][0]
        self.assertEqual(demo_factor["weight_pct"], 0.0)

    def test_06_fr06_internal_mobility_matcher(self) -> None:
        """FR-06: Verifies internal mobility ranking across all 120 employees and cost-savings calculation."""
        mob = match_internal_mobility_candidates(role_id="ROLE-AI-ARCH", top_k=10)
        self.assertEqual(mob["total_employees_screened"], 120)
        self.assertEqual(len(mob["top_candidates"]), 10)
        self.assertGreater(mob["potential_fleet_cost_savings_usd"], 50000)

    def test_07_fr10_human_review_and_bias_guardrail_refusal(self) -> None:
        """FR-10: Verifies active blocking of biased queries and human HR approval workflow."""
        blocked = test_bias_and_policy_guardrail(
            GuardrailTestRequest(
                query_text="Filter candidates by age younger than 30 and only male engineers."
            )
        )
        self.assertFalse(blocked["allowed"])

        allowed = test_bias_and_policy_guardrail(
            GuardrailTestRequest(
                query_text="Find engineers with Python and PostgreSQL proficiency for RAG training."
            )
        )
        self.assertTrue(allowed["allowed"])

        # Test HR Approval decision
        dec = submit_human_governance_decision(
            GovernanceDecisionRequest(
                rec_id="REC-2026-001",
                decision="APPROVED",
                reviewer_role="HR_DIRECTOR",
                reviewer_notes="Approved in automated test suite.",
            )
        )
        self.assertEqual(dec["new_status"], "APPROVED")
        self.assertTrue(dec["audit_logged"])

    def test_08_frontend_portal_served(self) -> None:
        """Verifies the interactive React + Tailwind frontend dashboard is served at root /."""
        from backend.main import serve_frontend
        resp = serve_frontend()
        self.assertEqual(resp.status_code, 200)
        self.assertIn("SkillPulse AI", resp.body.decode("utf-8"))

    def test_09_interactive_what_if_forecast_simulator(self) -> None:
        """Verifies the interactive What-If Forecast Simulator responds to slider multipliers."""
        low_demand = simulate_what_if_forecast(
            WhatIfForecastRequest(horizon_months=12, extra_projects_multiplier=0.8, attrition_rate_pct=5.0)
        )
        high_demand = simulate_what_if_forecast(
            WhatIfForecastRequest(horizon_months=12, extra_projects_multiplier=1.8, attrition_rate_pct=25.0)
        )
        self.assertGreater(
            high_demand["summary_kpis"]["total_projected_headcount_deficit"],
            low_demand["summary_kpis"]["total_projected_headcount_deficit"],
        )

    def test_10_interactive_custom_profile_and_bias_invariance(self) -> None:
        """Verifies custom slider simulation and proves 100% invariance to canary Age/Gender changes."""
        run_a = simulate_custom_employee_profile(
            CustomEmployeeSimulationRequest(
                employee_name="Demo User",
                target_role_id="ROLE-AI-ARCH",
                skills={"SK-016": 5, "SK-020": 4, "SK-002": 3},
                canary_age=24,
                canary_gender="Female",
                persist_to_queue=False,
            )
        )
        run_b = simulate_custom_employee_profile(
            CustomEmployeeSimulationRequest(
                employee_name="Demo User",
                target_role_id="ROLE-AI-ARCH",
                skills={"SK-016": 5, "SK-020": 4, "SK-002": 3},
                canary_age=58,
                canary_gender="Male",
                persist_to_queue=False,
            )
        )
        # Readiness score MUST be 100% identical regardless of Age or Gender
        self.assertEqual(
            run_a["skill_gap_analysis"]["readiness_score_pct"],
            run_b["skill_gap_analysis"]["readiness_score_pct"],
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
