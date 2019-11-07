# This file is executed on every boot (including wake-boot from deepsleep)
import esp
esp.osdebug(0)
import uos, machine
#uos.dupterm(None, 1) # disable REPL on UART(0)
import gc
#import webrepl
#webrepl.start()
gc.collect()
import time
from umqtt.simple import MQTTClient
import machine
import micropython
import network

ssid='ledsinh'
password='ledinhsinh1212'

last_message = 0
message_interval = 5
counter = 0

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print("Connected to ledsinh")
print(station.ifconfig())