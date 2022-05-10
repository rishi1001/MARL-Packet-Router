from src.Packets import packet


class BaseStation():

    def __init__(self, x, y, reward):
        self.reward = 1000
        self.position = (x,y)
        self.packetRecv = 0
        self.packets_received = []


    def acceptPacket(self, packet):
        # TODO some local computation maybe to update the variable reward
        self.packetRecv += 1
        self.packets_received.append(packet)

    def getReward(self):
        # ttl can be extracted from last received packet 
        ttl = self.packets_received[-1].get_ttl()
        return ttl*ttl

    def getPosition(self):
        return self.position

    def isUAV(self):
        return False
    
    def isBase(self):
        return True
     
    def isIot(self):
        return False

    def getVal(self):
        return self.packetRecv

    