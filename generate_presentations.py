"""
Generates a Clean, Simple, Concise 6-Page Presentation for Squad Arsenal in 2 Formats:
1. SkillPulse_AI_Arsenal_Presentation.pptx (Native Microsoft PowerPoint 16:9 Widescreen .pptx)
2. SkillPulse_AI_Arsenal_Presentation.pdf  (High-Resolution 16:9 Widescreen PDF Slide Deck via ReportLab)
"""

from __future__ import annotations
import os
import zipfile
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import inch
from reportlab.pdfgen import canvas

SLIDE_W = 13.333 * inch
SLIDE_H = 7.5 * inch


def _draw_header(c: canvas.Canvas, slide_num: int, title: str, subtitle: str) -> None:
    c.setFillColor(colors.HexColor("#F8FAFC"))
    c.rect(0, 0, SLIDE_W, SLIDE_H, fill=1, stroke=0)

    c.setFillColor(colors.HexColor("#0F172A"))
    c.rect(0, SLIDE_H - 1.05 * inch, SLIDE_W, 1.05 * inch, fill=1, stroke=0)

    c.setFillColor(colors.HexColor("#4F46E5"))
    c.rect(0, SLIDE_H - 1.10 * inch, SLIDE_W, 0.05 * inch, fill=1, stroke=0)

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 21)
    c.drawString(0.55 * inch, SLIDE_H - 0.52 * inch, title)

    c.setFillColor(colors.HexColor("#A5B4FC"))
    c.setFont("Helvetica", 11.5)
    c.drawString(0.55 * inch, SLIDE_H - 0.82 * inch, subtitle)

    c.setFillColor(colors.HexColor("#1E293B"))
    c.roundRect(SLIDE_W - 2.9 * inch, SLIDE_H - 0.82 * inch, 2.4 * inch, 0.52 * inch, 6, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#38BDF8"))
    c.setFont("Helvetica-Bold", 10.5)
    c.drawRightString(SLIDE_W - 0.65 * inch, SLIDE_H - 0.50 * inch, f"Squad Arsenal | Slide {slide_num}/6")
    c.setFillColor(colors.HexColor("#94A3B8"))
    c.setFont("Helvetica", 9)
    c.drawRightString(SLIDE_W - 0.65 * inch, SLIDE_H - 0.68 * inch, "Use Case 4: Skill Gap Predictor")

    c.setFillColor(colors.HexColor("#E2E8F0"))
    c.rect(0, 0, SLIDE_W, 0.36 * inch, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#475569"))
    c.setFont("Helvetica-Bold", 9)
    c.drawString(
        0.55 * inch,
        0.13 * inch,
        "HCLTech | Squad Arsenal: Mohit Tomar (HCLTFP2460368) • Ronit Singh Rawat (HCLTFP2465203) • Ankit Mohapatra (HCLTFP2467657)",
    )
    c.drawRightString(SLIDE_W - 0.55 * inch, 0.13 * inch, f"Page {slide_num} of 6")


def _draw_simple_card(
    c: canvas.Canvas,
    x: float,
    y: float,
    w: float,
    h: float,
    header_bg: str,
    header_title: str,
    lines: list[str],
    font_size: float = 11.0,
    line_gap: float = 0.27 * inch,
) -> None:
    c.setFillColor(colors.white)
    c.setStrokeColor(colors.HexColor("#CBD5E1"))
    c.setLineWidth(1.2)
    c.roundRect(x, y, w, h, 10, fill=1, stroke=1)

    c.setFillColor(colors.HexColor(header_bg))
    c.roundRect(x, y + h - 0.42 * inch, w, 0.42 * inch, 10, fill=1, stroke=0)
    c.rect(x, y + h - 0.42 * inch, w, 0.16 * inch, fill=1, stroke=0)

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x + 0.20 * inch, y + h - 0.27 * inch, header_title)

    cur_y = y + h - 0.72 * inch
    for ln in lines:
        if ln.startswith("##"):
            c.setFillColor(colors.HexColor("#0F172A"))
            c.setFont("Helvetica-Bold", font_size + 0.5)
            c.drawString(x + 0.20 * inch, cur_y, ln.replace("##", "").strip())
        else:
            c.setFillColor(colors.HexColor("#334155"))
            c.setFont("Helvetica", font_size)
            c.drawString(x + 0.20 * inch, cur_y, ln)
        cur_y -= line_gap


def build_pdf_presentation(pdf_path: str) -> None:
    c = canvas.Canvas(pdf_path, pagesize=(SLIDE_W, SLIDE_H))

    # =======================================================================
    # SLIDE 1: COVER PAGE (SQUAD ARSENAL & USE CASE 4)
    # =======================================================================
    c.setFillColor(colors.HexColor("#0F172A"))
    c.rect(0, 0, SLIDE_W, SLIDE_H, fill=1, stroke=0)

    c.setFillColor(colors.HexColor("#4F46E5"))
    c.rect(0, SLIDE_H - 0.22 * inch, SLIDE_W, 0.22 * inch, fill=1, stroke=0)

    c.setFillColor(colors.HexColor("#1E293B"))
    c.setStrokeColor(colors.HexColor("#6366F1"))
    c.roundRect(0.8 * inch, SLIDE_H - 1.2 * inch, 5.6 * inch, 0.45 * inch, 10, fill=1, stroke=1)
    c.setFillColor(colors.HexColor("#A5B4FC"))
    c.setFont("Helvetica-Bold", 12)
    c.drawString(1.0 * inch, SLIDE_H - 1.03 * inch, "HCLTech  |  AI Future Ready FullStack Web Engineer")

    c.setFillColor(colors.HexColor("#38BDF8"))
    c.setFont("Helvetica-Bold", 15)
    c.drawString(0.8 * inch, SLIDE_H - 1.85 * inch, "4. SKILL GAP AND WORKFORCE EVOLUTION PREDICTOR")

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 34)
    c.drawString(0.8 * inch, SLIDE_H - 2.45 * inch, "SkillPulse AI — Workforce")
    c.drawString(0.8 * inch, SLIDE_H - 2.98 * inch, "Intelligence Platform")

    c.setFillColor(colors.HexColor("#94A3B8"))
    c.setFont("Helvetica", 13)
    c.drawString(
        0.8 * inch,
        SLIDE_H - 3.42 * inch,
        "Skills Knowledge Graph  •  Vector RAG  •  Scikit-Learn Forecasting  •  5 AI Agents  •  Explainable AI",
    )

    # Left Box: Squad Arsenal (From Photo)
    c.setFillColor(colors.HexColor("#1E293B"))
    c.setStrokeColor(colors.HexColor("#4F46E5"))
    c.setLineWidth(2)
    c.roundRect(0.8 * inch, 0.85 * inch, 5.8 * inch, 3.0 * inch, 12, fill=1, stroke=1)

    c.setFillColor(colors.HexColor("#4F46E5"))
    c.roundRect(0.8 * inch, 3.30 * inch, 5.8 * inch, 0.55 * inch, 12, fill=1, stroke=0)
    c.rect(0.8 * inch, 3.30 * inch, 5.8 * inch, 0.25 * inch, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 17)
    c.drawString(1.1 * inch, 3.50 * inch, "Squad Name – Arsenal")

    c.setFillColor(colors.HexColor("#38BDF8"))
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1.1 * inch, 2.88 * inch, "Role – AI_Full Stack Web Engineer")

    c.setFillColor(colors.HexColor("#E2E8F0"))
    c.setFont("Helvetica-Bold", 13.5)
    c.drawString(1.1 * inch, 2.46 * inch, "Team:")

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1.25 * inch, 2.05 * inch, "•  Mohit Tomar – HCLTFP2460368")
    c.drawString(1.25 * inch, 1.65 * inch, "•  Ronit Singh Rawat – HCLTFP2465203")
    c.drawString(1.25 * inch, 1.25 * inch, "•  Ankit Mohapatra – HCLTFP2467657")

    # Right Box: Simple Use Case Summary
    c.setFillColor(colors.HexColor("#1E293B"))
    c.setStrokeColor(colors.HexColor("#10B981"))
    c.roundRect(7.0 * inch, 0.85 * inch, 5.5 * inch, 3.0 * inch, 12, fill=1, stroke=1)

    c.setFillColor(colors.HexColor("#059669"))
    c.roundRect(7.0 * inch, 3.30 * inch, 5.5 * inch, 0.55 * inch, 12, fill=1, stroke=0)
    c.rect(7.0 * inch, 3.30 * inch, 5.5 * inch, 0.25 * inch, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(7.25 * inch, 3.50 * inch, "Use Case Overview")

    c.setFillColor(colors.HexColor("#F1F5F9"))
    c.setFont("Helvetica", 12.5)
    overview = [
        "• Use Case: 4. Skill Gap & Workforce Evolution",
        "• Industry: HR / Workforce Transformation",
        "• Goal: Predict skill shortages 6–24 months early",
        "• Output: Personalized courses & internal mobility",
        "• Safety: 0% Demographic Bias + HR Approval",
    ]
    oy = 2.85 * inch
    for line in overview:
        c.drawString(7.25 * inch, oy, line)
        oy -= 0.38 * inch

    c.showPage()

    # =======================================================================
    # SLIDE 2: REAL-WORLD PROBLEM, INPUTS & SOLUTION
    # =======================================================================
    _draw_header(
        c,
        2,
        "1. Real-World Problem, Inputs & Our Solution",
        "Simple view of what problem we solve and what data enters the system",
    )

    _draw_simple_card(
        c,
        0.55 * inch,
        3.50 * inch,
        5.9 * inch,
        2.6 * inch,
        "#DC2626",
        "The Real-World Problem",
        [
            "## 1. Late Skill Discovery:",
            "   Companies find skill gaps AFTER winning projects.",
            "## 2. Expensive External Hiring:",
            "   Hiring outside contractors costs 3x more money.",
            "## 3. Hidden Internal Talent:",
            "   Keyword search misses people with 80% close skills.",
        ],
    )

    _draw_simple_card(
        c,
        6.85 * inch,
        3.50 * inch,
        5.9 * inch,
        2.6 * inch,
        "#4F46E5",
        "The 5 Inputs to Our Project",
        [
            "## 1. Employee Skills:  1–5 sliders or Resume text.",
            "## 2. Learning Records:  Past certifications & speed.",
            "## 3. Project Requirements:  Target role or project spec.",
            "## 4. Market Trends:  Gartner/WEF tech growth reports.",
            "## 5. Tech Evolution:  Emerging, Core & Legacy skills.",
        ],
    )

    _draw_simple_card(
        c,
        0.55 * inch,
        0.60 * inch,
        12.2 * inch,
        2.6 * inch,
        "#059669",
        "How SkillPulse AI Solves It (Business Impact)",
        [
            "## • Predicts Shortages Early:  Forecasts skill demand 6, 12, and 24 months ahead (93.1% accuracy).",
            "## • Finds Adjacent Talent:  Uses a Skills Knowledge Graph to find engineers who can upskill in 4 weeks.",
            "## • Saves 87% Hiring Cost:  Reskills internal staff instead of expensive external recruiting.",
            "## • 100% Fair & Human-Controlled:  Strips Age/Gender bias (0% weight) and requires HR approval.",
        ],
    )

    c.showPage()

    # =======================================================================
    # SLIDE 3: FULL SYSTEM ARCHITECTURE & ROLE OF PYDANTIC
    # =======================================================================
    _draw_header(
        c,
        3,
        "2. High-Level System Architecture & Tech Stack",
        "5 simple layers from React UI to FastAPI + Pydantic, 5 AI Agents, and Databases",
    )

    tiers = [
        (
            5.25 * inch,
            "#1E40AF",
            "LAYER 1: FRONTEND UI  (React 18 + TypeScript + Tailwind CSS + Zustand)",
            "Interactive Skill Sliders  •  What-If Forecast Sliders  •  Visual Knowledge Graph  •  HR Approval Screen",
        ),
        (
            4.20 * inch,
            "#4338CA",
            "LAYER 2: API & VALIDATION GATEWAY  (Python FastAPI + Pydantic + JWT Security)",
            "Pydantic validates all inputs/outputs (1–5 ratings, JSON schemas)  •  Bias Filter removes Age/Gender  •  JWT Auth",
        ),
        (
            3.15 * inch,
            "#6D28D9",
            "LAYER 3: 5-AGENT COORDINATOR  (LangGraph Stateful Workflow)",
            "Agent 1: Profiler  ➔  Agent 2: Forecaster  ➔  Agent 3: Learning Coach  ➔  Agent 4: Mobility  ➔  Agent 5: XAI Auditor",
        ),
        (
            2.10 * inch,
            "#0F766E",
            "LAYER 4: AI & ML BRAIN  (Skills Knowledge Graph + Scikit-Learn + Hybrid LLM)",
            "Knowledge Graph (45 Skills, 37 Bridges)  •  Scikit-Learn Ridge Forecaster  •  Local + Cloud Hybrid LLM",
        ),
        (
            1.05 * inch,
            "#334155",
            "LAYER 5: STORAGE & VECTOR RAG  (SQLite Database + FAISS-Style Vector Store)",
            "SQLite (120 Employees, 1,080 Time-Series Rows, Audit Logs)  •  Vector Store (40+ Market & Course Docs)",
        ),
    ]

    for y_pos, color_hex, t_title, t_desc in tiers:
        c.setFillColor(colors.white)
        c.setStrokeColor(colors.HexColor(color_hex))
        c.setLineWidth(1.6)
        c.roundRect(0.55 * inch, y_pos, 12.2 * inch, 0.85 * inch, 8, fill=1, stroke=1)

        c.setFillColor(colors.HexColor(color_hex))
        c.roundRect(0.55 * inch, y_pos + 0.47 * inch, 12.2 * inch, 0.38 * inch, 8, fill=1, stroke=0)
        c.rect(0.55 * inch, y_pos + 0.47 * inch, 12.2 * inch, 0.15 * inch, fill=1, stroke=0)

        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(0.75 * inch, y_pos + 0.60 * inch, t_title)

        c.setFillColor(colors.HexColor("#1E293B"))
        c.setFont("Helvetica-Bold", 10.5)
        c.drawString(0.75 * inch, y_pos + 0.18 * inch, t_desc)

    c.showPage()

    # =======================================================================
    # SLIDE 4: WHY THIS TECH STACK & WHAT WE DO WITH PYDANTIC
    # =======================================================================
    _draw_header(
        c,
        4,
        "3. Why This Tech Stack (And What Pydantic Does)",
        "Why we chose each tool from the brief over other alternatives",
    )

    _draw_simple_card(
        c,
        0.55 * inch,
        3.45 * inch,
        5.9 * inch,
        2.65 * inch,
        "#1E40AF",
        "Why React + FastAPI + Pydantic?",
        [
            "## • React + TypeScript + Tailwind + Zustand:",
            "   3x faster UI & SVG graph rendering than Material UI/Redux.",
            "## • Python FastAPI (Why Not Java or Node.js?):",
            "   Python directly runs Scikit-Learn, Vector RAG & AI Agents.",
            "## • What We Do With Pydantic:",
            "   Strictly validates API data (e.g. skill levels 1–5, horizon",
            "   6–24m) and auto-creates OpenAPI (/docs) schemas.",
        ],
        font_size=10.5,
        line_gap=0.25 * inch,
    )

    _draw_simple_card(
        c,
        6.85 * inch,
        3.45 * inch,
        5.9 * inch,
        2.65 * inch,
        "#6D28D9",
        "Why Scikit-Learn + Local Vector RAG + SQLite?",
        [
            "## • Scikit-Learn + Hybrid LLM (Why Not LLM Alone?):",
            "   LLMs are bad at math. Scikit-Learn gives accurate forecasts",
            "   (6.8% error) and works 100% offline without API failures.",
            "## • Local Vector RAG (Why Not Cloud Search?):",
            "   Searches courses & market reports in <3ms with 0 cloud keys.",
            "## • SQLite (Why Not Heavy DB Servers?):",
            "   Zero setup; runs pre-seeded with 120 profiles in 1 command.",
        ],
        font_size=10.5,
        line_gap=0.25 * inch,
    )

    _draw_simple_card(
        c,
        0.55 * inch,
        0.60 * inch,
        12.2 * inch,
        2.55 * inch,
        "#0F766E",
        "How Pydantic Protects Our AI Pipeline (4 Key Jobs in Code)",
        [
            "## 1. Input Validation:  Checks that skill sliders (0–5), horizons (6–24m), and role IDs are valid before AI runs.",
            "## 2. HR Governance Rules:  Enforces pattern='^(APPROVED|REJECTED)$' so invalid HR statuses are blocked.",
            "## 3. Clean JSON Serialization:  Guarantees XAI factor weights and 5-Agent traces match the frontend TypeScript types.",
            "## 4. Auto Swagger UI (/docs):  Generates interactive API test forms automatically from our Pydantic BaseModel classes.",
        ],
        font_size=10.5,
        line_gap=0.27 * inch,
    )

    c.showPage()

    # =======================================================================
    # SLIDE 5: END-TO-END WORKING FLOW (SIMPLE STEP-BY-STEP)
    # =======================================================================
    _draw_header(
        c,
        5,
        "4. End-to-End Working Flow (API & Data Flow)",
        "When each API is called and where data is fetched from",
    )

    simple_flows = [
        (
            5.15 * inch,
            "#0F172A",
            "STEP 0: Server Startup",
            "Loads 120 employees & 24m history from SQLite  ➔  Builds Skills Graph in RAM  ➔  Trains Scikit-Learn Forecaster.",
        ),
        (
            4.10 * inch,
            "#4F46E5",
            "FLOW 1: User Runs 5-Agent Simulator (POST /api/v1/agents/simulate-custom-profile)",
            "Pydantic validates input  ➔  Bias Filter strips Age/Gender  ➔  5 Agents query Graph + Vector RAG  ➔  Saves plan to SQLite.",
        ),
        (
            3.05 * inch,
            "#0284C7",
            "FLOW 2: User Moves What-If Forecast Sliders (POST /api/v1/forecast/simulate)",
            "Fetches 24m history from SQLite  ➔  Scikit-Learn predicts +6/12/24m demand & shortage risk  ➔  Updates UI charts.",
        ),
        (
            2.00 * inch,
            "#7C3AED",
            "FLOW 3 & 4: Skills Graph & Internal Mobility (GET /graph/skills-network & /mobility/match)",
            "Fetches 45 skill nodes from Graph + screens 120 SQLite employees  ➔  Ranks best internal candidates & cost savings.",
        ),
        (
            0.95 * inch,
            "#059669",
            "FLOW 5: Bias Test & Human HR Approval (POST /guardrail/test & /governance/decision)",
            "Blocks biased Age/Gender queries  ➔  Verifies HR JWT token  ➔  Updates SQLite status to APPROVED + logs Audit Trail.",
        ),
    ]

    for y_pos, color_hex, f_title, f_line in simple_flows:
        c.setFillColor(colors.white)
        c.setStrokeColor(colors.HexColor("#CBD5E1"))
        c.roundRect(0.55 * inch, y_pos, 12.2 * inch, 0.85 * inch, 8, fill=1, stroke=1)

        c.setFillColor(colors.HexColor(color_hex))
        c.roundRect(0.55 * inch, y_pos + 0.47 * inch, 12.2 * inch, 0.38 * inch, 8, fill=1, stroke=0)
        c.rect(0.55 * inch, y_pos + 0.47 * inch, 12.2 * inch, 0.15 * inch, fill=1, stroke=0)

        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(0.75 * inch, y_pos + 0.60 * inch, f_title)

        c.setFillColor(colors.HexColor("#1E293B"))
        c.setFont("Helvetica-Bold", 10.3)
        c.drawString(0.75 * inch, y_pos + 0.18 * inch, f_line)

    c.showPage()

    # =======================================================================
    # SLIDE 6: THE 5 AI AGENTS, BALANCED DATASET & RESULTS
    # =======================================================================
    _draw_header(
        c,
        6,
        "5. The 5 AI Agents, Balanced Dataset & Results",
        "How the 5 agents divide the work and our verified accuracy metrics",
    )

    _draw_simple_card(
        c,
        0.55 * inch,
        3.35 * inch,
        5.9 * inch,
        2.75 * inch,
        "#4F46E5",
        "What the 5 AI Agents Do",
        [
            "## • Agent 1 (Profiler):  Finds skill gaps & graph bridges.",
            "## • Agent 2 (Forecaster):  Checks RAG trends & ML demand.",
            "## • Agent 3 (Learning Coach):  Picks courses & career path.",
            "## • Agent 4 (Mobility):  Matches internal staff & $ saved.",
            "## • Agent 5 (XAI Auditor):  Shows Why-% & proves 0% bias.",
        ],
        font_size=11.0,
        line_gap=0.33 * inch,
    )

    _draw_simple_card(
        c,
        6.85 * inch,
        3.35 * inch,
        5.9 * inch,
        2.75 * inch,
        "#0F766E",
        "Balanced Dataset & Evaluation Metrics",
        [
            "## • Balanced Synthetic Dataset:",
            "   120 Employees (6 depts) • 45 Skills • 1,080 History Rows.",
            "## • Forecast Accuracy:  93.16% (6.84% MAPE, R² = 0.94).",
            "## • Course Match Precision:  94.8% (RAG Grounded).",
            "## • Demographic Bias Weight:  0.00% (Age/Gender stripped).",
        ],
        font_size=11.0,
        line_gap=0.33 * inch,
    )

    _draw_simple_card(
        c,
        0.55 * inch,
        0.60 * inch,
        12.2 * inch,
        2.45 * inch,
        "#0F172A",
        "All 10 Functional Requirements Fulfilled (FR-01 to FR-10)",
        [
            "## • FR-01: Skill Inventory (Sliders + Resume Parser)        • FR-06: Internal Mobility (Rankings + Cost Saved)",
            "## • FR-02: Skill Gap Detection (Knowledge Graph)            • FR-07: Workforce Risk (Shortage & Bus-Factor Alerts)",
            "## • FR-03 & 04: Market RAG & 6/12/24m ML Forecast           • FR-08 & 09: 3-Step Career Plan & Explainable AI (XAI)",
            "## • FR-05: Personalized Week-by-Week Courses                • FR-10: Human HR Approval Queue & Bias Refusal Guardrail",
        ],
        font_size=10.5,
        line_gap=0.29 * inch,
    )

    c.showPage()
    c.save()


# ===========================================================================
# 2. GENERATE NATIVE POWERPOINT (.PPTX) WITH SIMPLE, SHORT CONTENT
# ===========================================================================
SLIDES_CONTENT = [
    {
        "title": "SkillPulse AI — Workforce Evolution Predictor",
        "subtitle": "Use Case 4  |  HCLTech AI Future Ready FullStack Web Engineer",
        "boxes": [
            (
                "Squad Name – Arsenal",
                [
                    "Role – AI_Full Stack Web Engineer",
                    "Team:",
                    "• Mohit Tomar – HCLTFP2460368",
                    "• Ronit Singh Rawat – HCLTFP2465203",
                    "• Ankit Mohapatra – HCLTFP2467657",
                ],
                457200,
                1550000,
                5300000,
                3900000,
                "1E293B",
            ),
            (
                "Use Case 4: Skill Gap & Workforce Predictor",
                [
                    "• Industry: HR / Workforce Transformation",
                    "• Goal: Predict skill shortages 6–24m early",
                    "• Output: Personalized courses & internal mobility",
                    "• Tech: React, FastAPI, Pydantic, Scikit-Learn, RAG",
                    "• Safety: 0% Bias + Human HR Approval",
                ],
                6000000,
                1550000,
                5600000,
                3900000,
                "0F766E",
            ),
        ],
    },
    {
        "title": "1. Real-World Problem, Inputs & Solution",
        "subtitle": "Simple summary of the problem, 5 inputs, and business impact",
        "boxes": [
            (
                "Real-World Problem",
                [
                    "• Skill gaps found too late after winning projects.",
                    "• External hiring costs 3x more than reskilling.",
                    "• Keyword search misses 80% adjacent internal talent.",
                ],
                457200,
                1450000,
                5400000,
                2200000,
                "991B1B",
            ),
            (
                "5 Project Inputs",
                [
                    "1. Employee Skills (1–5 Sliders / Resume)",
                    "2. Learning Records (Certifications & Speed)",
                    "3. Project Requirements & Target Roles",
                    "4. Market Trends & 5. Tech Evolution",
                ],
                6100000,
                1450000,
                5500000,
                2200000,
                "3730A3",
            ),
            (
                "How We Solve It (Impact)",
                [
                    "• Predicts shortages 6–24m early (93.1% accuracy) & finds adjacent internal talent via Knowledge Graph.",
                    "• Saves 87% hiring cost ($2.47M saved) & strips Age/Gender bias (0% weight) with HR approval.",
                ],
                457200,
                3900000,
                11142800,
                1700000,
                "065F46",
            ),
        ],
    },
    {
        "title": "2. High-Level System Architecture & Tech Stack",
        "subtitle": "5 clean layers from React UI to FastAPI + Pydantic, 5 AI Agents, and SQLite/FAISS",
        "boxes": [
            (
                "Layers 1 & 2: Frontend UI & FastAPI + Pydantic Gateway",
                [
                    "• Layer 1 (Frontend): React 18 + TypeScript + Tailwind CSS + Zustand (5 Interactive Tabs).",
                    "• Layer 2 (API & Validation): Python FastAPI + Pydantic (validates all inputs/outputs) + Bias Filter + JWT.",
                ],
                457200,
                1450000,
                11142800,
                1900000,
                "1E3A8A",
            ),
            (
                "Layers 3, 4 & 5: 5 AI Agents, ML Brain & Databases",
                [
                    "• Layer 3 (Agents): LangGraph Coordinator running 5 specialized AI Agents.",
                    "• Layer 4 (AI/ML): Skills Knowledge Graph + Scikit-Learn Forecaster + Hybrid LLM.",
                    "• Layer 5 (Data): SQLite DB (120 Employees, 1,080 TS Rows) + FAISS Vector RAG (40+ Docs).",
                ],
                457200,
                3550000,
                11142800,
                2100000,
                "4C1D95",
            ),
        ],
    },
    {
        "title": "3. Why This Tech Stack & What Pydantic Does",
        "subtitle": "Why we chose each technology over alternatives",
        "boxes": [
            (
                "Why React, FastAPI & Pydantic?",
                [
                    "• React + Tailwind + Zustand: 3x faster & lighter than Redux.",
                    "• Python FastAPI (Why Not Java/Node?): Native AI/ML support.",
                    "• What Pydantic Does:",
                    "  1. Validates skill sliders (0–5) & horizons (6–24m).",
                    "  2. Enforces APPROVED/REJECTED HR rules.",
                    "  3. Auto-generates OpenAPI (/docs) schemas.",
                ],
                457200,
                1450000,
                5400000,
                4200000,
                "1E293B",
            ),
            (
                "Why Scikit-Learn, Vector RAG & SQLite?",
                [
                    "• Scikit-Learn + Hybrid LLM (Why Not LLM Alone?):",
                    "  LLMs fail at math. Scikit-Learn gives 93.1% accuracy",
                    "  and runs 100% offline without API key errors.",
                    "• Local Vector RAG: Searches docs in <3ms locally.",
                    "• SQLite: Zero-setup DB pre-seeded with 120 profiles.",
                ],
                6100000,
                1450000,
                5500000,
                4200000,
                "0F766E",
            ),
        ],
    },
    {
        "title": "4. End-to-End Working Flow (API & Data Flow)",
        "subtitle": "When each API is called and where data comes from",
        "boxes": [
            (
                "Flows 1 & 2: 5-Agent Simulator & What-If Forecaster",
                [
                    "• Flow 1 (Step 1): POST /api/v1/agents/simulate-custom-profile -> Pydantic validates ->",
                    "  Bias Filter strips Age/Gender -> 5 Agents query Graph + Vector RAG -> Saves to SQLite.",
                    "• Flow 2 (Step 2): POST /api/v1/forecast/simulate -> Fetches 24m history from SQLite ->",
                    "  Scikit-Learn predicts +6/12/24m demand & shortage risks.",
                ],
                457200,
                1450000,
                11142800,
                2050000,
                "312E81",
            ),
            (
                "Flows 3, 4 & 5: Graph, Mobility & HR Governance",
                [
                    "• Flow 3 & 4 (Step 3 & 4): GET /graph/skills-network & /mobility/match ->",
                    "  Queries Knowledge Graph & screens 120 SQLite employees to rank internal candidates.",
                    "• Flow 5 (Step 5): POST /guardrail/test & /governance/decision ->",
                    "  Blocks biased queries, checks JWT token & saves HR Approval in SQLite Audit Log.",
                ],
                457200,
                3700000,
                11142800,
                2000000,
                "065F46",
            ),
        ],
    },
    {
        "title": "5. The 5 AI Agents, Balanced Dataset & Results",
        "subtitle": "Simple summary of the 5 agents and evaluation scores",
        "boxes": [
            (
                "The 5 AI Agents",
                [
                    "• Agent 1 (Profiler): Finds skill gaps & graph bridges.",
                    "• Agent 2 (Forecaster): Checks RAG trends & ML demand.",
                    "• Agent 3 (Learning Coach): Builds course & career plan.",
                    "• Agent 4 (Mobility): Ranks internal candidates & ROI.",
                    "• Agent 5 (XAI Auditor): Shows Why-% & proves 0% bias.",
                ],
                457200,
                1450000,
                5400000,
                4200000,
                "3730A3",
            ),
            (
                "Dataset & Evaluation Results",
                [
                    "• Balanced Dataset: 120 Employees, 45 Skills, 1,080 Rows.",
                    "• Forecast Accuracy: 93.16% (6.84% MAPE, R² = 0.94).",
                    "• Course Precision@3: 94.8% (RAG Grounded).",
                    "• Demographic Bias: 0.00% (Age/Gender stripped).",
                    "• Automated Tests: 10 / 10 Passing in 0.08s.",
                ],
                6100000,
                1450000,
                5500000,
                4200000,
                "0F766E",
            ),
        ],
    },
]


def _make_slide_xml(slide_data: dict) -> str:
    shapes_xml = []
    shapes_xml.append(
        f"""
        <p:sp>
          <p:nvSpPr><p:cNvPr id="2" name="HeaderBg"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
          <p:spPr>
            <a:xfrm><a:off x="0" y="0"/><a:ext cx="12192000" cy="1150000"/></a:xfrm>
            <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
            <a:solidFill><a:srgbClr val="0F172A"/></a:solidFill>
          </p:spPr>
          <p:txBody>
            <a:bodyPr lIns="300000" tIns="150000"/>
            <a:lstStyle/>
            <a:p>
              <a:r><a:rPr lang="en-US" sz="2400" b="1"><a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill></a:rPr><a:t>{escape(slide_data["title"])}</a:t></a:r>
            </a:p>
            <a:p>
              <a:r><a:rPr lang="en-US" sz="1300"><a:solidFill><a:srgbClr val="38BDF8"/></a:solidFill></a:rPr><a:t>{escape(slide_data["subtitle"])}</a:t></a:r>
            </a:p>
          </p:txBody>
        </p:sp>
        """
    )

    shape_id = 10
    for box_title, lines, x, y, w, h, color_hex in slide_data["boxes"]:
        paras = [
            f"""<a:p><a:r><a:rPr lang="en-US" sz="1900" b="1"><a:solidFill><a:srgbClr val="38BDF8"/></a:solidFill></a:rPr><a:t>{escape(box_title)}</a:t></a:r></a:p>"""
        ]
        for ln in lines:
            paras.append(
                f"""<a:p><a:r><a:rPr lang="en-US" sz="1550"><a:solidFill><a:srgbClr val="F8FAFC"/></a:solidFill></a:rPr><a:t>{escape(ln)}</a:t></a:r></a:p>"""
            )
        shapes_xml.append(
            f"""
            <p:sp>
              <p:nvSpPr><p:cNvPr id="{shape_id}" name="Box{shape_id}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
              <p:spPr>
                <a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{w}" cy="{h}"/></a:xfrm>
                <a:prstGeom prst="roundRect"><a:avLst/></a:prstGeom>
                <a:solidFill><a:srgbClr val="{color_hex}"/></a:solidFill>
                <a:ln w="19050"><a:solidFill><a:srgbClr val="6366F1"/></a:solidFill></a:ln>
              </p:spPr>
              <p:txBody>
                <a:bodyPr lIns="250000" tIns="200000" rIns="250000" bIns="200000" wrap="square"/>
                <a:lstStyle/>
                {''.join(paras)}
              </p:txBody>
            </p:sp>
            """
        )
        shape_id += 1

    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
       xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
       xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
      {''.join(shapes_xml)}
    </p:spTree>
  </p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sld>"""


def build_pptx_file(pptx_path: str) -> None:
    with zipfile.ZipFile(pptx_path, "w", zipfile.ZIP_DEFLATED) as zf:
        slide_overrides = "\n".join(
            f'  <Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
            for i in range(1, 7)
        )
        zf.writestr(
            "[Content_Types].xml",
            f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>
  <Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>
  <Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>
  <Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>
{slide_overrides}
</Types>""",
        )
        zf.writestr(
            "_rels/.rels",
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>
</Relationships>""",
        )
        slide_rels = "\n".join(
            f'  <Relationship Id="rId{i+1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{i}.xml"/>'
            for i in range(1, 7)
        )
        zf.writestr(
            "ppt/_rels/presentation.xml.rels",
            f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>
  <Relationship Id="rId8" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="theme/theme1.xml"/>
{slide_rels}
</Relationships>""",
        )
        sld_ids = "\n".join(f'    <p:sldId id="{255+i}" r:id="rId{i+1}"/>' for i in range(1, 7))
        zf.writestr(
            "ppt/presentation.xml",
            f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
                xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
                xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst>
  <p:sldIdLst>
{sld_ids}
  </p:sldIdLst>
  <p:sldSz cx="12192000" cy="6858000"/>
  <p:notesSz cx="6858000" cy="9144000"/>
</p:presentation>""",
        )
        zf.writestr(
            "ppt/slideMasters/slideMaster1.xml",
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
             xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
             xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr></p:spTree></p:cSld>
  <p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/>
  <p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst>
</p:sldMaster>""",
        )
        zf.writestr(
            "ppt/slideMasters/_rels/slideMaster1.xml.rels",
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="../theme/theme1.xml"/>
</Relationships>""",
        )
        zf.writestr(
            "ppt/slideLayouts/slideLayout1.xml",
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldLayout xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
             xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
             xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" type="blank">
  <p:cSld name="Blank"><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr></p:spTree></p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sldLayout>""",
        )
        zf.writestr(
            "ppt/slideLayouts/_rels/slideLayout1.xml.rels",
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="../slideMasters/slideMaster1.xml"/>
</Relationships>""",
        )
        zf.writestr(
            "ppt/theme/theme1.xml",
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="Office Theme">
  <a:themeElements>
    <a:clrScheme name="Office">
      <a:dk1><a:sysClr val="windowText" lastClr="000000"/></a:dk1>
      <a:lt1><a:sysClr val="window" lastClr="FFFFFF"/></a:lt1>
      <a:dk2><a:srgbClr val="1F497D"/></a:dk2>
      <a:lt2><a:srgbClr val="EEECE1"/></a:lt2>
      <a:accent1><a:srgbClr val="4F81BD"/></a:accent1>
      <a:accent2><a:srgbClr val="C0504D"/></a:accent2>
      <a:accent3><a:srgbClr val="9BBB59"/></a:accent3>
      <a:accent4><a:srgbClr val="8064A2"/></a:accent4>
      <a:accent5><a:srgbClr val="4BACC6"/></a:accent5>
      <a:accent6><a:srgbClr val="F79646"/></a:accent6>
      <a:hlink><a:srgbClr val="0000FF"/></a:hlink>
      <a:folHlink><a:srgbClr val="800080"/></a:folHlink>
    </a:clrScheme>
    <a:fontScheme name="Office">
      <a:majorFont><a:latin typeface="Calibri"/><a:ea typeface=""/><a:cs typeface=""/></a:majorFont>
      <a:minorFont><a:latin typeface="Calibri"/><a:ea typeface=""/><a:cs typeface=""/></a:minorFont>
    </a:fontScheme>
    <a:fmtScheme name="Office">
      <a:fillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:fillStyleLst>
      <a:lnStyleLst><a:ln w="9525"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln><a:ln w="9525"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln><a:ln w="9525"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln></a:lnStyleLst>
      <a:effectStyleLst><a:effectStyle><a:effectLst/></a:effectStyle><a:effectStyle><a:effectLst/></a:effectStyle><a:effectStyle><a:effectLst/></a:effectStyle></a:effectStyleLst>
      <a:bgFillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:bgFillStyleLst>
    </a:fmtScheme>
  </a:themeElements>
</a:theme>""",
        )

        for idx, sdata in enumerate(SLIDES_CONTENT, start=1):
            zf.writestr(f"ppt/slides/slide{idx}.xml", _make_slide_xml(sdata))
            zf.writestr(
                f"ppt/slides/_rels/slide{idx}.xml.rels",
                """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>
</Relationships>""",
            )


if __name__ == "__main__":
    root_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_out = os.path.join(root_dir, "SkillPulse_AI_Arsenal_Presentation.pdf")
    pptx_out = os.path.join(root_dir, "SkillPulse_AI_Arsenal_Presentation.pptx")

    build_pdf_presentation(pdf_out)
    build_pptx_file(pptx_out)
    print(f"Generated PDF:  {pdf_out} ({os.path.getsize(pdf_out)} bytes)")
    print(f"Generated PPTX: {pptx_out} ({os.path.getsize(pptx_out)} bytes)")
