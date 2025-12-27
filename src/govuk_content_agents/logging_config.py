import logging
import sys
import json
from .config import settings

class JsonFormatter(logging.Formatter):
    """Formatter that outputs JSON strings."""
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record)

def setup_logging():
    """Configure logging for the application."""
    root_logger = logging.getLogger()
    root_logger.setLevel(settings.LOG_LEVEL)

    # Clear existing handlers
    if root_logger.handlers:
        root_logger.handlers.clear()

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    
    if settings.ENVIRONMENT == "production":
        # JSON logging for production
        formatter = JsonFormatter()
        console_handler.setFormatter(formatter)
    else:
        # Standard logging for development
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(formatter)

    root_logger.addHandler(console_handler)

    # Set library log levels to avoid noise
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("pymongo").setLevel(logging.WARNING)

# Initialize logging on import
setup_logging()
logger = logging.getLogger(__name__)
