import numpy as np
import sys
from datetime import datetime
import time
import cPickle as pkl

from DBCParser import DBCParser

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
    with open('../data/Data_03092017/' + filename, 'r') as file:
        f = file.readlines()
    for line in f:
        length = len(line)
        tmpData = ''
        for j in range (0, length):
            if j == 0:
                tmpTime = line[0:13]
            if j == 21: # save the canID
                tmpID = line[21:24]
                #j += 5
            if j == 27: # save the message size
                tmpDataDigits = str(int(line[27])-1)
            if j >= 29: # save the data bytes
                if line[j] != ' ' and line[j] != '\n':
                    tmpData += line[j]
        if i == 0:
            data = [tmpTime + tmpID + tmpData]
        else:
            data.append(tmpTime + tmpID + tmpData)
        i += 1
    return data

def str2binary(str_data):
    msgID = int(str_data[13:16], 16) # decimal msg ID

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
            #FILE.write(str(currTime) + '    ')
            FILE.write(str(decData))
            FILE.write('\n')
            #pkl.dump(decData, DICT)
            return decData
    return None   


if __name__ == '__main__':  
	# code for reading and publishing string type data
    filename = 'AroundAnnArbor_CAN_1_Mobileye_2.log'
    data = logReader(filename)

    # read and parse DBC file, obtain the message list
    DBCFileName = "../data/Mobileye_Honda_Accord_2013.dbc"
    dbc = DBCParser(DBCFileName)
    msgList = dbc.parse()
    print "DBC file is parsed!"

    #start translate
    FILE = open('translated_data.txt', 'w')
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
        tmpData = translate(msgID, binaryData, currTime, msgList, FILE)
        if tmpData != None:
            DICTs.append(tmpData)
        i += 1
    pkl.dump(DICTs,open( "translated_dict.pkl", "wb" ))
