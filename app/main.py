from fastapi import FastAPI

from app.api.routes import chat, health, info


def create_app() -> FastAPI:
    app = FastAPI(
        title="AI Knowledge Assistant",
        version="0.1.0",
        description="Bootstrap API - primer incremento funcional (sin LLM).",
    )
    app.include_router(health.router)
    app.include_router(chat.router)
    app.include_router(info.router)
    return app


app = create_app()
