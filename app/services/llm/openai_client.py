import json

from openai import OpenAI

from app.config import settings
from app.schemas import InspectionExtractionResponse


client = OpenAI(api_key=settings.openai_api_key) # initialize the OpenAI client

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

    response = client.responses.create(   # create the response from the OpenAI client
        model=settings.openai_model,
        input=prompt,   # the prompt to the OpenAI client
    )

    raw_text = response.output_text # get the raw text from the response

    parsed = json.loads(raw_text) # parse the response into a Python dictionary

    return InspectionExtractionResponse(**parsed) # return the response as a Pydantic model