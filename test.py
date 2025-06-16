import time

def test_code(left_motor):
    print("Starting left motor at 70% speed in forward direction")
    left_motor.set_speed(speed = 70, direction = 'forward')

    print("Waiting for 1 seconds...")
    time.sleep(1)

    print("Starting left motor at 70% speed in backward direction")
    left_motor.set_speed(speed = 70, direction = 'backward')

    print("Waiting for 1 seconds...")
    time.sleep(1)

    print("Stopping left motor")
    left_motor.set_speed(speed = 0, direction = 'backward')