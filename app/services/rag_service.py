import os
from typing import Any, Dict, List

from dotenv import load_dotenv
from fastapi import HTTPException
from openai import OpenAI, OpenAIError

from app.services.vector_store import search_chunks

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LLM_MODEL = os.getenv("LLM_MODEL", os.getenv("MODEL_NAME", "gpt-4o-mini"))

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in the environment.")

client = OpenAI(api_key=OPENAI_API_KEY)

def build_context(retrieved_chunks: List[Dict[str, Any]]) -> str:
    """
    Convert retrieved chunks into a context block for the LLM.
    """
    context_blocks = []

    for index, chunk in enumerate(retrieved_chunks, start=1):
        metadata = chunk["metadata"]

        filename = metadata.get("filename", "unknown file")
        page_number = metadata.get("page_number", "unknown page")
        chunk_index = metadata.get("chunk_index", "unknown chunk")

        context_blocks.append(
            f"""
[Source {index}]
File: {filename}
Page: {page_number}
Chunk: {chunk_index}

Text:
{chunk["text"]}
""".strip()
        )

    return "\n\n".join(context_blocks)


def answer_question_with_rag(question: str, top_k: int = 5) -> Dict[str, Any]:
    """
    Retrieve relevant document chunks and generate an answer using only those chunks.
    """
    retrieved_chunks = search_chunks(query=question, top_k=top_k)

    if not retrieved_chunks:
        return {
            "answer": "I could not find relevant information in the uploaded documents.",
            "sources": [],
        }

    context = build_context(retrieved_chunks)

    system_prompt = """
You are a document question-answering assistant.

Answer the user's question using only the provided context.
Do not use outside knowledge.
If the answer is not available in the context, say:
"I could not find the answer in the uploaded documents."

Keep the answer concise and factual.
""".strip()

    user_prompt = f"""
Context:
{context}

Question:
{question}
""".strip()

    try:
        response = client.chat.completions.create(
            model=LLM_MODEL,
            temperature=0,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
    except OpenAIError:
        raise HTTPException(
            status_code=502,
            detail="OpenAI API request failed.",
        )

    answer = response.choices[0].message.content or ""

    sources = [
        {
            "source_id": index,
            "filename": chunk["metadata"].get("filename"),
            "page_number": chunk["metadata"].get("page_number"),
            "chunk_index": chunk["metadata"].get("chunk_index"),
            "text": chunk["text"],
            "distance": chunk["distance"],
        }
        for index, chunk in enumerate(retrieved_chunks, start=1)
    ]

    return {
        "answer": answer,
        "sources": sources,
    }