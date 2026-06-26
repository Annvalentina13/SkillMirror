"""
SkillMirror — Syllabus PDF Parser
Module 1 of 4
"""

import pdfplumber
import re
import json
from collections import defaultdict, Counter
from keybert import KeyBERT
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import stopwords

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('punkt_tab', quiet=True)

# ── Skill Taxonomy ────────────────────────────────────────────────────────────

SKILL_TAXONOMY = {
    "Python":           ["python", "python3"],
    "Java":             ["java", "jdk", "jvm"],
    "C":                [" c programming", "c language"],
    "C++":              ["c++", "cpp"],
    "JavaScript":       ["javascript", "js", "nodejs"],
    "SQL":              ["sql", "mysql", "postgresql", "sqlite", "nosql"],
    "R":                ["r programming", "rlang"],
    "MATLAB":           ["matlab"],
    "Machine Learning": ["machine learning", "supervised learning",
                         "unsupervised learning", "classification",
                         "regression", "clustering"],
    "Deep Learning":    ["deep learning", "neural network", "neural networks",
                         "ann", "cnn", "rnn", "lstm", "backpropagation"],
    "NLP":              ["natural language processing", "nlp", "text mining",
                         "sentiment analysis", "word embedding", "bert",
                         "tokenization", "text classification"],
    "Computer Vision":  ["computer vision", "image processing",
                         "object detection", "image classification", "opencv"],
    "Generative AI":    ["generative ai", "llm", "large language model",
                         "gpt", "diffusion model", "gan"],
    "Data Analysis":    ["data analysis", "data analytics",
                         "exploratory data analysis", "eda"],
    "Statistics":       ["statistics", "probability", "hypothesis testing",
                         "bayesian", "distributions", "correlation",
                         "p-value", "confidence interval"],
    "Data Visualization": ["data visualization", "matplotlib", "seaborn",
                           "plotly", "tableau", "power bi", "dashboards"],
    "Big Data":         ["big data", "hadoop", "spark", "pyspark",
                         "kafka", "mapreduce"],
    "Data Engineering": ["data engineering", "etl", "data pipeline",
                         "data warehouse", "airflow"],
    "TensorFlow":       ["tensorflow", "keras"],
    "PyTorch":          ["pytorch", "torch"],
    "Scikit-learn":     ["scikit-learn", "sklearn"],
    "Pandas":           ["pandas", "dataframe"],
    "NumPy":            ["numpy"],
    "XGBoost":          ["xgboost", "gradient boosting", "lightgbm"],
    "Databases":        ["database", "dbms", "rdbms", "mongodb", "redis"],
    "Cloud Computing":  ["cloud computing", "aws", "azure", "gcp",
                         "google cloud", "amazon web services"],
    "Docker":           ["docker", "containerization"],
    "Kubernetes":       ["kubernetes", "k8s"],
    "DevOps":           ["devops", "ci/cd", "continuous integration",
                         "jenkins"],
    "Data Structures":  ["data structures", "arrays", "linked list",
                         "trees", "graphs", "hash table", "stack", "queue"],
    "Algorithms":       ["algorithms", "sorting", "searching",
                         "dynamic programming", "complexity", "big o"],
    "OOP":              ["object oriented", "oop", "encapsulation",
                         "inheritance", "polymorphism"],
    "Web Development":  ["web development", "html", "css", "django",
                         "flask", "fastapi", "rest api"],
    "Git":              ["git", "github", "version control"],
    "Linux":            ["linux", "unix", "bash", "shell scripting"],
    "Operating Systems":["operating systems", "process management",
                         "memory management", "scheduling", "deadlock"],
    "Computer Networks":["computer networks", "networking", "tcp/ip",
                         "osi model", "protocols", "routing"],
    "Cryptography":     ["cryptography", "encryption", "decryption",
                         "ssl", "tls", "hashing"],
    "Linear Algebra":   ["linear algebra", "matrix", "vectors",
                         "eigenvalues", "determinant"],
    "Calculus":         ["calculus", "differentiation", "integration",
                         "gradient", "partial derivatives"],
    "Discrete Maths":   ["discrete mathematics", "discrete maths",
                         "set theory", "graph theory", "boolean algebra"],
    # ECE & Embedded
    "Embedded Systems": ["embedded systems", "microcontrollers", "firmware",
                         "arduino", "raspberry pi", "rtos", "arm cortex"],
    "VLSI":             ["vlsi", "verilog", "vhdl", "fpga", "digital circuits",
                         "semiconductor"],
    "IoT":              ["iot", "internet of things", "mqtt", "sensors",
                         "wireless protocols"],
    "Signal Processing":["signal processing", "dsp", "communications",
                         "wireless", "fourier"],
    "MATLAB":           ["matlab"],

    # Mechanical
    "CAD":              ["cad", "solidworks", "autocad", "catia", "creo"],
    "FEA":              ["fea", "ansys", "finite element", "simulation"],
    "Manufacturing":    ["manufacturing", "lean manufacturing", "six sigma",
                         "quality control", "cnc"],
    "Thermodynamics":   ["thermodynamics", "thermal analysis", "heat transfer",
                         "fluid mechanics"],

    # Civil
    "Structural Analysis": ["structural analysis", "staad pro", "etabs",
                            "structural design", "concrete", "steel design"],
    "Surveying":        ["surveying", "gis", "geographic information",
                         "remote sensing"],
    "Construction Mgmt":["construction management", "project management",
                         "site engineer", "quantity surveying"],

    # Cybersecurity
    "Network Security": ["network security", "firewalls", "network protocols",
                         "tcp/ip", "intrusion detection"],
    "Cryptography":     ["cryptography", "encryption", "decryption",
                         "ssl", "tls", "hashing", "public key"],
    "Penetration Testing": ["penetration testing", "ethical hacking",
                            "vulnerability", "owasp", "exploit"],
    "SIEM":             ["siem", "soc", "threat detection", "incident response",
                         "threat intelligence"],
    # Finance & MBA
    "Financial Modeling": ["financial modeling", "dcf", "lbo", "valuation",
                           "forecasting", "budgeting", "financial analysis"],
    "Excel":              ["excel", "vba", "spreadsheet", "pivot table",
                           "vlookup", "power bi", "tableau"],
    "Accounting":         ["accounting", "financial statements", "balance sheet",
                           "income statement", "m&a", "investment banking"],
    "Business Analysis":  ["business analysis", "requirements gathering",
                           "stakeholder management", "agile", "scrum",
                           "product management", "roadmap", "user research"],

    # Medical & Healthcare
    "Clinical Research":  ["clinical research", "clinical trials", "medical research",
                           "clinical data", "medical coding", "health informatics"],
    "Medical Statistics": ["spss", "sas", "r statistics", "biostatistics",
                           "statistical analysis", "clinical data analysis"],
    "Healthcare Mgmt":    ["healthcare management", "hospital administration",
                           "health informatics", "healthcare analytics"],

    # Law
    "Legal Research":     ["legal research", "case law", "legal analysis",
                           "legal writing", "jurisprudence"],
    "Contract Law":       ["contract drafting", "contract review",
                           "contract management", "legal drafting"],
    "Compliance":         ["compliance", "regulatory compliance",
                           "corporate law", "intellectual property",
                           "patent", "regulatory"],

    # Design & UX
    "Figma":              ["figma", "adobe xd", "sketch", "prototyping",
                           "wireframing", "mockup"],
    "UI Design":          ["ui design", "user interface", "visual design",
                           "typography", "branding", "graphic design"],
    "UX Research":        ["ux research", "user research", "usability testing",
                           "user experience", "interaction design"],
    "Adobe Suite":        ["adobe photoshop", "photoshop", "illustrator",
                           "indesign", "adobe suite", "motion design"],

    # Media & Marketing
    "SEO":                ["seo", "search engine optimization", "sem",
                           "search engine marketing", "keyword research",
                           "link building"],
    "Google Analytics":   ["google analytics", "web analytics", "ga4",
                           "google ads", "digital analytics"],
    "Social Media":       ["social media", "instagram", "facebook", "twitter",
                           "linkedin marketing", "content creation",
                           "social media management"],
    "Content Marketing":  ["content marketing", "content strategy",
                           "copywriting", "content writing", "blogging"],
    "Digital Marketing":  ["digital marketing", "online marketing",
                           "email marketing", "marketing analytics",
                           "growth hacking"],
}

# Reverse map: alias → canonical skill
ALIAS_TO_SKILL = {}
for skill, aliases in SKILL_TAXONOMY.items():
    for alias in aliases:
        ALIAS_TO_SKILL[alias.lower().strip()] = skill

# ── Category Map ──────────────────────────────────────────────────────────────

SKILL_CATEGORIES = {
    "Programming":    ["Python", "Java", "C", "C++", "JavaScript",
                       "SQL", "R", "MATLAB"],
    "AI / ML":        ["Machine Learning", "Deep Learning", "NLP",
                       "Computer Vision", "Generative AI",
                       "TensorFlow", "PyTorch", "Scikit-learn", "XGBoost"],
    "Data":           ["Data Analysis", "Statistics", "Data Visualization",
                       "Big Data", "Data Engineering", "Pandas", "NumPy"],
    "Cloud & DevOps": ["Cloud Computing", "Docker", "Kubernetes",
                       "DevOps", "Git", "Linux"],
    "Software Eng":   ["Data Structures", "Algorithms", "OOP",
                       "Web Development", "Databases"],
    "Core CS":        ["Operating Systems", "Computer Networks",
                       "Cryptography"],
    "Mathematics":    ["Linear Algebra", "Calculus", "Discrete Maths"],
    "ECE & Embedded": ["Embedded Systems", "VLSI", "IoT",
                       "Signal Processing", "MATLAB"],
    "Mechanical":     ["CAD", "FEA", "Manufacturing", "Thermodynamics"],
    "Civil":          ["Structural Analysis", "Surveying", "Construction Mgmt"],
    "Cybersecurity":  ["Network Security", "Cryptography",
                       "Penetration Testing", "SIEM"],
    "Finance & MBA":  ["Financial Modeling", "Excel", "Accounting",
                       "Business Analysis"],
    "Medical":        ["Clinical Research", "Medical Statistics",
                       "Healthcare Mgmt"],
    "Law":            ["Legal Research", "Contract Law", "Compliance"],
    "Design & UX":    ["Figma", "UI Design", "UX Research", "Adobe Suite"],
    "Marketing":      ["SEO", "Google Analytics", "Social Media",
                       "Content Marketing", "Digital Marketing"],
}


def get_category(skill):
    for cat, skills in SKILL_CATEGORIES.items():
        if skill in skills:
            return cat
    return "Other"

# ── PDF Extraction ────────────────────────────────────────────────────────────

def extract_text(pdf_path):
    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                pages.append(text)
    full_text = "\n".join(pages)
    # Clean up
    full_text = re.sub(r'[ \t]+', ' ', full_text)
    full_text = re.sub(r'\n{3,}', '\n\n', full_text)
    return full_text

# ── Skill Extraction ──────────────────────────────────────────────────────────

def extract_skills(text):
    text_lower = text.lower()
    found = defaultdict(int)

    for alias, skill in ALIAS_TO_SKILL.items():
        pattern = r'\b' + re.escape(alias.strip()) + r'\b'
        matches = re.findall(pattern, text_lower)
        if matches:
            found[skill] += len(matches)

    # KeyBERT for novel keywords
    novel = []
    try:
        kw_model = KeyBERT()
        keywords = kw_model.extract_keywords(
            text,
            keyphrase_ngram_range=(1, 2),
            stop_words='english',
            top_n=20
        )
        known = {s.lower() for s in found.keys()}
        for kw, score in keywords:
            if score > 0.3 and kw.lower() not in known:
                if kw.lower() not in ALIAS_TO_SKILL:
                    novel.append(kw)
    except:
        pass

    return found, novel

# ── Main Parser ───────────────────────────────────────────────────────────────

def parse_syllabus(pdf_path, course_name="Syllabus"):
    print(f"\n[1/3] Reading PDF: {pdf_path}")
    text = extract_text(pdf_path)

    if not text.strip():
        return {"error": "No text found in PDF"}

    print(f"[2/3] Extracting skills...")
    found_skills, novel = extract_skills(text)

    print(f"[3/3] Building output...")

    # Rank skills
    ranked = []
    for skill, count in sorted(found_skills.items(),
                                key=lambda x: x[1], reverse=True):
        ranked.append({
            "skill": skill,
            "mentions": count,
            "category": get_category(skill)
        })

    # Group by category
    by_category = defaultdict(list)
    for item in ranked:
        by_category[item["category"]].append(item)

    result = {
        "course_name": course_name,
        "total_skills": len(ranked),
        "skills_ranked": ranked,
        "skills_by_category": dict(by_category),
        "novel_keywords": novel[:10]
    }

    # Save JSON
    out_path = "data/syllabus_skills.json"
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)

    return result


# ── Run it ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python modules/parser.py <pdf_path> [course_name]")
        sys.exit(1)

    pdf = sys.argv[1]
    name = sys.argv[2] if len(sys.argv) > 2 else "My Syllabus"

    result = parse_syllabus(pdf, name)

    if "error" in result:
        print("Error:", result["error"])
    else:
        print(f"\n✅ Done! Found {result['total_skills']} skills\n")
        print("Top 10 skills:")
        for i, s in enumerate(result["skills_ranked"][:10], 1):
            print(f"  {i:2}. {s['skill']:<25} ({s['mentions']} mentions)")
        print(f"\nNovel keywords: {result['novel_keywords']}")
        print(f"\nSaved to data/syllabus_skills.json")