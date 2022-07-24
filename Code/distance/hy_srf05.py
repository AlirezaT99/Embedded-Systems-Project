import RPi.GPIO as GPIO
import time
import statistics


TRIGGER_PIN = 18  # is set to high to send out a wave (OUT)
ECHO_PIN = 17  # indicates a returning wave when set to high (IN)


# TODO precision vs. load on the device
no_of_samples = 5  # number of trials to picks the middle value from and return
sample_sleep = 0.2  # interval between sending sample requests.

calibration1 = 30  # the distance the sensor was calibrated at
calibration2 = 1750  # the median value reported back from the sensor at 30 cm
time_out = 0.05  # measured in seconds in case the program gets stuck in a loop

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(TRIGGER_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

samples_list = []
stack = []


def timer_call(channel) :
    now = time.monotonic()
    stack.append(now)


def trigger():
    GPIO.output(TRIGGER_PIN, GPIO.HIGH) 
    time.sleep(0.00001)  # send out a 10us long pulse
    GPIO.output(TRIGGER_PIN, GPIO.LOW)


def check_distance():
    samples_list.clear()

    while len(samples_list) < no_of_samples:
        trigger()

        while len(stack) < 2:
            start = time.monotonic()
            while time.monotonic() < start + time_out:  # check for a timeout
                pass

            trigger()  # In case of a long futile wait

        if len(stack) == 2:
            samples_list.append(stack.pop() - stack.pop())

        elif len(stack) > 2:
            stack.clear()

        time.sleep(sample_sleep)

    return statistics.median(samples_list) * 1e6 * calibration1 / calibration2


GPIO.add_event_detect(ECHO_PIN, GPIO.BOTH, callback=timer_call)

while True:
    print(round(check_distance(), 1))
