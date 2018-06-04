import network

def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('www.deenaja.com', '4910421038')
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())