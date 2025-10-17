import logging
import logging.config
import sys
from pathlib import Path
from typing import Optional
import json
from datetime import datetime
from config import settings

class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging."""
    
    def format(self, record):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields
        for key, value in record.__dict__.items():
            if key not in ['name', 'msg', 'args', 'levelname', 'levelno', 'pathname', 
                          'filename', 'module', 'exc_info', 'exc_text', 'stack_info',
                          'lineno', 'funcName', 'created', 'msecs', 'relativeCreated',
                          'thread', 'threadName', 'processName', 'process', 'getMessage']:
                log_entry[key] = value
        
        return json.dumps(log_entry)

class RequestLogger:
    """Custom logger for HTTP requests."""
    
    def __init__(self, name: str = "request"):
        self.logger = logging.getLogger(name)
    
    def log_request(self, method: str, path: str, status_code: int, 
                   response_time: float, user_id: Optional[str] = None,
                   ip_address: Optional[str] = None, user_agent: Optional[str] = None):
        """Log HTTP request details."""
        self.logger.info(
            "HTTP Request",
            extra={
                "method": method,
                "path": path,
                "status_code": status_code,
                "response_time_ms": round(response_time * 1000, 2),
                "user_id": user_id,
                "ip_address": ip_address,
                "user_agent": user_agent
            }
        )

class SecurityLogger:
    """Custom logger for security events."""
    
    def __init__(self, name: str = "security"):
        self.logger = logging.getLogger(name)
    
    def log_auth_attempt(self, email: str, success: bool, ip_address: Optional[str] = None,
                        user_agent: Optional[str] = None, reason: Optional[str] = None):
        """Log authentication attempts."""
        level = logging.INFO if success else logging.WARNING
        self.logger.log(
            level,
            f"Authentication attempt: {'success' if success else 'failed'}",
            extra={
                "event_type": "auth_attempt",
                "email": email,
                "success": success,
                "ip_address": ip_address,
                "user_agent": user_agent,
                "reason": reason
            }
        )
    
    def log_token_validation(self, user_id: str, success: bool, reason: Optional[str] = None):
        """Log token validation events."""
        level = logging.INFO if success else logging.WARNING
        self.logger.log(
            level,
            f"Token validation: {'success' if success else 'failed'}",
            extra={
                "event_type": "token_validation",
                "user_id": user_id,
                "success": success,
                "reason": reason
            }
        )
    
    def log_rate_limit_exceeded(self, ip_address: str, endpoint: str, limit: int):
        """Log rate limit exceeded events."""
        self.logger.warning(
            "Rate limit exceeded",
            extra={
                "event_type": "rate_limit_exceeded",
                "ip_address": ip_address,
                "endpoint": endpoint,
                "limit": limit
            }
        )

def setup_logging():
    """Setup application logging configuration."""
    
    # Create logs directory if it doesn't exist
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Logging configuration
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": settings.log_format,
                "datefmt": "%Y-%m-%d %H:%M:%S"
            },
            "json": {
                "()": JSONFormatter
            },
            "detailed": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s:%(lineno)d - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": settings.log_level,
                "formatter": "standard",
                "stream": sys.stdout
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "INFO",
                "formatter": "json",
                "filename": "logs/app.log",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
                "encoding": "utf8"
            },
            "error_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "ERROR",
                "formatter": "detailed",
                "filename": "logs/error.log",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
                "encoding": "utf8"
            },
            "security_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "INFO",
                "formatter": "json",
                "filename": "logs/security.log",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 10,
                "encoding": "utf8"
            }
        },
        "loggers": {
            "": {  # Root logger
                "level": settings.log_level,
                "handlers": ["console", "file"],
                "propagate": False
            },
            "uvicorn": {
                "level": "INFO",
                "handlers": ["console", "file"],
                "propagate": False
            },
            "uvicorn.error": {
                "level": "INFO",
                "handlers": ["console", "error_file"],
                "propagate": False
            },
            "uvicorn.access": {
                "level": "INFO",
                "handlers": ["console", "file"],
                "propagate": False
            },
            "security": {
                "level": "INFO",
                "handlers": ["console", "security_file"],
                "propagate": False
            },
            "request": {
                "level": "INFO",
                "handlers": ["console", "file"],
                "propagate": False
            },
            "sqlalchemy.engine": {
                "level": "WARNING",
                "handlers": ["console", "file"],
                "propagate": False
            }
        }
    }
    
    # Apply logging configuration
    logging.config.dictConfig(logging_config)
    
    # Create specialized loggers
    request_logger = RequestLogger()
    security_logger = SecurityLogger()
    
    return request_logger, security_logger

def get_logger(name: str) -> logging.Logger:
    """Get a logger instance."""
    return logging.getLogger(name)

# Initialize loggers
request_logger, security_logger = setup_logging()

