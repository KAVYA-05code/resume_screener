"""
PDF handling utilities.
Handles resume PDF upload and text extraction with error handling
for unreadable / scanned / empty PDFs.
"""

from pypdf import PdfReader


class PDFExtractionError(Exception):
    """Raised when a PDF has no extractable text."""
    pass


def extract_pdf_text(uploaded_file) -> str:
    """
    Extract text from an uploaded PDF file object (Streamlit UploadedFile).

    Returns:
        str: cleaned extracted text.

    Raises:
        PDFExtractionError: if no readable text could be found
            (e.g. the PDF is a scanned image with no OCR layer).
    """
    try:
        reader = PdfReader(uploaded_file)
    except Exception as exc:
        raise PDFExtractionError(f"Could not open PDF file: {exc}") from exc

    if len(reader.pages) == 0:
        raise PDFExtractionError("The uploaded PDF has no pages.")

    text_chunks = []
    for page in reader.pages:
        page_text = page.extract_text() or ""
        text_chunks.append(page_text)

    full_text = "\n".join(text_chunks).strip()

    if not full_text:
        raise PDFExtractionError(
            "No readable text was found in this PDF. "
            "It may be a scanned image without a text layer — "
            "try a text-based PDF or an OCR'd version."
        )

    return clean_text(full_text)


def clean_text(text: str) -> str:
    """Basic cleanup / preprocessing of extracted text."""
    lines = [line.strip() for line in text.splitlines()]
    lines = [line for line in lines if line]
    return "\n".join(lines)
