import pigpio
import threading
import time

class QuadratureEncoder:
    def __init__(self, gpioA, gpioB, pigpo_daemon=None):

        # Initialize pigpio class instance.
        self.pigpo_daemon = pigpo_daemon or pigpio.pi()

        # Allow some time for the pigpio daemon to start.
        time.sleep(0.5)

        # Check if the pigpio daemon is running.
        if not self.pigpo_daemon.connected:
            raise RuntimeError("pigpio daemon not running")

        # Set the GPIO pins for the encoder.
        self.gpioA = gpioA
        self.gpioB = gpioB

        # Initialize some variables.
        self.position = 0
        self.last_gpio = None

        # Create a lock for thread-safe access to position.
        self.lock = threading.Lock()

        # Setup calling _callback() when GPIO state changes.
        self.cbA = self.pigpo_daemon.callback(self.gpioA, pigpio.EITHER_EDGE, self._callback)
        self.cbB = self.pigpo_daemon.callback(self.gpioB, pigpio.EITHER_EDGE, self._callback)

    def _callback(self, gpio, level, tick):

        # Get the current state of both GPIOs.
        a = self.pigpo_daemon.read(self.gpioA)
        b = self.pigpo_daemon.read(self.gpioB)

        # With lock to ensure thread-safe access to position.
        with self.lock:

            # If the GPIO that triggered the callback is A...
            if gpio == self.gpioA:
                # If the level is high (1)...
                if level == 1:
                    # If B is low (0), increment position; otherwise, decrement.
                    if b == 0: self.position += 1 
                    else: -1
            
            # If the GPIO that triggered the callback is B...
            elif gpio == self.gpioB:
                # If the level is high (1)...
                if level == 1:
                    # If A is high, increment position; otherwise, decrement.
                    if a == 1: self.position += 1 
                    else: -1

    def get_position(self):
        with self.lock:
            return self.position

    def reset(self):
        with self.lock:
            self.position = 0

    def cancel(self):
        self.cbA.cancel()
        self.cbB.cancel()
        self.pigpo_daemon.stop()


# Background thread for monitoring
def monitor_encoder(encoder):
    while True:
        pos = encoder.get_position()
        print(f"Encoder Position: {pos}")
        time.sleep(0.1)  # Adjust as needed for sampling rate


if __name__ == "__main__":
    # Use GPIO17 and GPIO27 for encoder A and B
    encoder = QuadratureEncoder(gpioA=17, gpioB=27)

    try:
        # Start monitoring in a background thread
        monitor_thread = threading.Thread(target=monitor_encoder, args=(encoder,), daemon=True)
        monitor_thread.start()

        # Main thread continues doing other tasks
        # GPIO pin definitions
        L_ENA = 18  # PWM pin (GPIO18, Physical pin 12)
        L_IN1 = 24  # Direction pin
        L_IN2 = 25  # Direction pin

        from motor_control import MotorControl

        left_motor = MotorControl(pwm_pin = L_ENA, dir_pin_a = L_IN1, dir_pin_b = L_IN2)


        print("Starting left motor at 70% speed in forward direction")
        left_motor.set_speed(speed = 70, direction = 'forward')

        print("Waiting for 5 seconds...")
        time.sleep(5)

        print("Starting left motor at 70% speed in backward direction")
        left_motor.set_speed(speed = 70, direction = 'backward')

        print("Waiting for 5 seconds...")
        time.sleep(5)

        print("Stopping left motor")
        left_motor.set_speed(speed = 0, direction = 'backward')

    except KeyboardInterrupt:
        print("Shutting down.")
    finally:
        print("Shutting down.")
        encoder.cancel()
