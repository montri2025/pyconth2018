import machine
import wifi
import coin
import mqtt_pub

ENV_NAME = "devlopment"
wifi.connect()



coin.bill_last_state = 0
coin.bill_pulse_count = 0 
coin.total = 0
pin_coin =  machine.Pin(4, machine.Pin.IN)
pin_coin.irq(trigger=machine.Pin.IRQ_FALLING | machine.Pin.IRQ_RISING, handler=coin.coin_callback)

curren  =  0 
while True:
    
    if  curren< coin.bill_pulse_count:
        mqtt_pub.pub(b"coin",str(coin.bill_pulse_count))
        curren =  coin.bill_pulse_count
    


