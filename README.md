# SkillMatch AI — Explainable Resume Screening & Job Matching System
### FINAL BUILD (100%)

A complete, explainable AI system that screens resumes against job
descriptions, with a bright, floral-themed UI, login + role selection
(Student vs. Recruiter), and bias-aware review tools.

## Build history
- **Stage 1 (30%)** — text input, cleaning, keyword skill matching, basic dashboard.
- **Stage 2 (70%)** — PDF upload, semantic similarity (Sentence Transformers),
  combined weighted score, explainable output, job-role recommendations.
- **Stage 3 (100%, this build)** — login & roles, advanced synonym-aware skill
  extraction, experience-aware confidence, skill knowledge graph, personalized
  learning recommendations, bias-aware/blind-review mode, recruiter dashboard,
  downloadable PDF reports, and a bright floral UI.

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

The first run downloads the `all-MiniLM-L6-v2` sentence-embedding model
(~80MB) once; it's then cached for the rest of the session.

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

## Honest scope notes (what's simplified for a mini-project)
- **Fine-tuning**: uses the pre-trained `all-MiniLM-L6-v2` model as-is.
  Fine-tuning on a labeled resume–job dataset (e.g. public Hugging Face
  ATS-scoring datasets) is documented as future work — say so plainly in
  your review rather than claiming it's done.
- **Skill knowledge graph**: a small, hand-authored graph — not a learned
  or weighted graph.
- **Bias/fairness**: rule-based redaction of a few common identifiers, not
  a statistical fairness audit. Present it as "bias-aware design," not a
  compliance guarantee.
- **Login**: session-only, no persistent user database — sufficient for a
  live demo, not for production deployment.

## Suggested line for your review
> "In the first stage, we built a keyword-matching prototype. In the second
> stage, we added PDF upload, semantic similarity, and explainable scoring.
> In this final stage, we added advanced synonym-aware skill extraction,
> experience-aware confidence, a skill knowledge graph, personalized
> learning recommendations, bias-aware blind-review mode, a multi-candidate
> recruiter dashboard, and downloadable PDF reports — all wrapped in a
> role-based, login-gated interface."
