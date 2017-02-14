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
    i = 0
    with open('../data/Data_01032017/' + filename, 'r') as file:
        f = file.readlines()
    for line in f:
        length = len(line)
        tmpData = ''
        for j in range (0, length):
            if j == 21: # save the canID
                tmpID = line[21:24]
                j += 5
            if j == 27:
                tmpDataDigits = str(int(line[27])-1)
            if j >=29: # save the data bytes
                if line[j] != ' ' and line[j] != '\n':
                    tmpData += line[j]
        if i == 0:
            data = [tmpID + tmpDataDigits + tmpData]
        else:
            data.append(tmpID + tmpDataDigits + tmpData)
        i += 1
    return data

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
    #while data[i]:
    while i <= 200000:
        msg.utime = time.time()-init_time
        #msg.data = np.array(data[i,:], dtype = float)
        msg.str_data = data[i]
        print "Time : ", msg.utime
        print "data: ", msg.str_data
        lc.publish("JKU_data", msg.encode())
        time.sleep(0.1)
        i += 1
    
