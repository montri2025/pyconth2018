from umqtt.simple import MQTTClient
import ubinascii
import machine


SERVER = "deenaja.com"
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
TOPIC = b"coin"
conn = MQTTClient(CLIENT_ID, SERVER)
conn.connect()
def pub(conn=conn, topic=TOPIC, message="1"):
    print("Connected to %s, waiting for button presses" % SERVER)
    conn.publish(topic, message.encode())