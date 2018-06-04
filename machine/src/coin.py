import mqtt_pub

bill_pulse_count = 0
bill_last_state = 0 
total = 0
def coin_callback(p):
    global total, bill_pulse_count
    if p.value()==0: 
        total = total + 1
        bill_pulse_count = bill_pulse_count +1
    print('pin_coin change', p.value(), "total money", total)

# def coin_callback(p):
#     global bill_pulse_count, bill_last_state, total
#     pulse_state = p.value()
#     if pulse_state == 0 and bill_last_state == 0 :  #// this means we entered a new pulse
#         bill_last_state = 1 #// set the previous state
#     elif pulse_state == 1 and bill_last_state == 1: #// this means a pulse just ended
#         bill_last_state = 0
#         bill_pulse_count = bill_pulse_count +1  #// increment the pulse counter
#         total = bill_pulse_count * 1
#         # mqtt_pub.pub(b"coin","1")
#         #mqtt_pub.pub(b"total",str(bill_pulse_count))
        
#     print('bill_last_state',pulse_state, "total money", total, "bill_pulse_count", bill_pulse_count) 