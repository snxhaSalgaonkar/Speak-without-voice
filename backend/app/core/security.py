"""Security & CORS Middleware Configuration Module.

Configures Cross-Origin Resource Sharing (CORS) policies and security headers.
Restricts API access to authorized frontend origins.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.config import settings
from backend.app.core.logging import logger


def setup_cors(app: FastAPI) -> None:
    """Attaches CORSMiddleware to FastAPI application with settings-defined origins."""
    origins = settings.CORS_ORIGINS
    logger.info(f"Configuring CORS middleware with allowed origins: {origins}")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
    )
