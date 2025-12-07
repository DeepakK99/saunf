# app/logger.py
import logging
from logging.handlers import RotatingFileHandler
import os
from app.config import settings

LOG_LEVEL = settings.LOG_LEVEL
LOG_DIR = "logs"

# make sure logs/ folder exists
os.makedirs(LOG_DIR, exist_ok=True)

def get_logger(name: str = "app"):
    """
    Creates or returns a logger with its own file.
    Example: get_logger("main_worker") -> logs/main_worker.log
    """
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger  # already created → no duplicate handlers

    logger.setLevel(LOG_LEVEL)

    # File handler
    file_path = os.path.join(LOG_DIR, f"{name}.log")
    file_handler = RotatingFileHandler(
        file_path,
        maxBytes=5_000_000,
        backupCount=3,
    )

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
        "%Y-%m-%d %H:%M:%S"
    )

    file_handler.setFormatter(formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Attach handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.propagate = False

    return logger
