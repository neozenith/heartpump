import RPi.GPIO as GPIO
import asyncio
import math
from datetime import datetime
from time import sleep
from contextlib import AbstractAsyncContextManager
import logging
logger = logging.getLogger(__name__)

class MotorDriver(AbstractAsyncContextManager):
    def __init__(self, in1 = 24, in2 = 23, en = 25, freq=10_000):
        self.in1 = in1
        self.in2 = in2
        self.en = en
        self.freq = freq

    def setup_pins(self):
        logger.info("Configuring...")
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.in1, GPIO.OUT)
        GPIO.setup(self.in2, GPIO.OUT)
        GPIO.setup(self.en, GPIO.OUT)
        self.forward()
        self.p = GPIO.PWM(self.en, self.freq)


    def stop(self):
        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.LOW)

    def forward(self):
        GPIO.output(self.in1, GPIO.HIGH)
        GPIO.output(self.in2, GPIO.LOW)

    def backward(self):
        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.HIGH)

    def set_heart_rate(self, bpm=70):
        t = datetime.now().timestamp()
        wavelength = 60.0 / float(bpm)
        # 220 bpm is 3.67Hz = 272ms between events, eg 136ms in off state
        # 50 bpm is 0.83hz = 1204ms between events
        # Given a sinewave with the given "heartrate" frequency,
        # I want the positive half of the wave to map to duty cycle 0-100
        # I want the negative half of the wave to map to duty cycle 0
        heart_intensity = max(100.0 * math.sin(t * (2*math.pi) / wavelength), 0)
        # logger.info(f"{datetime.now()} {t=} {wavelength=} {bpm=} {heart_intensity=}")
        self.set_speed(heart_intensity)

    def set_speed(self, s):
        self.p.ChangeDutyCycle(s)

    async def __aenter__(self):
        logger.info("Entering...")
        self.setup_pins()
        self.p.start(25)
        return self

    async def __aexit__(self, exc_type, exc_value, exc_traceback):
        logger.info("Exiting...")
        self.p.stop()
        GPIO.cleanup()
