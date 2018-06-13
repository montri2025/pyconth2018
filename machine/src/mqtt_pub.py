from umqtt.simple import MQTTClient
import ubinascii
import machine
import ujson
from config import  MQTT_SERVER,PUBLISH_TOPIC
CLIENT_ID = ubinascii.hexlify(machine.unique_id())

default_message = ujson.dumps({"deposit":1})

def connected():
   conn = MQTTClient(CLIENT_ID, MQTT_SERVER)
   conn.connect()
   return conn
def push_coins(conn=connected, topic=PUBLISH_TOPIC, message=default_message):  
    print("push_message::::"+message)
    conn.publish(topic, message.encode())