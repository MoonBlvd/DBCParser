import numpy as np
import sys
from datetime import datetime
import time
import cPickle as pkl

from DBCParser import DBCParser
'''
This code load the raw BUSMASTER data log (in this project, Mobileye data),
and translate it and save as a pkl file and a text file.
'''

'''
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
'''
def logReader(filedir, filename):
    i = 0
    with open(filedir + filename, 'r') as file:
        f = file.readlines()
    init_flag = 0;
    for line in f:
        length = len(line)
        tmpData = ''
        for j in range (0, length):
            if j == 0:
                tmpTime = line[0:13]
            if j == 17:
                tmpCH = line[17]
                #if tmpCH == '2':
                #    break
            if j == 21: # save the canID
                tmpID = line[21:24]
                if tmpID == '18D':
                    break
                #j += 5
            if j == 27: # save the message size
                print ('====================')
                print (i)
                print (line)
                print (line[27])
                tmpDataDigits = str(int(line[27])-1)
            if j >= 29: # save the data bytes
                if line[j] != ' ' and line[j] != '\n':
                    tmpData += line[j]
        # only translate one channel
        if init_flag == 0:
            if (tmpCH == '1' or '2') and (tmpID != '18D'):
                data = [tmpTime + tmpID + tmpData]
                init_flag = 1;
        else:
            if (tmpCH == '1' or '2') and (tmpID != '18D'):
                data.append(tmpTime + tmpID + tmpData)
        i += 1
    return data

def str2binary(str_data):
    msgID = int(str_data[13:16], 16) # decimal msg ID
    #if msgID == 397:
    #    return msgID, None

    dataLength = (len(str_data[16:])-1) * 4
    binaryStr = format(int(str_data[16:], 16), '0'+str(dataLength)+'b')
    binaryData = np.ones([dataLength/8,8], dtype = str)
    for i in range (0,dataLength/8):
        for j in range (0, 8):
            binaryData[i][j] = binaryStr[i*8 + j]
    return msgID, binaryData

def translate(msgID, binaryData, currTime, msgList, FILE):
    for i in range (0, len(msgList)):
        if msgID == msgList[i].decIdx:
            decData = msgList[i].convert(binaryData) # translate the binary Data to decimal values
            decData['Time'] = currTime
            decData['msgID'] = msgID
            FILE.write(str(msgID) + '    ')
            FILE.write(str(decData))
            FILE.write('\n')
            #pkl.dump(decData, DICT)
            return decData
    return None   


if __name__ == '__main__':  
	# code for reading and publishing string type data
    #filename = 'AroundAnnArbor_CAN_1_Mobileye_2.log'
    dir_name = sys.argv[1]
    trajectory_name = sys.argv[2]
    # filename = 'BUSMASTER_'+ trajectory_name+ '.log'
    filename = trajectory_name + '.log'
    #filedir = '../data/Data_06192017/'
    # filedir = '../data/Data_10172017/'#'../test_08052017/'
    # target_dir = '../translated_data/10172017/' #'../test_08052017/'
    filedir = '../data/' + dir_name + '/' #'../test_08052017/'
    target_dir = '../translated_data/' + dir_name + '/'#'../test_08052017/'
    data = logReader(filedir,filename)

    # read and parse DBC file, obtain the message list
    DBCFileName = "../data/Mobileye_Honda_Accord_2013.dbc"
    dbc = DBCParser(DBCFileName)
    msgList, msgIDList = dbc.parse()
    print "DBC file is parsed!"

    #start translate
    FILE = open(target_dir + trajectory_name + '.txt', 'w')
    #FILE = 1
    DICTs = []
    maxNum = len(data)
    print 'max num is: ', maxNum
    for i in range (0,maxNum):
        print "Time : ", data[i][0:13]
        #print "data: ", data[i]
        currTime = data[i][0:13]
        pt = datetime.strptime(currTime, '%H:%M:%S:%f')
        currTime = pt.microsecond*10e-7 + pt.second + pt.minute*60 + pt.hour*3600
        msgID, binaryData = str2binary(data[i])
        #if msgID == 397:
        #    continue

        tmpData = translate(msgID, binaryData, currTime, msgList, FILE)
        if tmpData != None:
            DICTs.append(tmpData)
        i += 1
    pkl.dump(DICTs,open( target_dir + trajectory_name + '.pkl', "wb" ))
