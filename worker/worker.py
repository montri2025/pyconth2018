import paho.mqtt.client as mqtt
import time
from config import MQTT_SERVER, SUBSCRIBE
from monitoring import statsd

worker_name = "mac-book"
MQTT_CLIENT_ID = "local-mac-33333"

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
    print(msg.topic+" "+str(msg.payload))

@statsd.timer(worker_name + '.loop-misc')
def loop_misc():
    print("Service Is Ok")
      

client = mqtt.Client(MQTT_CLIENT_ID)
client.on_connect = on_connect
client.on_message = on_message
#client.loop_misc = loop_misc
client.connect(MQTT_SERVER, 1883, 60)
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
# try:
#     client.loop_forever()
# except Exception:
#     pass   