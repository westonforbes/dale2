import pigpio
import threading
import time

class QuadratureEncoder:
    def __init__(self, gpio_a, gpio_b, pigpio_daemon_connector=None):

        # Initialize pigpio class instance.
        self.pigpio_daemon_connector = pigpio_daemon_connector or pigpio.pi()

        # Allow some time for the pigpio daemon to start.
        time.sleep(0.5)

        # Check if the pigpio daemon is running.
        if not self.pigpio_daemon_connector.connected:
            raise RuntimeError("pigpio daemon not running")

        # Set the GPIO pins for the encoder.
        self.gpio_b = gpio_b
        self.gpio_a = gpio_a

        # Initialize some variables.
        self.position = 0
        self.last_gpio = None

        # Create a lock for thread-safe access to position.
        self.lock = threading.Lock()

        # Get the initial state of the GPIO pins.
        # self.last_state = (self.pigpio_daemon_connector.read(gpio_b) << 1) | self.pigpio_daemon_connector.read(gpio_a)
        self.last_state = 0

        # Setup calling _callback() when GPIO state changes.
        self.cbA = self.pigpio_daemon_connector.callback(self.gpio_b, pigpio.EITHER_EDGE, self._callback)
        self.cbB = self.pigpio_daemon_connector.callback(self.gpio_a, pigpio.EITHER_EDGE, self._callback)

    def _callback(self, gpio, level, tick):

        # Read the current state of the GPIO pins.
        a = self.pigpio_daemon_connector.read(self.gpio_b)
        b = self.pigpio_daemon_connector.read(self.gpio_a)

        # Create a new state based on the current GPIO readings.
        # Bit shift A value to position 1 and B value to position 0.
        # a=0, b=0 → new_state = 0 (binary 00)
        # a=0, b=1 → new_state = 1 (binary 01)
        # a=1, b=0 → new_state = 2 (binary 10)
        # a=1, b=1 → new_state = 3 (binary 11)
        new_state = (a << 1) | b

        # Create a mapping table we'll use to determine direction.
        delta_table = {
            (0, 1): 1,
            (1, 3): 1,
            (3, 2): 1,
            (2, 0): 1,
            (1, 0): -1,
            (3, 1): -1,
            (2, 3): -1,
            (0, 2): -1,
        }

        # Using the thread lock to ensure thread-safe access to position...
        with self.lock:
            
            # Get the direction.
            delta = delta_table.get((self.last_state, new_state), 0)
            
            # Add the direction to the position.
            self.position += delta
            
            # Update the last state.
            self.last_state = new_state

    def get_position(self):
        # Return the current position in a thread-safe manner.
        with self.lock:
            return self.position

    def reset(self):
        # Reset the position to zero in a thread-safe manner.
        with self.lock:
            self.position = 0

    def cancel(self):
        # Cancel the callbacks and stop the pigpio daemon.
        self.cbA.cancel()
        self.cbB.cancel()
        self.pigpio_daemon_connector.stop()