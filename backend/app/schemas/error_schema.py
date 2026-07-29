"""Error Response Schema Module.

Defines standardized Pydantic data schemas for API error responses.
"""

from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class ErrorDetailSchema(BaseModel):
    """Structured error payload returned on API failures."""

    error_code: str = Field(..., description="Unique machine-readable error code identifier", example="VALIDATION_ERROR")
    message: str = Field(..., description="Human-readable summary of the error", example="Invalid landmark vector size")
    details: Optional[Dict[str, Any]] = Field(default=None, description="Additional contextual details or validation errors")
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z", description="UTC timestamp of the error event")


class ErrorResponseSchema(BaseModel):
    """Wrapper container for error details."""

    error: ErrorDetailSchema = Field(..., description="Error detail object")
