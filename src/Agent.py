
from src.DQN.dqn_agent import DQNAgent
# class agent
class Agent():
    def __init__(self,neighbours, x,y):
        self.queue = []
        self.neighbours = neighbours
        self.dqn_object = DQNAgent(self)        # TODO add parameters here
        self.position = (x,y)

    def pushQueue(self, packet):
        self.queue.append(packet)
    
    def popQueue(self):
        return self.queue.pop(0)

    def nextAgent(self):
        # use dqn to find this
        return self.dqn_object.nextAgent()      # TODO

    def trainAgent(self,reward):
        # use dqn to train this
        self.dqn_object.trainAgent(reward)

    def getPosition(self):
        return self.position

    def addNeighbour(self,neighbour: Agent):
        self.neighbors.append(neighbour)

    def isUAV(self):
        return True

    def sendReward(self):       # TODO 
        pass




