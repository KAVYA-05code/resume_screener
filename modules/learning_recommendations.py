"""
Personalized learning recommendations: for each missing required skill,
suggest a course, a small project, and a link.
"""

LEARNING_RESOURCES = {
    "Docker": {
        "Course": "Docker for Beginners — freeCodeCamp",
        "Project": "Containerize a small Flask app and deploy it.",
        "Link": "https://www.youtube.com/watch?v=fqMOX6JJhGo",
    },
    "AWS": {
        "Course": "AWS Cloud Practitioner Essentials",
        "Project": "Deploy a simple API on AWS Lambda.",
        "Link": "https://aws.amazon.com/training/",
    },
    "Deep Learning": {
        "Course": "Deep Learning Specialization — Coursera",
        "Project": "Build an image classifier using TensorFlow.",
        "Link": "https://www.coursera.org/specializations/deep-learning",
    },
    "Machine Learning": {
        "Course": "Machine Learning — Andrew Ng (Coursera)",
        "Project": "Build a predictive model on a Kaggle dataset.",
        "Link": "https://www.coursera.org/learn/machine-learning",
    },
    "SQL": {
        "Course": "SQL for Data Analysis — Udacity/freeCodeCamp",
        "Project": "Write queries against a sample sales database.",
        "Link": "https://www.freecodecamp.org/news/learn-sql/",
    },
    "React": {
        "Course": "React — The Complete Guide",
        "Project": "Build a to-do list app with React hooks.",
        "Link": "https://react.dev/learn",
    },
    "Git": {
        "Course": "Git & GitHub Crash Course",
        "Project": "Push a project to GitHub with a proper branching workflow.",
        "Link": "https://www.freecodecamp.org/news/git-and-github-for-beginners/",
    },
    "Kubernetes": {
        "Course": "Kubernetes for Beginners",
        "Project": "Deploy a containerized app on a local Kubernetes cluster (minikube).",
        "Link": "https://kubernetes.io/docs/tutorials/",
    },
    "Data Visualization": {
        "Course": "Data Visualization with Python",
        "Project": "Build an interactive dashboard with Plotly/Streamlit.",
        "Link": "https://www.coursera.org/learn/python-for-data-visualization",
    },
    "Statistics": {
        "Course": "Statistics with Python — Coursera",
        "Project": "Perform hypothesis testing on a public dataset.",
        "Link": "https://www.coursera.org/specializations/statistics-with-python",
    },
}

DEFAULT_RESOURCE = {
    "Course": "Search for a beginner course on this skill (Coursera, freeCodeCamp, YouTube).",
    "Project": "Build a small hands-on project applying this skill.",
    "Link": "https://www.freecodecamp.org/",
}


def get_learning_recommendations(missing_skills: list) -> list:
    """Return a list of {skill, course, project, link} dicts for missing skills."""
    recommendations = []
    for skill in missing_skills:
        resource = LEARNING_RESOURCES.get(skill, DEFAULT_RESOURCE)
        recommendations.append({
            "Skill": skill,
            "Course": resource["Course"],
            "Project": resource["Project"],
            "Link": resource["Link"],
        })
    return recommendations
