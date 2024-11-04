import time
import RPi.GPIO as GPIO
from threading import Thread

# GPIO setup
GPIO.setmode(GPIO.BCM)
relay_pins = {
    1: 17,  # Example: Relay 1 connected to GPIO pin 17
    2: 27,  # Relay 2 connected to GPIO pin 27, and so on
}
for pin in relay_pins.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)  # Default all relays to OFF

# Dictionary to store relay configurations
relays = {
    1: {
        'mode': 'NONE',
        'ping': {'interval': 0, 'missed': 0, 'reset': 0, 'missed_count': 0},
        'timer': {'on_time': None, 'off_time': None},
        'state': 'OFF',  # Current state of the relay
        'init_state': 'OFF'  # Initial state after reset/reboot
    },
    2: {
        'mode': 'NONE',
        'ping': {'interval': 0, 'missed': 0, 'reset': 0, 'missed_count': 0},
        'timer': {'on_time': None, 'off_time': None},
        'state': 'OFF',
        'init_state': 'OFF'
    }
}

# Function to handle ping monitoring in a separate thread
def ping_monitor(relay_num):
    config = relays[relay_num]['ping']
    while config['interval'] > 0:
        print(f"Pinging for Relay {relay_num}...")
        config['missed_count'] += 1  # Simulate ping failure for demo purposes
        print(f"Missed Pings: {config['missed_count']} / {config['missed']}")

        if config['missed_count'] >= config['missed']:
            toggle_relay(relay_num, 'RESET', config['reset'])
            config['missed_count'] = 0  # Reset missed ping count after toggle

        time.sleep(config['interval'])

# Function to handle relay toggling
def toggle_relay(relay_num, mode='MANUAL', reset_duration=0):
    current_state = relays[relay_num]['state']
    new_state = 'OFF' if current_state == 'ON' else 'ON'

    # Update GPIO state
    GPIO.output(relay_pins[relay_num], GPIO.HIGH if new_state == 'ON' else GPIO.LOW)
    relays[relay_num]['state'] = new_state
    print(f"Relay {relay_num} toggled {mode}: {new_state}")

    if reset_duration > 0:  # If reset_duration is provided, toggle back after a delay
        time.sleep(reset_duration)
        GPIO.output(relay_pins[relay_num], GPIO.HIGH if current_state == 'ON' else GPIO.LOW)
        relays[relay_num]['state'] = current_state
        print(f"Relay {relay_num} reset back to {current_state} after {reset_duration} seconds")

# Function to manually control relay (ON/OFF)
def set_relay_state(relay_num, state):
    if state.upper() == 'ON':
        relays[relay_num]['state'] = 'ON'
        GPIO.output(relay_pins[relay_num], GPIO.HIGH)
        print(f"Relay {relay_num} turned ON")
    elif state.upper() == 'OFF':
        relays[relay_num]['state'] = 'OFF'
        GPIO.output(relay_pins[relay_num], GPIO.LOW)
        print(f"Relay {relay_num} turned OFF")
    else:
        print("ERROR: Invalid state")

# Function to set initial state of relays
def set_initial_state(relay_num, state):
    relays[relay_num]['init_state'] = state
    GPIO.output(relay_pins[relay_num], GPIO.HIGH if state == 'ON' else GPIO.LOW)
    print(f"Relay {relay_num} initial state set to {state}")

# Function to configure relay in Ping mode
def configure_ping_mode(relay_num, interval, missed, reset):
    relays[relay_num]['mode'] = 'PING'
    relays[relay_num]['ping'] = {
        'interval': interval,
        'missed': missed,
        'reset': reset,
        'missed_count': 0
    }
    print(f"Relay {relay_num} configured for Ping mode")
    # Start ping monitoring thread
    Thread(target=ping_monitor, args=(relay_num,)).start()

# Function to configure relay in Timer mode
def configure_timer_mode(relay_num, on_time, off_time):
    relays[relay_num]['mode'] = 'TIMER'
    relays[relay_num]['timer'] = {'on_time': on_time, 'off_time': off_time}
    print(f"Relay {relay_num} configured for Timer mode")

# Cleanup GPIO on exit
def cleanup_gpio():
    GPIO.cleanup()