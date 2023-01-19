# source: https://mpython.readthedocs.io/en/master/library/mPython/umqtt.simple.html
import dht
import time
import network
import machine
from umqtt.simple import MQTTClient

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

wlan.connect("HUAWEI-0F59","T51NN0MFNB2")
client_id = 'lenka'
mqtt_server = 'nodered.local'
port = 1883
user = 'student'
password = '1234567890ABC'
topic_pub_temp = b'tanguera/temp'
topic_pub_humid = b'tanguera/humidity'

led = machine.Pin("LED", machine.Pin.OUT)

def mqtt_connect():
   client = MQTTClient(client_id, mqtt_server, port, user, password, keepalive=3600)
   client.connect()
   print('Connected to %s MQTT Broker'%(mqtt_server))
   return client


def reconnect():
   print('Failed to connect to the MQTT Broker. Reconnecting...')
   time.sleep(5)
   machine.reset()
   
try:
    client = mqtt_connect()
except OSError as e:
    reconnect()
if __name__ == "__main__":
    sensor = dht.DHT22(machine.Pin(15))
    temperature = 0
    humidity = 0
    print("Lokalita Martin")
    print()
    while True:
        sensor.measure()
        temperature = sensor.temperature()
        humidity = sensor.humidity()
        print("Teplota: ", temperature)
        print("Vlhkost:", humidity)
        led.on()
        time.sleep(0.1)
        client.publish(topic_pub_temp, str(temperature))
        led.off()
        client.publish(topic_pub_humid, str(humidity))
        time.sleep(0.4)