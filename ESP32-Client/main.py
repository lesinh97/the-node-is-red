from time import sleep_ms
from machine import Pin, SPI
from mfrc522 import MFRC522
from umqtt.simple import MQTTClient
#RFID pinout
sck = Pin(18, Pin.OUT)
mosi = Pin(23, Pin.OUT)
miso = Pin(19, Pin.OUT)
spi = SPI(baudrate=100000, polarity=0, phase=0, sck=sck, mosi=mosi, miso=miso)
sda = Pin(5, Pin.OUT)

#MQTT params
mqtt_server = '192.168.12.40'
client_id = 'esp32'
rfid_swipe = b'/devices/esp32/rfid_swipe'
rfid_checkin = b'/devices/esp32/rfid_checkin'

client = MQTTClient(client_id, mqtt_server)
client.connect()

#Relay params
door_lock = Pin(13, Pin.OUT)
door_lock.value(0)

def twoDigitHex(number):
  return '%02x' % number

def do_read():
    try:
        while True:
            rdr = MFRC522(spi, sda)
            uid = ""
            (stat, tag_type) = rdr.request(rdr.REQIDL)
            if stat == rdr.OK:
                (stat, raw_uid) = rdr.anticoll()
                if stat == rdr.OK:
                    uid = ("0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
                    print(uid)
                    hex_uid = twoDigitHex(raw_uid[0]) + twoDigitHex(raw_uid[1]) + twoDigitHex(raw_uid[2]) + twoDigitHex(raw_uid[3])
                    print(hex_uid)
                    if (hex_uid == "8dba282d"):
                      door_lock.on()

                      print("relay on")
                    else:
                      print("Wrong user")
                    sleep_ms(100)
    except KeyboardInterrupt:
        print("Bye")

while True:
  do_read()
