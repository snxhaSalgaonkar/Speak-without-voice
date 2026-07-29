"""Centralized Application Configuration Module.

Loads and validates environment variables using Pydantic BaseSettings.
Guarantees type-safety and fail-fast validation on startup.
"""

from typing import List, Union
from pydantic import Field, validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings schema and environment variable loader."""

    # Application Metadata
    APP_NAME: str = Field(default="Speak-without-voice", description="Name of the application")
    APP_ENV: str = Field(default="development", description="Environment: development, staging, production")
    DEBUG: bool = Field(default=True, description="Enable debug mode and detailed logs")

    # Server Network Settings
    HOST: str = Field(default="0.0.0.0", description="Server host interface binding")
    PORT: int = Field(default=8000, description="Server port binding")

    # Security & CORS Settings
    CORS_ORIGINS: Union[List[str], str] = Field(
        default=["http://localhost:3000", "http://127.0.0.1:3000"],
        description="Allowed HTTP origins for Cross-Origin Resource Sharing",
    )

    # Logging Settings
    LOG_LEVEL: str = Field(default="INFO", description="Logging output level (DEBUG, INFO, WARNING, ERROR)")

    # Machine Learning Model Artifact Paths
    MODEL_PATH: str = Field(
        default="models/gesture_classifier.keras",
        description="Relative path to trained Keras model artifact",
    )
    SCALER_PATH: str = Field(
        default="models/feature_scaler.pkl",
        description="Relative path to fitted StandardScaler artifact",
    )
    LABEL_MAP_PATH: str = Field(
        default="models/label_map.json",
        description="Relative path to gesture label mapping JSON file",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        """Parses comma-separated string or list into a list of origin strings."""
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",") if i.strip()]
        elif isinstance(v, list):
            return v
        return ["http://localhost:3000", "http://127.0.0.1:3000"]

    @property
    def is_development(self) -> bool:
        """Returns True if the application is running in development mode."""
        return self.APP_ENV.lower() in ("development", "dev", "local")


# Global Singleton Settings Instance
settings = Settings()
