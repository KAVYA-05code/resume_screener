"""
Explainable AI-Based Resume Screening and Job Matching System
FINAL BUILD (100%)

Stage 1 (30%): keyword skill matching, basic dashboard
Stage 2 (70%): PDF upload, semantic similarity, combined score, explanation,
               job recommendations
Stage 3 (100% — this file): login & roles (Student / Recruiter), advanced
               synonym-aware skill extraction, experience-aware confidence,
               skill knowledge graph, personalized learning recommendations,
               bias-aware / blind-review mode, recruiter multi-candidate
               dashboard, downloadable PDF reports, bright floral UI.
"""

import os
import streamlit as st
import pandas as pd

from modules.pdf_utils import extract_pdf_text, PDFExtractionError
from modules.skill_utils import match_skills, SKILL_DATABASE
from modules.advanced_skills import extract_skills_advanced
from modules.experience_analysis import split_resume_sections, compute_experience_confidence
from modules.knowledge_graph import get_related_skills
from modules.learning_recommendations import get_learning_recommendations
from modules.bias_utils import redact_sensitive_info, anonymize_candidate_label, FAIRNESS_STATEMENT
from modules.semantic_utils import get_semantic_score
from modules.scoring import compute_final_score, categorize_score
from modules.explanation import generate_explanation
from modules.job_matching import load_jobs, recommend_jobs
from modules.report_generator import build_pdf_report
from modules.theme import get_custom_css
from modules import auth

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JOBS_CSV_PATH = os.path.join(BASE_DIR, "data", "job_descriptions.csv")

st.set_page_config(
    page_title="SkillMatch AI — Resume Screening & Job Matching",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(get_custom_css(), unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# HELPERS
# ----------------------------------------------------------------------------
def get_job_titles():
    if os.path.exists(JOBS_CSV_PATH):
        return load_jobs(JOBS_CSV_PATH)["title"].tolist()
    return ["General Role"]


def analyze_resume(resume_text: str, job_description: str, required_skills: list) -> dict:
    """Run the full 100% pipeline on one resume against one job."""
    detected_map = extract_skills_advanced(resume_text)
    detected_skills = sorted(detected_map.keys())

    sections = split_resume_sections(resume_text)
    confidence = compute_experience_confidence(detected_skills, sections)

    skill_result = match_skills(detected_skills, required_skills)
    semantic_score = get_semantic_score(resume_text, job_description)
    final_score = compute_final_score(skill_result["skill_score"], semantic_score)
    category = categorize_score(final_score)
    explanation = generate_explanation(
        final_score, skill_result["matching_skills"], skill_result["missing_skills"]
    )
    related_skills = get_related_skills(detected_skills)
    learning_recs = get_learning_recommendations(skill_result["missing_skills"])

    return {
        "detected_skills": detected_skills,
        "detection_sources": detected_map,
        "confidence": confidence,
        "skill_score": skill_result["skill_score"],
        "matching_skills": skill_result["matching_skills"],
        "missing_skills": skill_result["missing_skills"],
        "semantic_score": semantic_score,
        "final_score": final_score,
        "category": category,
        "explanation": explanation,
        "related_skills": related_skills,
        "learning_recommendations": learning_recs,
    }


def metric_card(col, label, value, css_class):
    col.markdown(
        f"""
        <div class="metric-card {css_class}">
            <div class="label">{label}</div>
            <div class="value">{value}%</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def skill_pills(skills, css_class):
    if not skills:
        return "<span style='color:#9CA3AF;'>None</span>"
    return "".join(f'<span class="pill {css_class}">{s}</span>' for s in skills)


# ----------------------------------------------------------------------------
# LOGIN GATE
# ----------------------------------------------------------------------------
if not auth.is_authenticated():
    auth.render_login(get_job_titles())
    st.stop()

# ----------------------------------------------------------------------------
# SESSION STATE DEFAULTS
# ----------------------------------------------------------------------------
st.session_state.setdefault("resume_text", "")
st.session_state.setdefault("resume_filename", "")
st.session_state.setdefault("analysis_result", None)
st.session_state.setdefault("recommendations", None)
st.session_state.setdefault("candidate_results", [])

user_role = st.session_state.user_role
user_name = st.session_state.user_name
is_student = user_role == auth.ROLE_STUDENT

# ----------------------------------------------------------------------------
# SIDEBAR
# ----------------------------------------------------------------------------
with st.sidebar:
    st.markdown(f"### 🌸 Hi, {user_name.split()[0]}!")
    st.caption(user_role)

    if is_student:
        pages = ["🏠 Home", "📄 Upload & Analyze", "🎯 Job Recommendations", "📚 Learning Path", "ℹ️ About"]
    else:
        pages = ["🏠 Home", "🧑‍💼 Recruiter Dashboard", "ℹ️ About"]

    page = st.radio("Navigate", pages, label_visibility="collapsed")

    st.markdown("---")
    blind_mode = st.toggle("🕶️ Blind / Bias-Aware Mode", value=False,
                            help="Hides personal identifiers (name, email, phone, age, gender) from resume text and candidate labels.")
    st.markdown("---")
    if st.button("🚪 Log out", use_container_width=True):
        auth.logout()
        st.rerun()

# ----------------------------------------------------------------------------
# HEADER
# ----------------------------------------------------------------------------
st.markdown(
    """
    <div class="app-header">
        <h1>🌸 SkillMatch AI — Explainable Resume Screening &amp; Job Matching</h1>
        <p>Advanced skill detection, experience-aware confidence, knowledge-graph
        suggestions, learning paths, bias-aware review, and recruiter tools — all in one place.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================================
# HOME
# ============================================================================
if page == "🏠 Home":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    if is_student:
        target = st.session_state.user_context.get("target_role", "your target role")
        st.markdown(f"#### 👋 Welcome, {user_name}!")
        st.write(
            f"You're set up as a **Student / Job Seeker** targeting **{target}**. "
            "Head to **Upload & Analyze** to check how your resume matches a job, "
            "see your skill gaps, get related-skill suggestions, and a personalized learning path."
        )
    else:
        company = st.session_state.user_context.get("company_name", "your organization")
        st.markdown(f"#### 👋 Welcome, {user_name}!")
        st.write(
            f"You're set up as a **Recruiter** at **{company or 'your organization'}**. "
            "Head to the **Recruiter Dashboard** to upload multiple candidate resumes, "
            "rank them against a job description, and export reports."
        )
    st.markdown("</div>", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    metric_card(c1, "Skill DB Size", len(SKILL_DATABASE), "grad-pink")
    metric_card(c2, "Saved Job Roles", len(get_job_titles()), "grad-orange")
    metric_card(c3, "Synonyms Mapped", 30, "grad-teal")
    metric_card(c4, "Pipeline Stages", 100, "grad-purple")

# ============================================================================
# STUDENT: UPLOAD & ANALYZE
# ============================================================================
elif page == "📄 Upload & Analyze":
    col_left, col_right = st.columns([1, 1.2], gap="large")

    with col_left:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### 📄 Step 1 — Upload Resume (PDF)")
        uploaded_resume = st.file_uploader("Upload Resume", type=["pdf"], label_visibility="collapsed")

        if uploaded_resume is not None:
            try:
                resume_text = extract_pdf_text(uploaded_resume)
                st.session_state.resume_text = resume_text
                st.session_state.resume_filename = uploaded_resume.name
                st.success(f"✅ Extracted text from **{uploaded_resume.name}**")
            except PDFExtractionError as e:
                st.session_state.resume_text = ""
                st.session_state.resume_filename = ""
                st.error(f"⚠️ {e}")

        if st.session_state.resume_text:
            display_text = (
                redact_sensitive_info(st.session_state.resume_text)
                if blind_mode else st.session_state.resume_text
            )
            with st.expander("View extracted resume text" + (" (blinded)" if blind_mode else "")):
                st.text_area("Extracted Resume Text", display_text, height=180, label_visibility="collapsed")

        if blind_mode:
            st.markdown(f'<div class="fairness-note">🕶️ {FAIRNESS_STATEMENT}</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### 💼 Step 2 — Job Description")
        job_source = st.radio("Job description source",
                               ["Select from saved roles", "Paste custom job description"], horizontal=True)

        job_title, job_description, required_skills = "Custom Job", "", SKILL_DATABASE
        if job_source == "Select from saved roles" and os.path.exists(JOBS_CSV_PATH):
            jobs_df = load_jobs(JOBS_CSV_PATH)
            default_idx = 0
            target = st.session_state.user_context.get("target_role")
            if target in jobs_df["title"].tolist():
                default_idx = jobs_df["title"].tolist().index(target)
            job_title = st.selectbox("Choose a job role", jobs_df["title"].tolist(), index=default_idx)
            row = jobs_df[jobs_df["title"] == job_title].iloc[0]
            job_description = row["description"]
            required_skills = [s.strip() for s in row["required_skills"].split(",")]
            st.caption(job_description)
        else:
            job_title = st.text_input("Job title", value="Custom Job")
            job_description = st.text_area("Paste job description text", height=140,
                                            placeholder="e.g. Looking for a Python developer with SQL and ML experience...")
            skills_input = st.text_input("Required skills (comma-separated)",
                                          placeholder="Python, SQL, Machine Learning, Git")
            if skills_input:
                required_skills = [s.strip() for s in skills_input.split(",") if s.strip()]
        st.markdown("</div>", unsafe_allow_html=True)

        analyze_clicked = st.button("🔍 Analyze Resume", type="primary", use_container_width=True)

    with col_right:
        if analyze_clicked:
            if not st.session_state.resume_text:
                st.warning("Please upload a readable PDF resume first.")
            elif not job_description.strip():
                st.warning("Please provide or select a job description first.")
            else:
                with st.spinner("Running advanced skill extraction, experience analysis, and semantic matching..."):
                    result = analyze_resume(st.session_state.resume_text, job_description, required_skills)
                    result["job_title"] = job_title
                st.session_state.analysis_result = result

        result = st.session_state.analysis_result
        if result:
            st.markdown(f"#### 📊 Results — {result['job_title']}")

            m1, m2, m3 = st.columns(3)
            metric_card(m1, "Skill Match", result["skill_score"], "grad-pink")
            metric_card(m2, "Semantic Similarity", result["semantic_score"], "grad-orange")
            metric_card(m3, "Final Score", result["final_score"], "grad-teal")

            cat_class = {"Strong Match": "cat-strong", "Moderate Match": "cat-moderate", "Low Match": "cat-low"}[result["category"]]
            st.markdown(f'<div style="margin:1rem 0;">Category: <span class="category-badge {cat_class}">{result["category"]}</span></div>', unsafe_allow_html=True)

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("##### ✅ Matching Skills")
            st.markdown(skill_pills(result["matching_skills"], "pill-green"), unsafe_allow_html=True)
            st.markdown("##### ❌ Missing Skills")
            st.markdown(skill_pills(result["missing_skills"], "pill-red"), unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("##### 🧪 Experience-Aware Confidence")
            st.caption("Skills confirmed by Projects/Experience sections score higher confidence than those only listed.")
            for skill, info in result["confidence"].items():
                icon = "🟢" if info["used_in_practice"] else "🟡"
                st.markdown(f"{icon} **{skill}** — weight `{info['weight']}` — {info['note']}")
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("##### 🕸️ Related Skills (Knowledge Graph)")
            st.caption("Adjacent skills often paired with what you already have — consider adding these.")
            st.markdown(skill_pills(result["related_skills"], "pill-purple"), unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("##### 🧠 Explanation")
            st.write(result["explanation"])
            st.markdown("</div>", unsafe_allow_html=True)

            report_bytes = build_pdf_report({
                "candidate_name": user_name,
                "job_title": result["job_title"],
                "skill_score": result["skill_score"],
                "semantic_score": result["semantic_score"],
                "final_score": result["final_score"],
                "category": result["category"],
                "matching_skills": result["matching_skills"],
                "missing_skills": result["missing_skills"],
                "explanation": result["explanation"],
                "related_skills": result["related_skills"],
                "learning_recommendations": result["learning_recommendations"],
                "blind_mode": blind_mode,
            })
            st.download_button(
                "⬇️ Download PDF Report", data=report_bytes,
                file_name=f"{user_name.replace(' ', '_')}_match_report.pdf",
                mime="application/pdf", use_container_width=True,
            )
        else:
            st.info("Upload a resume and job description, then click **Analyze Resume** to see results here.")

# ============================================================================
# STUDENT: JOB RECOMMENDATIONS
# ============================================================================
elif page == "🎯 Job Recommendations":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("#### 🎯 Job Role Recommendations")
    st.write("Compares your uploaded resume against every saved job description using semantic similarity.")
    st.markdown("</div>", unsafe_allow_html=True)

    if not st.session_state.resume_text:
        st.warning("Please upload a resume on the **Upload & Analyze** page first.")
    else:
        if st.button("🔁 Generate Recommendations", type="primary"):
            with st.spinner("Scoring resume against all saved job roles..."):
                jobs_df = load_jobs(JOBS_CSV_PATH)
                st.session_state.recommendations = recommend_jobs(st.session_state.resume_text, jobs_df)

        if st.session_state.recommendations is not None:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("##### 🏆 Ranked Job Roles")
            st.dataframe(st.session_state.recommendations, use_container_width=True)
            top = st.session_state.recommendations.iloc[0]
            st.success(f"Best-fit role: **{top['Job Role']}** ({top['Match Score (%)']}% match)")
            st.markdown("</div>", unsafe_allow_html=True)

# ============================================================================
# STUDENT: LEARNING PATH
# ============================================================================
elif page == "📚 Learning Path":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("#### 📚 Personalized Learning Path")
    st.write("Based on your last analysis, here's what to learn next to close your skill gaps.")
    st.markdown("</div>", unsafe_allow_html=True)

    result = st.session_state.analysis_result
    if not result:
        st.info("Run an analysis on the **Upload & Analyze** page first to get a learning path.")
    elif not result["missing_skills"]:
        st.success("🎉 No missing skills detected for your last analysis — great coverage!")
    else:
        for rec in result["learning_recommendations"]:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(f"##### 🎯 {rec['Skill']}")
            st.markdown(f"**Course:** {rec['Course']}")
            st.markdown(f"**Project idea:** {rec['Project']}")
            st.markdown(f"**Link:** {rec['Link']}")
            st.markdown("</div>", unsafe_allow_html=True)

# ============================================================================
# RECRUITER DASHBOARD
# ============================================================================
elif page == "🧑‍💼 Recruiter Dashboard":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("#### 🧑‍💼 Multi-Candidate Screening")
    st.write("Upload multiple resumes, pick a job, and get a ranked, explainable comparison table.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    jobs_df = load_jobs(JOBS_CSV_PATH) if os.path.exists(JOBS_CSV_PATH) else pd.DataFrame()
    default_job = st.session_state.user_context.get("hiring_for")
    job_titles_list = jobs_df["title"].tolist() if not jobs_df.empty else []
    default_idx = job_titles_list.index(default_job) if default_job in job_titles_list else 0
    job_title = st.selectbox("Job role to screen for", job_titles_list, index=default_idx if job_titles_list else 0)

    if job_titles_list:
        row = jobs_df[jobs_df["title"] == job_title].iloc[0]
        job_description = row["description"]
        required_skills = [s.strip() for s in row["required_skills"].split(",")]
        st.caption(job_description)
    else:
        job_description, required_skills = "", SKILL_DATABASE

    uploaded_resumes = st.file_uploader("Upload candidate resumes (PDF, multiple allowed)",
                                         type=["pdf"], accept_multiple_files=True)
    run_screening = st.button("🚀 Screen Candidates", type="primary", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if run_screening:
        if not uploaded_resumes:
            st.warning("Please upload at least one candidate resume.")
        else:
            candidate_results = []
            with st.spinner(f"Screening {len(uploaded_resumes)} candidate(s)..."):
                for idx, file in enumerate(uploaded_resumes):
                    try:
                        text = extract_pdf_text(file)
                    except PDFExtractionError as e:
                        st.error(f"⚠️ {file.name}: {e}")
                        continue
                    result = analyze_resume(text, job_description, required_skills)
                    result["filename"] = file.name
                    result["resume_text"] = text
                    result["label"] = anonymize_candidate_label(idx) if blind_mode else file.name
                    candidate_results.append(result)

            candidate_results.sort(key=lambda r: r["final_score"], reverse=True)
            st.session_state.candidate_results = candidate_results

    if st.session_state.candidate_results:
        if blind_mode:
            st.markdown(f'<div class="fairness-note">🕶️ {FAIRNESS_STATEMENT}</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("##### 🏆 Candidate Comparison")
        table_rows = [{
            "Candidate": r["label"],
            "Final Score (%)": r["final_score"],
            "Skill Score (%)": r["skill_score"],
            "Semantic (%)": r["semantic_score"],
            "Matching Skills": ", ".join(r["matching_skills"]) or "—",
            "Missing Skills": ", ".join(r["missing_skills"]) or "—",
            "Category": r["category"],
        } for r in st.session_state.candidate_results]
        st.dataframe(pd.DataFrame(table_rows), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        for r in st.session_state.candidate_results:
            with st.expander(f"🔎 View details — {r['label']} ({r['final_score']}%)"):
                st.markdown(f"**Category:** {r['category']}")
                st.markdown("**Matching Skills:** " + (", ".join(r["matching_skills"]) or "None"))
                st.markdown("**Missing Skills:** " + (", ".join(r["missing_skills"]) or "None"))
                st.markdown("**Related Skills (Knowledge Graph):** " + (", ".join(r["related_skills"]) or "None"))
                st.markdown("**Explanation:** " + r["explanation"])

                if r["learning_recommendations"]:
                    st.markdown("**Suggested learning for missing skills:**")
                    for rec in r["learning_recommendations"]:
                        st.markdown(f"- *{rec['Skill']}* — {rec['Course']} ({rec['Link']})")

                report_bytes = build_pdf_report({
                    "candidate_name": r["label"],
                    "job_title": job_title,
                    "skill_score": r["skill_score"],
                    "semantic_score": r["semantic_score"],
                    "final_score": r["final_score"],
                    "category": r["category"],
                    "matching_skills": r["matching_skills"],
                    "missing_skills": r["missing_skills"],
                    "explanation": r["explanation"],
                    "related_skills": r["related_skills"],
                    "learning_recommendations": r["learning_recommendations"],
                    "blind_mode": blind_mode,
                })
                st.download_button(
                    f"⬇️ Download report — {r['label']}", data=report_bytes,
                    file_name=f"{r['label'].replace(' ', '_')}_report.pdf",
                    mime="application/pdf", key=f"dl_{r['label']}_{r['filename']}",
                )

# ============================================================================
# ABOUT
# ============================================================================
else:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("#### ℹ️ About This System — Final Build (100%)")
    st.write("This is the completed build of the Explainable AI-Based Resume Screening and Job Matching System.")

    st.markdown("##### Stage 1 (30%) — Baseline")
    st.markdown("- Resume/JD text input, cleaning, keyword skill extraction & matching, basic dashboard")

    st.markdown("##### Stage 2 (70%) — Intelligence layer")
    st.markdown(
        "- PDF resume upload & extraction\n"
        "- Semantic similarity (Sentence Transformers)\n"
        "- Combined weighted score, explainable output\n"
        "- Job-role recommendations"
    )

    st.markdown("##### Stage 3 (100%) — This final build")
    st.markdown(
        "- Login & role-based experience (Student vs. Recruiter)\n"
        "- Advanced synonym-aware skill extraction\n"
        "- Experience-aware confidence (Skills-list-only vs. used in Projects/Experience)\n"
        "- Skill knowledge graph with related-skill suggestions\n"
        "- Personalized learning recommendations (course, project, link)\n"
        "- Bias-aware / blind-review mode (redacts personal identifiers)\n"
        "- Recruiter dashboard: multi-candidate upload, ranking, comparison table\n"
        "- Downloadable PDF match reports\n"
        "- Bright, floral-themed, professional UI"
    )

    st.markdown("##### Fairness Note")
    st.markdown(f'<div class="fairness-note">🕶️ {FAIRNESS_STATEMENT}</div>', unsafe_allow_html=True)

    st.markdown("##### Future work (beyond this mini-project scope)")
    st.markdown(
        "- Full fine-tuning of the embedding model on labeled resume-JD pairs\n"
        "- Larger, weighted skill knowledge graph\n"
        "- Formal statistical fairness audits\n"
    )
    st.markdown("</div>", unsafe_allow_html=True)
