from machine import UART, Pin, ADC
from time import sleep, sleep_ms

serial = UART(2, 9600,tx=17,rx=16)
serial.init(9600, bits=8, parity=None, stop =1)
sleep(1)

ADC.width(ADC.WIDTH_10BIT)
mea = ADC(Pin(34))
mea.atten(ADC.ATTN_11DB)
tx_led = Pin(27, Pin.OUT)

def blink():
    tx_led.on()
    sleep_ms(150)
    tx_led.off()
    sleep_ms(150)
    tx_led.on()
    sleep_ms(150)
    tx_led.off()
    sleep_ms(150)
    tx_led.on()
    sleep_ms(150)
    tx_led.off()

while True: 
  mea_value = mea.read()
  sleep(1)
  humd_value = 100-((mea_value/1023)*100)
  round_humd_value = round(humd_value,1)
  data_to_write = str(round_humd_value)+"\n"
  if (serial.write(data_to_write) > 0):
    blink()
