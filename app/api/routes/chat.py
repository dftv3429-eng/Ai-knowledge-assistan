from fastapi import APIRouter, Depends

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.assistant import AssistantService, get_assistant_service

router = APIRouter(prefix="/api/v1", tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat(
    payload: ChatRequest,
    service: AssistantService = Depends(get_assistant_service),
) -> ChatResponse:
    # El router solo coordina: la lógica vive en la capa de servicio.
    answer = await service.answer(payload.question)
    return ChatResponse(answer=answer, provider=service.provider)
