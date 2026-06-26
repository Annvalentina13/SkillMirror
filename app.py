"""
SkillMirror — Streamlit Dashboard
Phase 4 — Premium UI Redesign
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
    /* Base */
    .stApp { background-color: #0d1117; }
    .block-container { padding: 2rem 2.5rem 2rem 2.5rem; }

    /* Hide Streamlit branding */
    #MainMenu, footer, header { visibility: hidden; }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0d1117;
        border-right: 1px solid #21262d;
    }
    [data-testid="stSidebar"] .block-container {
        padding: 2rem 1.2rem;
    }

    /* Typography */
    h1, h2, h3 { color: #e6edf3 !important; }
    p, li { color: #8b949e; }

    /* Metric cards */
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

    /* Role tag */
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

    /* Gap badges */
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

    /* Covered badges */
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

    /* Roadmap cards */
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
    .roadmap-project-title {
        font-size: 13px;
        font-weight: 600;
        color: #3fb950;
        margin-bottom: 4px;
    }
    .roadmap-project-desc {
        font-size: 12px;
        color: #8b949e;
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

    /* Divider */
    hr { border-color: #21262d !important; }

    /* Expander */
    .streamlit-expanderHeader {
        background: #161b22 !important;
        border: 1px solid #21262d !important;
        border-radius: 8px !important;
        color: #e6edf3 !important;
        font-size: 13px !important;
    }
    .streamlit-expanderContent {
        background: #0d1117 !important;
        border: 1px solid #21262d !important;
        border-top: none !important;
    }

    /* Buttons */
    .stButton > button {
        background: #238636 !important;
        color: #ffffff !important;
        border: 1px solid #2ea043 !important;
        border-radius: 6px !important;
        font-weight: 500 !important;
        padding: 0.5rem 1rem !important;
        width: 100% !important;
        transition: background 0.2s !important;
    }
    .stButton > button:hover {
        background: #2ea043 !important;
    }

    /* Inputs */
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

    /* File uploader */
    [data-testid="stFileUploader"] {
        background: #161b22 !important;
        border: 1px dashed #21262d !important;
        border-radius: 8px !important;
    }

    /* Role cards at bottom */
    .role-card {
        background: #161b22;
        border: 1px solid #21262d;
        border-radius: 8px;
        padding: 10px 14px;
        text-align: center;
        font-size: 12px;
        color: #8b949e;
    }

    /* Section headers */
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

    /* Hero */
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
</style>
""", unsafe_allow_html=True)

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

    st.markdown(
        '<div style="font-size:11px;font-weight:500;color:#484f58;'
        'text-transform:uppercase;letter-spacing:.06em;margin-bottom:8px">'
        'Setup</div>',
        unsafe_allow_html=True
    )

    uploaded = st.file_uploader(
        "Syllabus PDF",
        type=["pdf"],
        label_visibility="collapsed"
    )
    if not uploaded:
        st.markdown(
            '<div style="font-size:11px;color:#484f58;margin-top:-8px;'
            'margin-bottom:8px">Upload your syllabus PDF</div>',
            unsafe_allow_html=True
        )

    course_name = st.text_input(
        "Course name",
        value="SRM CI 2024",
        placeholder="e.g. SRM CI 2024"
    )

    st.markdown(
        '<div style="font-size:11px;font-weight:500;color:#484f58;'
        'text-transform:uppercase;letter-spacing:.06em;'
        'margin-top:16px;margin-bottom:8px">Target Role</div>',
        unsafe_allow_html=True
    )

    role_group = st.selectbox(
        "Role",
        options=[
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
        ],
        label_visibility="collapsed"
    )

    st.markdown("<br>", unsafe_allow_html=True)
    analyse_btn = st.button("Analyse →", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="border-top:1px solid #21262d;padding-top:16px">
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

# ── Load results ──────────────────────────────────────────────────────────────

def load_results():
    with open("data/gap_analysis.json") as f:
        gap = json.load(f)
    with open("data/syllabus_skills.json") as f:
        syllabus = json.load(f)
    with open("data/jd_skills.json") as f:
        jd = json.load(f)
    return gap, syllabus, jd

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

# ── Main dashboard ────────────────────────────────────────────────────────────

try:
    gap, syllabus, jd = load_results()

    summary      = gap["summary"]
    covered      = gap["covered"]
    gaps         = gap["gaps"]
    roadmap      = gap["roadmap"]
    current_role = jd.get("role_group", "Data & AI")

    # ── Hero ──────────────────────────────────────────────────────────────────

    col_hero, col_tag = st.columns([3, 1])
    with col_hero:
        st.markdown(f"""
        <div class="hero-title">🪞 SkillMirror</div>
        <div class="hero-sub">
        Know exactly what your syllabus is missing —
        before your first interview.</div>
        """, unsafe_allow_html=True)
    with col_tag:
        st.markdown(f"""
        <div style="text-align:right;padding-top:8px">
            <div class="role-tag">🎯 {current_role}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(
        '<hr style="margin:1.2rem 0">',
        unsafe_allow_html=True
    )

    # ── Metric cards ──────────────────────────────────────────────────────────

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

    # ── Heatmap + Roadmap ─────────────────────────────────────────────────────

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
            labels={"demand": "% of Job Descriptions", "skill": ""},
            height=max(400, len(all_skills) * 28)
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#8b949e", size=12),
            legend=dict(
                title="",
                orientation="h",
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
            '<div class="section-sub">Top skills by industry demand</div>',
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

    st.markdown(
        '<hr style="margin:2rem 0">',
        unsafe_allow_html=True
    )

    # ── Detailed Roadmap ──────────────────────────────────────────────────────

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
                    f'<b style="color:#e6edf3">Why this matters</b><br>'
                    f'{plan["why_it_matters"]}</div>',
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
                            Week {week['week']} — {week['focus']}</div>
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
                            f'<div style="font-size:12px;color:#8b949e;'
                            f'padding:4px 0">{icon} '
                            f'<a href="{res["url"]}" target="_blank" '
                            f'style="color:#58a6ff;text-decoration:none">'
                            f'{res["name"]}</a>'
                            f' <span style="color:#484f58">·</span> '
                            f'<span style="color:#484f58">'
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
                    <div class="roadmap-project-title">
                    {plan['project_to_build']['name']}</div>
                    <div class="roadmap-project-desc">
                    {plan['project_to_build']['description']}</div>
                    <div style="font-size:11px;color:#484f58;margin-top:6px">
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
            🎉 No gaps found — your syllabus covers everything
            industry wants for this role!
        </div>
        """, unsafe_allow_html=True)

    st.markdown(
        '<hr style="margin:2rem 0">',
        unsafe_allow_html=True
    )

    # ── Coverage by Category ──────────────────────────────────────────────────

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

    cats           = list(cat_data.keys())
    covered_counts = [cat_data[c]["covered"] for c in cats]
    gap_counts     = [cat_data[c]["gap"] for c in cats]

    fig2 = go.Figure(data=[
        go.Bar(
            name="Covered", x=cats, y=covered_counts,
            marker_color="#3fb950",
            marker_line_width=0
        ),
        go.Bar(
            name="Gap", x=cats, y=gap_counts,
            marker_color="#f85149",
            marker_line_width=0
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
            orientation="h",
            yanchor="bottom", y=1.02,
            xanchor="right", x=1
        ),
        xaxis=dict(gridcolor="rgba(0,0,0,0)"),
        yaxis=dict(gridcolor="#21262d", zerolinecolor="#21262d"),
    )
    st.plotly_chart(fig2, use_container_width=True)

    # ── Roles in analysis ─────────────────────────────────────────────────────

    st.markdown(
        '<hr style="margin:2rem 0">',
        unsafe_allow_html=True
    )
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
                st.markdown(f"""
                <div class="role-card">{role}</div>
                """, unsafe_allow_html=True)

except FileNotFoundError:
    # ── Empty state ───────────────────────────────────────────────────────────

    st.markdown("""
    <div class="hero-title">🪞 SkillMirror</div>
    <div class="hero-sub">Know exactly what your syllabus is missing
    — before your first interview.</div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<hr style="margin:1.5rem 0">',
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="metric-card" style="text-align:left;padding:1.4rem">
            <div style="font-size:20px;margin-bottom:8px">📄</div>
            <div style="font-size:13px;font-weight:600;color:#e6edf3;
            margin-bottom:4px">Upload Syllabus</div>
            <div style="font-size:12px;color:#484f58">
            Any engineering, medical, law, finance, or design syllabus PDF
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="metric-card" style="text-align:left;padding:1.4rem">
            <div style="font-size:20px;margin-bottom:8px">🎯</div>
            <div style="font-size:13px;font-weight:600;color:#e6edf3;
            margin-bottom:4px">Pick Target Role</div>
            <div style="font-size:12px;color:#484f58">
            12 domains — Data & AI, SWE, ECE, Medical, Law, Finance and more
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="metric-card" style="text-align:left;padding:1.4rem">
            <div style="font-size:20px;margin-bottom:8px">🗺️</div>
            <div style="font-size:13px;font-weight:600;color:#e6edf3;
            margin-bottom:4px">Get Your Roadmap</div>
            <div style="font-size:12px;color:#484f58">
            Week-by-week learning plan with free resources and projects
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div style="background:#161b22;border:1px solid #21262d;
    border-radius:12px;padding:1.5rem">
        <div style="font-size:13px;font-weight:600;color:#e6edf3;
        margin-bottom:12px">12 Domains Supported</div>
        <div style="display:flex;flex-wrap:wrap;gap:8px">
            <span style="background:#0d1117;border:1px solid #21262d;
            border-radius:20px;padding:4px 12px;font-size:12px;
            color:#8b949e">📊 Data & AI</span>
            <span style="background:#0d1117;border:1px solid #21262d;
            border-radius:20px;padding:4px 12px;font-size:12px;
            color:#8b949e">💻 Software Engineering</span>
            <span style="background:#0d1117;border:1px solid #21262d;
            border-radius:20px;padding:4px 12px;font-size:12px;
            color:#8b949e">☁️ Cloud & DevOps</span>
            <span style="background:#0d1117;border:1px solid #21262d;
            border-radius:20px;padding:4px 12px;font-size:12px;
            color:#8b949e">🔐 Cybersecurity</span>
            <span style="background:#0d1117;border:1px solid #21262d;
            border-radius:20px;padding:4px 12px;font-size:12px;
            color:#8b949e">⚡ ECE & Embedded</span>
            <span style="background:#0d1117;border:1px solid #21262d;
            border-radius:20px;padding:4px 12px;font-size:12px;
            color:#8b949e">⚙️ Mechanical</span>
            <span style="background:#0d1117;border:1px solid #21262d;
            border-radius:20px;padding:4px 12px;font-size:12px;
            color:#8b949e">🏗️ Civil</span>
            <span style="background:#0d1117;border:1px solid #21262d;
            border-radius:20px;padding:4px 12px;font-size:12px;
            color:#8b949e">💰 Finance & MBA</span>
            <span style="background:#0d1117;border:1px solid #21262d;
            border-radius:20px;padding:4px 12px;font-size:12px;
            color:#8b949e">🏥 Medical & Healthcare</span>
            <span style="background:#0d1117;border:1px solid #21262d;
            border-radius:20px;padding:4px 12px;font-size:12px;
            color:#8b949e">⚖️ Law</span>
            <span style="background:#0d1117;border:1px solid #21262d;
            border-radius:20px;padding:4px 12px;font-size:12px;
            color:#8b949e">🎨 Design & UX</span>
            <span style="background:#0d1117;border:1px solid #21262d;
            border-radius:20px;padding:4px 12px;font-size:12px;
            color:#8b949e">📢 Media & Marketing</span>
        </div>
    </div>
    """, unsafe_allow_html=True)