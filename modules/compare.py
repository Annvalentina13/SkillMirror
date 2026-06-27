"""
SkillMirror — College Comparison Engine
Module 6 of 6 — Phase 5
"""

import json
import os
from modules.parser import parse_syllabus
from modules.scraper import scrape_jobs
from modules.gap_engine import analyse_gap


# ── Compare two syllabuses ────────────────────────────────────────────────────

def compare_colleges(
    pdf_path_1, college_name_1,
    pdf_path_2, college_name_2,
    role_group
):
    """
    Parse both syllabuses, run gap analysis for each,
    and return a structured comparison result.
    """

    results = {}

    for pdf_path, college_name in [
        (pdf_path_1, college_name_1),
        (pdf_path_2, college_name_2)
    ]:
        print(f"\nAnalysing: {college_name}")

        # Parse syllabus
        parse_syllabus(pdf_path, college_name)

        # Load JD data for role
        scrape_jobs(role_group=role_group, use_fallback=True)

        # Run gap analysis
        gap = analyse_gap()

        # Load syllabus skills
        with open("data/syllabus_skills.json") as f:
            syllabus = json.load(f)

        results[college_name] = {
            "college": college_name,
            "role_group": role_group,
            "coverage_score": gap["summary"]["coverage_score"],
            "covered_count": gap["summary"]["covered_count"],
            "gap_count": gap["summary"]["gap_count"],
            "industry_skills": gap["summary"]["industry_skills_count"],
            "covered": gap["covered"],
            "gaps": gap["gaps"],
            "roadmap": gap["roadmap"],
            "syllabus_skills": syllabus["total_skills"],
            "top_gaps": gap["gaps"][:5],
            "top_covered": gap["covered"][:5],
        }

    # Save comparison result
    comparison = {
        "role_group": role_group,
        "college_1": college_name_1,
        "college_2": college_name_2,
        "results": results,
        "winner": get_winner(results, college_name_1, college_name_2),
        "common_gaps": get_common_gaps(
            results, college_name_1, college_name_2
        ),
        "unique_gaps": get_unique_gaps(
            results, college_name_1, college_name_2
        ),
    }

    with open("data/comparison.json", "w") as f:
        json.dump(comparison, f, indent=2)

    print(f"\n✅ Comparison saved to data/comparison.json")
    return comparison


# ── Helper functions ──────────────────────────────────────────────────────────

def get_winner(results, name1, name2):
    """Return which college has better coverage."""
    score1 = results[name1]["coverage_score"]
    score2 = results[name2]["coverage_score"]
    if score1 > score2:
        return {"college": name1, "score": score1, "margin": round(score1 - score2, 1)}
    elif score2 > score1:
        return {"college": name2, "score": score2, "margin": round(score2 - score1, 1)}
    else:
        return {"college": "Tie", "score": score1, "margin": 0}


def get_common_gaps(results, name1, name2):
    """Skills missing in BOTH colleges."""
    gaps1 = {g["skill"] for g in results[name1]["gaps"]}
    gaps2 = {g["skill"] for g in results[name2]["gaps"]}
    common = gaps1 & gaps2

    # Get demand for common gaps from college 1
    demand_map = {
        g["skill"]: g["demand"]
        for g in results[name1]["gaps"]
    }

    return [
        {"skill": skill, "demand": demand_map.get(skill, 0)}
        for skill in common
    ]


def get_unique_gaps(results, name1, name2):
    """Skills missing in one college but not the other."""
    gaps1 = {g["skill"] for g in results[name1]["gaps"]}
    gaps2 = {g["skill"] for g in results[name2]["gaps"]}

    demand_map1 = {g["skill"]: g["demand"] for g in results[name1]["gaps"]}
    demand_map2 = {g["skill"]: g["demand"] for g in results[name2]["gaps"]}

    return {
        name1: [
            {"skill": s, "demand": demand_map1[s]}
            for s in gaps1 - gaps2
        ],
        name2: [
            {"skill": s, "demand": demand_map2[s]}
            for s in gaps2 - gaps1
        ]
    }