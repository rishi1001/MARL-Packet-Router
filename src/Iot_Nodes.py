import sys
sys.path.append(".")
from Packets import packet

## def_ttl initial value of ttl
class Iot_Nodes():

    def __init__(self,rate,def_ttl):
        self.rate=rate
        self.def_ttl=def_ttl
    
    def generate_packet(self):
        l=[]
        for i in range(self.rate):
            l.append(packet(self.def_ttl))
        return l
    
    
    def find_neighbour(self):
        pass
        # TODO
        ## doubt?? 

    def isUAV(self):
        return false