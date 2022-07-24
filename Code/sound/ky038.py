import RPi.GPIO as GPIO
import time

SOUND_CHANNEL = 24
GPIO.setmode(GPIO.BCM)  # for GPIO numbering, not PIN numbering (BOARD)
GPIO.setup(SOUND_CHANNEL, GPIO.IN, pull_up_down=GPIO.PUD_OFF)

def sound_callback(channel):
    if GPIO.input(channel):
        print("Sound detected")
    else:
        print("Sound detected")

GPIO.add_event_detect(SOUND_CHANNEL, GPIO.BOTH, bouncetime=300)  # BOTH = RISING + FALLING
GPIO.add_event_callback(SOUND_CHANNEL, sound_callback)

while True:
    time.sleep(1)
