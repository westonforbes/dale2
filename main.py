import time

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

print("Stopping left motor")
left_motor.set_speed(speed = 0, direction = 'backward')