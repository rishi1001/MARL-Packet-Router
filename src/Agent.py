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
        return True                            ## return true if packet is pushed for ensuring queue is not full
    
    def popQueue(self):
        return self.queue.pop(0)

    def nextAgent(self):
        # use dqn to find this
        return self.dqn_object.nextAgent()      # TODO based in q-value

    def trainAgent(self,reward):
        # use dqn to train this
        self.dqn_object.trainAgent(reward)     ## TODO put in a replay memory

        # dqn_agent.memory.store(state=state, action=action, next_state=next_state, reward=reward, done=done)
        # dqn_agent.learn(batchsize=batchsize)


    def getPosition(self):
        return self.position

    def addNeighbour(self,neighbour: Agent):
        self.neighbors.append(neighbour)

    def isUAV(self):
        return True

    def sendReward(self):                      # TODO based on q-value 
        pass

    def run(self):
        topPacket = self.popQueue()
        topPacket.decrease_ttl()         # ttl of packet decreases

        if(topPacket.get_ttl() == 0):
            # TODO: negative reward for ttl = 0
            pass
                    
        nextAgent = self.nextAgent()                ## from dqn
        nextAgent.pushQueue(topPacket)  ## push to next agent
        self.trainAgent(nextAgent.getReward()) ## train agent





