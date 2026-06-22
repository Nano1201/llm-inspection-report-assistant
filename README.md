# LLM Inspection Report Assistant

This is a simple FastAPI backend for inspection tasks.
It uses OpenAI to read notes, answer questions, and search uploaded PDF files.

## What it can do now

- Health check
- Extract structured inspection information
- Ask an inspection-related question (general)
- Upload a PDF and split it into chunks
- Search document chunks
- Ask a question using uploaded documents (RAG)

## Planned (not finished yet)

- Keep tracking results and evaluation
- Track cost and speed

## Tech stack

- Python
- FastAPI
- Pydantic
- OpenAI API
- PyMuPDF (read PDF text)
- ChromaDB (store and search chunks)
- Docker

## API

### Health Check

**Endpoint:** `GET /health`

Use this endpoint to make sure the server is running.

Example response:

```json
{
  "status": "ok",
  "service": "llm-inspection-report-assistant",
  "version": "0.1.0"
}
```

### Extract Structured Inspection Information

**Endpoint:** `POST /extract`

Send one inspection note. The API returns structured fields.

Request example:

```json
{
  "note": "Logo marking appears slightly shifted. Package surface has minor scratches."
}
```

Response example:

```json
{
  "issue_type": "marking_issue",
  "severity": "medium",
  "affected_component": "logo_marking",
  "recommended_action": "manual_review",
  "confidence": 0.82
}
```

### Ask an Inspection-Related Question

**Endpoint:** `POST /ask`

Send a general question about inspection workflow, defects, or report meaning.
This does not use uploaded PDF files.

Request example:

```json
{
  "question": "What does manual review mean in quality inspection?"
}
```

Response example:

```json
{
  "answer": "Manual review means a person should check the item before approval."
}
```

### Upload a PDF

**Endpoint:** `POST /documents/upload`

Upload one PDF file. The server will:
1. save the file
2. read text from each page
3. split text into chunks
4. save chunks to ChromaDB

Use `multipart/form-data` with a file field named `file`.

Response example:

```json
{
  "document_id": "b1c2d3e4-...",
  "filename": "sample_ic_inspection_report.pdf",
  "pages": 3,
  "chunks": 12,
  "indexed_chunks": 12
}
```

### Search Document Chunks

**Endpoint:** `POST /documents/search`

Search saved chunks by meaning (not exact keyword match).

Request example:

```json
{
  "query": "What defects were found on the package surface?",
  "top_k": 5
}
```

Response example:

```json
{
  "query": "What defects were found on the package surface?",
  "top_k": 5,
  "results": [
    {
      "chunk_id": "...",
      "text": "...",
      "metadata": {
        "filename": "sample_ic_inspection_report.pdf",
        "page_number": 2,
        "chunk_index": 0
      },
      "distance": 0.21
    }
  ]
}
```

### Ask with Uploaded Documents (RAG)

**Endpoint:** `POST /rag/ask`

Ask a question and let the server search uploaded PDF chunks first.
The answer should come from those chunks.

Request example:

```json
{
  "question": "What action was recommended for the logo marking issue?",
  "top_k": 5
}
```

Response example:

```json
{
  "question": "What action was recommended for the logo marking issue?",
  "top_k": 5,
  "answer": "Manual review was recommended.",
  "sources": [
    {
      "source_id": 1,
      "filename": "sample_ic_inspection_report.pdf",
      "page_number": 2,
      "chunk_index": 0,
      "text": "...",
      "distance": 0.21
    }
  ]
}
```

## Run locally

1. Install dependencies

```bash
pip install -r requirements.txt
```

2. Add your environment variables

Create a `.env` file in the project root:

```bash
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini          # optional
EMBEDDING_MODEL=text-embedding-3-small  # optional
LLM_MODEL=gpt-4o-mini             # optional, used by RAG
```

3. Start the server

```bash
uvicorn app.main:app --reload
```

Open:

- Swagger UI: `http://127.0.0.1:8000/docs`
- Health check: `http://127.0.0.1:8000/health`

## Run with Docker

```bash
docker build -t llm-inspection-report-assistant .
docker run -p 8000:8000 --env-file .env llm-inspection-report-assistant
```
