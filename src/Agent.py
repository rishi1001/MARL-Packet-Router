
# from src.DQN import DQN
# class agent
class Agent():
    def __init__(self,neighbours, x,y):
        self.queue = []
        self.neighbours = neighbours
        self.dqn_object = DQN()
        self.position = (x,y)

    def pushQueue(self, packet):
        self.queue.append(packet)
    
    def popQueue(self):
        return self.queue.pop(0)

    def nextAgent(self):
        # use dqn to find this
        return self.dqn_object.nextAgent()

    def trainAgent(self,reward):
        # use dqn to train this
        self.dqn_object.trainAgent(reward)

    def getPosition(self):
        return self.position

    def addNeighbour(self,neighbour: Agent):
        self.neighbors.append(neighbour)

    def isUAV(self):
        return true




