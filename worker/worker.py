import paho.mqtt.client as mqtt
import time
from config import MQTT_SERVER, SUBSCRIBE, PIGGY_ID
from sender import statsd
from transaction import  deposit, balance, withdraw
import json 
import uuid
import hashlib
import time

worker_name = "mac-book"
MQTT_CLIENT_ID ="pigg_bank_"+str(uuid.uuid1())

LAST_MESSAGE_TIME = time.time()
MACHINE_STATUS = 'online'

# The callback for when the client receives a CONNACK response from the server.
@statsd.timer(worker_name + '.on-connect')
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(SUBSCRIBE)

# The callback for when a PUBLISH message is received from the server.
@statsd.timer(worker_name + '.on-message')
def on_message(client, userdata, msg):
    try:
        LAST_MESSAGE_TIME = time.time()
        MACHINE_STATUS = 'online'
        print(msg.topic+" "+str(msg.payload))
        msg_json = json.loads(msg.payload)
        if isinstance(msg_json,dict):
            # d = deposit
            if msg_json.get('deposit'):
                amount_deposit = msg_json.get('deposit',0)
                deposit(PIGGY_ID,amount_deposit,'desc deposit')
                statsd.incr('deposit',amount_deposit)
                statsd.gauge('deposit',amount_deposit)
                current_balance = balance(PIGGY_ID)
                statsd.gauge('balance',current_balance)
                print("deposit::", amount_deposit)
                print("balance::",current_balance)
            elif msg_json.get('withdraw'):
                amount_withdraw = withdraw(PIGGY_ID,'desc withdraw')
                statsd.gauge('withdraw',amount_withdraw)
                statsd.incr('withdraw',amount_withdraw)
                current_balance = balance(PIGGY_ID)
                statsd.gauge('balance',current_balance)
                print("withdraw::", amount_withdraw)
                print("balance::",current_balance)
            elif msg_json.get('status'):
                statsd.gauge('status',msg_json.get('status'))  
            elif msg_json.get('balance'):
                current_balance = balance(PIGGY_ID)
                statsd.gauge('balance',current_balance)
                statsd.incr('balance',current_balance)
                print("balance::",current_balance)
    except Exception as e:
        print(e)          
            
print("MQTT_ID::",MQTT_CLIENT_ID,"MQTT_SERVER::",MQTT_SERVER)        
client = mqtt.Client(MQTT_CLIENT_ID)
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_SERVER, 1883, 120)
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_start()
while True:
    #client.loop()
    TIME_FREE = time.time()
    elapsed = TIME_FREE - LAST_MESSAGE_TIME
    if elapsed > 60 and MACHINE_STATUS=='online':
        offline_message = json.dumps({"status":1})
        client.publish(SUBSCRIBE, offline_message)
        MACHINE_STATUS='offline'
        
#client.loop_forever()
