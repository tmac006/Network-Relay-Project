import PiRelay
import time

# Initialize relays
relay1 = PiRelay.Relay("RELAY1")
relay2 = PiRelay.Relay("RELAY2")
relay3 = PiRelay.Relay("RELAY3")
relay4 = PiRelay.Relay("RELAY4")

# Functions to toggle each relay and print status
def toggle_relay(relay, relay_num):
    if relay.status() == "OFF":
        relay.on()
        print(f"Relay {relay_num} is now ON")
    else:
        relay.off()
        print(f"Relay {relay_num} is now OFF")

# Control loop for relay operations
while True:
    print("\nRelay Control Menu:")
    print("1. Toggle Relay 1")
    print("2. Toggle Relay 2")
    print("3. Toggle Relay 3")
    print("4. Toggle Relay 4")
    print("5. Turn all relays ON")
    print("6. Turn all relays OFF")
    print("0. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        toggle_relay(relay1, 1)
    elif choice == "2":
        toggle_relay(relay2, 2)
    elif choice == "3":
        toggle_relay(relay3, 3)
    elif choice == "4":
        toggle_relay(relay4, 4)
    elif choice == "5":
        relay1.on()
        relay2.on()
        relay3.on()
        relay4.on()
        print("All relays are now ON")
    elif choice == "6":
        relay1.off()
        relay2.off()
        relay3.off()
        relay4.off()
        print("All relays are now OFF")
    elif choice == "0":
        print("Exiting relay control.")
        break
    else:
        print("Invalid choice, please try again.")

    time.sleep(0.5)  # Brief delay for readability
