from logging_utility import configure_logging, log_connection, log_received, log_reset, log_boot, log_error, LogType

def get_user_input(prompt, options=None, default=None):
    """
    Utility function to get validated user input.
    If options are provided, the input will be validated against them.
    """
    while True:
        user_input = input(f"{prompt} ").strip()
        if not user_input and default is not None:
            return default
        if options and user_input not in options:
            print(f"Invalid input. Please choose from: {', '.join(options)}")
        else:
            return user_input

def choose_log_file():
    """
    Prompt the user to choose or input a log file name.
    """
    log_file = input("Enter the name of the log file (default: relay.txt): ").strip()
    return log_file if log_file else "relay.txt"

def choose_log_level():
    """
    Prompt the user to choose a log level.
    """
    log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    log_level = get_user_input(
        "Choose the log level (DEBUG, INFO, WARNING, ERROR, CRITICAL - default: INFO):", 
        options=log_levels, 
        default="INFO"
    )
    return log_level

def choose_log_types():
    """
    Prompt the user to choose which log types to enable.
    """
    available_log_types = {
        '1': LogType.CONNECTION,
        '2': LogType.RECEIVED,
        '3': LogType.RESET,
        '4': LogType.BOOT,
        '5': LogType.ERROR
    }

    print("Choose the log types to enable (e.g., 1 2 5 for connection, received, and error):")
    print("1 - connection")
    print("2 - received")
    print("3 - reset")
    print("4 - boot")
    print("5 - error")

    log_types_input = input("Enter your choices (default: 1 5 for connection and error): ").strip()
    if not log_types_input:
        log_types_input = "1 5"  # Default selection

    log_types = set()
    for choice in log_types_input.split():
        if choice in available_log_types:
            log_types.add(available_log_types[choice])
        else:
            print(f"Invalid choice: {choice}. Ignoring it.")
    
    return log_types

def configure_logging_interactive():
    """
    Interactive logging configuration. Prompts the user for log file, level, and types.
    """
    print("\n--- Logging Configuration ---")

    # Choose log file
    log_file = choose_log_file()

    # Choose log level
    log_level = choose_log_level()

    # Choose log types
    log_types = choose_log_types()

    # Configure logging with user choices
    configure_logging(log_file=log_file, log_level=log_level, log_types=log_types)

    print(f"\nLogging configured. Log file: {log_file}, Log level: {log_level}, Log types: {[t.name for t in log_types]}")

def simulate_log_events():
    """
    Function to simulate log events after configuration.
    """
    print("\n--- Simulating log events ---")
    log_connection("192.168.1.100")
    log_received("Test data")
    log_reset()
    log_boot()
    log_error("Simulated error")

def main():
    """
    Main function that runs the interactive terminal for configuring logging.
    """
    configure_logging_interactive()  # Configure logging interactively
    simulate_log_events()  # Simulate some log events

if __name__ == "__main__":
    main()
