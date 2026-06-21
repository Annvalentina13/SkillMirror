"""
SkillMirror — Job Description Scraper
Module 2 of 4
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
from collections import defaultdict, Counter
from modules.parser import ALIAS_TO_SKILL, get_category

# ── Headers to mimic a real browser ──────────────────────────────────────────

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

# ── Target roles to scrape ────────────────────────────────────────────────────

TARGET_ROLES = [
    "data scientist",
    "data analyst",
    "machine learning engineer",
    "AI engineer",
]

# ── Scraper ───────────────────────────────────────────────────────────────────

def scrape_linkedin_jobs(role, max_jobs=25):
    """Scrape LinkedIn job listings for a given role."""
    role_query = role.replace(" ", "%20")
    url = (
        f"https://www.linkedin.com/jobs/search/"
        f"?keywords={role_query}&location=India"
        f"&f_TPR=r604800"  # last 7 days
    )

    print(f"  Fetching: {role}...")
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")

        # Get job cards
        cards = soup.find_all(
            "div",
            class_=re.compile("job-search-card|base-card")
        )

        jobs = []
        for card in cards[:max_jobs]:
            title_el = card.find(
                ["h3", "h4"],
                class_=re.compile("title|job-title")
            )
            desc_el = card.find(
                ["p", "div"],
                class_=re.compile("description|summary")
            )
            title = title_el.get_text(strip=True) if title_el else role
            desc = desc_el.get_text(strip=True) if desc_el else ""
            if title:
                jobs.append({"title": title, "description": desc})

        print(f"    Found {len(jobs)} listings")
        return jobs

    except Exception as e:
        print(f"    LinkedIn blocked or error: {e}")
        return []


def scrape_indeed_jobs(role, max_jobs=25):
    """Fallback: scrape Indeed India for job descriptions."""
    role_query = role.replace(" ", "+")
    url = f"https://in.indeed.com/jobs?q={role_query}&l=India"

    print(f"  Trying Indeed: {role}...")
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")

        jobs = []
        cards = soup.find_all("div", class_=re.compile("job_seen_beacon|jobsearch"))
        for card in cards[:max_jobs]:
            title_el = card.find(["h2", "h3", "a"])
            desc_el = card.find(["div", "ul"],
                                class_=re.compile("underShelfFooter|summary"))
            title = title_el.get_text(strip=True) if title_el else role
            desc = desc_el.get_text(strip=True) if desc_el else ""
            jobs.append({"title": title, "description": desc})

        print(f"    Found {len(cards)} listings")
        return jobs
    except Exception as e:
        print(f"    Indeed error: {e}")
        return []

# ── Skill extractor from JD text ──────────────────────────────────────────────

def extract_skills_from_jd(text):
    """Extract skills from a job description using the same taxonomy."""
    text_lower = text.lower()
    found = set()
    for alias, skill in ALIAS_TO_SKILL.items():
        pattern = r'\b' + re.escape(alias.strip()) + r'\b'
        if re.search(pattern, text_lower):
            found.add(skill)
    return list(found)

# ── Fallback: hardcoded realistic JD data ────────────────────────────────────
# Used when scraping is blocked — based on real Naukri/LinkedIn JDs

FALLBACK_JDS = {
    "data scientist": [
        "Python, machine learning, deep learning, SQL, statistics, pandas, numpy, scikit-learn, data visualization, matplotlib, TensorFlow or PyTorch, git, cloud computing AWS",
        "NLP, BERT, transformers, Python, machine learning algorithms, statistics, hypothesis testing, data analysis, SQL, big data, spark",
        "Python programming, supervised learning, unsupervised learning, regression, classification, clustering, neural networks, data visualization, plotly, tableau",
        "Machine learning, deep learning, computer vision, object detection, TensorFlow, keras, python, sql, git, linux, docker",
        "Data analysis, statistics, probability, python, pandas, numpy, matplotlib, seaborn, scikit-learn, machine learning, sql databases",
        "Python, NLP, text classification, sentiment analysis, word embeddings, bert, transformers, deep learning, sql, data engineering",
        "Machine learning, XGBoost, lightgbm, gradient boosting, feature engineering, pandas, python, sql, data visualization, git",
        "Deep learning, CNN, RNN, LSTM, computer vision, image classification, tensorflow, pytorch, python, sql, cloud computing",
    ],
    "data analyst": [
        "SQL, excel, python, data visualization, tableau, power bi, statistics, data analysis, pandas, numpy",
        "SQL, python, data analysis, statistical analysis, hypothesis testing, matplotlib, seaborn, dashboards, reporting",
        "Data visualization, power bi, tableau, SQL, excel, statistics, python, pandas, data analysis, business intelligence",
        "Python, SQL, data analysis, exploratory data analysis, pandas, numpy, matplotlib, statistics, databases, git",
        "SQL queries, python scripting, tableau dashboards, data visualization, statistical analysis, excel, data cleaning",
        "Data analytics, SQL, python, power bi, statistics, data visualization, pandas, business intelligence, reporting",
        "Python, data analysis, SQL, visualization, matplotlib, seaborn, statistics, hypothesis testing, data cleaning",
        "SQL, data analysis, python, tableau, power bi, statistics, excel, databases, data visualization, reporting",
    ],
    "machine learning engineer": [
        "Python, machine learning, deep learning, TensorFlow, PyTorch, scikit-learn, SQL, docker, kubernetes, git, cloud computing, AWS",
        "Machine learning, deep learning, python, neural networks, tensorflow, model deployment, docker, kubernetes, REST API, git",
        "Python, machine learning algorithms, deep learning, NLP, computer vision, tensorflow, pytorch, sql, cloud computing, devops",
        "Machine learning, python, scikit-learn, XGBoost, feature engineering, data pipelines, docker, git, linux, SQL",
        "Deep learning, CNN, transformers, NLP, python, pytorch, tensorflow, model optimization, docker, kubernetes, cloud",
        "Python, machine learning, TensorFlow, keras, data engineering, ETL, data pipelines, SQL, git, linux, docker",
        "ML engineering, python, model deployment, REST APIs, docker, kubernetes, machine learning, deep learning, SQL, git",
        "Machine learning, deep learning, python, tensorflow, pytorch, NLP, computer vision, cloud computing AWS, docker",
    ],
    "AI engineer": [
        "Python, machine learning, deep learning, generative AI, LLM, NLP, TensorFlow, PyTorch, cloud computing, docker, git",
        "Generative AI, LLM, GPT, python, NLP, deep learning, transformers, machine learning, cloud computing, REST API",
        "Python, AI, machine learning, deep learning, NLP, computer vision, tensorflow, pytorch, SQL, docker, kubernetes",
        "LLM, generative AI, python, NLP, transformers, BERT, GPT, machine learning, deep learning, cloud computing, git",
        "AI engineering, python, machine learning, deep learning, NLP, generative AI, docker, kubernetes, REST API, SQL",
        "Python, deep learning, generative AI, LLM fine-tuning, NLP, machine learning, cloud computing, AWS, docker, git",
        "Machine learning, AI, python, NLP, computer vision, deep learning, tensorflow, pytorch, SQL, git, linux",
        "Generative AI, LLM, python, NLP, transformers, machine learning, cloud, docker, REST API, SQL, data engineering",
    ]
}

def get_fallback_jds():
    """Return realistic JD data when scraping fails."""
    all_jds = []
    for role, descriptions in FALLBACK_JDS.items():
        for desc in descriptions:
            all_jds.append({
                "role": role,
                "description": desc,
                "skills": extract_skills_from_jd(desc)
            })
    return all_jds

# ── Main scrape function ──────────────────────────────────────────────────────

def scrape_jobs(use_fallback=False):
    """
    Main function — tries live scraping first,
    falls back to realistic hardcoded JD data if blocked.
    """
    all_jds = []

    if not use_fallback:
        print("\n[1/2] Attempting live scraping...")
        for role in TARGET_ROLES:
            jobs = scrape_linkedin_jobs(role, max_jobs=15)
            if not jobs:
                jobs = scrape_indeed_jobs(role, max_jobs=15)
            for job in jobs:
                skills = extract_skills_from_jd(
                    job["title"] + " " + job["description"]
                )
                all_jds.append({
                    "role": role,
                    "title": job["title"],
                    "description": job["description"],
                    "skills": skills
                })
            time.sleep(2)  # be polite

    if not all_jds:
        print("\n[1/2] Live scraping blocked — using realistic JD dataset...")
        all_jds = get_fallback_jds()

    print(f"\n[2/2] Analysing {len(all_jds)} job descriptions...")

    # Count skill frequency across all JDs
    skill_freq = Counter()
    skill_per_role = defaultdict(lambda: defaultdict(int))

    for jd in all_jds:
        for skill in jd["skills"]:
            skill_freq[skill] += 1
            skill_per_role[jd["role"]][skill] += 1

    # Build ranked output
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
        "roles_covered": list(FALLBACK_JDS.keys()),
        "skills_ranked": ranked,
        "skill_per_role": {
            role: dict(skills)
            for role, skills in skill_per_role.items()
        }
    }

    # Save
    with open("data/jd_skills.json", "w") as f:
        json.dump(result, f, indent=2)

    print(f"\n✅ Done! Top 10 in-demand skills:")
    for i, s in enumerate(ranked[:10], 1):
        print(f"  {i:2}. {s['skill']:<25} ({s['percentage']}% of JDs)")

    print("\nSaved to data/jd_skills.json")
    return result


if __name__ == "__main__":
    scrape_jobs(use_fallback=True)