from src.Packets import packet

from configparser import ConfigParser
  
configur = ConfigParser()
configur.read('config.ini')


class BaseStation():

    def __init__(self, x, y):
        self.position = (x,y)
        self.packetRecv = 0
        self.packets_received = []


    def acceptPacket(self, packet):
        self.packetRecv += 1
        self.packets_received.append(packet)

    def getReward(self):
        # ttl can be extracted from last received packet 
        # TODO scale this reward
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

    