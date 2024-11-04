import PiRelay  # Ensure PiRelay library is installed with: pip install pirelay
import time

# Initialize the relay (adjust for relay channel if needed)
relay = PiRelay.Relay("RELAY1")  # Use RELAY1, RELAY2, etc., for specific channels

# Turn the relay on, wait 30 seconds, then turn it off
print("Turning relay ON...")
relay.on()
print("Relay is ON. Waiting for 30 seconds...")
time.sleep(30)

print("Turning relay OFF...")
relay.off()
print("Relay is OFF.")
