"""Demostración de AsyncIO + HTTPX asíncrono.

Lanza varias peticiones CONCURRENTES contra la propia aplicación FastAPI usando
``httpx.AsyncClient`` con ``ASGITransport`` (no requiere servidor en ejecución).

Uso (desde la raíz del repo, con el entorno activado):

    python scripts/async_demo.py

Opcional: contra un servidor real (uvicorn app.main:app) usando --url:

    python scripts/async_demo.py --url http://127.0.0.1:8000
"""

import argparse
import asyncio
import sys
import time
from pathlib import Path

import httpx

# Permite ejecutar el script directamente sin instalar el paquete.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

QUESTIONS = [
    "¿Qué es FastAPI?",
    "¿Qué es Pydantic?",
    "¿Qué es AsyncIO?",
    "Cuéntame sobre HTTPX",
    "¿Para qué sirve pytest?",
]


async def ask(client: httpx.AsyncClient, question: str) -> dict:
    response = await client.post("/api/v1/chat", json={"question": question})
    response.raise_for_status()
    return response.json()


async def main(base_url: str | None) -> None:
    if base_url:
        client = httpx.AsyncClient(base_url=base_url, timeout=10.0)
    else:
        from app.main import app

        client = httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://testserver"
        )

    async with client:
        health = await client.get("/health")
        print(f"GET /health -> {health.status_code} {health.json()}")

        start = time.perf_counter()
        # asyncio.gather ejecuta las corrutinas de forma concurrente.
        results = await asyncio.gather(*(ask(client, q) for q in QUESTIONS))
        elapsed = time.perf_counter() - start

    for question, result in zip(QUESTIONS, results, strict=True):
        print(f"\nQ: {question}\nA: {result['answer']}\n   provider={result['provider']}")
    print(f"\n{len(QUESTIONS)} peticiones concurrentes en {elapsed:.4f}s")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--url", default=None, help="URL base de un servidor en ejecución")
    args = parser.parse_args()
    asyncio.run(main(args.url))
