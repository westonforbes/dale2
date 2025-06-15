import RPi.GPIO as GPIO

class MotorControl():
    
    def __init__(self, pwm_pin, dir_pin_a, dir_pin_b):

        self.GPIO = GPIO
        self.pwm_pin = pwm_pin
        self.dir_pin_a = dir_pin_a
        self.dir_pin_b = dir_pin_b

        # GPIO setup.
        self.GPIO.setmode(self.GPIO.BCM)
        self.GPIO.setup(self.pwm_pin, self.GPIO.OUT)
        self.GPIO.setup(self.dir_pin_a, self.GPIO.OUT)
        self.GPIO.setup(self.dir_pin_b, self.GPIO.OUT)

        # Set up PWM on the PWM pin with 1000 Hz frequency.
        self.pwm = self.GPIO.PWM(self.pwm_pin, 1000)
        self.pwm.start(0)

    def set_speed(self, speed, direction):
        """
        Control the motor speed and direction.
        :param speed: 0 to 100 (duty cycle)
        :param direction: 'forward' or 'backward'
        """
        if direction == 'forward':
            self.GPIO.output(self.dir_pin_a, self.GPIO.HIGH)
            self.GPIO.output(self.dir_pin_b, self.GPIO.LOW)
        elif direction == 'backward':
            self.GPIO.output(self.dir_pin_a, self.GPIO.LOW)
            self.GPIO.output(self.dir_pin_b, self.GPIO.HIGH)
        else:
            raise ValueError("Invalid direction. Use 'forward' or 'backward'.")

        self.pwm.ChangeDutyCycle(speed)