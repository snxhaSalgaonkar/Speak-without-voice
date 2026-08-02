"""FastAPI Core Application Entrypoint.

Initializes FastAPI application instance, configures CORS middleware,
registers global exception handlers, and mounts API v1 routes.
"""

import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.constants import API_V1_STR, PROJECT_NAME, VERSION
from app.core.logging import logger
from app.core.security import setup_cors
# pyrefly: ignore [missing-import]
from app.core.errors import (
    AppException,
    app_exception_handler,
    unhandled_exception_handler,
)
from app.api.v1.router import api_v1_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application Lifespan Event Handler (Startup & Shutdown)."""
    # Startup tasks
    logger.info(f"Starting {PROJECT_NAME} API v{VERSION} [{settings.APP_ENV}]...")
    yield
    # Shutdown tasks
    logger.info(f"Shutting down {PROJECT_NAME} API service...")


def create_application() -> FastAPI:
    """Application Factory Function initializing FastAPI instance and middleware."""
    app = FastAPI(
        title=PROJECT_NAME,
        version=VERSION,
        description="Real-time Sign Language Recognition API using MediaPipe keypoints and TensorFlow Keras DNN.",
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
        lifespan=lifespan,
    )

    # Configure CORS Middleware
    setup_cors(app)

    # Register Exception Handlers
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)

    # Request Processing Time & Context Logging Middleware
    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time_ms = round((time.time() - start_time) * 1000, 2)
        response.headers["X-Process-Time-MS"] = str(process_time_ms)
        logger.debug(f"{request.method} {request.url.path} processed in {process_time_ms}ms")
        return response

    # Mount API v1 Router
    app.include_router(api_v1_router, prefix=API_V1_STR)

    # Root redirect / baseline endpoint
    @app.get("/", include_in_schema=False)
    async def root_redirect():
        return JSONResponse(
            content={
                "message": f"Welcome to {PROJECT_NAME} API",
                "version": VERSION,
                "docs": "/docs" if settings.DEBUG else "Disabled in production",
                "health": f"{API_V1_STR}/health",
            }
        )

    return app


# Instantiated FastAPI Application
app = create_application()
