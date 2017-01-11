import lcm
import threading
import numpy as np
from JKUlcm import JKU_t
#import pygame, sys
#import pygame.locals()
import time

from compress import lz77_compressor

#pygame.init()
lc = lcm.LCM()

# parameters and buffers for double type data reading

data_size = 10
num_data = 805 
#global buf
#buf = np.zeros(num_data)
#global data
#data = np.zeros((data_size, 805))

# buffer and parameters for string type data reading
global buf
buf = []
global compressed_data
window_size = 20
compressor = lz77_compressor(window_size)

def data_handler(channel, data):
    msg = JKU_t.decode(data)
    print "Data received time is: ", msg.utime
    #print "Received message 1 is: ", msg.data[0]
    print "Received message 1 is: ", msg.str_data
    global buf
    #buf = np.vstack([buf, msg.data])
    buf.append(str(msg.str_data))
    print "type of buf is: ", type(buf[0])

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
        except KeyboardInterrupt:
            print "KeyboardInterrupted!"
            thread.exit()
            sys.exit()
            #pass
        lc.unsubscribe(subsription)
'''
class processing_thread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        init_data = buf
        prev_buf = buf
        global buf
        global data
        while True:
            tmpData = np.zeros((data_size, 805))
            i = 0
            #print"Time of buf in processing loop: ", buf[0]
            while i<10:
                if buf[0] == prev_buf[0]:
                    continue
                #print"Time of buf in processing loop: ", buf[0]
                tmpData[i,:] = buf
                prev_buf = buf
                i = i + 1
            data = tmpData
            # Compress the  data batch
'''
class compression_thread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        '''
        global data
        j = 0
        try:
            while True:
                for i in range(0, data_size):
                    j = j+i
                    data[i,:] = buf[j,:]
        except KeyboardInterrupt:
            thread.exit()
            sys.exit()
        '''
        # string data compression
        global buf
        global compressed_data
        compressed_data = []
        i = 0
        size = 0
        try: 
            while True:
                if i < len(buf):
                    print "buf is: ", buf[i]
                    tmp = compressor.compress(buf[i])
                    compressed_data.append(tmp)
                    print size + len(tmp)
                    i += 1
        except KeyboardInterrupt:
            sys.exit()

if __name__ == "__main__":
    lcm_loop = lcm_thread(1, "lcm_thread")
    #processing_loop = processing_thread(2, "processing_thread")
    compression = compression_thread(3,"compression_thread")
    
    lcm_loop.start()
    #processing_loop.start()
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
