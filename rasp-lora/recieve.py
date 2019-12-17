import time
import serial
import paho.mqtt.client as mqtt

MQTT_SERVER = "localhost"
lora_signal = "devices/lora/"
tx_indicate = "devices/raspberry/tx"
rx_indicate = "devices/raspberry/rx"
lora_action = "devices/raspberry/lora_action"
client_id = "raspberry"
# MQTT Callback
def on_connect(client, userdata, flags, rc):
  print("Connected to server, result code "+str(rc))
  client.connected_flags = True

def subscribe_callback(client, userdata, message):
  if(message.payload.decode()=="on"):
    client.publish(tx_indicate, "on")
    ser.write("on")	
    ser.flush()
    client.publish(tx_indicate, "off")
  elif(message.payload.decode()=="off"):
    client.publish(tx_indicate, "on")
    ser.write("off")
    ser.flush()
    client.publish(tx_indicate, "off")
  time.sleep(2)

client = mqtt.Client()
client.connect("127.0.0.1", 1883, 60)
client.on_connect = on_connect
client.subscribe(lora_action, 0)
client.message_callback_add(lora_action, subscribe_callback)

ser = serial.Serial(
  port = '/dev/ttyAMA0',
  baudrate = 9600,
  parity = serial.PARITY_NONE,
  stopbits = serial.STOPBITS_ONE,
  bytesize = serial.EIGHTBITS,
  timeout = 1
)
time.sleep(1.5)
while True:
  s = ser.readline()
  data = s.decode().strip()
  if (data!=""):
    client.publish(lora_signal, data)
    print(data)
    client.publish(rx_indicate, "on")
  else: 
    client.publish(rx_indicate, "off")
    print("No data")
  time.sleep(2)
