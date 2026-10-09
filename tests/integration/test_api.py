import httpx
import pytest

from app.main import app


@pytest.fixture
async def client():
    """Cliente asíncrono que invoca la app ASGI directamente (sin servidor externo)."""
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as c:
        yield c


async def test_health_returns_200(client):
    """T-02"""
    response = await client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


async def test_chat_valid_question_returns_200(client):
    """T-03"""
    response = await client.post("/api/v1/chat", json={"question": "¿Qué es FastAPI?"})

    assert response.status_code == 200
    body = response.json()
    assert set(body) == {"answer", "provider"}
    assert body["provider"] == "bootstrap-local"
    assert body["answer"]


async def test_chat_too_short_question_returns_422(client):
    """T-04"""
    response = await client.post("/api/v1/chat", json={"question": "ab"})

    assert response.status_code == 422


async def test_chat_too_long_question_returns_422(client):
    response = await client.post("/api/v1/chat", json={"question": "a" * 2001})

    assert response.status_code == 422


async def test_chat_boundary_lengths_are_accepted(client):
    for question in ("abc", "a" * 2000):
        response = await client.post("/api/v1/chat", json={"question": question})
        assert response.status_code == 200


async def test_chat_missing_question_returns_422(client):
    response = await client.post("/api/v1/chat", json={})

    assert response.status_code == 422


async def test_info_returns_200_and_llm_disabled(client):
    """T-05"""
    response = await client.get("/api/v1/info")

    assert response.status_code == 200
    body = response.json()
    assert body["llm_enabled"] is False
    assert body == {
        "name": "AI Knowledge Assistant",
        "version": "0.1.0",
        "environment": "development",
        "llm_enabled": False,
    }


async def test_docs_available(client):
    response = await client.get("/docs")

    assert response.status_code == 200
