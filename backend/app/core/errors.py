"""Custom Exception Classes and Global Error Handling Middleware.

Establishes a unified exception hierarchy and FastAPI exception handlers
to ensure consistent JSON error responses across the entire REST API.
"""

from typing import Dict, Any, Optional
from fastapi import Request, status
from fastapi.responses import JSONResponse
from datetime import datetime

from backend.app.core.logging import logger


class AppException(Exception):
    """Base application exception for all domain errors."""

    def __init__(
        self,
        message: str,
        error_code: str = "INTERNAL_SERVER_ERROR",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}


class ModelNotFoundError(AppException):
    """Raised when required machine learning model artifacts are missing."""

    def __init__(self, artifact_name: str, path: str):
        super().__init__(
            message=f"Model artifact '{artifact_name}' not found at specified path: {path}",
            error_code="MODEL_NOT_FOUND",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details={"artifact_name": artifact_name, "path": path},
        )


class LandmarkValidationError(AppException):
    """Raised when incoming MediaPipe hand landmark vectors fail spatial validation."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="INVALID_LANDMARK_DATA",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details=details,
        )


class InferenceExecutionError(AppException):
    """Raised when neural network inference fails during evaluation."""

    def __init__(self, message: str):
        super().__init__(
            message=f"Model inference execution failed: {message}",
            error_code="INFERENCE_EXECUTION_ERROR",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """FastAPI Exception Handler for custom domain AppException errors."""
    logger.error(f"Domain Exception [{exc.error_code}] on {request.url.path}: {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "error_code": exc.error_code,
                "message": exc.message,
                "details": exc.details,
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }
        },
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Fallback FastAPI Exception Handler for unexpected Python runtime errors."""
    logger.critical(f"Unhandled Exception on {request.url.path}: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "error_code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected internal server error occurred.",
                "details": None,
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }
        },
    )
