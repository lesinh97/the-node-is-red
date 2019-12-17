from umqtt.simple import MQTTClient
import mfrc522
from os import uname
from machine import Pin
from time import sleep_ms
import machine
import dht

mqtt_server='192.168.12.45'
client_id = 'esp8266'
dht_data = b'/devices/esp8266/dht_data'
switch_control = b'/devices/esp8266/switch'
switch1_state = b'/devices/esp8266/switch/1/state'
switch2_state = b'/devices/esp8266/switch/2/state'

switch1 = Pin(12, Pin.OUT)
switch1.on()
switch2 = Pin(13, Pin.OUT)
switch2.on()
sensor = dht.DHT11(Pin(4))

#MQTT callback  
def subscribe_calback(topic, msg):
  if (msg==b"switch1_on"):
    switch1.off()
    sleep_ms(200)
    client.publish(switch1_state, "150000")
    sleep_ms(200)
  elif (msg==b"switch2_on"):
    switch2.off()
    sleep_ms(200)
    client.publish(switch2_state, "300000")
    sleep_ms(200)
  elif (msg==b"switch1_off"):
    switch1.on()
    sleep_ms(200)
    client.publish(switch1_state, "0")
    sleep_ms(200)
  elif (msg==b"switch2_off"):
    switch2.on()
    sleep_ms(200)
    client.publish(switch2_state, "0")
    sleep_ms(200)

client = MQTTClient(client_id, mqtt_server)
client.set_callback(subscribe_calback)
client.connect()
client.subscribe(switch_control, 0)

while True:
  try:
    sleep_ms(1500)
    sensor.measure()
    temp = sensor.temperature()
    hum = sensor.humidity()
    msg = ('TEMP={0:3.1f},HUM={1:3.1f}'.format(temp, hum))
    client.publish(dht_data, msg)  # Publish sensor data to MQTT topic
    client.check_msg()
    print(msg)
  except OSError:
    print('Failed to read sensor.')

sleep_ms(200)