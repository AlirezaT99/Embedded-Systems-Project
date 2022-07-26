# import Adafruit_DHT
import asyncio
import cv2
import psutil
import python_weather
# import RPi.GPIO as GPIO
import threading
import time

from display.face_detection import face_detected
# from distance.hy_srf05 import TRIGGER_PIN, ECHO_PIN, check_distance, timer_call
# from environment.dht22 import DHT_SENSOR, DHT_PIN
# from sound.ky038 import SOUND_CHANNEL


VIDEO_URL = 'http://192.168.94.79:4747/video'
LOCATION = 'Tehran, Tehran Province, Iran'
DISTANCE_THRESHOLD = 40  # cm
SOUND_GAP = 2

DEBUG = True


# Global vars
temperature = ''
humidity = ''
weather_forecast = {}
distance = -1
mirror_mode = True
sound_stack = []


def dprint(msg):
    if DEBUG:
        print(msg)


def init():
    for proc in psutil.process_iter():
        if proc.name() == 'libgpiod_pulsein' or proc.name() == 'libgpiod_pulsei':
            proc.kill()


# def env_thread():
#     global temperature, humidity
#
#     while True:
#         sensor_humidity, sensor_temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
#         if sensor_humidity is not None and sensor_temperature is not None:
#             dprint('{} {}'.format(temperature, humidity))
#             temperature = f'{0:0.1f}C' % sensor_temperature
#             humidity = f'{1:0.1f}%' % sensor_humidity
#         else:
#             dprint('DHT22 Sensor failure. Check wiring.')
#         time.sleep(3)


# def distance_thread():
#     global distance
#
#     while True:
#         distance = check_distance()
#         distance = distance if distance > 0 else -1


def is_object_nearby():
    return True
    # return distance != -1 and float(distance) < DISTANCE_THRESHOLD


async def get_weather(city):
    client = python_weather.Client(format=python_weather.METRIC)
    weather = await client.find(city)
    # print(weather.current.temperature)
    weather_forecast.clear()
    for forecast in weather.forecasts:
        weather_forecast[str(forecast.date)] = (forecast.sky_text, forecast.temperature)
    await client.close()


def set_weather_forecast():
    # loop = asyncio.get_event_loop()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(get_weather(LOCATION))
    if len(weather_forecast) == 0:
        set_weather_forecast()


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
    print('Sound detected')


def write_stuff_on_image(image, base_y, base_x):
    v_space = 25
    if len(weather_forecast) == 0:
        return cv2.putText(img=image, text="Hello User!", org=(base_x - v_space, base_y - v_space), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(0, 0, 0), thickness=2)
    cv2.putText(img=image, text="Weather forecast:", org=(base_x - v_space, base_y - v_space), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(0, 0, 0), thickness=2)
    for i, date in enumerate(weather_forecast.keys()):
        cv2.putText(img=image, text="{}: {}C  {}".format(date[:10], weather_forecast[date][1], weather_forecast[date][0]), org=(base_x, base_y + i * v_space), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=0.5, color=(0, 0, 0), thickness=1)
        if i == 3:
            break
    cv2.putText(img=image, text=f"Real feel: " + temperature, org=(640 - 150, 480 - 50),
                fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=0.5, color=(0, 0, 0), thickness=1)
    cv2.putText(img=image, text="Humidity: " + humidity, org=(640 - 150, 480 - 25),
                fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=0.5, color=(0, 0, 0), thickness=1)
    return image


def style_background(image):
    return write_stuff_on_image(image, 200, 200)


def style_video_frame(image):
    return write_stuff_on_image(image, 200, 75)


def run():
    window_name = "SmartMirror"
    # cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)  # TODO WINDOW_FREERATIO or WND_PROP_FULLSCREEN ?
    # cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    capture = cv2.VideoCapture(VIDEO_URL)
    background = cv2.imread("display/background.jpg")

    face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    
    # GPIO.setwarnings(False)
    # GPIO.setmode(GPIO.BCM)
    
    # # Sound sensor (KY038)
    # GPIO.setup(SOUND_CHANNEL, GPIO.IN, pull_up_down=GPIO.PUD_OFF)  # Sleep 1
    # GPIO.add_event_detect(SOUND_CHANNEL, GPIO.BOTH, bouncetime=300)
    # GPIO.add_event_callback(SOUND_CHANNEL, sound_callback)

    # # Distance sensor (HY-SRF05)
    # GPIO.setup(TRIGGER_PIN, GPIO.OUT)
    # GPIO.setup(ECHO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    # GPIO.add_event_detect(ECHO_PIN, GPIO.BOTH, callback=timer_call)
    # threading.Thread(target=distance_thread).start()

    # # Environment sensor (DHT22)
    # threading.Thread(target=env_thread).start()

    # Weather forecast
    threading.Thread(target=set_weather_forecast).start()

    while True:
        try:
            ret, frame = capture.read()
            if face_detected(frame, face_detector) and mirror_mode and is_object_nearby():
                cv2.imshow(window_name, style_video_frame(frame))  # TODO window is str
            else:
                cv2.imshow(window_name, style_background(background))

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            # time.sleep(0.05)
        except Exception as error:
            print(error)
            break

    capture.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    run()
