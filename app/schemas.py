from typing import Literal
from pydantic import BaseModel, Field

class InspectionNoteRequest(BaseModel):
    note: str = Field(
        ...,
        description="Raw inspection note which is provided by the user.",
        examples=[
            "Logo marking appears a little bit shifted. Package surface has minor scratches."
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