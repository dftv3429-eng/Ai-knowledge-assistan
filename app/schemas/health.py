from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Estado de salud de la API."""

    status: str
