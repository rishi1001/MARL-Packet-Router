#import imp
#from pkgutil import ImpImporter
import random
from Agent import Agent
from IotNodes import IotNodes
from BaseStation import BaseStation

from configparser import ConfigParser
  
configur = ConfigParser()
configur.read('config.ini')

defTtl = int(configur.get('packet','def_ttl'))
# generate map of size n*m 
## p is probability of getting a UAV at particular cell
class Map():

    def __init__(self,n,m,p):
        self.n=n
        self.m=m
        self.p=p
        self.map = []
        self.agents = []
        self.Iot_Nodes = []
        self.BaseStation = None

    def generate(self):
        map_=[['-' for i in range(self.m)] for j in range(self.n)]
        x=random.randint(0,self.n-1)
        y=random.randint(0,self.m-1)
        map_[x][y]= BaseStation(x,y)
        self.BaseStation = map_[x][y]
        for i in range(self.n):
            for j in range(self.m):
                if i==x and j==y:
                    continue
                x=random.uniform(0,1)
                if(x<=self.p):
                    agent  = Agent([], i, j, self.BaseStation)
                    map_[i][j]= agent
                    self.agents.append(agent)
                else:
                    rate=  random.randint(0,10) # TODO: add actual rate
                    iot = IotNodes(rate, defTtl,i,j) 
                    map_[i][j]= iot
                    self.Iot_Nodes.append(iot)  

        # populate neightbours for each agent
        for i in range(self.n):
            for j in range(self.m):
                if i==x and j==y:
                    continue
                # if map_[i,j].isUAV: # commenting this because IoT nodes also need neighbours
                if i>0 and map_[i-1, j].isUAV() or map_[i-1, j].isBase():
                    map_[i,j].addNeighbour(map_[i-1, j])
                if j>0 and map_[i, j-1].isUAV() or map_[i, j-1].isBase():
                    map_[i,j].addNeighbour(map_[i, j-1])
                if i<self.n-1 and map_[i+1, j].isUAV() or map_[i+1, j].isBase():
                    map_[i,j].addNeighbour(map_[i+1, j])
                if j<self.m-1 and map_[i-1, j+1].isUAV() or map_[i-1, j+1].isBase():
                    map_[i,j].addNeighbour(map_[i, j+1])

        self.map = map_ 

    def getBaseStation(self):
        return self.BaseStation
    
    def getAgents(self):
        return self.Agents
     
    def getIotNodes(self):
        return self.Iot_Nodes
        

    def renderMap(self):
        for i in range(self.m):
            print('----',end="")
        print()
        for i in range(self.n):
            print('|',end="")
            for j in range(self.m):
                if self.map[i][j].isBaseStation():
                    print('|',end="")
                    print(self.map[i][j].getVal(),end="")
                    print('|',end="")
                else:
                    print(self.map[i][j].getVal(),end="")
                print('|',end="")
            print()
            for j in range(self.m):
                print('----',end="")
            print()
        print()
    def dummyMap(self):  ## 1*3 map
        map_= map_=[['-' for i in range(1)] for j in range(3)]
        map[0][0] = BaseStation(0,0)
        self.BaseStation = map_[0][0]

        agent  = Agent([], 0, 1, self.BaseStation)
        map_[0][1]= agent
        self.agents.append(agent)

        rate=  random.randint(0,10) # TODO: add actual rate
        iot = IotNodes(rate, defTtl,0,2) 
        map_[0][2]= iot
        self.Iot_Nodes.append(iot)  


        map[0][1].addNeighbour(map[0][0])
        map[0][2].addNeighbour(map[0][1])

        