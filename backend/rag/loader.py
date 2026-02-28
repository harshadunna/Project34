import os
from pypdf import PdfReader

# Compute the root of the backend folder relative to this file
# This assumes rag/loader.py is inside project_root/backend/rag/
# and project_root/backend/data contains the PDF.
# The project root is actually Project34/backend/ in this case.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(PROJECT_ROOT, "data", "airport_docs.pdf")

def load_pdf() -> str:
    """
    Extracts text from airport_docs.pdf using pypdf.
    Handles None returns from extract_text() and raises error if file missing.
    """
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"PDF file not found at: {DATA_PATH}")

    reader = PdfReader(DATA_PATH)
    full_text = []

    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text.append(text)
    
    return "\n".join(full_text)
