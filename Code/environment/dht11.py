import board
import adafruit_dht

def get_temperature_and_humidity(sensor):
    """
    Read temperature and humidity values from dht11 sensor
    """
    temp = sensor.temperature
    humidity = sensor.humidity
    return temp, humidity


dht11_sensor = adafruit_dht.DHT11(board.D23)
temperature, humidity = get_temperature_and_humidity(dht11_sensor)