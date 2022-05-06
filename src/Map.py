#import imp
#from pkgutil import ImpImporter
import random
from Agent import Agent
from IotNodes import IotNodes
from BaseStation import BaseStation

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
        self.BaseStation = 0

    def generate(self):
        map_=[['-' for i in range(self.m)] for j in range(self.n)]
        x=random.randint(0,self.n-1)
        y=random.randint(0,self.m-1)
        map_[x][y]= BaseStation()
        self.BaseStation = map_[x][y]
        for i in range(self.n):
            for j in range(self.m):
                if i==x and j==y:
                    continue
                x=random.uniform(0,1)
                if(x<=self.p):
                    agent  = Agent([], i, j)
                    map_[i][j]= agent
                    self.agents.append(agent)
                else:
                    iot = IotNodes(rate, def_ttl,i,j) # TODO: add actual rate and def_ttl here
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
