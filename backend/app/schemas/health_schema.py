"""Health Check Response Schema Module.

Defines Pydantic model for system health monitoring responses.
"""

from pydantic import BaseModel, Field
from datetime import datetime


class HealthCheckResponse(BaseModel):
    """Pydantic schema representing service health status metadata."""

    status: str = Field(..., description="Service status indicator: 'healthy' or 'degraded'", example="healthy")
    service: str = Field(..., description="Application service name", example="Speak-without-voice")
    version: str = Field(..., description="API semantic version number", example="1.0.0")
    environment: str = Field(..., description="Runtime environment name", example="development")
    timestamp: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat() + "Z",
        description="UTC timestamp of the health check response",
    )
