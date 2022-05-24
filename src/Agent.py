from src.DQN.dqn_agent import DQNAgent
import random
from .utils import getManhattanDistance
import math

from configparser import ConfigParser
  
configur = ConfigParser()
import builtins
configur.read(builtins.current_filename)

#configur.read('config.ini')
maxTtl = int(configur.get('packet','maxTtl')) 
defaultTtl = int(configur.get('packet','def_ttl')) 
packet_drop_reward = int(configur.get('reward','packet_drop_reward'))
ttl_zero_reward = int(configur.get('reward','ttl_zero_reward'))
agent_to_agent_scale = float(configur.get('reward','agent_to_agent_scale'))
scaling_type = configur.get('scaling_factor','type')
include_distance = configur.getboolean('reward','include_distance')

# class agent
class Agent():
    def __init__(self,neighbours, x,y,BaseStation, batchsize = 64):    
        self.queue = []
        self.neighbours = neighbours
        self.dqn_object = None
        self.position = (x,y)
        self.batchsize = batchsize
        self.state_size = 1  ## TODO : Removed head packet ttl from state
        self.action_size = 1
        self.targetBaseStation = BaseStation 
        self.latest_loss = 0
        self.losses = []

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
        # if len(self.queue)>0:
        #     state.append(self.queue[0].get_ttl())
        # else:
        #     state.append(maxTtl) #: MAX_TTL??
        return state

    def initDQN(self,device):
        self.dqn_object = DQNAgent(device ,self.state_size, self.action_size)        #  add parameters here

    def loadModel(self,filename):
        self.dqn_object.loadModel(filename)

    def pushQueue(self, packet):
        self.queue.append(packet)
        return True                            ## return true if packet is pushed for ensuring queue is not full
    
    def popQueue(self):
        if len(self.queue) == 0 :
            return -1
        return self.queue.pop(0)

    def getTopPacket(self):
        if len(self.queue) == 0:
            return -1
        return self.queue[-1]

    def nextAction(self,state):
        # use dqn to find this
        return self.dqn_object.selectAction(state)

    def trainAgent(self,state,action,nextState,reward):
        # use dqn to train this

        self.dqn_object.memory.store(state=state, action=action, next_state=nextState, reward=reward)
        self.latest_loss = self.dqn_object.learn(batchsize=self.batchsize)

    def saveLoss(self):
        self.losses.append(self.latest_loss)

    def getLoss(self):  
        return self.losses

    def acceptPacket(self,packet):
        ## TODO add queue size 
        self.pushQueue(packet)

    def getPosition(self):
        return self.position

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

    def getReward(self):       
        top_packet_ttl = self.getTopPacket().get_ttl()    
        reward = agent_to_agent_scale*self.dqn_object.getQValue(self.getCurrentState())    # TODO Scale this value. 
        if scaling_type == 'square':
            scaled_reward = reward*((top_packet_ttl/defaultTtl)**2)
        elif scaling_type == 'exponential':
            scaled_reward = reward*math.exp(top_packet_ttl-defaultTtl)     
        elif scaling_type == 'fraction': 
            scaled_reward = reward*(top_packet_ttl/defaultTtl)
        else:
            scaled_reward = reward
        print("postion {},reward {}".format(self.getPosition(), scaled_reward))         # based on q-value 
        return scaled_reward

    def run(self, train = True):
        state = self.getCurrentState()
        for packet in self.queue:  
            packet.decrease_ttl()         # ttl of packet decreases
        topPacket = self.popQueue()

        if topPacket == -1:
            return # if the queue is already empty, nothing to do

        
        nextAction = self.nextAction(state)                ## from dqn

        if not train:
            print("Position : ",self.getPosition())
            print("States : ", state)
            print("Next Action - ", nextAction)

        nextState = self.getCurrentState()
        if topPacket.get_ttl() <= 0:
            if train:
                self.trainAgent(state,nextAction,nextState,ttl_zero_reward) 
            return
        
        if  nextAction == len(self.neighbours):
            if train:  
                self.trainAgent(state,nextAction,nextState,packet_drop_reward) 
            return
        
        self.neighbours[nextAction].acceptPacket(topPacket)  ## push to next agent
        nextState = self.getCurrentState()
        #TODO: reward should be based on q-value and TTL
        #reward = getManhattanDistance(self.getPosition(), self.targetBaseStation.getPosition()) + self.neighbours[nextAction].getReward()
        reward = self.neighbours[nextAction].getReward()
        if(include_distance):
            reward *= 1/getManhattanDistance(self.getPosition(), self.targetBaseStation.getPosition())

        if train:
            self.trainAgent(state,nextAction,nextState,reward) 


    def randomRun(self):
        state = self.getCurrentState()
        for packet in self.queue:  
            packet.decrease_ttl()         # ttl of packet decreases
        topPacket = self.popQueue()
        # topPacket.decrease_ttl()         # ttl of packet decreases

        if topPacket == -1:
            return # if the queue is already empty, nothing to do

        action = random.randint(0,len(self.neighbours))
        if(topPacket.get_ttl() <= 0):
            reward = ttl_zero_reward
            nextState = self.getCurrentState()
            self.dqn_object.memory.store(state=state, action=action, next_state=nextState, reward=reward)
        

        
        if action == len(self.neighbours):
            reward = packet_drop_reward
            nextState = self.getCurrentState()
            self.dqn_object.memory.store(state=state, action=action, next_state=nextState, reward=reward)
        
        else:    
            self.neighbours[action].acceptPacket(topPacket)  ## push to next agent
            #TODO: reward should be based on q-value and TTL
            
            #reward = getManhattanDistance(self.getPosition(), self.targetBaseStation.getPosition()) + self.neighbours[action].getReward()
            reward = self.neighbours[action].getReward()
            if(include_distance):
                reward *= 1/getManhattanDistance(self.getPosition(), self.targetBaseStation.getPosition())

            nextState = self.getCurrentState()
            self.dqn_object.memory.store(state=state, action=action, next_state=nextState, reward=reward)

    
    def getVal(self):
        return len(self.queue)

    def reset(self):
        """
        reset everything in the agent to turn on test mode
        """
        self.queue = []
