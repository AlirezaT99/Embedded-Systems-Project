import Adafruit_DHT
import cv2
import psutil
import RPi.GPIO as GPIO
import threading
import time

from display.face_detection import face_detected
from distance.hy_srf05 import TRIGGER_PIN, ECHO_PIN, check_distance, timer_call
from environment.dht22 import DHT_SENSOR, DHT_PIN
from sound.ky038 import SOUND_CHANNEL


VIDEO_URL = 'http://192.168.1.4:4747/video'
DISTANCE_THRESHOLD = 40  # cm
DEBUG = True


# Global vars
temperature = ''
humidity = ''
weather_forecast = {}
distance = -1
mirror_mode = True


def dprint(msg):
    if DEBUG:
        print(msg)


def init():
    for proc in psutil.process_iter():
        if proc.name() == 'libgpiod_pulsein' or proc.name() == 'libgpiod_pulsei':
            proc.kill()


def env_thread():
    global temperature, humidity

    while True:
        sensor_humidity, sensor_temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
        if sensor_humidity is not None and sensor_temperature is not None:
            dprint('{} {}'.format(temperature, humidity))
            temperature = '{0:0.1f}C' % sensor_temperature
            humidity = '{1:0.1f}%' % sensor_humidity
        else:
            dprint('DHT22 Sensor failure. Check wiring.')
        time.sleep(3)


def distance_thread():
    global distance

    while True:
        distance = check_distance()
        distance = distance if distance > 0 else -1


def is_object_nearby():
    return distance != -1 and float(distance) < DISTANCE_THRESHOLD


def set_weather_forecast():
    pass  # TODO


def sound_callback(channel):  # TODO look for a pattern
    if GPIO.input(channel):
        print('Sound detected')
    else:
        print('Sound detected')


def style_background(image):
    cv2.putText(img=image, text="Hello World", org=(100, 200), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=3, color=(0, 0, 0), thickness=2)
    return image


def style_video_frame(image):
    return image


def run():
    window_name = "SmartMirror"
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)  # TODO WINDOW_NORMAL or WINDOW_FREERATIO ?
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    capture = cv2.VideoCapture(VIDEO_URL)
    background = cv2.imread("display/background.jpg")

    face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    
    # Sound sensor (KY038)
    GPIO.setup(SOUND_CHANNEL, GPIO.IN, pull_up_down=GPIO.PUD_OFF)  # Sleep 1
    GPIO.add_event_detect(SOUND_CHANNEL, GPIO.BOTH, bouncetime=300)
    GPIO.add_event_callback(SOUND_CHANNEL, sound_callback)

    # Distance sensor (HY-SRF05)
    GPIO.setup(TRIGGER_PIN, GPIO.OUT)
    GPIO.setup(ECHO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(ECHO_PIN, GPIO.BOTH, callback=timer_call)
    threading.Thread(target=distance_thread).start()

    # Environment sensor (DHT22)
    threading.Thread(target=env_thread).start()

    set_weather_forecast()

    while True:
        try:
            _, frame = capture.read()
            if face_detected(frame, face_detector) and mirror_mode and is_object_nearby():
                cv2.imshow(window_name, style_video_frame(frame))
            else:
                cv2.imshow(window_name, style_background(background))

            time.sleep(0.05)
        except Exception as error:
            print(error)
            break

    capture.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    run()
