from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, UploadFile, HTTPException

from pydantic import BaseModel

from app.services.vector_store import add_chunks_to_vector_store, search_chunks
from app.services.pdf_service import extract_text_from_pdf
from app.services.chunking_service import chunk_pages

router = APIRouter(prefix="/documents", tags=["documents"])

DOCUMENT_STORAGE_DIR = Path("app/storage/documents")
DOCUMENT_STORAGE_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a PDF document, extract text, and split it into chunks.
    """
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    document_id = str(uuid4())
    saved_path = DOCUMENT_STORAGE_DIR / f"{document_id}_{file.filename}"

    file_bytes = await file.read()

    with open(saved_path, "wb") as f:
        f.write(file_bytes)

    pages = extract_text_from_pdf(saved_path)

    chunks = chunk_pages(
        pages=pages,
        document_id=document_id,
        filename=file.filename,
    )
    indexed_chunks = add_chunks_to_vector_store(chunks)

    return {
        "document_id": document_id,
        "filename": file.filename,
        "saved_path": str(saved_path),
        "pages": len(pages),
        "chunks": len(chunks),
        "indexed_chunks": indexed_chunks,
        "sample_chunk": chunks[0].model_dump() if chunks else None,
    }

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5

@router.post("/search")
async def search_document_chunks(request: SearchRequest):
    """
    Search indexed document chunks using semantic similarity.
    """
    results = search_chunks(
        query=request.query,
        top_k=request.top_k,
    )

    return {
        "query": request.query,
        "top_k": request.top_k,
        "results": results,
    }