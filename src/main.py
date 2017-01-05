import numpy as np
'''def splitData(line):
    for entry in line:
        if entry == " ":

    return time, TX/RX, channel, ID, canType, DLC, Data
'''
def readData(filename):
    with open(filename,'r') as file:
        lines = file.readlines()
    print len(lines)
    time = []
    TXRX = []
    channel = []
    canID = []
    canType = []
    DLC = []
    dataBytes = []
    for line in lines:
        if line[0] != "*": 
            for entry in line.splitlines(): #the size of the loop is 1
                time.append(entry.split()[0])
                TXRX.append(entry.split()[1])
                channel.append(entry.split()[2])
                canID.append(entry.split()[3])
                canType.append(entry.split()[4])
                DLC.append(entry.split()[5])
                dataBytes.append(entry.split()[6])
                print dataBytes

    print dataBytes
            
if __name__ == "__main__":
    filename = "../data/Data_01032017/Greenhills maneuvering.log" 
    readData(filename)
