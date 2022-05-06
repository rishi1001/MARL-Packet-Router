from src.DQN.dqn_agent import DQNAgent
import random



# class agent
class Agent():
    def __init__(self,neighbours, x,y, batchsize = 64):    
        self.queue = []
        self.neighbours = neighbours
        self.dqn_object = None
        self.position = (x,y)
        self.batchsize = batchsize
        self.state_size = len(self.neighbours) + 2
        self.action_size = len(self.neighbours) + 1     

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
            state.append(1000) # TODO: MAX_TTL??
        return state

    def initDQN(self):
        self.dqn_object = DQNAgent(self, self.state_size, self.action_size)        # TODO add parameters here

    def pushQueue(self, packet):
        self.queue.append(packet)
        return True                            ## return true if packet is pushed for ensuring queue is not full
    
    def popQueue(self):
        if len(self.queue) == 0 :
            return -1
        return self.queue.pop(0)

    def nextAction(self,state):
        # use dqn to find this
        return self.dqn_object.selectAction(state)      # TODO based in q-value

    def trainAgent(self,state,action,nextState,reward):
        # use dqn to train this

        self.dqn_object.memory.store(state=state, action=action, nextState=nextState, reward=reward)
        self.dqn_object.learn(batchsize=self.batchsize)

    def acceptPacket(self,packet ):
        ## TODO add queue size 
        self.pushQueue(packet)

    def getPosition(self):
        return self.position

    def addNeighbour(self,neighbour: Agent):
        self.neighbors.append(neighbour)

    def isUAV(self):
        return True
    
    def isBase(self):
        return False
     
    def isIot(self):
        return False

    def isBaseStation(self):
        return False

    def sendReward(self):                      # based on q-value 
        return self.dqn_object.getQValue()    # TODO Scale this value. 
        
    def run(self):
        state = self.getCurrentState()
        for packet in self.queue:  
            packet.decrease_ttl()         # ttl of packet decreases
        topPacket = self.popQueue()

        if topPacket == -1:
            pass # if the queue is already empty, nothing to do

        if(topPacket.get_ttl() == 0):
            # TODO: negative reward for ttl = 0
            pass
        
        nextAction = self.nextAction(state)                ## from dqn
        if nextAction == len(self.neighbours):
            # TODO : heavy negative reward for dropping packet(as TTL non zero)
            pass
        
        if self.neighbours[nextAction].isBase():   # huge +ve reward. no need to push packet in neighbour
            nextState = self.getCurrentState()
            self.trainAgent(state,nextAction,nextState,1000) 

        self.neighbours[nextAction].acceptPacket(topPacket)  ## push to next agent
        nextState = self.getCurrentState()
        self.trainAgent(state,nextAction,nextState,self.neighbours[nextAction].getReward()) 


    def randomRun(self):
        state = self.getCurrentState()
        for packet in self.queue:  
            packet.decrease_ttl()         # ttl of packet decreases
        topPacket = self.popQueue()
        # topPacket.decrease_ttl()         # ttl of packet decreases

        if(topPacket.get_ttl() == 0):
            ## TODO : check reward for ttl = 0
            reward = -100
            self.dqn_object.memory.store(state=state, action=action, nextState=nextState, reward=reward)
        

        action = random.randint(0,len(self.neighbours)+1)
        if action == len(self.neighbours):
            # TODO : heavy negative reward for dropping packet(as TTL non zero)
            reward = -100
            nextState = self.getCurrentState()
            self.dqn_object.memory.store(state=state, action=action, nextState=nextState, reward=reward)
        
        else:    
            self.neighbours[action].acceptPacket(topPacket)  ## push to next agent
            reward = self.neighbours[action].getReward()
            nextState = self.getCurrentState()
            self.dqn_object.memory.store(state=state, action=action, nextState=nextState, reward=reward)

    
    def getVal(self):
        return len(self.queue)
            