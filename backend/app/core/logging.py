"""Production Logging Configuration Module.

Configures structured logging across the application with ISO timestamps,
log levels, and module name context. Replaces raw print() calls.
"""

import sys
import logging
from typing import Optional
from backend.app.core.config import settings


class CustomFormatter(logging.Formatter):
    """Custom Log Formatter delivering clean, ANSI-colored output for dev and structured strings for prod."""

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format_str = "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"

    FORMATS = {
        logging.DEBUG: grey + format_str + reset,
        logging.INFO: grey + format_str + reset,
        logging.WARNING: yellow + format_str + reset,
        logging.ERROR: red + format_str + reset,
        logging.CRITICAL: bold_red + format_str + reset,
    }

    def format(self, record: logging.LogRecord) -> str:
        """Format log record with colors based on log level."""
        log_fmt = self.FORMATS.get(record.levelno, self.format_str)
        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%dT%H:%M:%S%z")
        return formatter.format(record)


def setup_logging(log_level: Optional[str] = None) -> logging.Logger:
    """Configures application-wide logging output stream and log levels."""
    level = (log_level or settings.LOG_LEVEL).upper()
    numeric_level = getattr(logging, level, logging.INFO)

    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)

    # Clear existing handlers to prevent duplicate logging output
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    # Stream Handler to stdout
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(numeric_level)
    handler.setFormatter(CustomFormatter())

    root_logger.addHandler(handler)

    # Disable noisy third-party loggers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

    logger = logging.getLogger(settings.APP_NAME)
    logger.info(f"Logging initialized at level: {level}")
    return logger


# Pre-configured App Logger instance
logger = setup_logging()
