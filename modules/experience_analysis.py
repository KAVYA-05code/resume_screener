"""
Experience analysis: splits a resume into sections and checks whether a
detected skill appears only in a "Skills" list, or is also backed up by
mentions in Projects / Work Experience — giving it a higher confidence weight.
"""

import re

SECTION_ALIASES = {
    "skills": ["skills", "technical skills", "key skills", "core competencies"],
    "projects": ["projects", "academic projects", "personal projects"],
    "experience": [
        "work experience", "experience", "professional experience",
        "employment history", "internship", "internships",
    ],
    "education": ["education", "academic background", "qualifications"],
}

WEIGHT_LISTED_ONLY = 1.0
WEIGHT_USED_IN_PRACTICE = 1.3


def split_resume_sections(text: str) -> dict:
    """
    Split resume text into named sections based on common heading keywords.
    Falls back to putting everything under 'general' if no headings are found.
    """
    lines = text.splitlines()
    sections = {"general": []}
    current_section = "general"

    heading_lookup = {}
    for canonical, aliases in SECTION_ALIASES.items():
        for alias in aliases:
            heading_lookup[alias] = canonical

    for line in lines:
        stripped = line.strip().lower().rstrip(":")
        if stripped in heading_lookup and len(stripped) < 40:
            current_section = heading_lookup[stripped]
            sections.setdefault(current_section, [])
            continue
        sections.setdefault(current_section, []).append(line)

    return {name: "\n".join(content) for name, content in sections.items()}


def compute_experience_confidence(detected_skills: list, sections: dict) -> dict:
    """
    For each detected skill, determine whether it's backed by mentions in
    Projects/Experience sections (higher confidence) or only appears in a
    Skills list / general text (baseline confidence).

    Returns:
        dict: skill -> {"weight": float, "used_in_practice": bool, "note": str}
    """
    practice_text = " ".join([
        sections.get("projects", ""),
        sections.get("experience", ""),
    ]).lower()

    results = {}
    for skill in detected_skills:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"
        used_in_practice = bool(re.search(pattern, practice_text))

        if used_in_practice:
            results[skill] = {
                "weight": WEIGHT_USED_IN_PRACTICE,
                "used_in_practice": True,
                "note": f"{skill}: also mentioned in Projects/Experience — higher confidence.",
            }
        else:
            results[skill] = {
                "weight": WEIGHT_LISTED_ONLY,
                "used_in_practice": False,
                "note": f"{skill}: only found in a skills list — not confirmed by project/work mentions.",
            }

    return results
