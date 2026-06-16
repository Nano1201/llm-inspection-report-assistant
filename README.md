# LLM Inspection Report Assistant

This is a simple FastAPI backend for turning inspection notes into structured JSON.

## What it can do now

- `GET /health` : check if the server is running
- `GET /config-test` : check if your environment settings are loaded
- `POST /extract` : extract issue info from an inspection note (uses OpenAI)

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

### `GET /health`

Returns:

- `{ "status": "ok" }`

### `GET /config-test`

Returns whether `OPENAI_API_KEY` is set.

### `POST /extract`

Request body:

```json
{
  "note": "Logo marking appears slightly shifted. Package surface has minor scratches."
}
```

Response body (example):

```json
{
  "issue_type": "marking_issue",
  "severity": "medium",
  "affected_component": "logo_marking",
  "recommended_action": "manual_review",
  "confidence": 0.82
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
