from time import sleep_ms
from machine import Pin, SPI
from mfrc522 import MFRC522
from umqtt.simple import MQTTClient
import mfrc522
from os import uname
import micropython
import machine
import esp32
import sys
import time

#MQTT params
mqtt_server = '192.168.12.45'
client_id = 'esp32'
# Topic
rfid_swipe = b'/devices/esp32/rfid_swipe'
rfid_checkin = b'/devices/esp32/rfid_checkin'
device_state = b'/devices/esp32/state'
led_indicate = Pin(2, Pin.OUT)
led_indicate.on()
led_auth = Pin(33, Pin.OUT)
led_reject = Pin(32, Pin.OUT)
client = MQTTClient(client_id, mqtt_server)

#MQTT callback
def on_connect(client, userdata, flags, rc):
     print("Connected flags"+str(flags)+"result code "\
     +str(rc)+"client1_id ")
     client.connected_flag=True
       
def subscribe_calback(topic, msg):
  global canAccess
  if(msg == b"1"):
    canAccess = True
    print("Can access changed in payload 1")
  else: 
    print("Can access changed in payload -1")
    canAccess = False
  if (canAccess):
    led_indicate.off()
    led_auth.on()
    door_lock.off()
    print("Come in boiz")
    sleep_ms(4000)
    door_lock.on()
    led_indicate.on()
    led_auth.off()
  else:
    print("Get out")
    led_indicate.off()
    led_reject.on()
    door_lock.on()
    sleep_ms(1000)
    led_indicate.on()
    led_reject.off()

client.on_connect = on_connect
client.set_callback(subscribe_calback)
client.connect()
client.subscribe(rfid_checkin, 0)


# Initial state
normal_boot = True  

#Wake up trigger pin
pir_wake = Pin(34, mode = Pin.IN, pull = Pin.PULL_DOWN)
esp32.wake_on_ext1([pir_wake], Pin.WAKE_HIGH)
if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    print('woke from a deep sleep, by the pulling of pin 34')
    if normal_boot:
      client.publish(device_state, "Wake from deepsleep")
      normal_boot = False

if normal_boot:
  client.publish(device_state, "ON")
    
# Door unlock?
canAccess = False

#Relay params
door_lock = Pin(22, Pin.OUT)
door_lock.on()  # Initial state

def twoDigitHex(number):
  return '%02x' % number

def do_read():
  global canAccess
  working = True
  if uname()[0] == 'esp32':
    rdr = mfrc522.MFRC522(18, 23, 19, 4, 26)
  else:
    raise RuntimeError("Unsupported platform")

  print("")
  print("Place card before reader to read from address 0x08")
  print("")
  hex_uid = ""
  global start_reading
  start_reading = time.ticks_ms()
  try:
    while (working):
      client.check_msg()
      (stat, tag_type) = rdr.request(rdr.REQIDL)
      if stat == rdr.OK:
        (stat, raw_uid) = rdr.anticoll()
        if stat == rdr.OK:
          start_reading = time.ticks_ms()
          print("New card detected")
          print("  - tag type: 0x%02x" % tag_type)
          hex_uid = twoDigitHex(raw_uid[0]) + twoDigitHex(raw_uid[1]) + twoDigitHex(raw_uid[2]) + twoDigitHex(raw_uid[3])
          print(hex_uid)
          msg = ("UID={}".format(hex_uid))
          client.publish(rfid_swipe, msg)
          print("Publish to broker")
          if rdr.select_tag(raw_uid) == rdr.OK:

            key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

            if rdr.auth(rdr.AUTHENT1A, 8, key, raw_uid) == rdr.OK:
              print("Address 8 data: %s" % rdr.read(8))
              rdr.stop_crypto1()
            else:
              print("Authentication error")
          else:
            print("Failed to select tag")
          sleep_ms(300)
          micropython.mem_info()
          client.wait_msg()
          sleep_ms(1000)
          print("Can Access Value")
          print(canAccess)
      else:
        if (abs(time.ticks_diff(time.ticks_ms(), start_reading) > 60000)):
          print("Going to sleep")
          client.publish(device_state, "OFF")
          sleep_ms(1000)
          machine.deepsleep()

  except KeyboardInterrupt:
    print("Bye")

while True:
  do_read()

