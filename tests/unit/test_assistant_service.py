from app.services.assistant import PROVIDER_NAME, AssistantService


async def test_service_answers_known_question():
    """T-01: el servicio responde correctamente a una pregunta conocida."""
    service = AssistantService()

    answer = await service.answer("¿Qué es FastAPI?")

    assert "FastAPI" in answer
    assert "framework" in answer


async def test_service_known_question_ignores_case_and_accents():
    service = AssistantService()

    answer = await service.answer("QUE ES pydantic")

    assert "Pydantic" in answer


async def test_service_unknown_question_returns_bootstrap_answer():
    service = AssistantService()

    answer = await service.answer("¿Cuál es el sentido de la vida?")

    assert "bootstrap-local" in answer


def test_service_provider_is_bootstrap_local():
    assert AssistantService().provider == PROVIDER_NAME == "bootstrap-local"
