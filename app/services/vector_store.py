# app/services/vector_store.py
# store chunks in Chroma
# search chunks in Chroma
# manage Chroma collection

from pathlib import Path
from typing import Any, Dict, List

import chromadb

from app.services.chunking_service import DocumentChunk
from app.services.embedding_service import embed_query, embed_texts

CHROMA_DIR = Path("app/storage/chroma")
CHROMA_DIR.mkdir(parents=True, exist_ok=True)

COLLECTION_NAME = "documents"

client = chromadb.PersistentClient(path=str(CHROMA_DIR))

collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    metadata={"hnsw:space": "cosine"},
)

def add_chunks_to_vector_store(chunks: List[DocumentChunk]) -> int:
    """
    Add document chunks to Chroma with embeddings and metadata.
    """
    if not chunks:
        return 0

    texts = [chunk.text for chunk in chunks]
    embeddings = embed_texts(texts)

    ids = [chunk.chunk_id for chunk in chunks]

    metadatas = [
        {
            "document_id": chunk.document_id,
            "filename": chunk.filename,
            "page_number": chunk.page_number,
            "chunk_index": chunk.chunk_index,
        }
        for chunk in chunks
    ]

    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    return len(chunks)

def search_chunks(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Search Chroma for the most relevant chunks.
    """
    query_embedding = embed_query(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    output = []

    ids = results.get("ids", [[]])[0]
    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    for chunk_id, document, metadata, distance in zip(
        ids,
        documents,
        metadatas,
        distances,
    ):
        output.append(
            {
                "chunk_id": chunk_id,
                "text": document,
                "metadata": metadata,
                "distance": distance,
            }
        )

    return output