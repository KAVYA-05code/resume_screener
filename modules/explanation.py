"""
Human-readable explanation generation for the match result (explainable AI layer).
"""

from .scoring import categorize_score


def generate_explanation(final_score: float, matching_skills: list, missing_skills: list) -> str:
    """Build a plain-language explanation of why the resume received its score."""
    category = categorize_score(final_score)

    message = f"This resume is classified as a **{category}**. "

    if matching_skills:
        message += (
            "The score increased because the resume contains: "
            + ", ".join(matching_skills) + ". "
        )

    if missing_skills:
        message += (
            "The score is reduced because these required skills were not detected: "
            + ", ".join(missing_skills) + "."
        )

    if not matching_skills and not missing_skills:
        message += "No specific required skills were configured for this comparison."

    return message
