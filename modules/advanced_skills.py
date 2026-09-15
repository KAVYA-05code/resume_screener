"""
Advanced skill extraction: detects skills even when mentioned indirectly,
via a synonym dictionary (e.g. "predictive modeling" -> Machine Learning).
"""

import re

SKILL_SYNONYMS = {
    "Python": ["python", "py", "python programming"],
    "Machine Learning": [
        "machine learning", "ml", "predictive modeling", "predictive models",
        "supervised learning", "unsupervised learning",
    ],
    "Deep Learning": ["deep learning", "dl", "neural networks", "neural network"],
    "SQL": ["sql", "mysql", "postgresql", "relational databases", "database queries"],
    "Git": ["git", "version control", "github", "gitlab"],
    "Docker": ["docker", "containerization", "containers"],
    "AWS": ["aws", "amazon web services", "cloud (aws)"],
    "Azure": ["azure", "microsoft azure"],
    "GCP": ["gcp", "google cloud", "google cloud platform"],
    "TensorFlow": ["tensorflow", "tf"],
    "PyTorch": ["pytorch", "torch"],
    "Scikit-learn": ["scikit-learn", "sklearn", "scikit learn"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "Data Analysis": ["data analysis", "data analytics", "analyzing data"],
    "Data Visualization": ["data visualization", "dashboards", "charts and graphs"],
    "Statistics": ["statistics", "statistical analysis", "stats"],
    "Excel": ["excel", "ms excel", "spreadsheets"],
    "Natural Language Processing": ["natural language processing", "nlp", "text mining"],
    "Computer Vision": ["computer vision", "cv", "image processing"],
    "React": ["react", "react.js", "reactjs"],
    "JavaScript": ["javascript", "js"],
    "HTML": ["html", "html5"],
    "CSS": ["css", "css3"],
    "Django": ["django"],
    "Flask": ["flask"],
    "REST API": ["rest api", "restful api", "api development", "web api"],
    "Kubernetes": ["kubernetes", "k8s"],
    "Linux": ["linux", "unix"],
    "Agile": ["agile", "agile methodology"],
    "Scrum": ["scrum"],
    "Power BI": ["power bi", "powerbi"],
    "Tableau": ["tableau"],
    "Communication": ["communication skills", "communication"],
}


def extract_skills_advanced(text: str, skill_synonyms: dict = None) -> dict:
    """
    Detect skills in `text` using direct names and indirect synonym phrases.

    Returns:
        dict mapping detected skill -> the matched phrase that triggered detection
        (useful for explainability, e.g. "SQL (from 'mysql')").
    """
    skill_synonyms = skill_synonyms or SKILL_SYNONYMS
    text_lower = text.lower()

    detected = {}
    for skill, synonyms in skill_synonyms.items():
        for syn in synonyms:
            pattern = r"\b" + re.escape(syn) + r"\b"
            if re.search(pattern, text_lower):
                detected[skill] = syn
                break

    return detected


def format_detection_note(detected: dict) -> list:
    """Build human-readable notes like 'SQL (detected via \"mysql\")'."""
    notes = []
    for skill, phrase in detected.items():
        if phrase == skill.lower():
            notes.append(skill)
        else:
            notes.append(f'{skill} (detected via "{phrase}")')
    return notes
