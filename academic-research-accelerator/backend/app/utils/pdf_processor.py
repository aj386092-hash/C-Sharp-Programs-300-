import fitz  # PyMuPDF
import io
from typing import Optional

def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> Optional[str]:
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text.strip() if text.strip() else None
    except Exception:
        return None

def extract_text_from_pdf_path(path: str) -> Optional[str]:
    try:
        doc = fitz.open(path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text.strip() if text.strip() else None
    except Exception:
        return None
