# SkillMatch AI — Explainable Resume Screening & Job Matching System

 🔗 **Live Demo:** https://kavya-05code-resume-screener-app-kwrwh0.streamlit.app/
A complete, explainable AI system that screens resumes against job
descriptions, with a bright, floral-themed UI, login + role selection
(Student vs. Recruiter), and bias-aware review tools.

## Folder structure
```
resume_screener/
├── app.py                         # Main Streamlit app (login + role-based navigation)
├── requirements.txt
├── .streamlit/
│   └── config.toml                # Base theme colors
├── data/
│   └── job_descriptions.csv       # Saved job roles (title, description, required_skills)
└── modules/
    ├── auth.py                    # Session-based login & role capture
    ├── theme.py                   # Bright CSS + floral SVG background
    ├── pdf_utils.py                # PDF upload/extraction + error handling
    ├── skill_utils.py              # Base skill database + match_skills()
    ├── advanced_skills.py          # Synonym-aware skill detection
    ├── experience_analysis.py      # Skills-list-only vs. used-in-practice weighting
    ├── knowledge_graph.py          # Related-skill suggestions
    ├── learning_recommendations.py # Course/project/link per missing skill
    ├── bias_utils.py               # Redaction + fairness statement + candidate anonymizing
    ├── semantic_utils.py           # Sentence-Transformer cosine similarity
    ├── scoring.py                  # Weighted combined score + category
    ├── explanation.py              # Explainable-AI text generation
    ├── job_matching.py             # Multi-job ranking
    └── report_generator.py         # Downloadable PDF report (fpdf2)
```

## Setup

```bash
cd resume_screener
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
streamlit run app.py
```

## Using the app

1. **Login** — enter your name and choose **Student / Job Seeker** or
   **Recruiter / Hiring Manager**. Students are asked their target role and
   experience level; recruiters are asked their company and which role
   they're hiring for. *(This is a lightweight, session-based login for demo
   purposes — no password database. Swap in real auth for production.)*

2. **Student flow**
   - **Upload & Analyze** — upload a PDF resume, pick/paste a job
     description, click **Analyze Resume** to see: skill score, semantic
     score, final score, category, matching/missing skills,
     experience-aware confidence per skill, related skills from the
     knowledge graph, an explanation, and a **Download PDF Report** button.
   - **Job Recommendations** — ranks your resume against every saved job role.
   - **Learning Path** — course/project/link suggestions for each missing skill.

3. **Recruiter flow**
   - **Recruiter Dashboard** — pick a job role, upload multiple candidate
     resumes at once, click **Screen Candidates** to get a ranked comparison
     table (final score, skill score, semantic score, matching/missing
     skills, category). Expand **View Details** per candidate for the full
     explanation, related skills, learning suggestions, and a per-candidate
     downloadable PDF report.

4. **Blind / Bias-Aware Mode** (sidebar toggle) — redacts emails, phone
   numbers, ages, gender/marital-status mentions, and addresses from
   displayed resume text, and anonymizes candidate names in the recruiter
   comparison table to "Candidate A/B/C...". A fairness statement is shown
   in the UI and included in generated reports.

## Customizing
- Add/edit job roles in `data/job_descriptions.csv`.
- Extend `modules/advanced_skills.SKILL_SYNONYMS` for more indirect skill phrases.
- Extend `modules/knowledge_graph.SKILL_GRAPH` for more related-skill mappings.
- Extend `modules/learning_recommendations.LEARNING_RESOURCES` for more courses/links.
- Adjust scoring weights in `modules/scoring.py`.
- Change colors/floral pattern in `modules/theme.py`.


