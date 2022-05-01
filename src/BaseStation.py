class BaseStation():

    def __init__(self, x, y):
        reward = 0
        self.position = (x,y)

    def accept_packet(self):
        # some local computation maybe to update the variable reward
        pass 

    def get_reward(self):
        ## based on ttl of the packet
        return self.reward

    def getPosition(self):
        return self.position

