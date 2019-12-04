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
#from umqtt.simple import MQTTClient
import micropython
print(micropython.mem_info())