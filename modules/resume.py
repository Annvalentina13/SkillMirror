"""
SkillMirror — Resume Parser & Analyser
Module 7 of 7 — Phase 6
"""

import json
import re
import pdfplumber
from collections import defaultdict
from modules.parser import ALIAS_TO_SKILL, get_category, SKILL_TAXONOMY


# ── Extract text from resume PDF ──────────────────────────────────────────────

def extract_resume_text(pdf_path):
    """Extract raw text from resume PDF."""
    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                pages.append(text)
    full_text = "\n".join(pages)
    full_text = re.sub(r'[ \t]+', ' ', full_text)
    full_text = re.sub(r'\n{3,}', '\n\n', full_text)
    return full_text


# ── Extract skills from resume ────────────────────────────────────────────────

def extract_resume_skills(text):
    """Extract skills from resume text using taxonomy."""
    text_lower = text.lower()
    found = {}

    for alias, skill in ALIAS_TO_SKILL.items():
        pattern = r'\b' + re.escape(alias.strip()) + r'\b'
        if re.search(pattern, text_lower):
            found[skill] = found.get(skill, 0) + 1

    # Build ranked list
    ranked = []
    for skill, count in sorted(
        found.items(), key=lambda x: x[1], reverse=True
    ):
        ranked.append({
            "skill": skill,
            "mentions": count,
            "category": get_category(skill)
        })

    return ranked


# ── Resume vs JD Analysis ─────────────────────────────────────────────────────

def resume_vs_jd(resume_skills, jd_data):
    """
    Compare resume skills against JD requirements.
    Returns gap analysis from a personal perspective.
    """
    resume_skill_names = {s["skill"] for s in resume_skills}
    jd_skills = {
        item["skill"]: item["percentage"]
        for item in jd_data["skills_ranked"]
    }

    covered = []
    gaps    = []

    for skill, pct in sorted(
        jd_skills.items(), key=lambda x: x[1], reverse=True
    ):
        if skill in resume_skill_names:
            covered.append({
                "skill": skill,
                "demand": pct,
                "status": "on_resume"
            })
        else:
            gaps.append({
                "skill": skill,
                "demand": pct,
                "status": "missing_from_resume"
            })

    total = len(jd_skills)
    coverage = round((len(covered) / total) * 100, 1) if total else 0

    return {
        "covered": covered,
        "gaps": gaps,
        "coverage_score": coverage,
        "covered_count": len(covered),
        "gap_count": len(gaps),
        "total_jd_skills": total
    }


# ── Resume vs Syllabus Analysis ───────────────────────────────────────────────

def resume_vs_syllabus(resume_skills, syllabus_data):
    """
    Compare resume skills against syllabus skills.
    Shows how much of your education you're actually using.
    """
    resume_skill_names  = {s["skill"] for s in resume_skills}
    syllabus_skill_names = {
        s["skill"] for s in syllabus_data["skills_ranked"]
    }

    # Skills from syllabus on resume
    using = []
    not_using = []

    for item in syllabus_data["skills_ranked"]:
        skill = item["skill"]
        if skill in resume_skill_names:
            using.append(skill)
        else:
            not_using.append(skill)

    # Skills on resume not in syllabus (self-learned)
    self_learned = [
        s["skill"] for s in resume_skills
        if s["skill"] not in syllabus_skill_names
    ]

    utilisation = round(
        (len(using) / len(syllabus_skill_names)) * 100, 1
    ) if syllabus_skill_names else 0

    return {
        "utilisation_score": utilisation,
        "using": using,
        "not_using": not_using,
        "self_learned": self_learned,
        "syllabus_total": len(syllabus_skill_names),
        "using_count": len(using),
        "self_learned_count": len(self_learned)
    }


# ── Resume Score ──────────────────────────────────────────────────────────────

def score_resume(resume_skills, jd_data, role_group):
    """
    Score the resume for a specific role out of 100.
    Weighted by skill demand in JDs.
    """
    resume_skill_names = {s["skill"] for s in resume_skills}
    jd_skills = {
        item["skill"]: item["percentage"]
        for item in jd_data["skills_ranked"]
    }

    # Weighted score — high demand skills worth more
    total_weight  = sum(jd_skills.values())
    earned_weight = sum(
        pct for skill, pct in jd_skills.items()
        if skill in resume_skill_names
    )

    raw_score = (
        (earned_weight / total_weight) * 100
        if total_weight else 0
    )
    score = round(min(raw_score, 100), 1)

    # Grade
    if score >= 90:
        grade = "A"
        verdict = "Excellent match! You're highly qualified for this role."
    elif score >= 75:
        grade = "B"
        verdict = "Strong match. A few additions will make you stand out."
    elif score >= 60:
        grade = "C"
        verdict = "Decent match. Focus on the top gaps to improve your chances."
    elif score >= 40:
        grade = "D"
        verdict = "Partial match. Significant skill gaps to address."
    else:
        grade = "F"
        verdict = "Low match. Consider building foundational skills first."

    # What to add to resume
    gaps_sorted = sorted(
        [
            {"skill": s, "demand": p}
            for s, p in jd_skills.items()
            if s not in resume_skill_names
        ],
        key=lambda x: x["demand"],
        reverse=True
    )

    # Quick wins — skills that appear in JDs a lot
    quick_wins = [g for g in gaps_sorted if g["demand"] >= 30]
    nice_to_have = [g for g in gaps_sorted if g["demand"] < 30]

    return {
        "score": score,
        "grade": grade,
        "verdict": verdict,
        "quick_wins": quick_wins[:5],
        "nice_to_have": nice_to_have[:5],
        "role_group": role_group
    }


# ── Full Resume Analysis ──────────────────────────────────────────────────────

def analyse_resume(
    resume_pdf_path,
    role_group,
    syllabus_data=None
):
    """
    Full resume analysis pipeline.
    """
    print(f"\n[1/4] Extracting resume text...")
    text = extract_resume_text(resume_pdf_path)

    if not text.strip():
        return {"error": "No text found in resume PDF"}

    print(f"[2/4] Extracting skills from resume...")
    resume_skills = extract_resume_skills(text)

    print(f"[3/4] Loading JD data...")
    with open("data/jd_skills.json") as f:
        jd_data = json.load(f)

    print(f"[4/4] Running analysis...")

    # Resume vs JD
    vs_jd = resume_vs_jd(resume_skills, jd_data)

    # Resume score
    score = score_resume(resume_skills, jd_data, role_group)

    # Resume vs Syllabus (optional)
    vs_syllabus = None
    if syllabus_data:
        vs_syllabus = resume_vs_syllabus(resume_skills, syllabus_data)

    result = {
        "role_group": role_group,
        "resume_skills": resume_skills,
        "resume_skill_count": len(resume_skills),
        "vs_jd": vs_jd,
        "score": score,
        "vs_syllabus": vs_syllabus
    }

    with open("data/resume_analysis.json", "w") as f:
        json.dump(result, f, indent=2)

    print(f"\n✅ Resume analysis saved to data/resume_analysis.json")
    return result


# ── Test ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Resume module loaded successfully!")
    print(f"Taxonomy size: {len(ALIAS_TO_SKILL)} aliases")