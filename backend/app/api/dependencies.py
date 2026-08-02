"""FastAPI Dependency Injection Helper Module.

Provides shared dependencies for route handlers (e.g., Settings, Services).
"""

from app.core.config import Settings, settings


def get_settings() -> Settings:
    """Dependency provider for application settings."""
    return settings
