import lcm
import threading
from JKUlcm import JKU_t

lc = lcm.LCM()

def data_handler(channel, data):
    msg = JKU_t.decode(data)
    print "Data received time is: ", msg.utime
    print "Received message 1 is: ", msg.data[0]
    return msg.data

class lcm_thread(threading.Thread):
    def __init__(self,threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        subscription = lc.subscribe("JKU_data", data_handler)
        try:
            while True:
               lc.handle()
        except KeyboardInterrup:
            pass
        lc.unsubscribe(subsription)
#class processing_thread(threading.Thread):
#    def __init__(self)

if __name__ == "__main__":
    lcm_loop = lcm_thread(1, "lcm_thread")
#    processing_loop = processing_thread

    lcm_loop.start()
#    processing_loop.start()
