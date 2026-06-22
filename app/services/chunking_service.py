# app/services/chunking_service.py
# This file contains the code for the chunking service.
# It is used to chunk the text from the PDF service.

from typing import List
from uuid import uuid4

from pydantic import BaseModel

from app.services.pdf_service import PageText


class DocumentChunk(BaseModel):
    chunk_id: str
    document_id: str
    filename: str
    page_number: int
    chunk_index: int
    text: str

def chunk_text(
    text: str,
    chunk_size: int = 800,
    chunk_overlap: int = 150,
) -> List[str]:
    """
    Split text into overlapping chunks.
    """
    if not text:
        return []

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - chunk_overlap

    return chunks


def chunk_pages(
    pages: List[PageText],
    document_id: str,
    filename: str,
    chunk_size: int = 800,
    chunk_overlap: int = 150,
) -> List[DocumentChunk]:
    """
    Split PDF pages into chunks while keeping source metadata.
    """
    all_chunks: List[DocumentChunk] = []

    for page in pages:
        page_chunks = chunk_text(
            page.text,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

        for chunk_index, chunk in enumerate(page_chunks):
            all_chunks.append(
                DocumentChunk(
                    chunk_id=str(uuid4()),
                    document_id=document_id,
                    filename=filename,
                    page_number=page.page_number,
                    chunk_index=chunk_index,
                    text=chunk,
                )
            )

    return all_chunks