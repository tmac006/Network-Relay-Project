import logging
from enum import Enum
from threading import Lock

# Lock for thread-safe logging
log_lock = Lock()

# Enum for log types (categories)
class LogType(Enum):
    INFO = "INFO"
    ERROR = "ERROR"
    DEBUG = "DEBUG"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"

# Configuration constants
LOG_FILE = "relay.txt"  # Log file path
LOG_LEVEL = logging.INFO  # Set the log level to INFO

# Set up the logger with append mode and ensure it respects the log level
logging.basicConfig(
    filename=LOG_FILE,
    level=LOG_LEVEL,  # This controls the minimum level that gets logged
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filemode='a'  # Open in append mode
)

def log_message(log_type: LogType, message: str):
    """
    Logs a message based on the log type (INFO, ERROR, DEBUG, WARNING, CRITICAL).
    Thread-safe with a lock to ensure only one thread can log at a time.
    """
    with log_lock:  # Ensure thread-safe logging
        if log_type == LogType.INFO:
            logging.info(message)
        elif log_type == LogType.ERROR:
            logging.error(message)
        elif log_type == LogType.DEBUG:
            logging.debug(message)
        elif log_type == LogType.WARNING:
            logging.warning(message)
        elif log_type == LogType.CRITICAL:
            logging.critical(message)


if __name__ == "__main__":
    log_message(LogType.INFO, "This is an informational message.")
    log_message(LogType.ERROR, "This is an error message.")
    log_message(LogType.DEBUG, "This is a debug message.")
    log_message(LogType.WARNING, "This is a warning message.")
    log_message(LogType.CRITICAL, "This is a critical message.")
