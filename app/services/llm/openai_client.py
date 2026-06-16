import json

from json import JSONDecodeError

from fastapi import HTTPException
from openai import OpenAI, OpenAIError
from pydantic import ValidationError

from app.config import settings
from app.schemas import InspectionExtractionResponse, AskResponse

def get_openai_client() -> OpenAI:
    if not settings.openai_api_key:
        raise HTTPException(
            status_code=500,
            detail="OpenAI API key is not configured.",
        )

    return OpenAI(api_key=settings.openai_api_key)

def extract_inspection_note_with_openai(note: str) -> InspectionExtractionResponse:     # define the function to extract the inspection note
    prompt = f"""
You are an AI assistant for IC quality inspection.
Extract structured information from the inspection note.
Inspection note:
{note}

Return only valid JSON with the following fields:
- issue_type: one of ["texture_issue", "marking_issue", "pinhole_issue", "surface_scratch", "other_issue", "unknown"]
- severity: one of ["low", "medium", "high", "unknown"]
- affected_component: a short snake_case string
- recommended_action: one of ["approve", "manual_review", "reject", "unknown"]
- confidence: a float between 0.0 and 1.0

Note:
Do not include markdown.
Do not include explanation.
Do not include any other text or comments.
"""

    client = get_openai_client()

    try:
        response = client.responses.create(
            model=settings.openai_model,
            input=prompt,
        )

        raw_text = response.output_text.strip()
        parsed = json.loads(raw_text)

        return InspectionExtractionResponse(**parsed)

    except JSONDecodeError:
        raise HTTPException(
            status_code=502,
            detail="Failed to parse LLM response as valid JSON.",
        )

    except ValidationError:
        raise HTTPException(
            status_code=502,
            detail="LLM response did not match the expected extraction schema.",
        )

    except OpenAIError:
        raise HTTPException(
            status_code=502,
            detail="OpenAI API request failed.",
        )


def ask_openai(question: str) -> AskResponse:
    prompt = f"""
You are an AI assistant for quality inspection and inspection report analysis.
Answer the user's question clearly and concisely.
User question:
{question}

Guidelines:
- Focus on quality inspection, visual defects, reporting, and review workflow.
- If the question is outside your scope, answer briefly and say it is outside the inspection assistant's scope.
- Do not make up specific lot data or inspection results.
"""

    client = get_openai_client()

    try:
        response = client.responses.create(
            model=settings.openai_model,
            input=prompt,
        )

        return AskResponse(answer=response.output_text.strip())

    except OpenAIError:
        raise HTTPException(
            status_code=502,
            detail="OpenAI API request failed.",
        )