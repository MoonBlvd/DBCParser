import lcm
import threading
import numpy as np
from JKUlcm import JKU_t
#from msvcrt import getch

lc = lcm.LCM()
#buf_size = 10
num_data = 805 
buf = np.zeros(num_data)

def data_handler(channel, data):
    msg = JKU_t.decode(data)
    #print "Data received time is: ", msg.utime
    #print "Received message 1 is: ", msg.data[0]
    buf = msg.data

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
        
class processing_thread(threading.Thread):
    def __init__(self, threadID, name):
        self.threadID = threadID
        self.name = name
    def run(self):
        init_data = buf
        prev_buf = buf
        while True:
            data = np.zeros(buf_size, 805)
            i = 0
            while i<10:
                if buf[0] == prev_buf[0]:
                    continue
                data[i,:] = buf
                prev_buf = buf
                i = i+1
            print data
if __name__ == "__main__":
    lcm_loop = lcm_thread(1, "lcm_thread")
  #  processing_loop = processing_thread(2, "processing_thread")

    lcm_loop.start()
    prev_buf = buf
  #  processing_loop.start()
    while True:
        key = ord(getch())
        if key == 27: #ESC
            break
        if buf[0] != prev_buf[0]:
            print buf

