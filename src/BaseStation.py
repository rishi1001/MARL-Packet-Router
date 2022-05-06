class BaseStation():

    def __init__(self, x, y):
        reward = 0
        self.position = (x,y)

    def acceptPacket(self):
        # TODO some local computation maybe to update the variable reward
        pass 

    def getReward(self):
        ## TODO based on ttl of the packet
        return self.reward

    def getPosition(self):
        return self.position

    def isUAV(self):
        return False
    
    def isBase(self):
        return True
     
    def isIot(self):
        return False
    