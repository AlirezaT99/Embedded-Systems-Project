import RPi.GPIO as GPIO
import time

channel = 17
GPIO.setmode(GPIO.BCM)  # for GPIO numbering, not PIN numbering (BOARD)
GPIO.setup(channel, GPIO.IN)

def sound_callback(channel):
    if GPIO.input(channel):
        print("Sound detected")
    else:
        print("Sound Finished")

GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)  # BOTH = RISING + FALLING
GPIO.add_event_callback(channel, sound_callback)
