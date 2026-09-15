"""
Generates a downloadable PDF candidate-matching report using fpdf2.
"""

from datetime import date
from fpdf import FPDF

SYSTEM_VERSION = "v1.0 — Final Build (100%)"


_UNICODE_REPLACEMENTS = {
    "\u2014": "-",   # em dash
    "\u2013": "-",   # en dash
    "\u2018": "'", "\u2019": "'",
    "\u201c": '"', "\u201d": '"',
    "\u2022": "-",   # bullet
    "**": "",        # markdown bold marker
}


def _safe(text) -> str:
    """fpdf's core fonts only support latin-1; normalize common unicode punctuation
    and markdown markers first, then drop anything else outside latin-1."""
    if text is None:
        return ""
    text = str(text)
    for bad, good in _UNICODE_REPLACEMENTS.items():
        text = text.replace(bad, good)
    return text.encode("latin-1", "ignore").decode("latin-1")


class ReportPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(37, 99, 235)
        self.cell(0, 10, "Resume-Job Matching Report", ln=True, align="C")
        self.set_draw_color(37, 99, 235)
        self.line(10, 20, 200, 20)
        self.ln(6)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def section_title(self, title):
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(30, 41, 59)
        self.ln(3)
        self.cell(0, 8, _safe(title), ln=True)
        self.set_draw_color(200, 200, 200)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(2)

    def body_text(self, text):
        self.set_font("Helvetica", "", 11)
        self.set_text_color(20, 20, 20)
        self.multi_cell(0, 6, _safe(text))
        self.ln(1)


def build_pdf_report(data: dict) -> bytes:
    """
    Build a PDF report from a result dictionary. Expected keys:
      candidate_name, job_title, skill_score, semantic_score, final_score,
      category, matching_skills (list), missing_skills (list),
      explanation (str), related_skills (list, optional),
      learning_recommendations (list of dicts, optional),
      recommended_roles (list of dicts, optional), blind_mode (bool, optional)
    Returns raw PDF bytes suitable for st.download_button.
    """
    pdf = ReportPDF()
    pdf.add_page()

    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 7, _safe(f"Candidate: {data.get('candidate_name', 'N/A')}"), ln=True)
    pdf.cell(0, 7, _safe(f"Job Role: {data.get('job_title', 'N/A')}"), ln=True)
    pdf.cell(0, 7, _safe(f"Date: {date.today().isoformat()}"), ln=True)
    pdf.cell(0, 7, _safe(f"System Version: {SYSTEM_VERSION}"), ln=True)

    pdf.section_title("Scores")
    pdf.body_text(
        f"Skill Match Score: {data.get('skill_score', 0)}%\n"
        f"Semantic Similarity Score: {data.get('semantic_score', 0)}%\n"
        f"Final Match Score: {data.get('final_score', 0)}%\n"
        f"Category: {data.get('category', 'N/A')}"
    )

    pdf.section_title("Matching Skills")
    matching = data.get("matching_skills") or []
    pdf.body_text(", ".join(matching) if matching else "None detected.")

    pdf.section_title("Missing Skills")
    missing = data.get("missing_skills") or []
    pdf.body_text(", ".join(missing) if missing else "None — full coverage.")

    pdf.section_title("Explanation")
    pdf.body_text(data.get("explanation", ""))

    related = data.get("related_skills") or []
    if related:
        pdf.section_title("Related Skills (Knowledge Graph Suggestions)")
        pdf.body_text(", ".join(related))

    recs = data.get("learning_recommendations") or []
    if recs:
        pdf.section_title("Personalized Learning Recommendations")
        for r in recs:
            pdf.body_text(
                f"- {r['Skill']}\n"
                f"   Course: {r['Course']}\n"
                f"   Project: {r['Project']}\n"
                f"   Link: {r['Link']}"
            )

    roles = data.get("recommended_roles") or []
    if roles:
        pdf.section_title("Recommended Job Roles")
        for i, r in enumerate(roles, start=1):
            pdf.body_text(f"{i}. {r['Job Role']} — {r['Match Score (%)']}%")

    if data.get("blind_mode"):
        pdf.section_title("Fairness Note")
        from .bias_utils import FAIRNESS_STATEMENT
        pdf.body_text(FAIRNESS_STATEMENT)

    return bytes(pdf.output(dest="S"))
