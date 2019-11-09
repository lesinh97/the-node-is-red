from time import sleep_ms
from machine import Pin, SPI
from mfrc522 import MFRC522
from umqtt.simple import MQTTClient
import mfrc522
from os import uname
import micropython

#MQTT params
mqtt_server = '192.168.12.40'
client_id = 'esp32'
rfid_swipe = b'/devices/esp32/rfid_swipe'
rfid_checkin = b'/devices/esp32/rfid_checkin'
# Door unlock?
canAccess = False

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
    door_lock.off()
    print("Come in boiz")
    sleep_ms(4000)
    door_lock.on()
  else:
    print("Get out")
    door_lock.on()
    sleep_ms(200)

client.on_connect = on_connect
client.set_callback(subscribe_calback)
client.connect()
client.subscribe(rfid_checkin, 0)
#Relay params
door_lock = Pin(13, Pin.OUT)
door_lock.on()

def twoDigitHex(number):
  return '%02x' % number

def do_read():
  global canAccess
  if uname()[0] == 'WiPy':
    rdr = mfrc522.MFRC522("GP14", "GP16", "GP15", "GP22", "GP17")
  elif uname()[0] == 'esp8266':
    rdr = mfrc522.MFRC522(0, 2, 4, 5, 14)
    
  elif uname()[0] == 'esp32':
    rdr = mfrc522.MFRC522(18, 23, 19, 4, 12)
    
  else:
    raise RuntimeError("Unsupported platform")

  print("")
  print("Place card before reader to read from address 0x08")
  print("")
  hex_uid = ""
  try:
    while True:
      (stat, tag_type) = rdr.request(rdr.REQIDL)

      if stat == rdr.OK:

        (stat, raw_uid) = rdr.anticoll()

        if stat == rdr.OK:
          print("New card detected")
          print("  - tag type: 0x%02x" % tag_type)
          hex_uid = twoDigitHex(raw_uid[0]) + twoDigitHex(raw_uid[1]) + twoDigitHex(raw_uid[2]) + twoDigitHex(raw_uid[3])
          print(hex_uid)
          client.publish(rfid_swipe, hex_uid)
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

  except KeyboardInterrupt:
    print("Bye")

while True:
  do_read()

