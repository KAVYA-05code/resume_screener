"""
Rank multiple job roles against a resume using semantic similarity,
to produce job-role recommendations.
"""

import pandas as pd
from .semantic_utils import get_semantic_score


def load_jobs(csv_path: str) -> pd.DataFrame:
    """Load the job descriptions dataset."""
    return pd.read_csv(csv_path)


def recommend_jobs(resume_text: str, jobs_df: pd.DataFrame) -> pd.DataFrame:
    """
    Score the resume against every job description in `jobs_df` and
    return a ranked DataFrame sorted by match score (descending).
    """
    records = []
    for _, job in jobs_df.iterrows():
        score = get_semantic_score(resume_text, job["description"])
        records.append({
            "Job Role": job["title"],
            "Match Score (%)": score,
        })

    ranked = pd.DataFrame(records).sort_values(
        by="Match Score (%)", ascending=False
    ).reset_index(drop=True)
    ranked.index = ranked.index + 1
    ranked.index.name = "Rank"
    return ranked
