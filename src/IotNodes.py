import sys
sys.path.append(".")
from Packets import packet
from Agent import Agent
import numpy as np
from configparser import ConfigParser
  
configur = ConfigParser()
configur.read('config.ini')

## def_ttl initial value of ttl
class IotNodes():

    def __init__(self,rate,def_ttl,x,y, transmission_rate = 10):
        self.rate=rate
        self.def_ttl=def_ttl
        self.position=(x,y)
        self.neighbours = []
        self.total_packets=0
        self.queue = []
    
    def generatePacket(self):   # TODO what is this ? , and use of numpy ? and use of random ? 
        """
        generates 0-rate number of packets and adds to the back of queue
        In every cycle, transmission_rate number of packets would be transmitted to agents
        """
        l=[]
        num_packets = np.random.randint(self.rate)
        for i in range(num_packets):
            self.queue.append(packet(self.def_ttl))
    
    
    def findNeighbour(self):
        ## TODO :policy to find the neighbour : returning one with min queue size as of now
        queues = np.array([agent.getVal() for agent in self.neighbours])
        agents = [agent for agent in self.neighbours]
        return agents[ np.argmin(queues) ]

    def isUAV(self):
        return False
    
    def isBase(self):
        return False
     
    def isIot(self):
        return True

    def isBaseStation(self):
        return False

    def run(self):
        self.total_packets+=self.rate
        self.generatePacket()
        for packet in self.queue:
            packet.decrease_ttl()
        for i in range(self.transmission_rate):
            if self.getQueueSize() > 0:   # check if queue has any packets
                packet = self.queue.pop(0)
                agent=self.findNeighbour()
                agent.pushQueue(packet)
            

    def getPosition(self):
        return self.position

    def addNeighbour(self,neighbour: Agent):
        self.neighbors.append(neighbour)

    def getVal(self):               # returns the total number of packets generated
        return self.total_packets

    def getQueueSize(self):
        return len(self.queue)
