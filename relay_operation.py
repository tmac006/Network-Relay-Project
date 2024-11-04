import time
import datetime
import requests  # for pinging an external site
import RPi.GPIO as GPIO  # real GPIO library for Raspberry Pi

# Setup GPIO for relay control
RELAY_PIN = 17  # adjust based on your setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)

# Relay Modes
class RelayModes:
    PING = "ping"
    TIMER = "timer"
    NONE = "none"

# Relay Controller Class
class RelayController:
    def __init__(self, mode=RelayModes.NONE, ping_interval=60, missed_pings=3, reset_length=5, time_on=None, time_off=None):
        self.mode = mode
        self.ping_interval = ping_interval
        self.missed_pings = missed_pings
        self.reset_length = reset_length
        self.time_on = time_on
        self.time_off = time_off
        self.missed_ping_count = 0
        self.last_ping_time = time.time()

    def ping_mode_operation(self):
        """Operation for Ping Mode to check network connectivity."""
        if time.time() - self.last_ping_time >= self.ping_interval:
            try:
                # Attempt to ping a site (e.g., google.com)
                requests.get("https://www.google.com", timeout=3)
                print("Ping successful")
                self.missed_ping_count = 0  # reset missed pings
            except requests.RequestException:
                print("Ping failed")
                self.missed_ping_count += 1

            # If missed pings exceed threshold, toggle relay
            if self.missed_ping_count >= self.missed_pings:
                print("Missed pings exceeded threshold, toggling relay")
                self.toggle_relay()
                time.sleep(self.reset_length)
                self.turn_off_relay()

            self.last_ping_time = time.time()  # update last ping time

    def timer_mode_operation(self):
        """Operation for Timer Mode to control relay based on time."""
        current_time = datetime.datetime.now().time()
        
        if self.time_on <= current_time <= self.time_off:
            print("Timer Mode: Turning relay ON")
            self.turn_on_relay()
        else:
            print("Timer Mode: Turning relay OFF")
            self.turn_off_relay()

    def toggle_relay(self):
        """Toggle the relay."""
        GPIO.output(RELAY_PIN, not GPIO.input(RELAY_PIN))
        print("Relay toggled")

    def turn_on_relay(self):
        """Turn the relay ON."""
        GPIO.output(RELAY_PIN, GPIO.HIGH)
        print("Relay ON")

    def turn_off_relay(self):
        """Turn the relay OFF."""
        GPIO.output(RELAY_PIN, GPIO.LOW)
        print("Relay OFF")

    def run(self):
        """Main function to run the relay based on selected mode."""
        if self.mode == RelayModes.PING:
            self.ping_mode_operation()
        elif self.mode == RelayModes.TIMER:
            self.timer_mode_operation()
        else:
            print("No active mode. Relay is idle.")

# Main Execution
if __name__ == "__main__":
    # Configurations
    mode = RelayModes.PING  # or RelayModes.TIMER, RelayModes.NONE
    ping_interval = 60      # seconds
    missed_pings = 3
    reset_length = 5        # seconds

    # For timer mode
    time_on = datetime.time(8, 0)   # 8:00 AM
    time_off = datetime.time(18, 0) # 6:00 PM

    # Create RelayController object
    relay_controller = RelayController(mode=mode, ping_interval=ping_interval, missed_pings=missed_pings,
                                       reset_length=reset_length, time_on=time_on, time_off=time_off)

    try:
        # Run relay operation in a loop
        while True:
            relay_controller.run()
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting program.")
    finally:
        GPIO.cleanup()  # Reset GPIO settings
