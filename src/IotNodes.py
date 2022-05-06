import sys
sys.path.append(".")
from Packets import packet

## def_ttl initial value of ttl
class IotNodes():

    def __init__(self,rate,def_ttl,x,y):
        self.rate=rate
        self.def_ttl=def_ttl
        self.position=(x,y)
        self.total_packets=0
    
    def generatePacket(self):
        l=[]
        for i in range(self.rate):
            l.append(packet(self.def_ttl))
        return l
    
    
    def findNeighbour(self):
        ## TODO :policy to find the neighbour
        pass

    def isUAV(self):
        return False

    def isBaseStation(self):
        return False

    def run(self):
        self.total_packets+=self.rate
        packets=self.generatePacket()
        for packet in packets:
            packet.decrease_ttl()
            agent=self.findNeighbour()
            agent.pushQueue(packet)
            

    def getPosition(self):
        return self.position

    def getVal(self):               # returns the total number of packets generated
        return self.total_packets