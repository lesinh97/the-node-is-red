from machine import UART, Pin, ADC
from time import sleep, sleep_ms

serial = UART(2, 9600,tx=17,rx=16)
serial.init(baudrate=9600, bits=8, parity=None, stop =1)
sleep(1.5)

ADC.width(ADC.WIDTH_10BIT)
mea = ADC(Pin(34))
mea.atten(ADC.ATTN_11DB)
led_indicate = Pin(2, Pin.OUT)
led_indicate.on()
tx_led = Pin(27, Pin.OUT)
valve_led = Pin(33, Pin.OUT)
pump_valve = Pin(22, Pin.OUT)
pump_valve.on()

def tx_blink(): # 750ms 0.75
    led_indicate.off()
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
    led_indicate.on()

while True:
  sleep(2) 
  mea_value = mea.read()
  humd_value = 100-((mea_value/1023)*100)
  round_humd_value = round(humd_value,1)
  data_to_write = str(round_humd_value)+"\n"
  print(data_to_write)
  if(serial.write(data_to_write)>0):
    tx_blink()
  sleep(2)
  receive = serial.readline()
  print(receive)
  if(receive == b'on\n'):
    pump_valve.off()
    led_indicate.off()
    valve_led.on()
  if(receive == b'off\n'):
    pump_valve.on()
    valve_led.off()
    led_indicate.on()