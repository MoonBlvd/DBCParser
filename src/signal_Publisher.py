import numpy as np
import os
import csv
import time
from datetime import datetime

import lcm
from JKUlcm import JKU_t

msg = JKU_t()
lc = lcm.LCM()

def dataReader(filename):
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
if __name__ == '__main__':       
    filename = 'exp1_077.csv'
    data = dataReader(filename)
    num_rows, num_cols = data.shape
    msg.num_data = num_cols
    print num_rows, num_cols
    init_time = time.time()
    for i in range (0,num_rows):
        #tmp_time = datetime.now().time()
        msg.utime = time.time()-init_time
        msg.data = np.array(data[i,:], dtype = float)
        print "Time : ", msg.utime
        lc.publish("JKU_data", msg.encode())
        time.sleep(0.5)
