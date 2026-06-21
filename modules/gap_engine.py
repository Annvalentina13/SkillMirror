"""
SkillMirror — Gap Analysis Engine
Module 3 of 4
"""

import json
from collections import defaultdict

# ── Load data ─────────────────────────────────────────────────────────────────

def load_data():
    with open("data/syllabus_skills.json") as f:
        syllabus = json.load(f)
    with open("data/jd_skills.json") as f:
        jd = json.load(f)
    return syllabus, jd

# ── Gap Analysis ──────────────────────────────────────────────────────────────

def analyse_gap():
    syllabus, jd = load_data()

    # Skills your syllabus covers
    syllabus_skills = {
        item["skill"] for item in syllabus["skills_ranked"]
    }

    # All industry skills with their demand %
    jd_skills = {
        item["skill"]: item["percentage"]
        for item in jd["skills_ranked"]
    }

    # ── Classify each JD skill ────────────────────────────────────────────────
    covered     = []  # in syllabus AND industry wants
    gaps        = []  # industry wants but syllabus MISSING
    low_demand  = []  # in syllabus but industry doesn't care much

    for skill, pct in sorted(jd_skills.items(),
                             key=lambda x: x[1], reverse=True):
        if skill in syllabus_skills:
            covered.append({"skill": skill, "demand": pct, "status": "covered"})
        else:
            gaps.append({"skill": skill, "demand": pct, "status": "gap"})

    # Skills in syllabus not in JDs at all
    for item in syllabus["skills_ranked"]:
        skill = item["skill"]
        if skill not in jd_skills:
            low_demand.append({
                "skill": skill,
                "demand": 0,
                "status": "low_demand"
            })

    # ── Coverage score ────────────────────────────────────────────────────────
    total_industry_skills = len(jd_skills)
    covered_count = len(covered)
    coverage_score = round((covered_count / total_industry_skills) * 100, 1)

    # ── Weighted gap score ────────────────────────────────────────────────────
    # Higher weight for high-demand missing skills
    gap_score = sum(g["demand"] for g in gaps)
    max_possible = sum(jd_skills.values())
    gap_severity = round((gap_score / max_possible) * 100, 1) if max_possible else 0

    # ── Roadmap: prioritised learning list ───────────────────────────────────
    roadmap = sorted(gaps, key=lambda x: x["demand"], reverse=True)

    result = {
        "summary": {
            "syllabus_skills_count": len(syllabus_skills),
            "industry_skills_count": total_industry_skills,
            "covered_count": covered_count,
            "gap_count": len(gaps),
            "coverage_score": coverage_score,
            "gap_severity": gap_severity,
        },
        "covered": covered,
        "gaps": gaps,
        "low_demand": low_demand,
        "roadmap": roadmap
    }

    # Save
    with open("data/gap_analysis.json", "w") as f:
        json.dump(result, f, indent=2)

    # Print summary
    print("\n" + "="*50)
    print(f"  SkillMirror — Gap Analysis Report")
    print("="*50)
    print(f"\n  Syllabus skills   : {len(syllabus_skills)}")
    print(f"  Industry skills   : {total_industry_skills}")
    print(f"  Coverage score    : {coverage_score}%")
    print(f"  Gap severity      : {gap_severity}%")

    print(f"\n✅ COVERED ({len(covered)} skills):")
    for s in covered:
        print(f"   ✓  {s['skill']:<25} {s['demand']}% of JDs")

    print(f"\n❌ GAPS — Learn These ({len(gaps)} skills):")
    for s in roadmap:
        print(f"   ✗  {s['skill']:<25} {s['demand']}% of JDs")

    print(f"\n  Saved to data/gap_analysis.json")
    return result


if __name__ == "__main__":
    analyse_gap()