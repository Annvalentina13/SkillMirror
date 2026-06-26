"""
SkillMirror — Job Description Scraper
Module 2 of 4 — Phase 2 (Multi-role support)
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
from collections import defaultdict, Counter
from modules.parser import ALIAS_TO_SKILL, get_category

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

# ── Role Groups ───────────────────────────────────────────────────────────────

ROLE_GROUPS = {
    "Data & AI": [
        "data scientist",
        "data analyst",
        "machine learning engineer",
        "AI engineer",
    ],
    "Software Engineering": [
        "software engineer",
        "backend developer",
        "full stack developer",
        "frontend developer",
    ],
    "Cloud & DevOps": [
        "devops engineer",
        "cloud engineer",
        "site reliability engineer",
        "platform engineer",
    ],
    "Cybersecurity": [
        "cybersecurity analyst",
        "security engineer",
        "penetration tester",
        "SOC analyst",
    ],
    "ECE & Embedded": [
        "embedded systems engineer",
        "VLSI engineer",
        "IoT engineer",
        "signal processing engineer",
    ],
    "Mechanical": [
        "mechanical design engineer",
        "CAD engineer",
        "manufacturing engineer",
        "automotive engineer",
    ],
    "Civil": [
        "structural engineer",
        "civil site engineer",
        "urban planner",
        "environmental engineer",
    ],
    "Finance & MBA": [
        "financial analyst",
        "investment banking analyst",
        "business analyst",
        "product manager",
    ],
    "Medical & Healthcare": [
        "clinical data analyst",
        "healthcare analyst",
        "medical researcher",
        "hospital administrator",
    ],
    "Law": [
        "corporate lawyer",
        "legal analyst",
        "compliance officer",
        "legal researcher",
    ],
    "Design & UX": [
        "UI UX designer",
        "product designer",
        "graphic designer",
        "visual designer",
    ],
    "Media & Marketing": [
        "digital marketing analyst",
        "content strategist",
        "social media manager",
        "SEO analyst",
    ],
}

# ── Fallback JD datasets per role group ───────────────────────────────────────

FALLBACK_JDS = {
    "Data & AI": [
        "Python machine learning deep learning SQL statistics pandas numpy scikit-learn data visualization matplotlib TensorFlow PyTorch git cloud computing AWS",
        "NLP BERT transformers Python machine learning statistics hypothesis testing data analysis SQL big data spark",
        "Python supervised learning unsupervised learning regression classification clustering neural networks data visualization plotly tableau",
        "Machine learning deep learning computer vision object detection TensorFlow keras python sql git linux docker",
        "Data analysis statistics probability python pandas numpy matplotlib seaborn scikit-learn machine learning sql databases",
        "Python NLP text classification sentiment analysis word embeddings bert transformers deep learning sql data engineering",
        "Machine learning XGBoost lightgbm gradient boosting feature engineering pandas python sql data visualization git",
        "Deep learning CNN RNN LSTM computer vision image classification tensorflow pytorch python sql cloud computing",
        "Generative AI LLM GPT python NLP deep learning transformers machine learning cloud computing REST API docker",
        "Python data analysis SQL visualization matplotlib seaborn statistics hypothesis testing data cleaning pandas numpy",
    ],
    "Software Engineering": [
        "Python Java JavaScript data structures algorithms OOP REST API git SQL databases system design",
        "Java Spring Boot microservices REST API SQL git docker kubernetes AWS backend development",
        "JavaScript React NodeJS HTML CSS REST API git SQL MongoDB frontend backend full stack",
        "Python Django Flask REST API SQL git docker linux OOP data structures algorithms",
        "Java C++ data structures algorithms OOP system design SQL git linux problem solving",
        "JavaScript TypeScript React Redux NodeJS REST API git SQL MongoDB docker frontend",
        "Python Java SQL git OOP REST API microservices docker kubernetes cloud computing AWS",
        "Full stack development React NodeJS SQL MongoDB REST API git docker javascript HTML CSS",
        "Backend development Python SQL REST API git docker kubernetes microservices system design linux",
        "Software engineering Java Python data structures algorithms OOP git SQL databases system design",
    ],
    "Cloud & DevOps": [
        "AWS Azure GCP docker kubernetes CI/CD jenkins git linux bash scripting terraform ansible",
        "DevOps docker kubernetes CI/CD pipeline git jenkins AWS cloud computing linux infrastructure",
        "Cloud computing AWS EC2 S3 lambda docker kubernetes terraform linux git CI/CD devops",
        "Site reliability engineering SRE kubernetes docker monitoring prometheus grafana linux AWS git",
        "Platform engineering kubernetes docker terraform AWS CI/CD git linux python bash scripting",
        "DevOps CI/CD jenkins docker kubernetes AWS git linux ansible terraform python scripting",
        "Cloud engineer AWS Azure kubernetes docker terraform git linux CI/CD python bash",
        "Kubernetes docker AWS CI/CD terraform ansible linux git python monitoring grafana prometheus",
        "Cloud infrastructure AWS GCP Azure terraform kubernetes docker CI/CD git linux python",
        "DevOps automation docker kubernetes CI/CD AWS git terraform linux python bash ansible",
    ],
    "Cybersecurity": [
        "network security cryptography python linux penetration testing ethical hacking SIEM SQL firewalls",
        "cybersecurity SOC SIEM threat analysis python linux network security cryptography incident response",
        "penetration testing ethical hacking python linux network security vulnerabilities OWASP SQL",
        "security engineer cryptography python linux network protocols firewalls SIEM threat intelligence",
        "SOC analyst SIEM threat detection python linux network security incident response cryptography",
        "cybersecurity analyst python linux network security SQL cryptography firewalls threat analysis",
        "information security cryptography python linux penetration testing network protocols SIEM",
        "ethical hacking penetration testing python linux OWASP network security cryptography SQL",
        "cybersecurity python linux network security cryptography SIEM threat intelligence SQL firewalls",
        "security operations python linux network security SIEM cryptography incident response SQL",
    ],
    "ECE & Embedded": [
        "embedded systems C C++ microcontrollers RTOS Arduino Raspberry Pi IoT sensors firmware",
        "VLSI design Verilog VHDL digital circuits FPGA semiconductor signal processing",
        "IoT embedded systems C python sensors Arduino Raspberry Pi MQTT wireless protocols",
        "signal processing MATLAB python DSP communications wireless embedded systems C",
        "embedded C RTOS microcontrollers ARM cortex firmware PCB design IoT sensors",
        "VLSI VHDL Verilog digital design FPGA semiconductor manufacturing signal processing",
        "IoT C python MQTT embedded systems sensors wireless protocols Arduino cloud computing",
        "embedded systems firmware C C++ RTOS microcontrollers ARM IoT sensors debugging",
        "signal processing MATLAB DSP python communications wireless embedded systems C",
        "VLSI design digital circuits Verilog VHDL FPGA semiconductor signal processing MATLAB",
    ],
    "Mechanical": [
        "CAD SolidWorks AutoCAD mechanical design finite element analysis manufacturing materials",
        "mechanical engineering CAD AutoCAD SolidWorks ANSYS FEA thermal analysis manufacturing",
        "design engineering SolidWorks CAD FEA ANSYS manufacturing materials science thermodynamics",
        "automotive engineering CAD SolidWorks MATLAB thermal analysis FEA manufacturing materials",
        "manufacturing engineering CAD AutoCAD lean manufacturing Six Sigma quality control materials",
        "mechanical design CAD SolidWorks FEA ANSYS thermodynamics fluid mechanics manufacturing",
        "product design SolidWorks AutoCAD CAD materials science manufacturing FEA ANSYS",
        "CAD design SolidWorks AutoCAD ANSYS FEA mechanical engineering manufacturing materials",
        "thermal engineering MATLAB thermodynamics fluid mechanics CAD ANSYS FEA heat transfer",
        "mechanical engineer CAD SolidWorks AutoCAD FEA manufacturing materials thermodynamics",
    ],
    "Civil": [
        "structural engineering AutoCAD STAAD Pro ETABS concrete steel design construction management",
        "civil engineering AutoCAD STAAD Pro structural analysis construction management surveying",
        "structural design ETABS STAAD Pro AutoCAD concrete steel reinforcement construction",
        "site engineer AutoCAD construction management project management surveying structural analysis",
        "urban planning GIS AutoCAD environmental engineering construction project management",
        "environmental engineer GIS AutoCAD water treatment environmental impact assessment",
        "structural engineering STAAD Pro ETABS AutoCAD concrete design construction management",
        "civil site engineer AutoCAD construction management surveying structural analysis project",
        "geotechnical engineering AutoCAD soil mechanics foundation design construction management",
        "civil engineering AutoCAD GIS STAAD Pro structural analysis construction project management",
    ],
    "Finance & MBA": [
        "financial modeling Excel VBA Python SQL data analysis investment banking valuation DCF",
        "financial analysis Excel Python SQL statistics data visualization power bi tableau reporting",
        "business analysis SQL Excel Python data analysis statistics stakeholder management reporting",
        "product management SQL Excel data analysis user research agile scrum roadmap stakeholder",
        "investment banking financial modeling Excel valuation M&A DCF LBO accounting finance",
        "financial analyst Excel SQL Python statistics data analysis forecasting budgeting reporting",
        "business analyst SQL Excel data analysis requirements gathering agile stakeholder management",
        "product manager SQL Excel data analysis user research agile scrum prioritization roadmap",
        "financial modeling Excel Python SQL accounting valuation DCF financial analysis reporting",
        "data analysis Excel Python SQL statistics visualization tableau power bi business intelligence",
    ],
    "Medical & Healthcare": [
        "clinical data analysis SPSS SAS R statistics medical research Excel data management",
        "healthcare analytics SQL Python R statistics data visualization Excel clinical research",
        "medical research statistics SPSS SAS clinical trials data analysis Excel reporting",
        "hospital administration Excel SQL data analysis healthcare management statistics reporting",
        "clinical data management SAS R statistics medical coding data analysis Excel reporting",
        "healthcare data analytics SQL Python R statistics Excel visualization clinical research",
        "medical researcher statistics SPSS SAS R clinical trials data analysis Excel reporting",
        "health informatics SQL Python R statistics healthcare data analysis Excel visualization",
        "clinical research statistics SAS SPSS data analysis Excel medical coding reporting",
        "healthcare analyst SQL Excel Python statistics data visualization power bi reporting",
    ],
    "Law": [
        "legal research writing contract drafting corporate law compliance MS Office Excel",
        "corporate law contract drafting legal research compliance regulatory MS Office writing",
        "legal analyst research writing compliance contract review corporate law MS Office",
        "compliance officer legal research regulatory compliance contract review MS Office Excel",
        "intellectual property legal research patent drafting compliance writing MS Office",
        "corporate lawyer contract drafting legal research M&A compliance regulatory MS Office",
        "legal researcher writing research analysis compliance corporate law MS Office Excel",
        "contract management legal research drafting compliance corporate law MS Office writing",
        "regulatory compliance legal research writing contract review MS Office Excel analysis",
        "legal analysis research writing corporate law compliance contract drafting MS Office",
    ],
    "Design & UX": [
        "UI UX design Figma Adobe XD user research prototyping wireframing usability testing",
        "product design Figma sketch user research prototyping wireframing interaction design",
        "graphic design Adobe Photoshop Illustrator InDesign typography branding visual design",
        "UX design Figma user research usability testing prototyping wireframing interaction",
        "visual design Adobe Photoshop Illustrator Figma typography branding motion design",
        "UI design Figma Adobe XD prototyping wireframing user research usability HTML CSS",
        "product designer Figma user research prototyping wireframing interaction design visual",
        "graphic designer Adobe Illustrator Photoshop InDesign typography branding visual design",
        "UX researcher user research usability testing Figma prototyping wireframing analysis",
        "UI UX Figma Adobe XD prototyping wireframing user research HTML CSS visual design",
    ],
    "Media & Marketing": [
        "digital marketing SEO SEM Google Analytics social media content marketing Excel SQL",
        "content strategy SEO writing social media analytics Google Analytics Excel marketing",
        "social media management Instagram Facebook Twitter analytics content creation marketing",
        "SEO analyst Google Analytics keyword research content writing link building Excel SQL",
        "digital marketing Google Analytics SEO SEM social media content strategy Excel SQL",
        "content marketing SEO writing social media analytics Google Analytics strategy Excel",
        "marketing analyst Google Analytics SQL Excel data analysis SEO social media reporting",
        "social media marketing Instagram Facebook Twitter content creation analytics SEO Excel",
        "SEO SEM Google Analytics keyword research content writing digital marketing Excel SQL",
        "digital marketing analytics Google Analytics SEO social media content strategy Excel",
    ],
}

# ── Skill extractor ───────────────────────────────────────────────────────────

def extract_skills_from_jd(text):
    text_lower = text.lower()
    found = set()
    for alias, skill in ALIAS_TO_SKILL.items():
        pattern = r'\b' + re.escape(alias.strip()) + r'\b'
        if re.search(pattern, text_lower):
            found.add(skill)
    return list(found)


# ── Main scrape function ──────────────────────────────────────────────────────

def scrape_jobs(role_group="Data & AI", use_fallback=True):
    """
    Scrape or load JD data for a specific role group.
    """
    print(f"\n[1/2] Loading JD data for: {role_group}")

    if role_group not in FALLBACK_JDS:
        print(f"  Role group '{role_group}' not found, defaulting to Data & AI")
        role_group = "Data & AI"

    all_jds = []
    descriptions = FALLBACK_JDS[role_group]
    roles = ROLE_GROUPS[role_group]

    for i, desc in enumerate(descriptions):
        role = roles[i % len(roles)]
        skills = extract_skills_from_jd(desc)
        all_jds.append({
            "role": role,
            "description": desc,
            "skills": skills
        })

    print(f"[2/2] Analysing {len(all_jds)} job descriptions...")

    skill_freq = Counter()
    skill_per_role = defaultdict(lambda: defaultdict(int))

    for jd in all_jds:
        for skill in jd["skills"]:
            skill_freq[skill] += 1
            skill_per_role[jd["role"]][skill] += 1

    total_jds = len(all_jds)
    ranked = []
    for skill, count in skill_freq.most_common():
        ranked.append({
            "skill": skill,
            "frequency": count,
            "percentage": round((count / total_jds) * 100, 1),
            "category": get_category(skill)
        })

    result = {
        "total_jds": total_jds,
        "role_group": role_group,
        "roles_covered": roles,
        "skills_ranked": ranked,
        "skill_per_role": {
            role: dict(skills)
            for role, skills in skill_per_role.items()
        }
    }

    with open("data/jd_skills.json", "w") as f:
        json.dump(result, f, indent=2)

    print(f"\n✅ Top 10 skills for {role_group}:")
    for i, s in enumerate(ranked[:10], 1):
        print(f"  {i:2}. {s['skill']:<25} ({s['percentage']}% of JDs)")

    return result


if __name__ == "__main__":
    import sys
    group = sys.argv[1] if len(sys.argv) > 1 else "Data & AI"
    scrape_jobs(role_group=group)