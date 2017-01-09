import lcm
import threading
import numpy as np
from JKUlcm import JKU_t
import pygame, sys
#import pygame.locals()
import time

pygame.init()
lc = lcm.LCM()
buf_size = 10
num_data = 805 
global buf
buf = np.zeros(num_data)
global data
data = np.zeros((buf_size, 805))

def data_handler(channel, data):
    msg = JKU_t.decode(data)
    print "Data received time is: ", msg.utime
    print "Received message 1 is: ", msg.data[0]
    global buf
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
            print "killing lcm-thread..."
            sys.exit()
            #pass
        lc.unsubscribe(subsription)

class processing_thread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        init_data = buf
        prev_buf = buf
        global buf
        while True:
            tmpData = np.zeros((buf_size, 805))
            i = 0
            #print"Time of buf in processing loop: ", buf[0]
            while i<10:
                if buf[0] == prev_buf[0]:
                    continue
                #print"Time of buf in processing loop: ", buf[0]
                tmpData[i,:] = buf
                prev_buf = buf
                i = i + 1
            global data
            data = tmpData
            # Compress the  data batch
            

class compression_thread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        global data
        i = 0
        while True:
            if data[1,0] != 0:
                i = i+1
                print data
                if i == 3:
                    sys.exit()

if __name__ == "__main__":
    lcm_loop = lcm_thread(1, "lcm_thread")
    processing_loop = processing_thread(2, "processing_thread")
    compression = compression_thread(3,"compression_thread")
    
    lcm_loop.start()
    processing_loop.start()
    compression.start()
'''
    try:
        while True:
            print buf[0]
            if buf[0] != prev_buf[0]:
                print "in if"
                print buf
    except KeyboardInterrup:
        print "killing lcm-thread..."
        raise
        #sys.exit()

    while True:
        event = pygame.event.wait()
        #for event in events:
           # print "waiting for quit..."
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                print "Quit now..."
                pygame.quit()
                sys.exit()

'''
