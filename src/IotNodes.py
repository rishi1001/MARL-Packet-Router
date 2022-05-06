import sys
sys.path.append(".")
from Packets import packet
from Agent import Agent

## def_ttl initial value of ttl
class IotNodes():

    def __init__(self,rate,def_ttl,x,y):
        self.rate=rate
        self.def_ttl=def_ttl
        self.position=(x,y)
        self.neighbours = []
    
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
    
    def isBase(self):
        return False
     
    def isIot(self):
        return True

    def run(self):
        packets=self.generatePacket()
        for packet in packets:
            packet.decrease_ttl()
            agent=self.findNeighbour()
            agent.pushQueue(packet)
            

    def getPosition(self):
        return self.position

    def addNeighbour(self,neighbour: Agent):
        self.neighbors.append(neighbour)