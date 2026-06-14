# LLM Inspection Report Assistant

A Dockerized FastAPI backend for LLM-based inspection note extraction, PDF RAG, citation-grounded QA, and evaluation workflows.

## Project Goal

This project builds an AI backend for quality inspection report analysis. It starts with structured extraction from inspection notes, then expands into PDF-based RAG, citation-grounded question answering, evaluation tracking, and tool-calling workflows.

## Planned Features

- FastAPI backend
- Structured JSON extraction from inspection notes
- Pydantic schema validation
- OpenAI API integration
- PDF upload and parsing
- RAG-based question answering
- Citation-grounded responses
- Evaluation dataset and results tracking
- Cost and latency tracking
- Tool-calling workflow for report and email draft generation
- Docker support

## Tech Stack

- Python
- FastAPI
- Pydantic
- OpenAI API
- Chroma or pgvector
- Docker

## Week 1 Scope

The first milestone focuses on building a production-style AI backend instead of a notebook-only demo.

Planned endpoints:

- `GET /health`
- `POST /ask`
- `POST /extract`

Example input:

```json
{
  "note": "Logo marking appears slightly shifted. Package surface has minor scratches."
}
```
Example output:

```json
{
  "issue_type": "visual_defect",
  "severity": "medium",
  "affected_component": "logo_marking",
  "recommended_action": "manual_review",
  "confidence": 0.82
}
