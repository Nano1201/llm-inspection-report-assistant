from fastapi import FastAPI
from app.schemas import InspectionNoteRequest, InspectionExtractionResponse

app = FastAPI(
    title="LLM Inspection Report Assistant",
    description="A FastAPI backend for LLM-based inspection report analysis.",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "llm-inspection-report-assistant",
        "version": "0.1.0",
    }

@app.post("/extract", response_model=InspectionExtractionResponse)
def extract_inspection_note(request: InspectionNoteRequest):
    return {
        # sample output, for test
        "issue_type": "marking_issue",
        "severity": "medium",
        "affected_component": "logo_marking",
        "recommended_action": "manual_review",
        "confidence": 0.82,
    }