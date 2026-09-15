"""
Bias & fairness helpers.

Screening decisions should be based on skills, projects, experience and
education — not on name, gender, age, marital status, address, or a photo.
This module provides a lightweight "blind review" transform that redacts
common personal identifiers from resume text before it's shown/scored,
plus the fairness statement shown in the UI and reports.
"""

import re

FAIRNESS_STATEMENT = (
    "This system is designed to ignore personal identifiers such as name, "
    "gender, age, marital status, and photographs. The match score is based "
    "only on skills, projects, work experience, and education. This reduces "
    "the risk of bias linked to irrelevant personal information."
)

_EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
_PHONE_RE = re.compile(r"(\+?\d[\d\-\s()]{7,}\d)")
_AGE_RE = re.compile(r"\b(age[:\s]*\d{1,2}|\d{1,2}\s*years old)\b", re.IGNORECASE)
_GENDER_RE = re.compile(r"\b(male|female|gender[:\s]*\w+|non-binary)\b", re.IGNORECASE)
_MARITAL_RE = re.compile(r"\b(single|married|marital status[:\s]*\w+)\b", re.IGNORECASE)
_ADDRESS_KEYWORDS = ("address:", "residing at", "permanent address")


def redact_sensitive_info(text: str) -> str:
    """
    Return a 'blinded' version of resume text with common personal
    identifiers replaced by placeholders. Best-effort, not exhaustive —
    intended as a demonstration of bias-aware design, not a compliance tool.
    """
    redacted = text
    redacted = _EMAIL_RE.sub("[EMAIL REDACTED]", redacted)
    redacted = _PHONE_RE.sub("[PHONE REDACTED]", redacted)
    redacted = _AGE_RE.sub("[AGE REDACTED]", redacted)
    redacted = _GENDER_RE.sub("[GENDER REDACTED]", redacted)
    redacted = _MARITAL_RE.sub("[MARITAL STATUS REDACTED]", redacted)

    lines = redacted.splitlines()
    cleaned_lines = []
    for line in lines:
        if any(kw in line.lower() for kw in _ADDRESS_KEYWORDS):
            cleaned_lines.append("[ADDRESS REDACTED]")
        else:
            cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


def anonymize_candidate_label(index: int) -> str:
    """Generate a neutral candidate label (Candidate A, B, C...) for blind comparison tables."""
    letter = chr(ord("A") + index) if index < 26 else str(index + 1)
    return f"Candidate {letter}"
