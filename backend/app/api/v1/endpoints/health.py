"""Health Check Endpoint Module.

Provides GET /health REST route for system monitoring and liveness checks.
"""

from fastapi import APIRouter, status
from backend.app.schemas.health_schema import HealthCheckResponse
from backend.app.core.config import settings
from backend.app.core.constants import VERSION

router = APIRouter()


@router.get(
    "/health",
    response_model=HealthCheckResponse,
    status_code=status.HTTP_200_OK,
    summary="Service Health Check",
    description="Returns liveness status, API version, and environment context for monitoring systems.",
)
async def get_health() -> HealthCheckResponse:
    """Handles GET /health request and returns system readiness status."""
    return HealthCheckResponse(
        status="healthy",
        service=settings.APP_NAME,
        version=VERSION,
        environment=settings.APP_ENV,
    )
