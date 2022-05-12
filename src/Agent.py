from src.DQN.dqn_agent import DQNAgent
import random
from .utils import getManhattanDistance

from configparser import ConfigParser
  
configur = ConfigParser()
configur.read('config.ini')
maxTtl = int(configur.get('packet','maxTtl')) 
packet_drop_reward = int(configur.get('reward','packet_drop_reward'))
ttl_zero_reward = int(configur.get('reward','ttl_zero_reward'))
agent_to_agent_scale = int(configur.get('reward','agent_to_agent_scale'))

# class agent
class Agent():
    def __init__(self,neighbours, x,y,BaseStation, batchsize = 64):    
        self.queue = []
        self.neighbours = neighbours
        self.dqn_object = None
        self.position = (x,y)
        self.batchsize = batchsize
        self.state_size = 2
        self.action_size = 1
        self.targetBaseStation = BaseStation 

    def getCurrentState(self):
        """
            current queue size, queue sizes of all neighbours, remaining ttl of packet at head
        """
        state = [len(self.queue)]
        for neighbour in self.neighbours:
            if not neighbour.isBase():
                state.append(len(neighbour.queue))
            else:
                state.append(0)   # base station is always given empty queue, denoting availability TODO: think
        if len(self.queue)>0:
            state.append(self.queue[0].get_ttl())
        else:
            state.append(maxTtl) #TODO : MAX_TTL??
        return state

    def initDQN(self,device):
        self.dqn_object = DQNAgent(device ,self.state_size, self.action_size)        # TODO add parameters here

    def pushQueue(self, packet):
        self.queue.append(packet)
        return True                            ## return true if packet is pushed for ensuring queue is not full
    
    def popQueue(self):
        if len(self.queue) == 0 :
            return -1
        return self.queue.pop(0)

    def nextAction(self,state):
        # use dqn to find this
        return self.dqn_object.selectAction(state)

    def trainAgent(self,state,action,nextState,reward):
        # use dqn to train this

        self.dqn_object.memory.store(state=state, action=action, next_state=nextState, reward=reward)
        self.dqn_object.learn(batchsize=self.batchsize)

    def acceptPacket(self,packet):
        ## TODO add queue size 
        self.pushQueue(packet)

    def getPosition(self):
        return self.position

                                    ## TODO why agent?
    # def addNeighbour(self,neighbour: Agent):
    #     self.neighbors.append(neighbour)

    def addNeighbour(self,neighbour):
        self.neighbours.append(neighbour)
        self.action_size+=1
        self.state_size+=1

    def isUAV(self):
        return True
    
    def isBase(self):
        return False
     
    def isIot(self):
        return False

    def isBaseStation(self):
        return False

    def getReward(self):                      # based on q-value 
        return agent_to_agent_scale*self.dqn_object.getQValue()    # TODO Scale this value. 
        
    def run(self):
        state = self.getCurrentState()
        for packet in self.queue:  
            packet.decrease_ttl()         # ttl of packet decreases
        topPacket = self.popQueue()

        if topPacket == -1:
            return # if the queue is already empty, nothing to do

        
        nextAction = self.nextAction(state)                ## from dqn
        nextState = self.getCurrentState()
        if topPacket.get_ttl() == 0:
            self.trainAgent(state,nextAction,nextState,ttl_zero_reward) 
            return
        
        if  nextAction == len(self.neighbours):  
            self.trainAgent(state,nextAction,nextState,packet_drop_reward) 
            return
        
        self.neighbours[nextAction].acceptPacket(topPacket)  ## push to next agent
        nextState = self.getCurrentState()
        #TODO: reward should be based on q-value and TTL
        reward = getManhattanDistance(self.getPosition(), self.targetBaseStation.getPosition()) + self.neighbours[nextAction].getReward()
        self.trainAgent(state,nextAction,nextState,reward) 


    def randomRun(self):
        state = self.getCurrentState()
        for packet in self.queue:  
            packet.decrease_ttl()         # ttl of packet decreases
        topPacket = self.popQueue()
        # topPacket.decrease_ttl()         # ttl of packet decreases

        if topPacket == -1:
            return # if the queue is already empty, nothing to do


        if(topPacket.get_ttl() == 0):
            reward = -1000
            self.dqn_object.memory.store(state=state, action=action, next_state=nextState, reward=reward)
        

        action = random.randint(0,len(self.neighbours))
        if action == len(self.neighbours):
            reward = -1000
            nextState = self.getCurrentState()
            self.dqn_object.memory.store(state=state, action=action, next_state=nextState, reward=reward)
        
        else:    
            self.neighbours[action].acceptPacket(topPacket)  ## push to next agent
            #TODO: reward should be based on q-value and TTL
            
            reward = getManhattanDistance(self.getPosition(), self.targetBaseStation.getPosition()) + self.neighbours[action].getReward()
            nextState = self.getCurrentState()
            self.dqn_object.memory.store(state=state, action=action, next_state=nextState, reward=reward)

    
    def getVal(self):
        return len(self.queue)