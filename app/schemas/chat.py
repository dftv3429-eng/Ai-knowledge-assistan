from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Entrada del endpoint de chat."""

    question: str = Field(
        ...,
        min_length=3,
        max_length=2000,
        description="Pregunta del usuario (entre 3 y 2000 caracteres).",
        examples=["¿Qué es FastAPI?"],
    )


class ChatResponse(BaseModel):
    """Salida del endpoint de chat."""

    answer: str = Field(..., description="Respuesta generada por el servicio.")
    provider: str = Field(
        ...,
        description="Identifica el origen de la respuesta. 'bootstrap-local' = no es un LLM real.",
        examples=["bootstrap-local"],
    )
