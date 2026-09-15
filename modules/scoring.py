"""
Combined match score: weighted blend of keyword skill score and
semantic similarity score.
"""

SKILL_WEIGHT = 0.60
SEMANTIC_WEIGHT = 0.40


def compute_final_score(skill_score: float, semantic_score: float) -> float:
    """Weighted combination of skill match and semantic similarity."""
    final = (SKILL_WEIGHT * skill_score) + (SEMANTIC_WEIGHT * semantic_score)
    return round(final, 2)


def categorize_score(final_score: float) -> str:
    """Map a final score to a human-readable category."""
    if final_score >= 75:
        return "Strong Match"
    elif final_score >= 50:
        return "Moderate Match"
    else:
        return "Low Match"
