"""
SkillMirror — Streamlit Dashboard
Phase 5 — College Comparison added
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

# ── Page config ───────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="SkillMirror",
    page_icon="🪞",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Premium CSS ───────────────────────────────────────────────────────────────

st.markdown("""
<style>
    .stApp { background-color: #0d1117; }
    .block-container { padding: 2rem 2.5rem 2rem 2.5rem; }
    #MainMenu, footer, header { visibility: hidden; }

    [data-testid="stSidebar"] {
        background-color: #0d1117;
        border-right: 1px solid #21262d;
    }
    [data-testid="stSidebar"] .block-container {
        padding: 2rem 1.2rem;
    }

    h1, h2, h3 { color: #e6edf3 !important; }
    p, li { color: #8b949e; }

    .metric-card {
        background: #161b22;
        border: 1px solid #21262d;
        border-radius: 12px;
        padding: 1.4rem 1.2rem;
        text-align: center;
        transition: border-color 0.2s;
    }
    .metric-card:hover { border-color: #388bfd; }
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #58a6ff;
        letter-spacing: -1px;
    }
    .metric-value-red { color: #f85149 !important; }
    .metric-value-green { color: #3fb950 !important; }
    .metric-label {
        font-size: 0.78rem;
        color: #484f58;
        text-transform: uppercase;
        letter-spacing: .06em;
        margin-top: 6px;
    }

    .role-tag {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #1f2937;
        border: 1px solid #21262d;
        border-radius: 20px;
        padding: 4px 14px;
        font-size: 12px;
        color: #58a6ff;
        margin-bottom: 1.5rem;
    }

    .gap-badge {
        background: #1a0f0f;
        border: 1px solid #4a1515;
        border-radius: 8px;
        padding: 10px 14px;
        color: #f85149;
        margin: 5px 0;
        font-size: 13px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .gap-badge-pct {
        background: #2d1212;
        border-radius: 4px;
        padding: 2px 8px;
        font-size: 11px;
        color: #f85149;
    }

    .covered-badge {
        background: #0d1a0f;
        border: 1px solid #1a4a20;
        border-radius: 8px;
        padding: 10px 14px;
        color: #3fb950;
        margin: 5px 0;
        font-size: 13px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .covered-badge-pct {
        background: #0d1f10;
        border-radius: 4px;
        padding: 2px 8px;
        font-size: 11px;
        color: #3fb950;
    }

    .roadmap-week {
        background: #161b22;
        border: 1px solid #21262d;
        border-left: 3px solid #58a6ff;
        border-radius: 8px;
        padding: 12px 14px;
        margin: 6px 0;
    }
    .roadmap-week-title {
        font-size: 13px;
        font-weight: 500;
        color: #e6edf3;
    }
    .roadmap-week-goal {
        font-size: 12px;
        color: #3fb950;
        margin-top: 4px;
    }
    .roadmap-project {
        background: #0d1a0f;
        border: 1px solid #1a4a20;
        border-radius: 8px;
        padding: 14px;
        margin: 8px 0;
    }
    .roadmap-tip {
        background: #161b22;
        border: 1px solid #21262d;
        border-radius: 6px;
        padding: 8px 12px;
        font-size: 12px;
        color: #8b949e;
        margin: 4px 0;
    }

    hr { border-color: #21262d !important; }

    .streamlit-expanderHeader {
        background: #161b22 !important;
        border: 1px solid #21262d !important;
        border-radius: 8px !important;
        color: #e6edf3 !important;
        font-size: 13px !important;
    }

    .stButton > button {
        background: #238636 !important;
        color: #ffffff !important;
        border: 1px solid #2ea043 !important;
        border-radius: 6px !important;
        font-weight: 500 !important;
        padding: 0.5rem 1rem !important;
        width: 100% !important;
    }
    .stButton > button:hover { background: #2ea043 !important; }

    .stTextInput > div > div > input {
        background: #161b22 !important;
        border: 1px solid #21262d !important;
        color: #e6edf3 !important;
        border-radius: 6px !important;
    }
    .stSelectbox > div > div {
        background: #161b22 !important;
        border: 1px solid #21262d !important;
        color: #e6edf3 !important;
        border-radius: 6px !important;
    }

    [data-testid="stFileUploader"] {
        background: #161b22 !important;
        border: 1px dashed #21262d !important;
        border-radius: 8px !important;
    }

    .role-card {
        background: #161b22;
        border: 1px solid #21262d;
        border-radius: 8px;
        padding: 10px 14px;
        text-align: center;
        font-size: 12px;
        color: #8b949e;
    }

    .section-header {
        font-size: 16px;
        font-weight: 600;
        color: #e6edf3;
        margin: 0 0 4px 0;
    }
    .section-sub {
        font-size: 12px;
        color: #484f58;
        margin-bottom: 16px;
    }

    .hero-title {
        font-size: 2rem;
        font-weight: 700;
        color: #e6edf3;
        letter-spacing: -1px;
        margin-bottom: 4px;
    }
    .hero-sub {
        font-size: 14px;
        color: #484f58;
        margin-bottom: 0;
    }

    .compare-winner {
        background: #0d1a0f;
        border: 1px solid #1a4a20;
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .compare-card {
        background: #161b22;
        border: 1px solid #21262d;
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 12px;
    }
    .common-gap {
        background: #1a1a0f;
        border: 1px solid #4a4a15;
        border-radius: 8px;
        padding: 8px 14px;
        color: #e3b341;
        font-size: 12px;
        margin: 4px 0;
        display: flex;
        justify-content: space-between;
    }

    /* Native metric styling */
    [data-testid="metric-container"] {
        background: #161b22;
        border: 1px solid #21262d;
        border-radius: 8px;
        padding: 12px;
    }
    [data-testid="metric-container"] label {
        color: #484f58 !important;
        font-size: 11px !important;
        text-transform: uppercase;
        letter-spacing: .06em;
    }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #58a6ff !important;
        font-size: 1.6rem !important;
        font-weight: 700 !important;
    }
</style>
""", unsafe_allow_html=True)

# ── Role options ──────────────────────────────────────────────────────────────

ROLE_OPTIONS = [
    "Data & AI",
    "Software Engineering",
    "Cloud & DevOps",
    "Cybersecurity",
    "ECE & Embedded",
    "Mechanical",
    "Civil",
    "Finance & MBA",
    "Medical & Healthcare",
    "Law",
    "Design & UX",
    "Media & Marketing",
]

# ── Sidebar ───────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div style="margin-bottom:1.5rem">
        <div style="font-size:20px;font-weight:700;color:#e6edf3;
        letter-spacing:-0.5px">🪞 SkillMirror</div>
        <div style="font-size:11px;color:#484f58;margin-top:2px">
        Career gap analyser</div>
    </div>
    """, unsafe_allow_html=True)

    mode = st.radio(
        "Mode",
        options=["🔍 Analyse", "🏫 Compare"],
        label_visibility="collapsed",
        horizontal=True
    )

    st.markdown('<hr style="margin:12px 0">', unsafe_allow_html=True)

    if mode == "🔍 Analyse":
        uploaded = st.file_uploader(
            "Syllabus PDF", type=["pdf"],
            label_visibility="collapsed"
        )
        if not uploaded:
            st.markdown(
                '<div style="font-size:11px;color:#484f58;'
                'margin-top:-8px;margin-bottom:8px">'
                'Upload your syllabus PDF</div>',
                unsafe_allow_html=True
            )
        course_name = st.text_input(
            "Course name", value="SRM CI 2024",
            placeholder="e.g. SRM CI 2024"
        )
        st.markdown(
            '<div style="font-size:11px;font-weight:500;color:#484f58;'
            'text-transform:uppercase;letter-spacing:.06em;'
            'margin-top:16px;margin-bottom:8px">Target Role</div>',
            unsafe_allow_html=True
        )
        role_group = st.selectbox(
            "Role", options=ROLE_OPTIONS,
            label_visibility="collapsed"
        )
        st.markdown("<br>", unsafe_allow_html=True)
        analyse_btn = st.button("Analyse →", use_container_width=True)

    else:
        st.markdown(
            '<div style="font-size:11px;font-weight:500;color:#484f58;'
            'text-transform:uppercase;letter-spacing:.06em;'
            'margin-bottom:8px">College 1</div>',
            unsafe_allow_html=True
        )
        uploaded_1 = st.file_uploader(
            "College 1 PDF", type=["pdf"],
            label_visibility="collapsed", key="pdf1"
        )
        college_name_1 = st.text_input(
            "College 1 name", value="SRM CI",
            placeholder="e.g. SRM CI", key="name1"
        )
        st.markdown(
            '<div style="font-size:11px;font-weight:500;color:#484f58;'
            'text-transform:uppercase;letter-spacing:.06em;'
            'margin-top:16px;margin-bottom:8px">College 2</div>',
            unsafe_allow_html=True
        )
        uploaded_2 = st.file_uploader(
            "College 2 PDF", type=["pdf"],
            label_visibility="collapsed", key="pdf2"
        )
        college_name_2 = st.text_input(
            "College 2 name", value="VIT CSE",
            placeholder="e.g. VIT CSE", key="name2"
        )
        st.markdown(
            '<div style="font-size:11px;font-weight:500;color:#484f58;'
            'text-transform:uppercase;letter-spacing:.06em;'
            'margin-top:16px;margin-bottom:8px">Target Role</div>',
            unsafe_allow_html=True
        )
        compare_role = st.selectbox(
            "Role", options=ROLE_OPTIONS,
            label_visibility="collapsed", key="compare_role"
        )
        st.markdown("<br>", unsafe_allow_html=True)
        compare_btn = st.button("Compare →", use_container_width=True)

    st.markdown("""
    <div style="border-top:1px solid #21262d;padding-top:16px;
    margin-top:16px">
        <div style="font-size:11px;font-weight:500;color:#484f58;
        text-transform:uppercase;letter-spacing:.06em;margin-bottom:10px">
        How it works</div>
        <div style="font-size:12px;color:#484f58;line-height:1.8">
        1. Upload syllabus PDF<br>
        2. Pick target role<br>
        3. Get gap analysis<br>
        4. Follow your roadmap
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Helper functions ──────────────────────────────────────────────────────────

def load_results():
    with open("data/gap_analysis.json") as f:
        gap = json.load(f)
    with open("data/syllabus_skills.json") as f:
        syllabus = json.load(f)
    with open("data/jd_skills.json") as f:
        jd = json.load(f)
    return gap, syllabus, jd

def load_comparison():
    with open("data/comparison.json") as f:
        return json.load(f)

# ── ANALYSE MODE ──────────────────────────────────────────────────────────────

if mode == "🔍 Analyse":

    if analyse_btn and uploaded:
        pdf_path = f"data/{uploaded.name}"
        with open(pdf_path, "wb") as f:
            f.write(uploaded.getbuffer())
        with st.spinner("Parsing syllabus..."):
            parse_syllabus(pdf_path, course_name)
        with st.spinner(f"Loading JD data for {role_group}..."):
            scrape_jobs(role_group=role_group, use_fallback=True)
        with st.spinner("Running gap analysis..."):
            analyse_gap()
        st.success("Analysis complete!")
    elif analyse_btn and not uploaded:
        st.warning("Please upload a syllabus PDF first!")

    try:
        gap, syllabus, jd = load_results()
        summary      = gap["summary"]
        covered      = gap["covered"]
        gaps         = gap["gaps"]
        roadmap      = gap["roadmap"]
        current_role = jd.get("role_group", "Data & AI")

        col_hero, col_tag = st.columns([3, 1])
        with col_hero:
            st.markdown("""
            <div class="hero-title">🪞 SkillMirror</div>
            <div class="hero-sub">Know exactly what your syllabus
            is missing — before your first interview.</div>
            """, unsafe_allow_html=True)
        with col_tag:
            st.markdown(f"""
            <div style="text-align:right;padding-top:8px">
                <div class="role-tag">🎯 {current_role}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<hr style="margin:1.2rem 0">', unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        score = summary['coverage_score']
        score_color = (
            "metric-value-green" if score >= 90
            else "" if score >= 70
            else "metric-value-red"
        )
        with c1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value {score_color}">{score}%</div>
                <div class="metric-label">Coverage Score</div>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value metric-value-green">
                {summary['covered_count']}</div>
                <div class="metric-label">Skills Covered</div>
            </div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value metric-value-red">
                {summary['gap_count']}</div>
                <div class="metric-label">Skills Missing</div>
            </div>""", unsafe_allow_html=True)
        with c4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">
                {summary['industry_skills_count']}</div>
                <div class="metric-label">Skills Tracked</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        left, right = st.columns([1.3, 1])

        with left:
            st.markdown(
                '<div class="section-header">Skills Heatmap</div>'
                '<div class="section-sub">'
                'Green = covered · Red = missing</div>',
                unsafe_allow_html=True
            )
            all_skills = (
                [{"skill": s["skill"], "demand": s["demand"],
                  "status": "✅ Covered"} for s in covered] +
                [{"skill": s["skill"], "demand": s["demand"],
                  "status": "❌ Gap"} for s in gaps]
            )
            df = pd.DataFrame(all_skills).sort_values(
                "demand", ascending=True
            )
            fig = px.bar(
                df, x="demand", y="skill", color="status",
                orientation="h",
                color_discrete_map={
                    "✅ Covered": "#3fb950",
                    "❌ Gap":     "#f85149"
                },
                labels={
                    "demand": "% of Job Descriptions",
                    "skill": ""
                },
                height=max(400, len(all_skills) * 28)
            )
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#8b949e", size=12),
                legend=dict(
                    title="", orientation="h",
                    yanchor="bottom", y=1.02,
                    xanchor="right", x=1
                ),
                margin=dict(l=0, r=0, t=30, b=0),
                xaxis=dict(
                    gridcolor="#21262d",
                    zerolinecolor="#21262d"
                ),
                yaxis=dict(gridcolor="rgba(0,0,0,0)"),
            )
            st.plotly_chart(fig, use_container_width=True)

        with right:
            st.markdown(
                '<div class="section-header">Learning Roadmap</div>'
                '<div class="section-sub">'
                'Missing skills ranked by demand</div>',
                unsafe_allow_html=True
            )
            if roadmap:
                for i, skill in enumerate(roadmap, 1):
                    st.markdown(f"""
                    <div class="gap-badge">
                        <span><b>#{i}</b> &nbsp; {skill['skill']}</span>
                        <span class="gap-badge-pct">
                        {skill['demand']}% of JDs</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="background:#0d1a0f;border:1px solid #1a4a20;
                border-radius:8px;padding:16px;color:#3fb950;font-size:13px">
                    🎉 No gaps! Your syllabus covers everything.
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(
                '<div class="section-header">Already Covered</div>'
                '<div class="section-sub">'
                'Top skills by industry demand</div>',
                unsafe_allow_html=True
            )
            for skill in covered[:8]:
                st.markdown(f"""
                <div class="covered-badge">
                    <span>✓ &nbsp; {skill['skill']}</span>
                    <span class="covered-badge-pct">
                    {skill['demand']}% of JDs</span>
                </div>
                """, unsafe_allow_html=True)

        st.markdown('<hr style="margin:2rem 0">', unsafe_allow_html=True)

        st.markdown(
            '<div class="section-header">📚 Detailed Learning Roadmap</div>'
            '<div class="section-sub">'
            'Click any skill to expand your personalised plan</div>',
            unsafe_allow_html=True
        )

        if roadmap:
            for skill_data in roadmap:
                skill_name = skill_data["skill"]
                demand     = skill_data["demand"]
                plan = generate_skill_roadmap(
                    skill_name, current_role, demand
                )
                diff_icon = (
                    "🟢" if plan['difficulty'] == "Beginner"
                    else "🟡" if plan['difficulty'] == "Intermediate"
                    else "🔴"
                )
                with st.expander(
                    f"{skill_name}  ·  {demand}% of JDs  ·  "
                    f"⏱ {plan['time_estimate']}  ·  "
                    f"{diff_icon} {plan['difficulty']}"
                ):
                    st.markdown(
                        f'<div style="font-size:13px;color:#8b949e;'
                        f'margin-bottom:16px;padding:12px;'
                        f'background:#161b22;border-radius:8px;'
                        f'border:1px solid #21262d">'
                        f'<b style="color:#e6edf3">Why this matters</b>'
                        f'<br>{plan["why_it_matters"]}</div>',
                        unsafe_allow_html=True
                    )
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(
                            '<div style="font-size:12px;font-weight:600;'
                            'color:#e6edf3;margin-bottom:8px">'
                            '📅 Weekly Plan</div>',
                            unsafe_allow_html=True
                        )
                        for week in plan["weekly_plan"]:
                            st.markdown(f"""
                            <div class="roadmap-week">
                                <div class="roadmap-week-title">
                                Week {week['week']} — {week['focus']}
                                </div>
                                <div class="roadmap-week-goal">
                                🎯 {week['goal']}</div>
                            </div>
                            """, unsafe_allow_html=True)
                    with col2:
                        st.markdown(
                            '<div style="font-size:12px;font-weight:600;'
                            'color:#e6edf3;margin-bottom:8px">'
                            '🔗 Free Resources</div>',
                            unsafe_allow_html=True
                        )
                        icons = {
                            "Video": "📹", "Book": "📖",
                            "Course": "🎓", "Interactive": "💻",
                            "Docs": "📄", "Practice": "🏋️",
                            "Software": "💾", "Article": "📰"
                        }
                        for res in plan["free_resources"]:
                            icon = icons.get(res["type"], "🔗")
                            st.markdown(
                                f'<div style="font-size:12px;'
                                f'color:#8b949e;padding:4px 0">'
                                f'{icon} <a href="{res["url"]}" '
                                f'target="_blank" style="color:#58a6ff;'
                                f'text-decoration:none">{res["name"]}</a>'
                                f' · <span style="color:#484f58">'
                                f'{res["type"]}</span></div>',
                                unsafe_allow_html=True
                            )
                    st.markdown(
                        '<div style="font-size:12px;font-weight:600;'
                        'color:#e6edf3;margin:12px 0 8px">'
                        '🏗️ Project to Build</div>',
                        unsafe_allow_html=True
                    )
                    st.markdown(f"""
                    <div class="roadmap-project">
                        <div style="font-size:13px;font-weight:600;
                        color:#3fb950;margin-bottom:4px">
                        {plan['project_to_build']['name']}</div>
                        <div style="font-size:12px;color:#8b949e">
                        {plan['project_to_build']['description']}</div>
                        <div style="font-size:11px;color:#484f58;
                        margin-top:6px">
                        💡 {plan['project_to_build']['why']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown(
                        '<div style="font-size:12px;font-weight:600;'
                        'color:#e6edf3;margin:12px 0 8px">'
                        '💡 Pro Tips</div>',
                        unsafe_allow_html=True
                    )
                    for tip in plan["tips"]:
                        st.markdown(
                            f'<div class="roadmap-tip">→ {tip}</div>',
                            unsafe_allow_html=True
                        )
        else:
            st.markdown("""
            <div style="background:#0d1a0f;border:1px solid #1a4a20;
            border-radius:8px;padding:20px;color:#3fb950;font-size:14px;
            text-align:center">
                🎉 No gaps found — your syllabus covers everything!
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<hr style="margin:2rem 0">', unsafe_allow_html=True)

        st.markdown(
            '<div class="section-header">Coverage by Category</div>'
            '<div class="section-sub">'
            'How well each skill domain is covered</div>',
            unsafe_allow_html=True
        )
        cat_data = {}
        for s in covered:
            cat = s.get("category", "Other")
            cat_data.setdefault(cat, {"covered": 0, "gap": 0})
            cat_data[cat]["covered"] += 1
        for s in gaps:
            cat = s.get("category", "Other")
            cat_data.setdefault(cat, {"covered": 0, "gap": 0})
            cat_data[cat]["gap"] += 1
        cats = list(cat_data.keys())
        fig2 = go.Figure(data=[
            go.Bar(
                name="Covered", x=cats,
                y=[cat_data[c]["covered"] for c in cats],
                marker_color="#3fb950", marker_line_width=0
            ),
            go.Bar(
                name="Gap", x=cats,
                y=[cat_data[c]["gap"] for c in cats],
                marker_color="#f85149", marker_line_width=0
            )
        ])
        fig2.update_layout(
            barmode="stack",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#8b949e", size=12),
            height=280,
            margin=dict(l=0, r=0, t=10, b=0),
            legend=dict(
                orientation="h", yanchor="bottom",
                y=1.02, xanchor="right", x=1
            ),
            xaxis=dict(gridcolor="rgba(0,0,0,0)"),
            yaxis=dict(
                gridcolor="#21262d",
                zerolinecolor="#21262d"
            ),
        )
        st.plotly_chart(fig2, use_container_width=True)

        st.markdown('<hr style="margin:2rem 0">', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-header">Roles in this Analysis</div>'
            '<div class="section-sub">'
            'JDs analysed across these positions</div>',
            unsafe_allow_html=True
        )
        roles = jd.get("roles_covered", [])
        if roles:
            cols = st.columns(len(roles))
            for i, role in enumerate(roles):
                with cols[i]:
                    st.markdown(
                        f'<div class="role-card">{role}</div>',
                        unsafe_allow_html=True
                    )

    except FileNotFoundError:
        st.markdown("""
        <div class="hero-title">🪞 SkillMirror</div>
        <div class="hero-sub">Know exactly what your syllabus is missing
        — before your first interview.</div>
        """, unsafe_allow_html=True)
        st.markdown('<hr style="margin:1.5rem 0">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        for col, icon, title, desc in [
            (c1, "📄", "Upload Syllabus",
             "Any engineering, medical, law, finance or design PDF"),
            (c2, "🎯", "Pick Target Role",
             "12 domains — Data & AI, SWE, ECE, Medical, Law and more"),
            (c3, "🗺️", "Get Your Roadmap",
             "Week-by-week plan with free resources and projects"),
        ]:
            with col:
                st.markdown(f"""
                <div class="metric-card" style="text-align:left;
                padding:1.4rem">
                    <div style="font-size:20px;margin-bottom:8px">
                    {icon}</div>
                    <div style="font-size:13px;font-weight:600;
                    color:#e6edf3;margin-bottom:4px">{title}</div>
                    <div style="font-size:12px;color:#484f58">{desc}</div>
                </div>
                """, unsafe_allow_html=True)

# ── COMPARE MODE ──────────────────────────────────────────────────────────────

else:
    st.markdown("""
    <div class="hero-title">🏫 College Comparison</div>
    <div class="hero-sub">Compare two colleges side by side
    for the same target role.</div>
    """, unsafe_allow_html=True)
    st.markdown('<hr style="margin:1.2rem 0">', unsafe_allow_html=True)

    if compare_btn:
        if not uploaded_1 or not uploaded_2:
            st.warning("Please upload both syllabus PDFs!")
        else:
            path1 = f"data/{uploaded_1.name}"
            path2 = f"data/{uploaded_2.name}"
            with open(path1, "wb") as f:
                f.write(uploaded_1.getbuffer())
            with open(path2, "wb") as f:
                f.write(uploaded_2.getbuffer())
            with st.spinner(
                f"Comparing {college_name_1} vs {college_name_2}..."
            ):
                compare_colleges(
                    path1, college_name_1,
                    path2, college_name_2,
                    compare_role
                )
            st.success("Comparison complete!")

    try:
        comp = load_comparison()
        r    = comp["results"]
        n1   = comp["college_1"]
        n2   = comp["college_2"]
        role = comp["role_group"]
        winner = comp["winner"]

        # Winner banner
        if winner["college"] == "Tie":
            st.markdown(f"""
            <div style="background:#161b22;border:1px solid #21262d;
            border-radius:12px;padding:1.2rem;text-align:center;
            margin-bottom:1.5rem">
                <div style="font-size:14px;color:#e6edf3;font-weight:600">
                🤝 It's a tie! Both score {winner['score']}%
                for {role} roles</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="compare-winner">
                <div style="font-size:12px;color:#484f58;
                text-transform:uppercase;letter-spacing:.06em;
                margin-bottom:6px">Winner for {role} roles</div>
                <div style="font-size:20px;font-weight:700;
                color:#3fb950">{winner['college']} 🏆</div>
                <div style="font-size:13px;color:#484f58;margin-top:4px">
                {winner['score']}% coverage
                · {winner['margin']}% ahead</div>
            </div>
            """, unsafe_allow_html=True)

        # Side by side
        col1, col2 = st.columns(2)

        for col, name in [(col1, n1), (col2, n2)]:
            data      = r[name]
            is_winner = winner["college"] == name
            border    = "#3fb950" if is_winner else "#21262d"

            with col:
                st.markdown(f"""
                <div class="compare-card" style="border-color:{border}">
                    <div style="font-size:15px;font-weight:600;
                    color:#e6edf3;margin-bottom:14px">
                    {name} {"🏆" if is_winner else ""}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                m1, m2, m3 = st.columns(3)
                with m1:
                    st.metric("Coverage", f"{data['coverage_score']}%")
                with m2:
                    st.metric("Covered", data['covered_count'])
                with m3:
                    st.metric("Missing", data['gap_count'])

                st.markdown("<br>", unsafe_allow_html=True)

                if data["top_gaps"]:
                    st.markdown(
                        '<div style="font-size:11px;font-weight:500;'
                        'color:#484f58;text-transform:uppercase;'
                        'letter-spacing:.06em;margin-bottom:6px">'
                        'Top Gaps</div>',
                        unsafe_allow_html=True
                    )
                    for g in data["top_gaps"]:
                        st.markdown(f"""
                        <div class="gap-badge" style="font-size:12px">
                            <span>{g['skill']}</span>
                            <span class="gap-badge-pct">
                            {g['demand']}%</span>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style="background:#0d1a0f;
                    border:1px solid #1a4a20;border-radius:8px;
                    padding:10px;color:#3fb950;font-size:12px">
                    🎉 No gaps!</div>
                    """, unsafe_allow_html=True)

        st.markdown('<hr style="margin:2rem 0">', unsafe_allow_html=True)

        # Common gaps
        if comp["common_gaps"]:
            st.markdown(
                '<div class="section-header">⚠️ Common Gaps</div>'
                '<div class="section-sub">'
                'Skills missing in BOTH colleges</div>',
                unsafe_allow_html=True
            )
            cols = st.columns(min(len(comp["common_gaps"]), 4))
            for i, gap in enumerate(comp["common_gaps"]):
                with cols[i % 4]:
                    st.markdown(f"""
                    <div class="common-gap">
                        <span>{gap['skill']}</span>
                        <span>{gap['demand']}% of JDs</span>
                    </div>
                    """, unsafe_allow_html=True)
            st.markdown(
                '<hr style="margin:2rem 0">', unsafe_allow_html=True
            )

        # Unique gaps
        unique = comp["unique_gaps"]
        if unique.get(n1) or unique.get(n2):
            st.markdown(
                '<div class="section-header">🔍 Unique Gaps</div>'
                '<div class="section-sub">'
                'Skills one college misses but the other covers</div>',
                unsafe_allow_html=True
            )
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(
                    f'<div style="font-size:13px;font-weight:500;'
                    f'color:#e6edf3;margin-bottom:8px">'
                    f'Only missing in {n1}</div>',
                    unsafe_allow_html=True
                )
                if unique.get(n1):
                    for g in unique[n1]:
                        st.markdown(f"""
                        <div class="gap-badge" style="font-size:12px">
                            <span>{g['skill']}</span>
                            <span class="gap-badge-pct">
                            {g['demand']}%</span>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown(
                        '<div style="font-size:12px;color:#484f58">'
                        'No unique gaps</div>',
                        unsafe_allow_html=True
                    )
            with col2:
                st.markdown(
                    f'<div style="font-size:13px;font-weight:500;'
                    f'color:#e6edf3;margin-bottom:8px">'
                    f'Only missing in {n2}</div>',
                    unsafe_allow_html=True
                )
                if unique.get(n2):
                    for g in unique[n2]:
                        st.markdown(f"""
                        <div class="gap-badge" style="font-size:12px">
                            <span>{g['skill']}</span>
                            <span class="gap-badge-pct">
                            {g['demand']}%</span>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown(
                        '<div style="font-size:12px;color:#484f58">'
                        'No unique gaps</div>',
                        unsafe_allow_html=True
                    )

        # Score bar chart
        st.markdown('<hr style="margin:2rem 0">', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-header">Score Comparison</div>'
            '<div class="section-sub">'
            'Coverage score side by side</div>',
            unsafe_allow_html=True
        )
        fig3 = go.Figure(data=[
            go.Bar(
                x=[n1, n2],
                y=[r[n1]["coverage_score"], r[n2]["coverage_score"]],
                marker_color=[
                    "#3fb950" if r[n1]["coverage_score"] >=
                    r[n2]["coverage_score"] else "#58a6ff",
                    "#3fb950" if r[n2]["coverage_score"] >
                    r[n1]["coverage_score"] else "#58a6ff",
                ],
                marker_line_width=0,
                text=[
                    f"{r[n1]['coverage_score']}%",
                    f"{r[n2]['coverage_score']}%"
                ],
                textposition="outside",
                textfont=dict(color="#e6edf3", size=14)
            )
        ])
        fig3.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#8b949e", size=12),
            height=300,
            margin=dict(l=0, r=0, t=30, b=0),
            yaxis=dict(
                range=[0, 110],
                gridcolor="#21262d",
                zerolinecolor="#21262d"
            ),
            xaxis=dict(gridcolor="rgba(0,0,0,0)"),
        )
        st.plotly_chart(fig3, use_container_width=True)

    except FileNotFoundError:
        st.markdown("""
        <div style="background:#161b22;border:1px solid #21262d;
        border-radius:12px;padding:2rem;text-align:center">
            <div style="font-size:32px;margin-bottom:12px">🏫</div>
            <div style="font-size:14px;font-weight:600;color:#e6edf3;
            margin-bottom:6px">Compare Two Colleges</div>
            <div style="font-size:12px;color:#484f58">
            Upload two syllabus PDFs, pick a target role,<br>
            and see how they compare side by side.</div>
        </div>
        """, unsafe_allow_html=True)