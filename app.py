"""
SkillMirror — Streamlit Dashboard
Module 4 of 4 — Phase 2 (Multi-role support)
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

# ── Page config ───────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="SkillMirror",
    page_icon="🪞",
    layout="wide"
)

# ── Styling ───────────────────────────────────────────────────────────────────

st.markdown("""
<style>
    .main { background-color: #0f1117; }
    .metric-card {
        background: #1e2130;
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        border: 1px solid #2d3250;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #7c6ee0;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #8b8fa8;
        margin-top: 4px;
    }
    .gap-badge {
        background: #ff4b4b22;
        border: 1px solid #ff4b4b55;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        color: #ff4b4b;
        margin: 4px 0;
    }
    .covered-badge {
        background: #00c85322;
        border: 1px solid #00c85355;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        color: #00c853;
        margin: 4px 0;
    }
    .role-tag {
        background: #7c6ee022;
        border: 1px solid #7c6ee055;
        border-radius: 6px;
        padding: 3px 10px;
        color: #7c6ee0;
        font-size: 12px;
        display: inline-block;
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────

st.markdown("# 🪞 SkillMirror")
st.markdown("#### Know exactly what your syllabus is missing — before your first interview.")
st.divider()

# ── Sidebar ───────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("### ⚙️ Setup")
    uploaded = st.file_uploader(
        "Upload your syllabus PDF",
        type=["pdf"]
    )
    course_name = st.text_input(
        "Course name",
        value="SRM CI 2024"
    )

    st.markdown("### 🎯 Target Role")
    role_group = st.selectbox(
        "What jobs are you targeting?",
        options=[
            "Data & AI",
            "Software Engineering",
            "Cloud & DevOps",
            "Cybersecurity",
            "ECE & Embedded",
            "Mechanical",
            "Civil",
        ]
    )

    analyse_btn = st.button("🔍 Analyse", use_container_width=True)
    st.divider()
    st.markdown("### 📌 How it works")
    st.markdown("""
    1. Upload your syllabus PDF
    2. Pick your target role
    3. We compare against real JDs
    4. See exactly what to learn
    """)

# ── Load existing results or run analysis ─────────────────────────────────────

def load_results():
    with open("data/gap_analysis.json") as f:
        gap = json.load(f)
    with open("data/syllabus_skills.json") as f:
        syllabus = json.load(f)
    with open("data/jd_skills.json") as f:
        jd = json.load(f)
    return gap, syllabus, jd

if analyse_btn and uploaded:
    # Save uploaded PDF
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

# ── Main dashboard ────────────────────────────────────────────────────────────

try:
    gap, syllabus, jd = load_results()

    summary = gap["summary"]
    covered = gap["covered"]
    gaps    = gap["gaps"]
    roadmap = gap["roadmap"]

    # Show current role group tag
    current_role = jd.get("role_group", "Data & AI")
    st.markdown(f'<div class="role-tag">🎯 Analysed for: {current_role}</div>',
                unsafe_allow_html=True)

    # ── Metric cards ──────────────────────────────────────────────────────────

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{summary['coverage_score']}%</div>
            <div class="metric-label">Coverage Score</div>
        </div>""", unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{summary['covered_count']}</div>
            <div class="metric-label">Skills Covered</div>
        </div>""", unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color:#ff4b4b">{summary['gap_count']}</div>
            <div class="metric-label">Skills Missing</div>
        </div>""", unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{summary['industry_skills_count']}</div>
            <div class="metric-label">Industry Skills Tracked</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Two column layout ─────────────────────────────────────────────────────

    left, right = st.columns([1.2, 1])

    with left:
        st.markdown("### 📊 Skills Heatmap")

        all_skills = (
            [{"skill": s["skill"], "demand": s["demand"],
              "status": "✅ Covered"} for s in covered] +
            [{"skill": s["skill"], "demand": s["demand"],
              "status": "❌ Gap"} for s in gaps]
        )
        df = pd.DataFrame(all_skills).sort_values("demand", ascending=True)

        fig = px.bar(
            df,
            x="demand",
            y="skill",
            color="status",
            orientation="h",
            color_discrete_map={
                "✅ Covered": "#00c853",
                "❌ Gap": "#ff4b4b"
            },
            labels={"demand": "% of Job Descriptions", "skill": ""},
            height=600
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#c9d1d9",
            legend_title_text="",
            margin=dict(l=0, r=0, t=10, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.markdown("### 🗺️ Your Learning Roadmap")
        st.caption(f"Skills missing from your syllabus for {current_role} roles")

        if roadmap:
            for i, skill in enumerate(roadmap, 1):
                st.markdown(f"""
                <div class="gap-badge">
                    <b>#{i} {skill['skill']}</b>
                    — appears in {skill['demand']}% of JDs
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("🎉 No gaps! Your syllabus covers everything.")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### ✅ What You're Already Good At")
        st.caption("Top covered skills by industry demand")

        for skill in covered[:8]:
            st.markdown(f"""
            <div class="covered-badge">
                ✓ <b>{skill['skill']}</b> — {skill['demand']}% of JDs
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # ── Category breakdown ────────────────────────────────────────────────────

    st.markdown("### 🗂️ Coverage by Category")

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
    covered_counts = [cat_data[c]["covered"] for c in cats]
    gap_counts     = [cat_data[c]["gap"] for c in cats]

    fig2 = go.Figure(data=[
        go.Bar(name="Covered", x=cats, y=covered_counts,
               marker_color="#00c853"),
        go.Bar(name="Gap",     x=cats, y=gap_counts,
               marker_color="#ff4b4b")
    ])
    fig2.update_layout(
        barmode="stack",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#c9d1d9",
        height=300,
        margin=dict(l=0, r=0, t=10, b=0)
    )
    st.plotly_chart(fig2, use_container_width=True)

    # ── Roles covered ─────────────────────────────────────────────────────────

    st.divider()
    st.markdown("### 💼 Roles in this Analysis")
    roles = jd.get("roles_covered", [])
    cols = st.columns(len(roles))
    for i, role in enumerate(roles):
        with cols[i]:
            st.markdown(f"""
            <div class="metric-card" style="padding:0.8rem">
                <div style="font-size:13px;color:#c9d1d9">{role}</div>
            </div>""", unsafe_allow_html=True)

except FileNotFoundError:
    st.info("👈 Upload your syllabus PDF, pick your target role and click Analyse!")
    st.markdown("""
    ### What SkillMirror does
    - 📄 Parses your syllabus PDF
    - 🎯 Compares against your target role's JDs
    - 📊 Shows you the exact skills gap
    - 🗺️ Gives you a prioritised learning roadmap
    
    ### Supported roles
    - 📊 Data & AI
    - 💻 Software Engineering
    - ☁️ Cloud & DevOps
    - 🔐 Cybersecurity
    - ⚡ ECE & Embedded
    - ⚙️ Mechanical
    - 🏗️ Civil
    """)