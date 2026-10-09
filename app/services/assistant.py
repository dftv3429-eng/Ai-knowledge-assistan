"""Capa de servicio del asistente.

Implementación local de *bootstrap*: NO usa ningún LLM. En módulos posteriores
esta clase se reemplazará (o se complementará) por un proveedor real, manteniendo
estable el contrato con la capa HTTP.
"""

import asyncio
import unicodedata

PROVIDER_NAME = "bootstrap-local"

_KNOWN_ANSWERS: dict[str, str] = {
    "que es fastapi": (
        "FastAPI es un framework web moderno de Python para construir APIs "
        "rápidas, con tipado y documentación OpenAPI automática."
    ),
    "que es pydantic": (
        "Pydantic es una librería de Python para definir y validar modelos de "
        "datos a partir de anotaciones de tipo."
    ),
    "que es asyncio": (
        "AsyncIO es el módulo de Python para escribir código concurrente "
        "usando async/await sobre un event loop."
    ),
}


def _normalize(text: str) -> str:
    """Minúsculas, sin tildes ni signos de puntuación básicos."""
    text = unicodedata.normalize("NFKD", text.lower())
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = "".join(c if c.isalnum() or c.isspace() else " " for c in text)
    return " ".join(text.split())


class AssistantService:
    """Genera respuestas locales de bootstrap."""

    provider: str = PROVIDER_NAME

    async def answer(self, question: str) -> str:
        # Punto de cesión al event loop: simula el I/O que tendrá un proveedor real.
        await asyncio.sleep(0)
        known = _KNOWN_ANSWERS.get(_normalize(question))
        if known:
            return known
        return (
            f"[bootstrap-local] Recibí tu pregunta: '{question.strip()}'. "
            "Aún no hay un LLM conectado; esta es una respuesta de prueba."
        )


def get_assistant_service() -> AssistantService:
    """Dependencia de FastAPI (facilita sustituir el servicio en pruebas)."""
    return AssistantService()
