from typing import Literal
from pydantic import BaseModel, Field

class InspectionNoteRequest(BaseModel):
    note: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="Raw inspection note provided by the user.",
        examples=[
            "Logo marking appears slightly shifted. Package surface has minor scratches."
        ],
    )


class InspectionExtractionResponse(BaseModel):
    issue_type: Literal[
        "texture_issue",
        "marking_issue",
        "pinhole_issue",
        "surface_scratch",
        "other_issue",
        "unknown",
    ]
    severity: Literal["low", "medium", "high", "unknown"]
    affected_component: str
    recommended_action: Literal[
        "approve",
        "manual_review",
        "reject",
        "unknown",
    ]
    confidence: float = Field(..., ge=0.0, le=1.0)

    # example output:
    # {
    #     "issue_type": "texture_issue",
    #     "severity": "medium",
    #     "affected_component": "package_surface",
    #     "recommended_action": "manual_review",
    #     "confidence": 0.82
    # }

class AskRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="User question related to quality inspection or inspection reports.",
        examples=[
            "What does manual review mean in quality inspection?"
        ],
    )

class AskResponse(BaseModel):    # response schema in json format for asking a question
    answer: str = Field(        # answer field is required and is a string
        ...,
        description="LLM-generated answer to the user's question.",
    )