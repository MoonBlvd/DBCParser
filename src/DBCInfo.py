import re
class DBCMsg():
    def __init__(self, line):
        pat = r"BO_ " + \
              r"(?P<decIdx>[\d]+) " + \
              r"(?P<name>[\dA-Za-z_]+): (?P<size>[\d]) " + \
              r"(?P<node>[\dA-Za-z_]+)"
        values = re.search(pat, line).groupdict()
        self.decIdx = int(values['decIdx']) # get the decimal CAN ID
        self.hexIdx = '%x' % self.decIdx # get the hex CAN ID
        self.hexIdx = self.hexIdx.lower() # get the hex can ID
        self.name = values['name']
        self.size = int(values['size']) # Length of the msg in bytes
        self.node = values['node']
        self.signalDict = {} # signal dictionary, store the signals that already parsed

    def addSignal(self, signal):
        if signal.signalName in self.signalDict:
            print "DBCMsg addSignal: duplicated message name!"
        self.signalDict[signal.signalName] = signal

    #Add time to the dictionary
    def convert(self, binaryData):
        ret = {}
        for signalName, signal in self.signalDict.items():
            ret[signalName] = signal.extract(binaryData)
        return ret
    
    def __str__(self):
        return "Message ID: " + self.hexIdx + \
               " Message name: " + self.name + \
               " Message length: " + str(self.size) + " bytes" + \
               " # of signals: " + str(len(self.signalDict))

class DBCMsgSignal():
    def __init__(self, line): # load the
        FLOATP = r"[\d+-.E]"
        pat = r" SG_ " + \
              r"(?P<signalName>[\dA-Za-z_]+) ?(?P<multiplexGroup>[Mm\d]*) : " + \
              r"(?P<startBit>[\d]+)\|(?P<length>[\d]+)@(?P<order>[\d])(?P<sign>[+-]) " + \
              r"\((?P<factor>FLOATP+)[,](?P<offset>FLOATP+)\) " + \
              r"\[(?P<minimum>FLOATP+)\|(?P<maximum>FLOATP+)\] " + \
              r"\"(?P<unit>[\S\s]*)\" +" + \
              r"(?P<node>[\dA-Za-z_]+)"
        pat = pat.replace("FLOATP", FLOATP)
        values = re.search(pat, line).groupdict()
        self.signalName = values['signalName']
        self.startBit = int(values['startBit'])
        self.length = int(values['length'])
        self.byteOrder = 'Intel' if values['order'] == '1' else 'Motorola' # byte order is from LSB or MSB
        self.isSigned = 1 if values['sign'] == '-' else 0
        self.factor = float(values['factor'])
        self.offset = float(values['offset'])
        self.minimum = float(values['minimum'])
        self.maximum = float(values['maximum'])
        self.unit = values['unit']
        self.node = values['node']

    def extract(self, binaryData):
        binaryData = self.extractFieldBinary(binaryData)
        return self.extractValue(binaryData)

    def extractValue(self, binaryData):
        if self.isSigned: # shift to [-127, 128]if the signal is signed
            #val = DBCMsgSignal.twosComplement(int(binaryData,2), len(binaryData))
            val = DBCMsgSignal.twosComplement(binaryData, len(binaryData))
        else:
            val = int(binaryData, 2)
        val = val*self.factor + self.offset
        if val > self.maximum:
            val = self.maximum
        elif val < self.minimum:
            val = self.minimum
        return val # compute the real decimal value of the signal
    def extractFieldBinary(self, binaryData):
        binaryRet = ''
        if self.byteOrder == 'Intel' :
            row = self.startBit / 8
            col = self.startBit - row * 8
            for idx in range(self.length):
                #print "binaryData is: ", binaryData
                #print "row and col is:", [row, col]
                binaryRet += binaryData[row][col]
                if col == 7:
                    col = 0
                    row += 1
                else:
                    col += 1
            return binaryRet[::-1] #return MSB->LSB
        elif self.byteOrder == 'Motorola':
            binaryData = binaryData[:,::-1]
            row = self.startBit / 8
            col = self.startBit - row * 8
            for idx in range(self.length):
                #print "binaryData size is: ", binaryData.shape
                #print "row and col is:", [row, col]
                binaryRet += binaryData[row][col]

                if col == 0:
                    col = 7
                    row += 1
                else:
                    col -= 1
            return binaryRet #return MSB -> LSB
        '''
        elif self.byteOrder == 'Motorola':
            row = self.startBit / 8
            col = self.startBit - row * 8
            for idx in range(self.length):
                binaryRet += binaryData[row][col]
                if col == 0:
                    col = 7
                    row += 1
                else:
                    col -= 1
            return binaryRet #return MSB -> LSB
            '''
    @staticmethod
    def twosComplement(val, bits):  # positive and negative
    # compute the 2's compliment of int value val
        if bits > 1:
            value = int(val[1:],2)
            if val[0]=='1':
                value *= -1
        else:
            value = int(val,2)
        return value
    #    if (val & (1 << (bits - 1))) != 0:  # if sign bit is set e.g., 8bit: 128-255
    #        val -= (1 << bits)  # compute negative value
    #    return val
