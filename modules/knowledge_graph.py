"""
A small hand-authored skill knowledge graph: skill -> related skills.
Used to suggest related/adjacent skills a candidate hasn't listed yet.
"""

SKILL_GRAPH = {
    "Machine Learning": ["Python", "Scikit-learn", "Deep Learning", "Statistics"],
    "Deep Learning": ["TensorFlow", "PyTorch", "Neural Networks", "Computer Vision"],
    "Data Analysis": ["Python", "Pandas", "NumPy", "SQL", "Data Visualization"],
    "Data Visualization": ["Tableau", "Power BI", "Pandas"],
    "Web Development": ["HTML", "CSS", "JavaScript", "React"],
    "React": ["JavaScript", "HTML", "CSS"],
    "Backend Development": ["Python", "Django", "Flask", "REST API", "SQL"],
    "Cloud Computing": ["AWS", "Azure", "GCP", "Docker", "Kubernetes"],
    "DevOps": ["Docker", "Kubernetes", "Linux", "Git", "AWS"],
    "Natural Language Processing": ["Python", "Deep Learning", "Machine Learning"],
    "SQL": ["Data Analysis", "Excel"],
    "Python": ["Pandas", "NumPy", "Machine Learning"],
}


def get_related_skills(detected_skills: list, skill_graph: dict = None) -> list:
    """
    Given the skills already detected in a resume, return related skills
    from the knowledge graph that were NOT detected — useful as growth areas.
    """
    skill_graph = skill_graph or SKILL_GRAPH
    detected_set = set(detected_skills)
    related = set()

    for skill in detected_skills:
        if skill in skill_graph:
            related.update(skill_graph[skill])

    return sorted(related - detected_set)
