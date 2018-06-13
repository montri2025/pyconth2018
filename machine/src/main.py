import machine
import wifi
import coin
import mqtt_pub
import time
import ujson
import math
from config import  MQTT_SERVER,PUBLISH_TOPIC

ENV_NAME = "devlopment"
wifi.connect()

coin.pulse_total = 0 
coin.total = 0
pin_coin =  machine.Pin(4, machine.Pin.IN)
pin_coin.irq(trigger=machine.Pin.IRQ_FALLING | machine.Pin.IRQ_RISING, handler=coin.coin_callback)

current  =  0 
conn = mqtt_pub.connected()
online_message = ujson.dumps({"status":2})
mqtt_pub.push_coins(conn,PUBLISH_TOPIC,online_message)
i = 0
while True:
    try:
        i = i + 1
        if math.fmod(i,50000)==0:
            online_message = ujson.dumps({"status":2})
            mqtt_pub.push_coins(conn,PUBLISH_TOPIC,online_message)
            i = 0

        if current< coin.pulse_total:
            deposit_message = ujson.dumps({"deposit":coin.pulse_total})
            mqtt_pub.push_coins(conn,PUBLISH_TOPIC,deposit_message)
            current = coin.pulse_total
            coin.pulse_total = 0
            current = 0
            i = 0
    except:
        conn.disconnect()
        time.sleep(10)
        conn = mqtt_pub.connected()
        pass

    


