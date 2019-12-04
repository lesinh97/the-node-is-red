import time
import serial
import paho.mqtt.client as mqtt

MQTT_SERVER = "localhost"
lora_signal = "devices/lora/"
tx_indicate = "devices/raspberry/tx"
rx_indicate = "devices/raspberry/rx"
client_id = "raspberry"
# MQTT Callback
def on_connect(client, userdata, flags, rc):
  print("Connected to server, result code "+str(rc))
  client.connected_flags = True

client = mqtt.Client()
client.connect("127.0.0.1", 1883, 60)
client.on_connect = on_connect

ser = serial.Serial(
  port = '/dev/ttyAMA0',
  baudrate = 9600,
  parity = serial.PARITY_NONE,
  stopbits = serial.STOPBITS_ONE,
  bytesize = serial.EIGHTBITS,
  timeout = 1
)

while True:
  time.sleep(1)
  s = ser.readline()
  data = s.decode().strip()
  if (data!=""):
    client.publish(lora_signal, data)
    print(data)
    time.sleep(1)
    client.publish(tx_indicate, "on")
  else: 
    client.publish(tx_indicate, "off")
    print("No data")
  time.sleep(0.5)