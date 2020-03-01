import RPi.GPIO as GPIO
import time


class FT1117M:
    """
    Driver for the FT1117M servo
    """

    def __init__(self, pin=14, frequency=400):
        self.servoPIN = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.servoPIN, GPIO.OUT)
        self.freq = frequency  # [Hz]
        self.pinctl = GPIO.PWM(self.servoPIN, self.freq)
        self.started = False

    def _pos_to_pwm(self, pos):
        """
        Translates a 'pos' in deg (range -60 deg to +60 deg) to pwm (in percent)
        """
        pulse_us = (1500 + 10 * pos)
        period_us = 1/self.freq * 1e6
        assert period_us > pulse_us, "ERR desired pulse too long for frequency"
        return pulse_us/period_us * 100

    def start(self, initpos=0):
        self.pinctl.start(initpos)
        self.started = True

    def setpos(self, pos):
        assert self.started, "ERR not started yet"
        # clip:
        pos = min(60, pos)
        pos = max(-60, pos)
        pwm = self._pos_to_pwm(pos)
        print("Setting servo to %d deg (pwm %.2f pct)" % (pos, pwm))
        self.pinctl.ChangeDutyCycle(self._pos_to_pwm(pos))

    def stop(self):
        assert self.started, "ERR not even started yet"
        print("Stopping servo")
        self.pinctl.stop()
        GPIO.cleanup()


if __name__ == "__main__":
    serv = FT1117M()
    serv.start(0)
    try:
        while True:
            serv.setpos(10)
            time.sleep(0.5)
            serv.setpos(20)
            time.sleep(0.5)
            serv.setpos(30)
            time.sleep(0.5)
            serv.setpos(40)
            time.sleep(0.5)
            serv.setpos(50)
            time.sleep(0.5)
            serv.setpos(60)
            time.sleep(0.5)
            serv.setpos(-60)
            time.sleep(0.5)
            serv.setpos(-58)
            time.sleep(0.5)
    except KeyboardInterrupt:
        serv.stop()
