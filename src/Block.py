from torch import true_divide


class Block():
    def __init__(self,position):
        self.position= position
    
    def isUAV(self):
        return False
    
    def isBase(self):
        return False
     
    def isIot(self):
        return False

    def isBlock(self):
        return True

    def isBaseStation(self):
        return False
    
    def reset(self):
        pass