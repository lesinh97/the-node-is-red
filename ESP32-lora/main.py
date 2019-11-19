from machine import UART
from time import sleep

serial = UART(2, 9600,tx=17,rx=16)
serial.init(9600, bits=8, parity=None, stop =1)
sleep(2)

while True:
  print(serial.write('fromesp\n'))
  sleep(1)
