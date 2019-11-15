import time
import serial
 
ser = serial.Serial(
  port = '/dev/ttyS0',
  baudrate = 9600,
  parity = serial.PARITY_NONE,
  stopbits = serial.STOPBITS_ONE,
  bytesize = serial.EIGHTBITS,
  timeout = 1
)

def readFromLora(ser):
  rv = ''
  while True:
    if ser.inWaiting() > 0 :
      s = ser.read(4)
      rv += str(s)
      return rv

while True:
  rcv = readFromLora(ser)
  print(rcv)