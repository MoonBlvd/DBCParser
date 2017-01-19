import lcm
import threading
import numpy as np
from JKUlcm import JKU_t
import sys
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
    #print "Received message type is: ", type(msg.str_data)
    print "Received message is: ", msg.str_data
    msgLength = (len(msg.str_data)-1) * 4
    print "length is : ", msgLength
    binData = format(int(msg.str_data, base = 16),'0'+str(msgLength)+'b')
    print "Received message in binary is: ", binData
    global buf
    #buf = np.vstack([buf, msg.data])
    #buf.append(str(msg.str_data))
    buf.append(binData)

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
        sizeCompressed = 0
        sizeOriginal = 0

        # compress batch by batch
        batch_size = 10000
        try: 
            while True:
                if (i+1) * batch_size <= len(buf):
                    batch = "".join(buf[i*batch_size:(i+1)*batch_size])
                    #print "binary batch is: ", batch
                    tmp = compressor.compress(batch)
                    start = time.time()
                    compressed_data.append(tmp)
                    elapsed = time.time()-start
                    print "Compressing time is: ", elapsed
                    #print "compressed batch is: ", tmp
                    sizeOriginal += len(batch)
                    sizeCompressed += len(tmp)
                    print "Original batch size in bits is: ", sizeOriginal
                    print "Compressed batch size in bits is: ", sizeCompressed
                    i += 1
        except KeyboardInterrupt:
            sys.exit()
        ''' 
        # compress line by line
        try: 
            while True:
                if i < len(buf):
                    print "buf is: ", buf[i]
                    tmp = compressor.compress(buf[i])
                    compressed_data.append(tmp)
                    size += len(tmp)
                    print size
                    i += 1
        '''


if __name__ == "__main__":
    lcm_loop = lcm_thread(1, "lcm_thread")
    #processing_loop = processing_thread(2, "processing_thread")
    compression = compression_thread(3,"compression_thread")
    lcm_loop.daemon = True
    compression.daemon = True

    lcm_loop.start()
    #processing_loop.start()
    compression.start()
    while True:
        continue

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
