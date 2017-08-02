from DBCInfo import DBCMsg, DBCMsgSignal

class DBCParser():
    def __init__(self, filename = None):
        self.dbcDir = filename
        self.lines = []
        if self.dbcDir is not None:
            with open(self.dbcDir, 'r') as f:
                self.lines = f.readlines()
                f.close()
    def parse(self):
        idx = 0
        msgList = []
        msgIDList = []
        while idx < len(self.lines):
            line = self.lines[idx]
            if len(line) > 1: #and idx >1:
                if line.startswith("BO_ "):
                    idx, msg, msgID = self.parseOneMsg(idx) # start to parse a messgae
                    msgList.append(msg)
                    msgIDList.append(msgID)
            idx += 1
        return msgList, msgIDList
    def parseOneMsg(self, idx):
        msg = DBCMsg(self.lines[idx])
        idx += 1
        while len(self.lines[idx]) > 5: # start to parse all signals of the message
            signal = DBCMsgSignal(self.lines[idx])
            msgID = msg.addSignal(signal)
            idx += 1
        return idx, msg, msgID
