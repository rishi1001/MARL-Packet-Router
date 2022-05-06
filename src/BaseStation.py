from src.Packets import packet


class BaseStation():

    def __init__(self, x, y):
        reward = 0
        self.position = (x,y)
        self.packetRecv = 0


    def acceptPacket(self):
        # TODO some local computation maybe to update the variable reward
        self.packetRecv += 1

    def getReward(self):
        ## TODO based on ttl of the packet
        return self.reward

    def getPosition(self):
        return self.position

    def isUAV(self):
        return False
    
    def isBaseStation(self):
        return True

    def getVal(self):
        return self.packetRecv
    