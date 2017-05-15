import lcm
import threading
import numpy as np
from JKUlcm import JKU_t
import sys
#import pygame.locals()
from datetime import datetime
import time

from compress import lz77_compressor
from DBCParser import DBCParser

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
global data_buf
global time_buf
global ID_buf
global compressed_data
data_buf = []
time_buf = []
ID_buf = []
window_size = 20
compressor = lz77_compressor(window_size)

def data_handler(channel, data):
    msg = JKU_t.decode(data)
    #tic = time.clock()
    currTime = msg.str_data[0:13]
    pt = datetime.strptime(currTime, '%H:%M:%S:%f')
    currTime = pt.microsecond*10e-7 + pt.second + pt.minute*60 + pt.hour*3600
    msgID, binaryData = str2binary(msg.str_data)
    global data_buf # contains inary Data
    global time_buf
    global ID_buf
    data_buf.append(binaryData)
    time_buf.append(currTime)
    ID_buf.append(msgID)
    #toc = time.clock()
    #print toc-tic

def str2binary(str_data):
    msgID = int(str_data[13:16], 16) # decimal msg ID

    dataLength = (len(str_data[16:])-1) * 4
    binaryStr = format(int(str_data[16:], 16), '0'+str(dataLength)+'b')
    binaryData = np.ones([dataLength/8,8], dtype = str)
    for i in range (0,dataLength/8):
        for j in range (0, 8):
            binaryData[i][j] = binaryStr[i*8 + j]
#    if msgID == 804:
#        print "the temperature raw data is: ", str_data[16:]
#        print "the binary string of temperature:, ", binaryStr
#        print "the binary version of the temperature is: ", binaryData
#        print "datalength: ",dataLength 
#    if msgID == 476:
#        print "the engine speed2 raw data is: ", str_data[16:]
#        print "the binary string of engine speed2:, ", binaryStr
#        print "the binary version of the engine speed is: ", binaryData
#        print "datalength: ",dataLength 
    return msgID, binaryData

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

class translating_thread(threading.Thread):
    def __init__(self, threadID, name, msgList):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.msgList = msgList
    def run(self):
        global data_buf
        global time_buf
        global ID_buf

        prev_data = None
        j = 0
        try:
            FILE = open('translated_data.txt', 'w')
            while True:
                #print "data_buf is: ", data_buf  
                if j >= len(data_buf): #check if new data comes
                    continue
                else:
                    if np.array_equal(data_buf[j], prev_data): # check if new data comes
                        continue
                    else:
                        for i in range (0, len(self.msgList)):
                            if ID_buf[j] == self.msgList[i].decIdx:
                                decData = self.msgList[i].convert(data_buf[j]) # translate the binary Data to decimal values
                                #print decData
                                #if ID_buf[j] == 804:
                                #    print "Data reveived time is: ", time_buf[j]
                                #    print "Data ID is: ", ID_buf[j]
                                #    print "binary data is: ", data_buf[j]
                                #    some = data_buf[j]
                                #    print "binary data inverse is: ", some[:,::-1]
                                #    print decData
                                FILE.write(str(time_buf[j]) + '    ')
                                FILE.write(str(decData))
                                FILE.write('\n')
                        prevData = data_buf[j]
                        j += 1
        except KeyboardInterrupt:
            sys.exit()
'''
class compression_thread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        # string data compression
        global buf
        global compressed_data
        compressed_data = []
        i = 0
        sizeCompressed = 0
        sizeOriginal = 0

        # compress batch by batch
        batch_size = 200000
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

if __name__ == "__main__":
    # read and parse DBC file, obtain the message list
    #DBCFileName = "../data/2013_Honda_Accord_CVT.dbc"
    DBCFileName = "../data/Mobileye_Honda_Accord_2013.dbc"
    dbc = DBCParser(DBCFileName)
    msgList = dbc.parse()
    # print msgList[0].signalDict['GearDMU'].length
    print "DBC file is parsed!"

    lcm_loop = lcm_thread(1, "lcm_thread")
    translating_loop = translating_thread(2, "translating_thread", msgList)
    #compression = compression_thread(3, "compression_thread")
    lcm_loop.daemon = True
    #compression.daemon = True
    translating_loop.daemon = True

    lcm_loop.start()
    translating_loop.start()
    #compression.start()
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
