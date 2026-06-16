# main.py is responsible for the FastAPI application and the endpoints
# In other words, it is a router--an entry point for the application
# most of the logic 

from fastapi import FastAPI
from app.schemas import (
    InspectionNoteRequest,    # input for extract
    InspectionExtractionResponse,    # output for extract
    AskRequest,    # input for ask
    AskResponse,    # output for ask
)
from app.services.llm.openai_client import (
    extract_inspection_note_with_openai,    # function to extract the inspection note
    ask_openai,    # function to ask a question
)

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

# @app.post("/extract", response_model=InspectionExtractionResponse)
# def extract_inspection_note(request: InspectionNoteRequest):
#     return {
#         # sample output, for test
#         "issue_type": "marking_issue",
#         "severity": "medium",
#         "affected_component": "logo_marking",
#         "recommended_action": "manual_review",
#         "confidence": 0.82,
#     }

@app.post("/extract", response_model=InspectionExtractionResponse)
def extract_inspection_note(request: InspectionNoteRequest):
    return extract_inspection_note_with_openai(request.note)   # call the function to extract the inspection note by calling openai client

@app.post("/ask", response_model=AskResponse)
def ask_question(request: AskRequest):
    return ask_openai(request.question)