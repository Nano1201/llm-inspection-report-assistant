# app/services/pdf_service.py
# It transfer pdf into text
# [
#     PageText(page_number=1, text="..."),
#     PageText(page_number=2, text="..."),
# ]

from pathlib import Path
from typing import List

import fitz
from pydantic import BaseModel

class PageText(BaseModel):
    page_number: int
    text: str

def extract_text_from_pdf(file_path: str | Path) -> List[PageText]:
    """
    Extract text from each page of a PDF.

    Args:
        file_path: Path to the PDF file.

    Returns:
        A list of PageText objects, one per page.
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"PDF file not found: {file_path}")

    pages: List[PageText] = []

    with fitz.open(file_path) as doc:
        for page_index, page in enumerate(doc):
            text = page.get_text("text").strip()

            pages.append(
                PageText(
                    page_number=page_index + 1,
                    text=text,
                )
            )

    return pages