"""
SkillMirror — Streamlit Dashboard
v3 — Premium redesign, fixed layout
"""

import streamlit as st
import json
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from modules.parser import parse_syllabus
from modules.scraper import scrape_jobs
from modules.gap_engine import analyse_gap
from modules.roadmap import generate_skill_roadmap
from modules.compare import compare_colleges
from modules.resume import analyse_resume

st.set_page_config(
    page_title="SkillMirror",
    page_icon="🪞",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Theme state ───────────────────────────────────────────────────────────────
if "theme" not in st.session_state:
    st.session_state.theme = "dark"
if "mode" not in st.session_state:
    st.session_state.mode = "analyse"

is_dark = st.session_state.theme == "dark"

# ── Design tokens ─────────────────────────────────────────────────────────────
if is_dark:
    BG     = "#0A0A0F"
    BG2    = "#12121A"
    BG3    = "#1A1A2E"
    BORDER = "#2D2D4A"
    TEXT   = "#F0F0FF"
    TEXT2  = "#9090B0"
    TEXT3  = "#5A5A7A"
else:
    BG     = "#F4F4FF"
    BG2    = "#FFFFFF"
    BG3    = "#EEEEFF"
    BORDER = "#D0D0E8"
    TEXT   = "#0A0A1F"
    TEXT2  = "#4A4A6A"
    TEXT3  = "#8A8AAA"

PURPLE = "#6C47FF"
BLUE   = "#3B82F6"
GREEN  = "#10B981"
RED    = "#EF4444"
AMBER  = "#F59E0B"
GRAD   = f"linear-gradient(135deg, {PURPLE}, {BLUE})"

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

  html, body, .stApp {{
    background: {BG} !important;
    font-family: 'Inter', sans-serif !important;
  }}
  .block-container {{
    padding: 2rem 2.5rem !important;
    max-width: 100% !important;
  }}
  #MainMenu, footer, header {{ visibility: hidden; }}

  [data-testid="stSidebar"] {{
    background: {BG2} !important;
    border-right: 1px solid {BORDER} !important;
    min-width: 80px !important;
    max-width: 240px !important;
  }}
  [data-testid="stSidebar"] > div {{
    padding: 1.5rem 0.8rem !important;
  }}

  .nav-btn {{
    display: flex;
    align-items: center;
    gap: 10px;
    width: 100%;
    padding: 10px 12px;
    border-radius: 10px;
    border: none;
    background: transparent;
    color: {TEXT2};
    font-size: 13px;
    font-weight: 500;
    font-family: 'Inter', sans-serif;
    cursor: pointer;
    transition: all 0.15s;
    margin-bottom: 4px;
    text-align: left;
  }}
  .nav-btn:hover {{
    background: {BG3};
    color: {TEXT};
  }}
  .nav-btn.active {{
    background: {"#6C47FF18" if is_dark else "#6C47FF12"};
    color: {PURPLE};
    border-left: 3px solid {PURPLE};
  }}
  .nav-icon {{ font-size: 18px; }}

  .sm-logo {{
    width: 40px; height: 40px;
    background: {GRAD};
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 20px;
    margin-bottom: 24px;
    margin-left: 4px;
  }}

  .sm-hero {{
    background: {GRAD};
    border-radius: 20px;
    padding: 28px 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 20px;
  }}
  .sm-hero-score {{
    font-size: 60px;
    font-weight: 700;
    color: #fff;
    letter-spacing: -3px;
    font-variant-numeric: tabular-nums;
    line-height: 1;
  }}
  .sm-hero-label {{
    font-size: 11px;
    color: rgba(255,255,255,0.6);
    text-transform: uppercase;
    letter-spacing: .08em;
    margin-top: 6px;
  }}
  .sm-hero-right {{ text-align: right; }}
  .sm-hero-role {{
    font-size: 11px;
    color: rgba(255,255,255,0.5);
    margin-bottom: 8px;
    text-transform: uppercase;
    letter-spacing: .06em;
  }}
  .sm-hero-badge {{
    display: inline-block;
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 12px;
    color: #fff;
  }}
  .sm-grade {{
    font-size: 56px;
    font-weight: 800;
    letter-spacing: -2px;
    color: #ffffff;
    line-height: 1;
  }}

  .sm-stats {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin-bottom: 20px;
  }}
  .sm-stat {{
    background: {BG2};
    border: 1px solid {BORDER};
    border-radius: 14px;
    padding: 18px 20px;
  }}
  .sm-stat-val {{
    font-size: 28px;
    font-weight: 700;
    font-variant-numeric: tabular-nums;
    letter-spacing: -1px;
    color: {TEXT};
  }}
  .sm-stat-lbl {{
    font-size: 11px;
    color: {TEXT3};
    text-transform: uppercase;
    letter-spacing: .07em;
    margin-top: 4px;
  }}

  .sm-card {{
    background: {BG2};
    border: 1px solid {BORDER};
    border-radius: 16px;
    padding: 22px;
    margin-bottom: 16px;
  }}
  .sm-card-title {{
    font-size: 15px;
    font-weight: 600;
    color: {TEXT};
    margin-bottom: 4px;
  }}
  .sm-card-sub {{
    font-size: 12px;
    color: {TEXT3};
    margin-bottom: 16px;
  }}

  .sm-gap {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 9px 13px;
    border-radius: 9px;
    background: {"#EF444412" if is_dark else "#FEF2F2"};
    border: 1px solid {"#EF444430" if is_dark else "#FECACA"};
    color: {RED};
    font-size: 13px;
    margin: 4px 0;
  }}
  .sm-gap-pct {{
    font-size: 11px;
    font-weight: 600;
    background: {"#EF444422" if is_dark else "#FEE2E2"};
    padding: 2px 8px;
    border-radius: 5px;
  }}
  .sm-ok {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 9px 13px;
    border-radius: 9px;
    background: {"#10B98112" if is_dark else "#F0FDF4"};
    border: 1px solid {"#10B98130" if is_dark else "#BBF7D0"};
    color: {GREEN};
    font-size: 13px;
    margin: 4px 0;
  }}
  .sm-ok-pct {{
    font-size: 11px;
    font-weight: 600;
    background: {"#10B98122" if is_dark else "#DCFCE7"};
    padding: 2px 8px;
    border-radius: 5px;
  }}
  .sm-amber {{
    display: flex;
    justify-content: space-between;
    padding: 8px 13px;
    border-radius: 9px;
    background: {"#F59E0B12" if is_dark else "#FFFBEB"};
    border: 1px solid {"#F59E0B30" if is_dark else "#FDE68A"};
    color: {AMBER};
    font-size: 12px;
    margin: 4px 0;
  }}

  .sm-week {{
    background: {BG3};
    border: 1px solid {BORDER};
    border-left: 3px solid {PURPLE};
    border-radius: 9px;
    padding: 11px 14px;
    margin: 5px 0;
  }}
  .sm-week-t {{ font-size: 13px; font-weight: 500; color: {TEXT}; }}
  .sm-week-g {{ font-size: 12px; color: {GREEN}; margin-top: 3px; }}
  .sm-project {{
    background: {"#10B98112" if is_dark else "#F0FDF4"};
    border: 1px solid {"#10B98130" if is_dark else "#BBF7D0"};
    border-radius: 9px;
    padding: 13px;
    margin: 7px 0;
  }}
  .sm-tip {{
    background: {BG3};
    border: 1px solid {BORDER};
    border-radius: 7px;
    padding: 7px 13px;
    font-size: 12px;
    color: {TEXT2};
    margin: 3px 0;
  }}

  .sm-chip {{
    display: inline-block;
    background: {BG3};
    border: 1px solid {BORDER};
    border-radius: 20px;
    padding: 3px 11px;
    font-size: 12px;
    color: {TEXT2};
    margin: 2px;
  }}

  .sm-winner {{
    background: {GRAD};
    border-radius: 16px;
    padding: 22px;
    text-align: center;
    margin-bottom: 18px;
  }}
  .sm-winner-lbl {{
    font-size: 11px;
    color: rgba(255,255,255,0.55);
    text-transform: uppercase;
    letter-spacing: .08em;
    margin-bottom: 6px;
  }}
  .sm-winner-name {{
    font-size: 22px;
    font-weight: 700;
    color: #fff;
    margin-bottom: 4px;
  }}
  .sm-winner-sub {{ font-size: 13px; color: rgba(255,255,255,0.6); }}
  .sm-ccard {{
    background: {BG2};
    border: 1px solid {BORDER};
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 10px;
  }}
  .sm-ccard.win {{ border-color: {PURPLE}; background: {"#6C47FF0A" if is_dark else "#6C47FF06"}; }}
  .sm-ccard-name {{ font-size: 15px; font-weight: 600; color: {TEXT}; margin-bottom: 12px; }}

  .sm-empty {{
    background: {BG2};
    border: 2px dashed {BORDER};
    border-radius: 20px;
    padding: 56px 40px;
    text-align: center;
    margin-top: 20px;
  }}
  .sm-empty-icon {{ font-size: 38px; margin-bottom: 14px; }}
  .sm-empty-title {{ font-size: 18px; font-weight: 600; color: {TEXT}; margin-bottom: 8px; }}
  .sm-empty-sub {{ font-size: 13px; color: {TEXT3}; line-height: 1.65; }}

  .sm-page-title {{
    font-size: 24px;
    font-weight: 700;
    color: {TEXT};
    letter-spacing: -0.5px;
    margin-bottom: 4px;
  }}
  .sm-page-sub {{
    font-size: 14px;
    color: {TEXT2};
    margin-bottom: 24px;
  }}

  .stButton > button {{
    background: {GRAD} !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    padding: 10px 20px !important;
    width: 100% !important;
    font-family: 'Inter', sans-serif !important;
    transition: opacity 0.15s !important;
  }}
  .stButton > button:hover {{ opacity: 0.85 !important; }}

  .stTextInput > div > div > input {{
    background: {BG3} !important;
    border: 1px solid {BORDER} !important;
    color: {TEXT} !important;
    border-radius: 10px !important;
    font-size: 13px !important;
    font-family: 'Inter', sans-serif !important;
  }}
  .stSelectbox > div > div {{
    background: {BG3} !important;
    border: 1px solid {BORDER} !important;
    color: {TEXT} !important;
    border-radius: 10px !important;
  }}
  [data-testid="stFileUploader"] {{
    background: {BG3} !important;
    border: 1px dashed {BORDER} !important;
    border-radius: 10px !important;
  }}
  label {{
    color: {TEXT2} !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    text-transform: uppercase !important;
    letter-spacing: .06em !important;
  }}
  .stCheckbox label {{
    text-transform: none !important;
    letter-spacing: 0 !important;
    font-size: 13px !important;
    color: {TEXT2} !important;
  }}
  .streamlit-expanderHeader {{
    background: {BG3} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 10px !important;
    color: {TEXT} !important;
    font-size: 13px !important;
    font-weight: 500 !important;
  }}
  .streamlit-expanderContent {{
    background: {BG2} !important;
    border: 1px solid {BORDER} !important;
    border-top: none !important;
    border-radius: 0 0 10px 10px !important;
  }}
  [data-testid="metric-container"] {{
    background: {BG3} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 10px !important;
    padding: 12px !important;
  }}
  [data-testid="stMetricValue"] {{
    color: {PURPLE} !important;
    font-size: 1.5rem !important;
    font-weight: 700 !important;
  }}
  [data-testid="stMetricLabel"] {{
    color: {TEXT3} !important;
    font-size: 11px !important;
    text-transform: uppercase !important;
  }}
  .stAlert {{ border-radius: 10px !important; font-size: 13px !important; }}
  hr {{ border-color: {BORDER} !important; margin: 24px 0 !important; }}
  div[data-testid="stMarkdownContainer"] p {{ color: {TEXT2}; font-size: 13px; }}
  [data-testid="stForm"] {{
    background: {BG2};
    border: 1px solid {BORDER};
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 20px;
  }}
</style>
""", unsafe_allow_html=True)

ROLE_OPTIONS = [
    "Data & AI", "Software Engineering", "Cloud & DevOps",
    "Cybersecurity", "ECE & Embedded", "Mechanical", "Civil",
    "Finance & MBA", "Medical & Healthcare", "Law",
    "Design & UX", "Media & Marketing",
]

def plotly_layout(**kwargs):
    return dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=TEXT2, size=12, family="Inter"),
        margin=dict(l=0, r=0, t=10, b=0),
        **kwargs
    )

st.markdown(
    f'<div style="display:flex;align-items:center;gap:18px;margin-bottom:28px">'
    f'<div class="sm-logo" style="width:56px;height:56px;font-size:28px;border-radius:16px">🪞</div>'
    f'<div><div style="font-size:30px;font-weight:800;color:{TEXT};letter-spacing:-1px;line-height:1.1">SkillMirror</div>'
    f'<div style="font-size:13px;color:{TEXT3};margin-top:2px">Career gap analyser</div></div>'
    f'</div>',
    unsafe_allow_html=True
)

nav_col, theme_col = st.columns([5, 1])
with nav_col:
    tab_analyse, tab_compare, tab_resume = st.tabs(
        ["🔍  Analyse", "🏫  Compare", "📄  Resume"]
    )
with theme_col:
    theme_icon = "☀️" if is_dark else "🌙"
    if st.button(theme_icon, key="theme_btn", help="Toggle theme"):
        st.session_state.theme = "light" if is_dark else "dark"
        st.rerun()

def load_gap():
    with open("data/gap_analysis.json") as f: gap = json.load(f)
    with open("data/syllabus_skills.json") as f: syl = json.load(f)
    with open("data/jd_skills.json") as f: jd = json.load(f)
    return gap, syl, jd

def load_comparison():
    with open("data/comparison.json") as f: return json.load(f)

def load_resume():
    with open("data/resume_analysis.json") as f: return json.load(f)

def roadmap_expander(skill_name, demand, current_role):
    plan = generate_skill_roadmap(skill_name, current_role, demand)
    diff_icon = "🟢" if plan['difficulty']=="Beginner" else "🟡" if plan['difficulty']=="Intermediate" else "🔴"
    icons = {"Video":"📹","Book":"📖","Course":"🎓","Interactive":"💻",
             "Docs":"📄","Practice":"🏋️","Software":"💾","Article":"📰"}
    with st.expander(
        f"{skill_name}  ·  {demand}% of JDs  ·  "
        f"⏱ {plan['time_estimate']}  ·  {diff_icon} {plan['difficulty']}"
    ):
        st.markdown(
            f'<div style="font-size:13px;color:{TEXT2};margin-bottom:14px;'
            f'padding:12px;background:{BG3};border-radius:10px;'
            f'border:1px solid {BORDER}">'
            f'<b style="color:{TEXT}">Why it matters</b><br>'
            f'{plan["why_it_matters"]}</div>',
            unsafe_allow_html=True
        )
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<div style="font-size:12px;font-weight:600;color:{TEXT};margin-bottom:8px">📅 Weekly Plan</div>', unsafe_allow_html=True)
            for w in plan["weekly_plan"]:
                st.markdown(f'<div class="sm-week"><div class="sm-week-t">Week {w["week"]} — {w["focus"]}</div><div class="sm-week-g">🎯 {w["goal"]}</div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div style="font-size:12px;font-weight:600;color:{TEXT};margin-bottom:8px">🔗 Free Resources</div>', unsafe_allow_html=True)
            for res in plan["free_resources"]:
                icon = icons.get(res["type"], "🔗")
                st.markdown(
                    f'<div style="font-size:12px;color:{TEXT2};padding:4px 0">'
                    f'{icon} <a href="{res["url"]}" target="_blank" '
                    f'style="color:{PURPLE};text-decoration:none">'
                    f'{res["name"]}</a> · '
                    f'<span style="color:{TEXT3}">{res["type"]}</span></div>',
                    unsafe_allow_html=True
                )
        st.markdown(f'<div style="font-size:12px;font-weight:600;color:{TEXT};margin:12px 0 8px">🏗️ Project to Build</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="sm-project">'
            f'<div style="font-size:13px;font-weight:600;color:{GREEN};margin-bottom:4px">{plan["project_to_build"]["name"]}</div>'
            f'<div style="font-size:12px;color:{TEXT2}">{plan["project_to_build"]["description"]}</div>'
            f'<div style="font-size:11px;color:{TEXT3};margin-top:6px">💡 {plan["project_to_build"]["why"]}</div>'
            f'</div>',
            unsafe_allow_html=True
        )
        st.markdown(f'<div style="font-size:12px;font-weight:600;color:{TEXT};margin:12px 0 8px">💡 Pro Tips</div>', unsafe_allow_html=True)
        for tip in plan["tips"]:
            st.markdown(f'<div class="sm-tip">→ {tip}</div>', unsafe_allow_html=True)

with tab_analyse:
    st.markdown(
        f'<div class="sm-page-title">Syllabus Analyser</div>'
        f'<div class="sm-page-sub">Upload your syllabus PDF and see how it stacks up against real job descriptions.</div>',
        unsafe_allow_html=True
    )

    with st.form("analyse_form"):
        c1, c2, c3 = st.columns([2, 1.5, 1])
        with c1: uploaded = st.file_uploader("Syllabus PDF", type=["pdf"])
        with c2: course_name = st.text_input("Course name", value="SRM CI 2024")
        with c3: role_group = st.selectbox("Target role", options=ROLE_OPTIONS)
        submitted = st.form_submit_button("Analyse →")

    if submitted and uploaded:
        pdf_path = f"data/{uploaded.name}"
        with open(pdf_path, "wb") as f: f.write(uploaded.getbuffer())
        with st.spinner("Parsing syllabus..."): parse_syllabus(pdf_path, course_name)
        with st.spinner(f"Loading {role_group} JD data..."): scrape_jobs(role_group=role_group, use_fallback=True)
        with st.spinner("Running gap analysis..."): analyse_gap()
        st.success("Analysis complete!")
    elif submitted and not uploaded:
        st.warning("Please upload a syllabus PDF first!")

    try:
        gap, syl, jd = load_gap()
        summary = gap["summary"]
        covered = gap["covered"]
        gaps    = gap["gaps"]
        roadmap = gap["roadmap"]
        role    = jd.get("role_group", "Data & AI")
        score   = summary["coverage_score"]

        st.markdown(f"""
        <div class="sm-hero">
          <div>
            <div class="sm-hero-score">{score}%</div>
            <div class="sm-hero-label">Coverage Score</div>
          </div>
          <div class="sm-hero-right">
            <div class="sm-hero-role">Analysed for</div>
            <div class="sm-hero-badge">🎯 {role}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="sm-stats">
          <div class="sm-stat">
            <div class="sm-stat-val" style="color:{GREEN}">{summary["covered_count"]}</div>
            <div class="sm-stat-lbl">Skills Covered</div>
          </div>
          <div class="sm-stat">
            <div class="sm-stat-val" style="color:{RED}">{summary["gap_count"]}</div>
            <div class="sm-stat-lbl">Skills Missing</div>
          </div>
          <div class="sm-stat">
            <div class="sm-stat-val">{summary["industry_skills_count"]}</div>
            <div class="sm-stat-lbl">Industry Skills Tracked</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        left, right = st.columns([1.4, 1])

        with left:
            st.markdown(
                f'<div class="sm-card">'
                f'<div class="sm-card-title">Skills Heatmap</div>'
                f'<div class="sm-card-sub">Green = covered · Red = missing</div>',
                unsafe_allow_html=True
            )
            all_skills = (
                [{"skill": s["skill"], "demand": s["demand"], "status": "✅ Covered"} for s in covered] +
                [{"skill": s["skill"], "demand": s["demand"], "status": "❌ Gap"} for s in gaps]
            )
            df = pd.DataFrame(all_skills).sort_values("demand", ascending=True)
            fig = px.bar(
                df, x="demand", y="skill", color="status", orientation="h",
                color_discrete_map={"✅ Covered": GREEN, "❌ Gap": RED},
                labels={"demand": "% of Job Descriptions", "skill": ""},
                height=max(380, len(all_skills)*26)
            )
            fig.update_layout(**plotly_layout(
                legend=dict(title="", orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                xaxis=dict(gridcolor=BORDER, zerolinecolor=BORDER),
                yaxis=dict(gridcolor="rgba(0,0,0,0)"),
            ))
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with right:
            st.markdown(
                f'<div class="sm-card">'
                f'<div class="sm-card-title">Gap Roadmap</div>'
                f'<div class="sm-card-sub">Missing skills ranked by industry demand</div>',
                unsafe_allow_html=True
            )
            if roadmap:
                for i, s in enumerate(roadmap, 1):
                    st.markdown(f'<div class="sm-gap"><span><b>#{i}</b> &nbsp;{s["skill"]}</span><span class="sm-gap-pct">{s["demand"]}%</span></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div style="color:{GREEN};font-size:13px;padding:12px">🎉 No gaps! Your syllabus covers everything.</div>', unsafe_allow_html=True)

            st.markdown(f'<hr style="margin:14px 0"><div class="sm-card-title">Already Covered</div><div class="sm-card-sub">Top skills by demand</div>', unsafe_allow_html=True)
            for s in covered[:8]:
                st.markdown(f'<div class="sm-ok"><span>✓ &nbsp;{s["skill"]}</span><span class="sm-ok-pct">{s["demand"]}%</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)

        st.markdown(
            f'<div class="sm-card-title">📚 Detailed Learning Roadmap</div>'
            f'<div class="sm-card-sub" style="margin-bottom:16px">Click any skill to expand your personalised plan</div>',
            unsafe_allow_html=True
        )
        if roadmap:
            for s in roadmap:
                roadmap_expander(s["skill"], s["demand"], role)
        else:
            st.markdown(f'<div style="color:{GREEN};font-size:13px">🎉 No gaps to show!</div>', unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)

        st.markdown(
            f'<div class="sm-card-title">Coverage by Category</div>'
            f'<div class="sm-card-sub" style="margin-bottom:16px">How well each skill domain is covered</div>',
            unsafe_allow_html=True
        )
        cat_data = {}
        for s in covered:
            c = s.get("category","Other"); cat_data.setdefault(c,{"covered":0,"gap":0}); cat_data[c]["covered"] += 1
        for s in gaps:
            c = s.get("category","Other"); cat_data.setdefault(c,{"covered":0,"gap":0}); cat_data[c]["gap"] += 1
        cats = list(cat_data.keys())
        fig2 = go.Figure(data=[
            go.Bar(name="Covered", x=cats, y=[cat_data[c]["covered"] for c in cats], marker_color=GREEN, marker_line_width=0),
            go.Bar(name="Gap",     x=cats, y=[cat_data[c]["gap"] for c in cats],     marker_color=RED,   marker_line_width=0),
        ])
        fig2.update_layout(**plotly_layout(
            barmode="stack", height=260,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis=dict(gridcolor="rgba(0,0,0,0)"),
            yaxis=dict(gridcolor=BORDER, zerolinecolor=BORDER),
        ))
        st.plotly_chart(fig2, use_container_width=True)

        st.markdown("<hr>", unsafe_allow_html=True)
        roles = jd.get("roles_covered", [])
        if roles:
            st.markdown(f'<div class="sm-card-sub" style="margin-bottom:10px">Roles analysed</div>', unsafe_allow_html=True)
            cols = st.columns(len(roles))
            for i, r in enumerate(roles):
                with cols[i]:
                    st.markdown(
                        f'<div style="background:{BG3};border:1px solid {BORDER};'
                        f'border-radius:8px;padding:8px 12px;font-size:12px;'
                        f'color:{TEXT2};text-align:center">{r}</div>',
                        unsafe_allow_html=True
                    )

    except FileNotFoundError:
        st.markdown(
            f'<div class="sm-empty">'
            f'<div class="sm-empty-icon">🪞</div>'
            f'<div class="sm-empty-title">Upload your syllabus to get started</div>'
            f'<div class="sm-empty-sub">Select a PDF above, pick your target role,<br>and see exactly what you\'re missing.</div>'
            f'</div>',
            unsafe_allow_html=True
        )

with tab_compare:
    st.markdown(
        f'<div class="sm-page-title">College Comparison</div>'
        f'<div class="sm-page-sub">Compare two colleges side by side for the same target role.</div>',
        unsafe_allow_html=True
    )

    with st.form("compare_form"):
        c1, c2, c3 = st.columns(3)
        with c1:
            uploaded_1 = st.file_uploader("College 1 PDF", type=["pdf"], key="pdf1")
            college_name_1 = st.text_input("College 1 name", value="SRM CI", key="name1")
        with c2:
            uploaded_2 = st.file_uploader("College 2 PDF", type=["pdf"], key="pdf2")
            college_name_2 = st.text_input("College 2 name", value="VIT CSE", key="name2")
        with c3:
            compare_role = st.selectbox("Target role", options=ROLE_OPTIONS, key="compare_role")
            st.markdown("<br>", unsafe_allow_html=True)
            compare_submitted = st.form_submit_button("Compare →")

    if compare_submitted:
        if not uploaded_1 or not uploaded_2:
            st.warning("Please upload both PDFs!")
        else:
            path1 = f"data/{uploaded_1.name}"; path2 = f"data/{uploaded_2.name}"
            with open(path1,"wb") as f: f.write(uploaded_1.getbuffer())
            with open(path2,"wb") as f: f.write(uploaded_2.getbuffer())
            with st.spinner(f"Comparing {college_name_1} vs {college_name_2}..."):
                compare_colleges(path1, college_name_1, path2, college_name_2, compare_role)
            st.success("Comparison complete!")

    try:
        comp = load_comparison()
        r = comp["results"]; n1 = comp["college_1"]; n2 = comp["college_2"]
        role = comp["role_group"]; winner = comp["winner"]

        if winner["college"] == "Tie":
            st.markdown(f'<div class="sm-winner"><div class="sm-winner-lbl">Result</div><div class="sm-winner-name">🤝 It\'s a Tie!</div><div class="sm-winner-sub">Both score {winner["score"]}% for {role} roles</div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="sm-winner"><div class="sm-winner-lbl">Winner for {role} roles</div><div class="sm-winner-name">{winner["college"]} 🏆</div><div class="sm-winner-sub">{winner["score"]}% coverage · {winner["margin"]}% ahead</div></div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        for col, name in [(col1, n1), (col2, n2)]:
            data = r[name]; is_w = winner["college"] == name
            with col:
                st.markdown(f'<div class="sm-ccard {"win" if is_w else ""}"><div class="sm-ccard-name">{name} {"🏆" if is_w else ""}</div></div>', unsafe_allow_html=True)
                m1, m2, m3 = st.columns(3)
                with m1: st.metric("Coverage", f"{data['coverage_score']}%")
                with m2: st.metric("Covered",  data['covered_count'])
                with m3: st.metric("Missing",  data['gap_count'])
                st.markdown("<br>", unsafe_allow_html=True)
                if data["top_gaps"]:
                    st.markdown(f'<div style="font-size:11px;color:{TEXT3};text-transform:uppercase;letter-spacing:.06em;margin-bottom:6px">Top Gaps</div>', unsafe_allow_html=True)
                    for g in data["top_gaps"]:
                        st.markdown(f'<div class="sm-gap" style="font-size:12px"><span>{g["skill"]}</span><span class="sm-gap-pct">{g["demand"]}%</span></div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div style="color:{GREEN};font-size:12px;padding:8px">🎉 No gaps!</div>', unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)

        if comp["common_gaps"]:
            st.markdown(f'<div class="sm-card-title">⚠️ Common Gaps</div><div class="sm-card-sub" style="margin-bottom:12px">Skills missing in BOTH colleges</div>', unsafe_allow_html=True)
            cols = st.columns(min(len(comp["common_gaps"]), 4))
            for i, g in enumerate(comp["common_gaps"]):
                with cols[i%4]:
                    st.markdown(f'<div class="sm-amber"><span>{g["skill"]}</span><span>{g["demand"]}%</span></div>', unsafe_allow_html=True)
            st.markdown("<hr>", unsafe_allow_html=True)

        unique = comp["unique_gaps"]
        if unique.get(n1) or unique.get(n2):
            st.markdown(f'<div class="sm-card-title">🔍 Unique Gaps</div><div class="sm-card-sub" style="margin-bottom:12px">Skills one college misses but the other covers</div>', unsafe_allow_html=True)
            uc1, uc2 = st.columns(2)
            with uc1:
                st.markdown(f'<div style="font-size:13px;font-weight:500;color:{TEXT};margin-bottom:8px">Only missing in {n1}</div>', unsafe_allow_html=True)
                for g in (unique.get(n1) or []):
                    st.markdown(f'<div class="sm-gap" style="font-size:12px"><span>{g["skill"]}</span><span class="sm-gap-pct">{g["demand"]}%</span></div>', unsafe_allow_html=True)
                if not unique.get(n1): st.markdown(f'<div style="color:{TEXT3};font-size:12px">No unique gaps</div>', unsafe_allow_html=True)
            with uc2:
                st.markdown(f'<div style="font-size:13px;font-weight:500;color:{TEXT};margin-bottom:8px">Only missing in {n2}</div>', unsafe_allow_html=True)
                for g in (unique.get(n2) or []):
                    st.markdown(f'<div class="sm-gap" style="font-size:12px"><span>{g["skill"]}</span><span class="sm-gap-pct">{g["demand"]}%</span></div>', unsafe_allow_html=True)
                if not unique.get(n2): st.markdown(f'<div style="color:{TEXT3};font-size:12px">No unique gaps</div>', unsafe_allow_html=True)
            st.markdown("<hr>", unsafe_allow_html=True)

        st.markdown(f'<div class="sm-card-title">Score Comparison</div><div class="sm-card-sub" style="margin-bottom:16px">Coverage scores side by side</div>', unsafe_allow_html=True)
        fig3 = go.Figure(data=[go.Bar(
            x=[n1, n2],
            y=[r[n1]["coverage_score"], r[n2]["coverage_score"]],
            marker_color=[
                PURPLE if r[n1]["coverage_score"] >= r[n2]["coverage_score"] else BLUE,
                PURPLE if r[n2]["coverage_score"] > r[n1]["coverage_score"] else BLUE,
            ],
            marker_line_width=0,
            text=[f"{r[n1]['coverage_score']}%", f"{r[n2]['coverage_score']}%"],
            textposition="outside",
            textfont=dict(color=TEXT, size=14),
        )])
        fig3.update_layout(**plotly_layout(
            height=280,
            yaxis=dict(range=[0,115], gridcolor=BORDER, zerolinecolor=BORDER),
            xaxis=dict(gridcolor="rgba(0,0,0,0)"),
        ))
        st.plotly_chart(fig3, use_container_width=True)

    except FileNotFoundError:
        st.markdown(
            f'<div class="sm-empty">'
            f'<div class="sm-empty-icon">🏫</div>'
            f'<div class="sm-empty-title">Compare two colleges</div>'
            f'<div class="sm-empty-sub">Upload two syllabus PDFs, pick a target role,<br>and see how they compare side by side.</div>'
            f'</div>',
            unsafe_allow_html=True
        )

with tab_resume:
    st.markdown(
        f'<div class="sm-page-title">Resume Analyser</div>'
        f'<div class="sm-page-sub">See how your resume stacks up against real job descriptions — and what to add.</div>',
        unsafe_allow_html=True
    )

    with st.form("resume_form"):
        c1, c2 = st.columns([2, 1])
        with c1: resume_pdf = st.file_uploader("Resume PDF", type=["pdf"], key="resume_pdf")
        with c2: resume_role = st.selectbox("Target role", options=ROLE_OPTIONS, key="resume_role")
        also_syl = st.checkbox("Also compare against my syllabus")
        syllabus_pdf = None; syllabus_course = "My Syllabus"
        if also_syl:
            sc1, sc2 = st.columns(2)
            with sc1: syllabus_pdf = st.file_uploader("Syllabus PDF", type=["pdf"], key="syl_pdf")
            with sc2: syllabus_course = st.text_input("Course name", value="My Syllabus", key="syl_course")
        resume_submitted = st.form_submit_button("Analyse Resume →")

    if resume_submitted:
        if not resume_pdf:
            st.warning("Please upload your resume PDF!")
        else:
            resume_path = f"data/{resume_pdf.name}"
            with open(resume_path,"wb") as f: f.write(resume_pdf.getbuffer())
            with st.spinner(f"Loading {resume_role} JD data..."): scrape_jobs(role_group=resume_role, use_fallback=True)
            syl_data = None
            if also_syl and syllabus_pdf:
                syl_path = f"data/{syllabus_pdf.name}"
                with open(syl_path,"wb") as f: f.write(syllabus_pdf.getbuffer())
                with st.spinner("Parsing syllabus..."): syl_data = parse_syllabus(syl_path, syllabus_course)
            with st.spinner("Analysing resume..."): analyse_resume(resume_path, resume_role, syl_data)
            st.success("Resume analysis complete!")

    try:
        ra = load_resume()
        vs_jd = ra["vs_jd"]; score_data = ra["score"]
        vs_syl = ra.get("vs_syllabus"); role = ra["role_group"]
        grade = score_data["grade"]; score = score_data["score"]

        st.markdown(f"""
        <div class="sm-hero">
          <div>
            <div class="sm-grade">{grade}</div>
            <div class="sm-hero-label" style="margin-top:8px">Resume Grade</div>
          </div>
          <div style="text-align:center">
            <div class="sm-hero-score">{score}%</div>
            <div class="sm-hero-label">Role Fit Score</div>
          </div>
          <div class="sm-hero-right">
            <div class="sm-hero-role">Analysed for</div>
            <div class="sm-hero-badge" style="margin-bottom:10px">🎯 {role}</div>
            <div style="font-size:13px;color:rgba(255,255,255,0.8);max-width:200px;text-align:right">{score_data["verdict"]}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="sm-stats">
          <div class="sm-stat"><div class="sm-stat-val" style="color:{GREEN}">{vs_jd["covered_count"]}</div><div class="sm-stat-lbl">Skills Matched</div></div>
          <div class="sm-stat"><div class="sm-stat-val" style="color:{RED}">{vs_jd["gap_count"]}</div><div class="sm-stat-lbl">Skills Missing</div></div>
          <div class="sm-stat"><div class="sm-stat-val">{ra["resume_skill_count"]}</div><div class="sm-stat-lbl">Skills Detected</div></div>
        </div>
        """, unsafe_allow_html=True)

        left, right = st.columns(2)
        with left:
            st.markdown(f'<div class="sm-card"><div class="sm-card-title">✅ Skills on Your Resume</div><div class="sm-card-sub">Detected from your PDF</div>', unsafe_allow_html=True)
            chips = "".join([f'<span class="sm-chip">{s["skill"]}</span>' for s in ra.get("resume_skills",[])])
            st.markdown(f'<div>{chips or f"<span style=\'color:{TEXT3}\'>No skills detected.</span>"}</div></div>', unsafe_allow_html=True)
        with right:
            st.markdown(f'<div class="sm-card"><div class="sm-card-title">❌ Missing from Resume</div><div class="sm-card-sub">{role} roles want these</div>', unsafe_allow_html=True)
            for g in vs_jd["gaps"][:10]:
                st.markdown(f'<div class="sm-gap"><span>{g["skill"]}</span><span class="sm-gap-pct">{g["demand"]}%</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)

        st.markdown(f'<div class="sm-card-title">🚀 What to Add to Your Resume</div><div class="sm-card-sub" style="margin-bottom:16px">Prioritised by industry demand</div>', unsafe_allow_html=True)
        wc1, wc2 = st.columns(2)
        with wc1:
            st.markdown(f'<div style="font-size:13px;font-weight:600;color:{RED};margin-bottom:10px">🔴 Quick Wins — High Demand</div>', unsafe_allow_html=True)
            if score_data["quick_wins"]:
                for qw in score_data["quick_wins"]:
                    plan = generate_skill_roadmap(qw["skill"], role, qw["demand"])
                    st.markdown(
                        f'<div class="sm-gap" style="margin-bottom:6px">'
                        f'<div><div style="font-weight:600">{qw["skill"]}</div>'
                        f'<div style="font-size:11px;color:{TEXT2};margin-top:2px">⏱ {plan["time_estimate"]} · {plan["difficulty"]}</div></div>'
                        f'<span class="sm-gap-pct">{qw["demand"]}%</span></div>',
                        unsafe_allow_html=True
                    )
            else:
                st.markdown(f'<div style="color:{GREEN};font-size:13px">🎉 You have all high-demand skills!</div>', unsafe_allow_html=True)
        with wc2:
            st.markdown(f'<div style="font-size:13px;font-weight:600;color:{AMBER};margin-bottom:10px">🟡 Nice to Have</div>', unsafe_allow_html=True)
            if score_data["nice_to_have"]:
                for nth in score_data["nice_to_have"]:
                    st.markdown(f'<div class="sm-amber" style="margin-bottom:6px"><span>{nth["skill"]}</span><span>{nth["demand"]}%</span></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div style="color:{TEXT3};font-size:13px">Nothing more!</div>', unsafe_allow_html=True)

        if score_data["quick_wins"]:
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown(f'<div class="sm-card-title">📚 How to Learn Your Quick Wins</div><div class="sm-card-sub" style="margin-bottom:16px">Week-by-week plans for your highest priority gaps</div>', unsafe_allow_html=True)
            for qw in score_data["quick_wins"]:
                roadmap_expander(qw["skill"], qw["demand"], role)

        if vs_syl:
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown(f'<div class="sm-card-title">🎓 Resume vs Syllabus</div><div class="sm-card-sub" style="margin-bottom:16px">How much of your education are you actually using?</div>', unsafe_allow_html=True)
            vc1, vc2, vc3 = st.columns(3)
            with vc1: st.metric("Education Utilisation", f"{vs_syl['utilisation_score']}%")
            with vc2: st.metric("Syllabus Skills Used",  vs_syl['using_count'])
            with vc3: st.metric("Self-Learned Skills",   vs_syl['self_learned_count'])
            if vs_syl["self_learned"]:
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(f'<div style="font-size:13px;font-weight:600;color:{AMBER};margin-bottom:8px">⭐ Self-Learned (not in syllabus)</div>', unsafe_allow_html=True)
                chips = "".join([f'<span class="sm-chip" style="border-color:{AMBER}40;color:{AMBER}">{s}</span>' for s in vs_syl["self_learned"]])
                st.markdown(chips, unsafe_allow_html=True)

    except FileNotFoundError:
        st.markdown(
            f'<div class="sm-empty">'
            f'<div class="sm-empty-icon">📄</div>'
            f'<div class="sm-empty-title">Analyse your resume</div>'
            f'<div class="sm-empty-sub">Upload your resume PDF, pick your target role,<br>and get your personal role-fit score.</div>'
            f'</div>',
            unsafe_allow_html=True
        )