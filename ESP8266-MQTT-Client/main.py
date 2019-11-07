from umqtt.simple import MQTTClient
import mfrc522
from os import uname
from machine import Pin
from time import sleep
import uasyncio as asyncio
import machine

mqtt_server='192.168.12.40'
client_id = 'esp8266'
dht_data = b'/devices/esp8266/dht_data'
pir_detect = b'/devices/esp8266/pir_detect'
rfid_swipe = b'/devices/esp8266/rfid_swipe'
rfid_checkin = b'/devices/esp8266/rfid_checkin'
client = MQTTClient(client_id, mqtt_server)
client.connect()

solenoid = Pin(13, Pin.OUT)
solenoid.on()
#sensor = dht.DHT11(Pin(14))
def twoDigitHex( number ):
  return '%02x' % number

async def do_read_rfid():
  isSwipe = False
  if uname()[0] == 'WiPy':
    rdr = mfrc522.MFRC522("GP14", "GP16", "GP15", "GP22", "GP17")
  elif uname()[0] == 'esp8266':
    rdr = mfrc522.MFRC522(0, 2, 4, 5, 14)
    print("For esp8266")
  else:
    raise RuntimeError("Unsupported platform")

  print("")
  print("Place card before reader to read from address 0x08")
  print("")
  
  try:
      (stat, tag_type) = rdr.request(rdr.REQIDL)
      if stat == rdr.OK:

        (stat, raw_uid) = rdr.anticoll()
        isSwipe = True

        if stat == rdr.OK:

          print("New card detected")
          print("  - tag type: 0x%02x" % tag_type)
          print("  - uid	 : 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
          print("")
          hex_uid = twoDigitHex(raw_uid[0]) + twoDigitHex(raw_uid[1]) + twoDigitHex(raw_uid[2]) + twoDigitHex(raw_uid[3])
          print(hex_uid)
          client.publish(rfid_swipe, hex_uid)
          
          if rdr.select_tag(raw_uid) == rdr.OK:

            key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

            if rdr.auth(rdr.AUTHENT1A, 8, key, raw_uid) == rdr.OK:
              print("Address 8 data: %s" % rdr.read(8))
              rdr.stop_crypto1()
            else:
              print("Authentication error")
          else:
            print("Failed to select tag")

      if isSwipe:
        return None
      else:
          await asyncio.sleep(1)
  except OSError:
    print("Error")

loop = asyncio.get_event_loop()
loop.run_until_complete(do_read_rfid())
sleep(0.5)
print("Im going to sleep")
machine.deepsleep()
