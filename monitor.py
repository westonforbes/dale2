import time

def monitor_encoder(encoder):
    while True:
        pos = encoder.get_position()
        print(f"Encoder Position: {pos}")
        time.sleep(0.1)  # Adjust as needed for sampling rate

