import paho.mqtt.client as mqtt
import time
from config import MQTT_SERVER, SUBSCRIBE, PIGGY_ID
from sender import statsd
from transaction import deposite, balance, withdraw
import json 
import uuid
import hashlib

worker_name = "mac-book"
MQTT_CLIENT_ID ="pigg_bank_"+str(uuid.uuid1())

# The callback for when the client receives a CONNACK response from the server.
@statsd.timer(worker_name + '.on-connect')
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(SUBSCRIBE)

# The callback for when a PUBLISH message is received from the server.
#@statsd.timer(worker_name + '.on-message')
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    msg_json = json.loads(msg.payload)
    if isinstance(msg_json,dict):
        # d = deposite
        if msg_json.get('deposite'):
            amount_deposite = msg_json.get('deposite',0)
            deposite(PIGGY_ID,amount_deposite,'desc deposite')
            statsd.incr('deposite',amount_deposite)
            statsd.gauge('deposite',amount_deposite)
            current_balance = balance(PIGGY_ID)
            statsd.gauge('balance',current_balance)
            print("deposite::", amount_deposite)
            print("balance::",current_balance)

        elif msg_json.get('withdraw'):
            amount_withdraw = withdraw(PIGGY_ID,'desc withdraw')
            statsd.gauge('withdraw',amount_withdraw)
            statsd.incr('withdraw',amount_withdraw)
            current_balance = balance(PIGGY_ID)
            statsd.gauge('balance',current_balance)
            print("withdraw::", amount_withdraw)
            print("balance::",current_balance)
        elif msg_json.get('online'):
             statsd.gauge('online',msg_json.get('online'))  
        else:
            current_balance = balance(PIGGY_ID)
            statsd.gauge('balance',current_balance)
            statsd.incr('balance',current_balance)
            print("balance::",current_balance)
            
print("MQTT_ID::",MQTT_CLIENT_ID,"MQTT_SERVER::",MQTT_SERVER)        
client = mqtt.Client(MQTT_CLIENT_ID)
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_SERVER, 1883, 120)
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
