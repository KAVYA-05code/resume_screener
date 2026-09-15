"""
Semantic similarity between resume text and job description text,
using Sentence Transformers + cosine similarity.
"""

import streamlit as st
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


@st.cache_resource(show_spinner="Loading semantic similarity model...")
def load_model():
    """Load and cache the sentence embedding model (loaded once per session)."""
    return SentenceTransformer("all-MiniLM-L6-v2")


def get_semantic_score(resume_text: str, job_description: str) -> float:
    """
    Compute a 0-100 semantic similarity score between resume text
    and a job description using cosine similarity of sentence embeddings.
    """
    model = load_model()
    embeddings = model.encode([resume_text, job_description])
    score = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    return round(float(score) * 100, 2)
