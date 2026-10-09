from pydantic import BaseModel


class InfoResponse(BaseModel):
    """Información básica del proyecto."""

    name: str
    version: str
    environment: str
    llm_enabled: bool
