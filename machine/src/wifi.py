import network
from config import ESSID, ESSID_PASSWORD
def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(ESSID, ESSID_PASSWORD)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())