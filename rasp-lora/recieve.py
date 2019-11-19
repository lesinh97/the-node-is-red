import time
import serial
import paho.mqtt.client as mqtt

# MQTT_SERVER = "localhost"
# lora_signal = "devices/lora/"
# client_id = "raspberry"
# # MQTT Callback
# def on_connect(client, userdata, flags, rc):
#   print("Connected to server, result code "+str(rc))
#   client.connected_flags = True

# client = mqtt.Client()
# client.on_connect = on_connect
# client.connect(client_id, MQTT_SERVER)

ser = serial.Serial(
  port = '/dev/ttyAMA0',
  baudrate = 9600,
  parity = serial.PARITY_NONE,
  stopbits = serial.STOPBITS_ONE,
  bytesize = serial.EIGHTBITS,
  timeout = 1
)

while True:
    s = ser.readline()
    data = s.decode().strip()
    print(data)