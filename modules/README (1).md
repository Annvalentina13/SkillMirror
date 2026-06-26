# 🪞 SkillMirror

> **Know exactly what your syllabus is missing — before your first interview.**

SkillMirror is a career gap analyser that parses any college syllabus PDF, compares it against real job descriptions, and generates a personalised week-by-week learning roadmap for every missing skill.

Built by Ann Valentina — SRM Institute of Science and Technology, Computational Intelligence.

---

## 🎯 What it does

Upload your syllabus → Pick your target role → Get your gap score + roadmap in seconds.

- **Syllabus parser** — extracts skills from any PDF using pdfplumber and KeyBERT
- **JD analyser** — compares against 10 real job descriptions per role
- **Gap engine** — scores your syllabus coverage against industry demand
- **Roadmap generator** — week-by-week learning plan with free resources and a project to build for every missing skill
- **12 domains** — works for any student, not just engineering

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
| 🏥 Medical & Healthcare | Clinical Data Analyst, Healthcare Analyst, Medical Researcher |
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
│   app.py                  # Streamlit dashboard
│   requirements.txt        # Dependencies
│   README.md
│
├───modules/
│       parser.py           # PDF parser + skill taxonomy
│       scraper.py          # JD datasets (12 domains)
│       gap_engine.py       # Gap analysis engine
│       roadmap.py          # Personalised roadmap generator
│       __init__.py
│
└───data/
        syllabus_skills.json    # Parsed syllabus output
        jd_skills.json          # JD analysis output
        gap_analysis.json       # Gap report
```

---

## 🧠 How it works

```
Syllabus PDF
     ↓
pdfplumber extracts text
     ↓
Skill taxonomy (268 aliases → 80+ canonical skills) matches skills
KeyBERT extracts novel keywords not in taxonomy
     ↓
syllabus_skills.json

JD Dataset (10 JDs per role group)
     ↓
Same taxonomy extracts required skills
Frequency ranked across all JDs
     ↓
jd_skills.json

Gap Engine
     ↓
Compares syllabus skills vs JD skills
Coverage score = covered / total industry skills × 100
Roadmap = missing skills sorted by industry demand
     ↓
gap_analysis.json

Roadmap Generator
     ↓
For each gap skill → pulls from hand-curated roadmap database
Role-specific why_it_matters overrides applied
Weekly plan + free resources + project to build
```

---

## 📊 Sample Results

**SRM Computational Intelligence → Data & AI roles**
- Coverage Score: **96.3%**
- Skills Covered: 26
- Skills Missing: 1 (Git — appears in 40.6% of JDs)

**SRM CSBS → Data & AI roles**
- Coverage Score: **88.9%**
- Skills Covered: 24
- Skills Missing: 3 (Kubernetes, Data Engineering, XGBoost)

**SRM ECE → ECE & Embedded roles**
- Coverage Score: **100%**
- Skills Covered: 9
- Skills Missing: 0

---

## 🛠️ Tech Stack

| Layer | Tech |
|---|---|
| Frontend | Streamlit + Plotly |
| PDF Parsing | pdfplumber |
| Keyword Extraction | KeyBERT |
| Skill Matching | Custom taxonomy + regex |
| Gap Analysis | Python + pandas |
| Visualisation | Plotly Express + Graph Objects |

---

## 🗺️ Roadmap

- [x] Phase 1 — Core product (parser, scraper, gap engine, dashboard)
- [x] Phase 2 — Multi-role support (7 engineering domains)
- [x] Phase 3 — Personalised roadmap generator
- [x] Phase 4 — Beyond engineering (12 domains total)
- [ ] Phase 5 — College comparison (SRM vs VIT vs Anna Uni)
- [ ] Phase 6 — Resume upload mode
- [ ] Phase 7 — Deploy on Streamlit Cloud

---

## 🤝 Contributing

Pull requests welcome. For major changes, open an issue first.

---

## 📄 License

MIT

---

Built with 🖤 by [Ann Valentina](https://github.com/Annvalentina13)
