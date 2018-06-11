pulse_total = 0
def coin_callback(p):
    global pulse_total
    if p.value()==1: 
        pulse_total = pulse_total +1
    print('pulse signal::', p.value())
