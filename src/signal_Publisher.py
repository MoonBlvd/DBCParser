import numpy as np
import os
import csv
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
    return data, i+1
if __name__ == '__main__':       
    filename = 'exp1_077.csv'
    data = dataReader(filename)
    num_rows, num_cols = data.shape
    msg.num_data = num_cols
    print num_rows, num_cols
    for i in range (0,num_rows):
        msg.utime = datetime.now().time()
        msg.data =  data[i,:]
        lc.publish("JKU_data", msg.encode())
