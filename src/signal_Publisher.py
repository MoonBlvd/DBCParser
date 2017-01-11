import numpy as np
import os
import csv
import time
from datetime import datetime

import lcm
from JKUlcm import JKU_t

msg = JKU_t()
lc = lcm.LCM()

def csvReader(filename):
    i = 0
    with open('../data/'+filename, 'r') as file:
        tmp = csv.reader(file, delimiter=',')
        for line in tmp:
            if i == 0:
                data = line
                data = np.array(data)
            else:
            #print line[0]
               data =  np.vstack((data,line))
            i = i+1
    #print data[:,0]
    return data

def logReader(filename):
    with open('../data/Data_01032017/' + filename, 'r') as file:
        f = file.readlines()
    return f

if __name__ == '__main__':       
    # code for reading and publishing double type data

    #filename = 'exp1_077.csv'
    #data = csvReader(filename)
    #num_rows, num_cols = data.shape
    #msg.num_data = num_cols
    #print num_rows, num_cols

    # code for reading and publishing string type data

    filename = 'data1.log'
    data = logReader(filename)
    msg.num_data = 1
    
    #record time
    init_time = time.time()
    i = 0
    #for i in range (0,num_rows):
    while data[i]:
        msg.utime = time.time()-init_time
        #msg.data = np.array(data[i,:], dtype = float)
        msg.str_data = data[i]
        print "Time : ", msg.utime
        print "data: ", msg.str_data
        lc.publish("JKU_data", msg.encode())
        time.sleep(0.5)
        i += 1
