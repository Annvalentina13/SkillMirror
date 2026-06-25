# 🪞 SkillMirror

SkillMirror is an AI-powered curriculum gap analysis platform that helps students understand how aligned their academic syllabus is with real-world industry requirements.

Instead of blindly following college curriculum and discovering skill gaps during placements, SkillMirror makes those gaps visible early.

---

# Why SkillMirror?

Students often ask:

* “Is my syllabus enough for placements?”
* “What am I missing?”
* “What should I learn outside college?”

SkillMirror answers that by comparing:

**College syllabus** vs **Industry job descriptions**

and generating a personalized skill roadmap.

---

# Current Build (Till Now)

We have completed the first working MVP of SkillMirror.

---

# Workflow

```text
Upload syllabus PDF
        ↓
Extract syllabus skills
        ↓
Scrape industry job descriptions
        ↓
Extract industry-required skills
        ↓
Compare both datasets
        ↓
Generate skill gap report
        ↓
Visualize on dashboard
```

---

# Modules Completed

## 1. Syllabus Parser (`parser.py`)

Built using:

* pdfplumber
* KeyBERT
* NLTK
* Regex

### What it does:

* Reads syllabus PDFs
* Extracts text
* Identifies technical concepts
* Maps them into skill categories
* Generates ranked skill data

### Output:

`data/syllabus_skills.json`

### Current result:

Extracted **38 skills**

Top skills found:

* Machine Learning
* Algorithms
* Deep Learning
* Statistics
* Big Data

---

## 2. Job Description Scraper (`scraper.py`)

Built using:

* Requests
* BeautifulSoup

### What it does:

* Scrapes LinkedIn job listings
* Uses Indeed as fallback
* Uses internal fallback dataset when blocked
* Extracts demanded skills

### Roles covered:

* Data Scientist
* Data Analyst
* Machine Learning Engineer
* AI Engineer

### Output:

`data/jd_skills.json`

### Current top industry demand:

| Skill            | Demand |
| ---------------- | -----: |
| Python           |   100% |
| SQL              |    75% |
| Machine Learning |  71.9% |
| Deep Learning    |  56.2% |
| Git              |  40.6% |

---

## 3. Gap Analysis Engine (`gap_engine.py`)

### What it does:

* Compares syllabus skills against JD skills
* Finds overlap
* Finds missing skills
* Calculates coverage score
* Builds learning roadmap

### Output:

`data/gap_analysis.json`

---

# Current Analysis Result (SRM AI Syllabus)

| Metric          | Value |
| --------------- | ----: |
| Syllabus Skills |    38 |
| Industry Skills |    27 |
| Covered         |    26 |
| Missing         |     1 |
| Coverage Score  | 96.3% |
| Gap Severity    |  5.2% |

### Missing Skill:

❌ Git

This was the major insight found.

---

## 4. Dashboard (`app.py`)

Built using:

* Streamlit
* Plotly
* Pandas

### Features:

* Upload syllabus
* View coverage score
* Skills heatmap
* Missing skills roadmap
* Covered skills overview
* Category-wise breakdown

---

# Project Structure

```text
skillmirror/
│── app.py
│
├── modules/
│   ├── parser.py
│   ├── scraper.py
│   ├── gap_engine.py
│   └── __init__.py
│
├── data/
│   ├── syllabus_skills.json
│   ├── jd_skills.json
│   └── gap_analysis.json
│
├── outputs/
└── venv/
```

---

# Tech Stack

* Python
* pdfplumber
* KeyBERT
* NLTK
* Requests
* BeautifulSoup
* Streamlit
* Plotly
* Pandas

---

# Challenges Faced

* LinkedIn blocking automated scraping
* Handling noisy extracted keywords
* Normalizing syllabus terminology
* Building reliable skill taxonomy

---

# Current Status

✅ Functional MVP completed

Working features:

* Syllabus skill extraction
* Job market skill extraction
* Gap detection
* Dashboard visualization

Current test completed successfully on SRM AI syllabus.
