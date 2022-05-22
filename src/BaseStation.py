from .Packets import packet

from configparser import ConfigParser
  
configur = ConfigParser()
import builtins
configur.read(builtins.current_filename)

#configur.read('config.ini')
scale_base_reward = int(configur.get('reward','scale_base_reward'))

class BaseStation():

    def __init__(self, x, y):
        self.position = (x,y)
        self.packetRecv = 0
        self.packets_received = []


    def acceptPacket(self, packet):
        self.packetRecv += 1
        self.packets_received.append(packet)

    def getReward(self):
        ttl = self.packets_received[-1].get_ttl()
        return scale_base_reward*ttl*ttl

    def getPosition(self):
        return self.position

    def isUAV(self):
        return False
    
    def isBase(self):
        return True
     
    def isIot(self):
        return False

    def getVal(self):
        return self.packetRecv

    def reset(self):
        """
        reset everything in the agent to turn on test mode
        """
        self.packetRecv = 0
        self.packets_received = []

    