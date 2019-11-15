from umqtt.simple import MQTTClient
import mfrc522
from os import uname
from machine import Pin
from time import sleep_ms
import machine
import dht

# UART for Lora
uart = machine.UART(1, 9600)
uart.init(9600, bits=8, parity = None, stop =1)

mqtt_server='192.168.12.40'
client_id = 'esp8266'
dht_data = b'/devices/esp8266/dht_data'
switch_control = b'/devices/esp8266/switch'

switch1 = Pin(12, Pin.OUT)
switch2 = Pin(13, Pin.OUT)
sensor = dht.DHT11(Pin(4))

#MQTT callback
  
def subscribe_calback(topic, msg):
  if (msg==b"switch1_on"):
    switch1.on()
    sleep_ms(100)
  elif (msg==b"switch2_on"):
    switch2.on()
    sleep_ms(100)
  elif (msg==b"switch1_off"):
    switch1.off()
    sleep_ms(100)
  elif (msg==b"switch2_off"):
    switch2.off()
    sleep_ms(100)

client = MQTTClient(client_id, mqtt_server)
client.set_callback(subscribe_calback)
client.connect()
client.subscribe(switch_control, 0)

while True:
  try:
    sleep_ms(2000)
    sensor.measure()
    temp = sensor.temperature()
    hum = sensor.humidity()
    msg = ('TEMP={0:3.1f},HUM={1:3.1f}'.format(temp, hum))
    print(uart.write('esp\n'.encode('utf-8')))
    print("Published to LORA")
    client.publish(dht_data, msg)  # Publish sensor data to MQTT topic
    client.check_msg()
    print(msg)
  except OSError:
    print('Failed to read sensor.')

sleep_ms(200)