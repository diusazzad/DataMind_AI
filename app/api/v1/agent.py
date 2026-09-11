from fastapi import APIRouter, HTTPException, status
from app.models.schemas import AgentChatRequest, AgentChatResponse
from app.services.agent_service import agent_service

router = APIRouter(prefix="/agent", tags=["AI Agent"])


@router.post("/chat", response_model=AgentChatResponse)
def agent_chat(request: AgentChatRequest):
    """
    Unified Autonomous ReAct AI Agent Endpoint.
    Analyzes user intent and automatically coordinates:
    - Safe SQL execution for database queries
    - RAG Document Intelligence for policy / document queries
    - Tabular Data Analytics for dataset profiling questions
    - Contextual reasoning for interactive guidance
    """
    try:
        return agent_service.process_chat(request)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Agent processing error: {str(e)}"
        )
