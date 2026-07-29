"""API v1 Router Aggregator.

Aggregates all sub-routers (health, predict) under the /api/v1 prefix.
"""

from fastapi import APIRouter
from backend.app.api.v1.endpoints import health

api_v1_router = APIRouter()

# Include health endpoints
api_v1_router.include_router(health.router, tags=["Health"])
