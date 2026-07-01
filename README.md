# 🪞 SkillMirror

> **Know exactly what your syllabus is missing — before your first interview.**

SkillMirror is a career gap analyser that parses any college syllabus PDF, compares it against real job descriptions, and generates a personalised week-by-week learning roadmap for every missing skill. It also compares colleges side by side and analyses resumes for role fit.

Built by Ann Valentina — SRM Institute of Science and Technology, Computational Intelligence.

---

## 🎯 What it does

**Three modes, one tool:**

- **🔍 Analyse** — Upload your syllabus PDF, pick a target role, get your coverage score, gap heatmap, and a detailed week-by-week roadmap for every missing skill
- **🏫 Compare** — Upload two college syllabuses for the same role and see a head-to-head comparison: who covers more, common gaps, and unique gaps
- **📄 Resume** — Upload your resume PDF and get a role-fit grade (A–F), a personal skills gap score, prioritised "what to add" recommendations, and an optional resume-vs-syllabus education utilisation check

**Under the hood:**

- Syllabus parser using pdfplumber + KeyBERT for skill extraction
- A 350+ alias skill taxonomy mapped to 90+ canonical skills across 16 categories
- JD datasets across 12 career domains
- A weighted gap-scoring engine
- A hand-curated roadmap database with real, working resource links — no AI API required
- Light/dark theme toggle with a custom purple-blue gradient design system

---

## 🗂️ Supported Domains

| Domain | Roles Covered |
|---|---|
| 📊 Data & AI | Data Scientist, Data Analyst, ML Engineer, AI Engineer |
| 💻 Software Engineering | Software Engineer, Backend Dev, Full Stack Dev, Frontend Dev |
| ☁️ Cloud & DevOps | DevOps Engineer, Cloud Engineer, SRE, Platform Engineer |
| 🔐 Cybersecurity | Security Analyst, Security Engineer, Penetration Tester, SOC Analyst |
| ⚡ ECE & Embedded | Embedded Engineer, VLSI Engineer, IoT Engineer, Signal Processing |
| ⚙️ Mechanical | Design Engineer, CAD Engineer, Manufacturing Engineer, Automotive |
| 🏗️ Civil | Structural Engineer, Site Engineer, Urban Planner, Environmental |
| 💰 Finance & MBA | Financial Analyst, Investment Banking, Business Analyst, Product Manager |
| 🏥 Medical & Healthcare | Clinical Data Analyst, Healthcare Analyst, Medical Researcher, Hospital Admin |
| ⚖️ Law | Corporate Lawyer, Legal Analyst, Compliance Officer, Legal Researcher |
| 🎨 Design & UX | UI/UX Designer, Product Designer, Graphic Designer, Visual Designer |
| 📢 Media & Marketing | Digital Marketing, Content Strategist, Social Media Manager, SEO Analyst |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9 or higher
- pip

### Installation

```bash
# Clone the repo
git clone https://github.com/Annvalentina13/SkillMirror.git
cd SkillMirror

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Run the app

```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## 📁 Project Structure

```
skillmirror/
│   app.py                  # Streamlit dashboard — 3 tabs, theme toggle
│   requirements.txt        # Dependencies
│   .env                    # API keys (gitignored — not required for core app)
│   .gitignore
│   README.md
│
├───modules/
│       parser.py           # PDF parser + 350+ alias skill taxonomy
│       scraper.py          # JD datasets across 12 role groups
│       gap_engine.py        # Gap analysis engine
│       roadmap.py          # Hand-curated roadmap database (no API needed)
│       compare.py          # College-vs-college comparison engine
│       resume.py           # Resume parser, scorer, and gap analyser
│       __init__.py
│
└───data/
        syllabus_skills.json    # Parsed syllabus output
        jd_skills.json          # JD analysis output
        gap_analysis.json       # Gap report
        comparison.json         # College comparison output
        resume_analysis.json    # Resume analysis output
```

---

## 🧠 How it works

```
SYLLABUS ANALYSER
Syllabus PDF → pdfplumber extracts text
            → Taxonomy match (350+ aliases) + KeyBERT novel keywords
            → syllabus_skills.json

JD Dataset (10 JDs per role group, 12 role groups)
            → Same taxonomy extracts required skills
            → Frequency ranked across all JDs
            → jd_skills.json

Gap Engine  → Compares syllabus skills vs JD skills
            → Coverage score = covered / total industry skills × 100
            → Roadmap = missing skills sorted by industry demand
            → gap_analysis.json

Roadmap Generator → For each gap skill, pulls from a hand-curated database
                  → Role-specific "why it matters" overrides applied
                  → Weekly plan + real free resources + project to build
                  → No API calls, works offline, zero cost

COLLEGE COMPARISON
Two syllabuses → parsed independently → gap-analysed against the same role
              → Winner determined by coverage score
              → Common gaps (both missing) + unique gaps (one missing, other covers)
              → comparison.json

RESUME ANALYSER
Resume PDF → Same taxonomy extracts skills from resume text
          → Resume vs JD: weighted role-fit score (0–100) + letter grade (A–F)
          → Quick wins (high-demand gaps) vs nice-to-haves (low-demand gaps)
          → Optional: Resume vs Syllabus → education utilisation %
          → resume_analysis.json
```

---

## 📊 Sample Results

**SRM Computational Intelligence → Data & AI roles**
- Coverage Score: **96.3%**
- Skills Covered: 26
- Skills Missing: 1 (Git — appears in 40.6% of JDs)

**SRM CSBS → Data & AI roles**
- Coverage Score: **92.0%**
- Skills Covered: 23
- Skills Missing: 2 (Data Engineering, XGBoost)

**SRM ECE → ECE & Embedded roles**
- Coverage Score: **100%**
- Skills Covered: 9
- Skills Missing: 0

**SRM CI → Finance & MBA roles**
- Coverage Score: **90.0%**
- Skills Covered: 9
- Skills Missing: 1 (Python — appears in 60.0% of JDs)

**College Comparison — SRM AI vs SRM CSBS (Data & AI roles)**
- Winner: SRM AI, 96.0% vs 92.0% — 4.0% ahead
- Common gaps: none
- SRM AI unique gap: Git
- SRM CSBS unique gaps: Data Engineering, XGBoost

---

## 🛠️ Tech Stack

| Layer | Tech |
|---|---|
| Frontend | Streamlit + Plotly + custom CSS design system |
| PDF Parsing | pdfplumber |
| Keyword Extraction | KeyBERT |
| Skill Matching | Custom taxonomy (350+ aliases) + regex |
| Gap Analysis | Python + pandas |
| Visualisation | Plotly Express + Graph Objects |
| Theming | Dark/light toggle with purple-blue gradient tokens |

---

## 🗺️ Roadmap

- [x] Phase 1 — Core product (parser, scraper, gap engine, dashboard)
- [x] Phase 2 — Multi-role support (7 engineering domains)
- [x] Phase 3 — Personalised roadmap generator (no API, hand-curated)
- [x] Phase 4 — Beyond engineering (12 domains total)
- [x] Phase 5 — College comparison (head-to-head, common/unique gaps)
- [x] Phase 6 — Resume upload mode (role-fit score + resume-vs-syllabus)
- [x] Phase 7 — Premium UI redesign (dark/light theme, tab navigation)
- [x] Phase 8 — Deploy on Streamlit Cloud

---

## 🤝 Contributing

Pull requests welcome. For major changes, open an issue first.

---

## 📄 License

MIT

---

Built with 🖤 by [Ann Valentina](https://github.com/Annvalentina13)
