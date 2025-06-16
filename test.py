import time
SLEEP_TIME = 1

def test_code(left_motor, left_encoder):
    print("Starting left motor at 70% speed in forward direction")
    left_motor.set_speed(speed = 70, direction = 'forward')

    print("Waiting for 1 seconds...")
    time.sleep(SLEEP_TIME)

    print("Stopping left motor")
    left_motor.set_speed(speed = 0, direction = 'backward')
    time.sleep(2)
    print("Left encoder position:", left_encoder.get_position())