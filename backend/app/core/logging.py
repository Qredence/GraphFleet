"""
GraphFleet Logging Configuration

This module configures logging for the GraphFleet application.
It sets up logging handlers, formatters, and filters.
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from app.core.config import get_settings

settings = get_settings()

class RequestIdFilter(logging.Filter):
    """Filter that adds request ID to log records."""
    
    def __init__(self, request_id: str = ""):
        self.request_id = request_id
        super().__init__()
    
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = self.request_id
        return True

def setup_logging(
    log_level: Optional[str] = None,
    log_file: Optional[str] = None
) -> None:
    """Set up logging configuration.
    
    Args:
        log_level: Optional log level to override settings
        log_file: Optional log file path to override settings
    """
    level = getattr(logging, (log_level or settings.LOG_LEVEL).upper())
    
    # Create logs directory if it doesn't exist
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Configure logging format
    log_format = "%(asctime)s [%(request_id)s] %(levelname)s %(name)s: %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    
    # Create formatters
    console_formatter = logging.Formatter(log_format, date_format)
    file_formatter = logging.Formatter(log_format, date_format)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    
    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Add console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)
    console_handler.addFilter(RequestIdFilter())
    root_logger.addHandler(console_handler)
    
    # Add file handler if log file is specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(file_formatter)
        file_handler.addFilter(RequestIdFilter())
        root_logger.addHandler(file_handler)
    
    # Set levels for third-party loggers
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("fastapi").setLevel(logging.INFO)

def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the specified name.
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)

class LoggerAdapter(logging.LoggerAdapter):
    """Custom logger adapter that adds context to log messages."""
    
    def __init__(
        self,
        logger: logging.Logger,
        extra: Optional[Dict[str, Any]] = None
    ):
        """Initialize the logger adapter.
        
        Args:
            logger: Base logger instance
            extra: Additional context to add to log messages
        """
        super().__init__(logger, extra or {})
    
    def process(
        self,
        msg: str,
        kwargs: Dict[str, Any]
    ) -> tuple[str, Dict[str, Any]]:
        """Process the log message and kwargs.
        
        Args:
            msg: Log message
            kwargs: Additional keyword arguments
            
        Returns:
            Tuple of processed message and kwargs
        """
        extra = kwargs.get("extra", {})
        extra.update(self.extra)
        
        # Add timestamp if not present
        if "timestamp" not in extra:
            extra["timestamp"] = datetime.utcnow().isoformat()
        
        kwargs["extra"] = extra
        return msg, kwargs

def get_request_logger(
    name: str,
    request_id: str,
    **extra: Any
) -> LoggerAdapter:
    """Get a logger adapter for request handling.
    
    Args:
        name: Logger name
        request_id: Request ID
        **extra: Additional context
        
    Returns:
        LoggerAdapter instance
    """
    logger = get_logger(name)
    context = {"request_id": request_id, **extra}
    return LoggerAdapter(logger, context) 