"""
Keyword-based skill extraction and matching.
This is the 30% baseline, kept and reused as one half of the 70% combined score.
"""

import re

# Predefined master skill list (expand freely — this is the "skills database")
SKILL_DATABASE = [
    "Python", "Java", "C++", "SQL", "R", "JavaScript", "HTML", "CSS",
    "React", "Django", "Flask", "REST API", "Git", "Docker", "Kubernetes",
    "AWS", "Azure", "GCP", "Machine Learning", "Deep Learning",
    "Data Analysis", "Data Visualization", "Statistics", "Excel",
    "Pandas", "NumPy", "TensorFlow", "PyTorch", "Scikit-learn",
    "Natural Language Processing", "Computer Vision", "Power BI",
    "Tableau", "Linux", "Agile", "Scrum", "Communication",
]

# Optional lightweight synonym map to reduce false "missing skill" results
SYNONYMS = {
    "ml": "Machine Learning",
    "dl": "Deep Learning",
    "nlp": "Natural Language Processing",
    "cv": "Computer Vision",
    "js": "JavaScript",
    "sklearn": "Scikit-learn",
}


def _normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9\s]", " ", text.lower())


def extract_skills(text: str, skill_list=None) -> list:
    """Extract skills present in `text` by matching against the skill database."""
    skill_list = skill_list or SKILL_DATABASE
    normalized = _normalize(text)

    found = []
    for skill in skill_list:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"
        if re.search(pattern, normalized):
            found.append(skill)

    # Check synonyms too
    for abbr, full_skill in SYNONYMS.items():
        if re.search(r"\b" + re.escape(abbr) + r"\b", normalized) and full_skill not in found:
            found.append(full_skill)

    return sorted(set(found))


def match_skills(resume_skills: list, required_skills: list) -> dict:
    """
    Compare resume skills against a job's required skills.

    Returns:
        dict with matching_skills, missing_skills, and skill_score (0-100).
    """
    resume_set = {s.lower() for s in resume_skills}
    required_set = {s.lower() for s in required_skills}

    matching = [s for s in required_skills if s.lower() in resume_set]
    missing = [s for s in required_skills if s.lower() not in resume_set]

    skill_score = (len(matching) / len(required_set) * 100) if required_set else 0.0

    return {
        "matching_skills": matching,
        "missing_skills": missing,
        "skill_score": round(skill_score, 2),
    }
