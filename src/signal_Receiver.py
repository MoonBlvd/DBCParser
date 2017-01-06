import lcm
from JKUlcm import JKU_t

lc = lcm.LCM()

def data_handler(channel, data):
    msg = JKU_t.decode(data)
    print "Data received time is: ", msg.utime
    print "Received message 1 is: ", msg.data[0]

subscription = lc.subscribe("JKU_data", data_handler)

try:
    while True:
        lc.handle()
except KeyboardInterrup:
    pass

lc.unsubscribe(subsription)

