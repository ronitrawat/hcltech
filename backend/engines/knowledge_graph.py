"""
Skills Knowledge Graph Engine (FR-01, FR-02, FR-06, FR-07)
==========================================================
Constructs an in-memory weighted graph connecting:
- Skills (45 nodes across Emerging, Core, Legacy lifecycles)
- Skill-to-Skill Edges (PREREQUISITE_OF and ADJACENT_TO weights 0.0-1.0)
- Employees (proficiency vectors 1-5)
- Target Enterprise Roles & Upcoming Client Projects
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple


class SkillsKnowledgeGraphEngine:
    def __init__(self, skills: List[Dict[str, Any]], edges: List[Dict[str, Any]]) -> None:
        self.skills_by_id: Dict[str, Dict[str, Any]] = {s["id"]: s for s in skills}
        self.edges: List[Dict[str, Any]] = edges
        # Adjacency list: skill_id -> list of (neighbor_id, weight, relation, rationale)
        self.adj: Dict[str, List[Tuple[str, float, str, str]]] = {s["id"]: [] for s in skills}
        for e in edges:
            src, tgt, w, rel, rat = e["source"], e["target"], float(e["weight"]), e["relation"], e["rationale"]
            if src in self.adj and tgt in self.adj:
                self.adj[src].append((tgt, w, rel, rat))
                # Reverse adjacency with slight decay (0.9x) for bidirectional graph proximity
                self.adj[tgt].append((src, round(w * 0.9, 3), f"INVERSE_{rel}", rat))

    def get_best_adjacency_bridge(
        self, employee_skills: Dict[str, int], target_skill_id: str
    ) -> Dict[str, Any]:
        """
        Finds the strongest 1-hop or 2-hop graph bridge from an employee's existing skills
        to a missing target skill.
        """
        if target_skill_id in employee_skills:
            return {
                "bridge_skill_id": target_skill_id,
                "bridge_skill_name": self.skills_by_id[target_skill_id]["name"],
                "adjacency_weight": 1.0,
                "hops": 0,
                "rationale": "Employee already possesses direct proficiency in this skill.",
            }

        best_weight = 0.0
        best_bridge: Optional[Dict[str, Any]] = None

        # 1-hop check
        for emp_sk, emp_prof in employee_skills.items():
            if emp_sk not in self.adj:
                continue
            prof_factor = min(1.0, emp_prof / 4.0)
            for nbr, weight, rel, rationale in self.adj[emp_sk]:
                if nbr == target_skill_id:
                    effective = round(weight * (0.75 + 0.25 * prof_factor), 3)
                    if effective > best_weight:
                        best_weight = effective
                        best_bridge = {
                            "bridge_skill_id": emp_sk,
                            "bridge_skill_name": self.skills_by_id[emp_sk]["name"],
                            "employee_proficiency": emp_prof,
                            "adjacency_weight": effective,
                            "raw_edge_weight": weight,
                            "relation": rel,
                            "hops": 1,
                            "rationale": rationale,
                        }

        # 2-hop check if no strong 1-hop bridge found
        if best_weight < 0.65:
            for emp_sk, emp_prof in employee_skills.items():
                if emp_sk not in self.adj:
                    continue
                for mid_nbr, w1, rel1, _ in self.adj[emp_sk]:
                    for final_nbr, w2, rel2, rat2 in self.adj.get(mid_nbr, []):
                        if final_nbr == target_skill_id:
                            combined = round(w1 * w2 * 0.92, 3)
                            if combined > best_weight:
                                best_weight = combined
                                best_bridge = {
                                    "bridge_skill_id": emp_sk,
                                    "bridge_skill_name": (
                                        f"{self.skills_by_id[emp_sk]['name']} → "
                                        f"{self.skills_by_id[mid_nbr]['name']}"
                                    ),
                                    "employee_proficiency": emp_prof,
                                    "adjacency_weight": combined,
                                    "raw_edge_weight": round(w1 * w2, 3),
                                    "relation": f"2_HOP_{rel2}",
                                    "hops": 2,
                                    "rationale": rat2,
                                }

        if best_bridge:
            return best_bridge

        return {
            "bridge_skill_id": None,
            "bridge_skill_name": "Foundational Engineering",
            "adjacency_weight": 0.25,
            "hops": 3,
            "rationale": "Requires foundational onboarding track (no direct 1-2 hop graph edge).",
        }

    def analyze_employee_gaps_against_role(
        self, employee: Dict[str, Any], target_role: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        FR-01 & FR-02: Computes granular skill-by-skill gap breakdown, adjacency bridge scores,
        overall transition readiness %, and estimated reskilling duration.
        """
        emp_skills: Dict[str, int] = employee.get("skills", {})
        req_skills: Dict[str, int] = target_role.get("required_skills", {})
        learning_velocity: float = float(employee.get("learning_velocity_index", 0.8))

        skill_assessments: List[Dict[str, Any]] = []
        weighted_score_sum = 0.0
        total_weight = 0.0
        total_learning_hours = 0

        for req_sk_id, req_level in req_skills.items():
            sk_meta = self.skills_by_id.get(req_sk_id, {"name": req_sk_id, "domain": "General", "complexity": 3})
            current_level = int(emp_skills.get(req_sk_id, 0))
            importance_weight = float(req_level)
            total_weight += importance_weight

            if current_level >= req_level:
                status = "MASTERED"
                gap_delta = 0
                skill_credit = 1.0
                bridge_info = {
                    "bridge_skill_name": sk_meta["name"],
                    "adjacency_weight": 1.0,
                    "rationale": "Meets or exceeds target role requirement.",
                }
                hours_needed = 0
            elif current_level > 0:
                status = "PARTIAL_GAP"
                gap_delta = req_level - current_level
                skill_credit = (current_level / req_level) * 0.85
                bridge_info = {
                    "bridge_skill_name": f"Existing {sk_meta['name']} (L{current_level})",
                    "adjacency_weight": round(current_level / req_level, 2),
                    "rationale": f"Upgrade existing Level {current_level} proficiency to Level {req_level}.",
                }
                hours_needed = int(gap_delta * 10 * (sk_meta["complexity"] / 3.0))
            else:
                status = "MISSING_BRIDGEABLE"
                gap_delta = req_level
                bridge_info = self.get_best_adjacency_bridge(emp_skills, req_sk_id)
                adj_w = float(bridge_info["adjacency_weight"])
                # Adjacent skills give up to 78% readiness credit toward learning a new skill!
                skill_credit = adj_w * 0.78
                discount = 1.0 - (adj_w * 0.50)
                hours_needed = max(12, int(req_level * 12 * discount * (sk_meta["complexity"] / 3.0)))

            weighted_score_sum += skill_credit * importance_weight
            total_learning_hours += hours_needed

            skill_assessments.append({
                "skill_id": req_sk_id,
                "skill_name": sk_meta["name"],
                "domain": sk_meta.get("domain", "Enterprise"),
                "lifecycle": sk_meta.get("lifecycle", "CORE"),
                "current_level": current_level,
                "required_level": req_level,
                "gap_delta": gap_delta,
                "status": status,
                "adjacency_bridge": bridge_info,
                "estimated_study_hours": hours_needed,
            })

        raw_readiness = (weighted_score_sum / max(1.0, total_weight)) * 100.0
        # Incorporate employee learning velocity bonus (up to +6%)
        final_readiness = round(min(98.5, max(25.0, raw_readiness + (learning_velocity - 0.75) * 20.0)), 1)

        # Assuming ~10 hours/week dedicated enterprise upskilling allocation
        effective_weekly_hours = 10.0 * max(0.7, learning_velocity)
        estimated_weeks = max(1, int(round(total_learning_hours / effective_weekly_hours)))

        return {
            "employee_id": employee["id"],
            "employee_name": employee["display_name"],
            "current_role": employee["current_role"],
            "department": employee["department"],
            "target_role_id": target_role["id"],
            "target_role_title": target_role["title"],
            "readiness_score_pct": final_readiness,
            "total_learning_hours": total_learning_hours,
            "estimated_transition_weeks": estimated_weeks,
            "direct_gaps_count": sum(1 for a in skill_assessments if a["status"] != "MASTERED"),
            "mastered_count": sum(1 for a in skill_assessments if a["status"] == "MASTERED"),
            "skill_breakdown": skill_assessments,
        }

    def get_network_visualization_data(
        self, employees: List[Dict[str, Any]], domain_filter: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Returns nodes & links formatted for the interactive Skills Knowledge Graph canvas.
        """
        supply_counts: Dict[str, int] = {sk_id: 0 for sk_id in self.skills_by_id}
        avg_prof: Dict[str, List[int]] = {sk_id: [] for sk_id in self.skills_by_id}
        for emp in employees:
            for sk_id, prof in emp.get("skills", {}).items():
                if sk_id in supply_counts and prof >= 3:
                    supply_counts[sk_id] += 1
                if sk_id in avg_prof:
                    avg_prof[sk_id].append(prof)

        nodes: List[Dict[str, Any]] = []
        valid_ids = set()
        for sk_id, sk in self.skills_by_id.items():
            if domain_filter and domain_filter != "ALL" and sk["domain"] != domain_filter:
                continue
            valid_ids.add(sk_id)
            profs = avg_prof[sk_id]
            nodes.append({
                "id": sk_id,
                "label": sk["name"],
                "domain": sk["domain"],
                "lifecycle": sk["lifecycle"],
                "market_growth_yoy": sk["market_growth_yoy"],
                "qualified_headcount": supply_counts[sk_id],
                "avg_proficiency": round(sum(profs) / len(profs), 2) if profs else 0.0,
                "bus_factor_risk": supply_counts[sk_id] <= 6 and sk["lifecycle"] == "EMERGING",
            })

        links: List[Dict[str, Any]] = []
        for e in self.edges:
            if e["source"] in valid_ids and e["target"] in valid_ids:
                links.append({
                    "source": e["source"],
                    "target": e["target"],
                    "relation": e["relation"],
                    "weight": e["weight"],
                    "rationale": e["rationale"],
                })

        return {
            "total_nodes": len(nodes),
            "total_edges": len(links),
            "domains": sorted({s["domain"] for s in self.skills_by_id.values()}),
            "nodes": nodes,
            "links": links,
        }
