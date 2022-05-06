from src.DQN.dqn_agent import DQNAgent
import random



# class agent
class Agent():
    def __init__(self,neighbours, x,y, batchsize = 64):     # TODO define state
        self.queue = []
        self.neighbours = neighbours
        self.dqn_object = None
        self.position = (x,y)
        self.batchsize = batchsize

    def initDQN(self):
        self.dqn_object = DQNAgent(self, state_size, len(self.neighbours)+1)        # TODO add parameters here

    def pushQueue(self, packet):
        self.queue.append(packet)
        return True                            ## return true if packet is pushed for ensuring queue is not full
    
    def popQueue(self):
        return self.queue.pop(0)

    def nextAction(self,state):
        # use dqn to find this
        return self.dqn_object.selectAction(state)      # TODO based in q-value

    def trainAgent(self,state,action,nextState,reward):
        # use dqn to train this

        self.dqn_object.memory.store(state=state, action=action, nextState=nextState, reward=reward)
        self.dqn_object.learn(batchsize=self.batchsize)


    def getPosition(self):
        return self.position

    def addNeighbour(self,neighbour: Agent):
        self.neighbors.append(neighbour)

    def isUAV(self):
        return True

    def isBaseStation(self):
        return False

    def sendReward(self):                      # based on q-value 
        return self.dqn_object.getQValue()    # TODO Scale this value
        

    def run(self):
        topPacket = self.popQueue()
        topPacket.decrease_ttl()         # ttl of packet decreases

        if(topPacket.get_ttl() == 0):
            # TODO: negative reward for ttl = 0
            pass
                    
        nextAction = self.nextAction(state)                ## from dqn      
        if nextAction == len(self.neighbours):
            # TODO : heavy negative reward for dropping packet(as TTL non zero)
            pass

        ## TODO : if neighbours.nextAction is base station then call accept packet

        self.neighbours[nextAction].pushQueue(topPacket)  ## push to next agent
        self.trainAgent(state,nextAction,nextState,self.neighbours[nextAction].getReward()) ## TODO 


    def randomRun(self):
        topPacket = self.popQueue()
        topPacket.decrease_ttl()         # ttl of packet decreases

        if(topPacket.get_ttl() == 0):
            ## TODO : check reward for ttl = 0
            reward = -100
            self.dqn_object.memory.store(state=state, action=action, nextState=nextState, reward=reward)
        

        action = random.randint(0,len(self.neighbours)+1)
        if action == len(self.neighbours):
            # TODO : heavy negative reward for dropping packet(as TTL non zero)
            reward = -100
            self.dqn_object.memory.store(state=state, action=action, nextState=nextState, reward=reward)
        
        else:    
            self.neighbours[action].pushQueue(topPacket)  ## push to next agent
            reward = self.neighbours[action].getReward()
            self.dqn_object.memory.store(state=state, action=action, nextState=nextState, reward=reward)

    
    def getVal(self):
        return len(self.queue)
            