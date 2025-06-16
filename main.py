from quadrature_monitor import QuadratureEncoder
from motor_control import MotorControl
import monitor
import test
import threading

# GPIO pin definitions
L_ENA = 18  # PWM pin
L_IN1 = 24  # Direction pin
L_IN2 = 25  # Direction pin
L_PHASE_A = 17  # Encoder A pin
L_PHASE_B = 27  # Encoder B pin

# Use GPIO17 and GPIO27 for encoder A and B.
left_encoder = QuadratureEncoder(gpio_a=L_PHASE_A, gpio_b=L_PHASE_B)

# Start monitoring in a background thread.
monitor_thread = threading.Thread(target=monitor.monitor_encoder, args=(left_encoder,), daemon=True)
monitor_thread.start()

# Initialize the motor control for the left motor.
left_motor = MotorControl(pwm_pin = L_ENA, dir_pin_a = L_IN1, dir_pin_b = L_IN2)

# Test stuff.
test.test_code(left_motor, left_encoder)

# Shut down.
left_encoder.cancel()