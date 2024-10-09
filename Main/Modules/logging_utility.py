import argparse
import logging
from enum import Enum
from threading import Lock

# Thread-safe lock for logging operations
log_lock = Lock()

# Log configuration dictionary to store the log settings
_log_config = {
    "log_file": "relay.txt",  # Default log file changed to .txt
    "log_level": logging.INFO,
    "log_types": set()  # To be set by the user
}

# Enum to define log types
class LogType(Enum):
    CONNECTION = "connection"
    RECEIVED = "received"
    RESET = "reset"
    BOOT = "boot"
    ERROR = "error"

# Configure the logging module based on user input
def configure_logging(log_file="relay.txt", log_level=logging.INFO, log_types=None):
    if log_types is None:
        log_types = {LogType.CONNECTION, LogType.RECEIVED, LogType.RESET, LogType.BOOT, LogType.ERROR}
    
    _log_config["log_file"] = log_file
    _log_config["log_level"] = log_level
    _log_config["log_types"] = set(log_types)

# Internal function to handle writing logs to a file
def _write_log(message, level=logging.INFO):
    with log_lock:
        logger = logging.getLogger("NetworkRelayLogger")
        logger.setLevel(_log_config["log_level"])
        
        handler = logging.FileHandler(_log_config["log_file"])
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        handler.setFormatter(formatter)
        
        logger.addHandler(handler)
        
        if level == logging.DEBUG:
            logger.debug(message)
        elif level == logging.INFO:
            logger.info(message)
        elif level == logging.WARNING:
            logger.warning(message)
        elif level == logging.ERROR:
            logger.error(message)
        elif level == logging.CRITICAL:
            logger.critical(message)
        
        logger.removeHandler(handler)
        handler.close()

# Logging functions for different log types
def log_connection(user_ip):
    if LogType.CONNECTION in _log_config["log_types"]:
        _write_log(f"User connected with IP: {user_ip}", logging.INFO)

def log_received(data):
    if LogType.RECEIVED in _log_config["log_types"]:
        _write_log(f"Data received: {data}", logging.INFO)

def log_reset():
    if LogType.RESET in _log_config["log_types"]:
        _write_log("System reset", logging.INFO)

def log_boot():
    if LogType.BOOT in _log_config["log_types"]:
        _write_log("System booted", logging.INFO)

def log_error(error_message):
    if LogType.ERROR in _log_config["log_types"]:
        _write_log(f"Error occurred: {error_message}", logging.ERROR)

# Dynamically set the log level if needed
def set_log_level(level):
    _log_config["log_level"] = level

# Helper function to map log level strings to logging constants
def parse_log_level(level_str):
    level_str = level_str.upper()
    levels = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
    }
    return levels.get(level_str, logging.INFO)  # Default to INFO if not found

# Helper function to convert log type strings into LogType enum values
def parse_log_types(log_types_str):
    available_log_types = {
        "connection": LogType.CONNECTION,
        "received": LogType.RECEIVED,
        "reset": LogType.RESET,
        "boot": LogType.BOOT,
        "error": LogType.ERROR
    }

    log_types = set()
    for log_type in log_types_str:
        if log_type in available_log_types:
            log_types.add(available_log_types[log_type])
        else:
            raise ValueError(f"Invalid log type: {log_type}")
    
    return log_types

def test_log_levels():
    """
    Logs messages at all different log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL).
    This is useful to test whether each log level is being correctly handled.
    """
    print("\n--- Testing All Log Levels ---")
    
    _write_log("This is a DEBUG message", level=logging.DEBUG)
    _write_log("This is an INFO message", level=logging.INFO)
    _write_log("This is a WARNING message", level=logging.WARNING)
    _write_log("This is an ERROR message", level=logging.ERROR)
    _write_log("This is a CRITICAL message", level=logging.CRITICAL)
    
    print("All log levels tested. Check the log file to verify the output.\n")

# Simulate some log events for testing purposes
def simulate_log_events():
    print("\n--- Simulating Log Events ---")
    log_connection("192.168.1.100")
    log_received("Test data")
    log_reset()
    log_boot()
    log_error("Simulated error")

# Test harness function to simulate log events and accept command-line input
def main():
    parser = argparse.ArgumentParser(description="Configure network relay logging.")
    
    parser.add_argument(
        '--log-file', 
        type=str, 
        default='relay.txt',  # Change default to .txt
        help='Path to the log file (default: relay.txt)'
    )
    parser.add_argument(
        '--log-level', 
        type=str, 
        default='INFO', 
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Logging level (default: INFO)'
    )
    parser.add_argument(
        '--log-types', 
        type=str, 
        nargs='+', 
        default=['connection', 'error'], 
        help='Log types to enable (e.g., connection, received, reset, boot, error)'
    )
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Parse log level and log types
    log_level = parse_log_level(args.log_level)
    log_types = parse_log_types(args.log_types)
    
    # Configure logging based on parsed arguments
    configure_logging(log_file=args.log_file, log_level=log_level, log_types=log_types)
    
    # Test all log levels
    test_log_levels()

    # Simulate some logging events
    simulate_log_events()

if __name__ == "__main__":
    main()
