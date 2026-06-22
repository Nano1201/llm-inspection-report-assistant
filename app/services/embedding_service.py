import os
from typing import List

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in the environment.")

client = OpenAI(api_key=OPENAI_API_KEY)

def embed_texts(texts: List[str]) -> List[List[float]]:
    """
    Convert a list of texts into embedding vectors.
    """
    if not texts:
        return []

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=texts,
    )

    return [item.embedding for item in response.data]

def embed_query(query: str) -> List[float]:
    """
    Convert one user query into an embedding vector.
    """
    embeddings = embed_texts([query])
    return embeddings[0]