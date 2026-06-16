# LLM Inspection Report Assistant

This is a simple FastAPI backend for inspection tasks.
It uses OpenAI to read notes and answer questions.

## What it can do now

- Health check
- Extract structured inspection information
- Ask an inspection-related question

## Planned (not finished yet)

- Upload and parse PDF files
- Q&A using document search (RAG)
- Keep tracking results and evaluation
- Track cost and speed

## Tech stack

- Python
- FastAPI
- Pydantic
- OpenAI API
- Chroma or pgvector (planned for RAG)
- Docker (planned)

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

Send a question about inspection workflow, defects, or report meaning.

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

## Run locally

1. Install dependencies

```bash
pip install -r requirements.txt
```

2. Add your environment variables

Create a `.env` file in the project root:

```bash
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini  # optional (default exists)
```

3. Start the server

```bash
uvicorn app.main:app --reload
```

Open:

- Swagger UI: `http://127.0.0.1:8000/docs`
- Health check: `http://127.0.0.1:8000/health`
