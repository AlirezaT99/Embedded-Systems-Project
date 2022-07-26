import RPi.GPIO as GPIO
import time

SOUND_CHANNEL = 24
GPIO.setmode(GPIO.BCM)  # for GPIO numbering, not PIN numbering (BOARD)
GPIO.setup(SOUND_CHANNEL, GPIO.IN, pull_up_down=GPIO.PUD_OFF)

sound_stack = []
mirror_mode = True
SOUND_GAP = 3


def sound_callback(channel):
    global mirror_mode

    now = time.monotonic()
    if len(sound_stack) == 1:
        if sound_stack[0] < now - SOUND_GAP:
            sound_stack[0] = now
        else:
            mirror_mode = not mirror_mode
        sound_stack.clear()
    else:
        sound_stack.append(now)

    # if GPIO.input(channel):
    #     sound_stack.append(now)
    # else:
    #     sound_stack.append(now)
    print('Sound detected', mirror_mode)

GPIO.add_event_detect(SOUND_CHANNEL, GPIO.BOTH, bouncetime=300)  # BOTH = RISING + FALLING
GPIO.add_event_callback(SOUND_CHANNEL, sound_callback)

while True:
    time.sleep(1)
