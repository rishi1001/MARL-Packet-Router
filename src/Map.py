#import imp
#from pkgutil import ImpImporter

import random

from numpy import block
from .IotNodes import IotNodes
from .BaseStation import BaseStation
from .Agent import Agent
from .Block import Block
from configparser import ConfigParser
  
configur = ConfigParser()

import builtins
configur.read(builtins.current_filename)
print(builtins.current_filename)
#configur.read('config.ini')

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

    def read(self):
        file  = open('./Maps/'+configur.get('map','name'),'r') 
        map_=[['-' for i in range(self.m)] for j in range(self.n)]
        print("read ",file)
        i=0
        j=0
        initial_rate=10
        for line in file:
            j=0
            for char in line:
                if char==' ':
                    continue
                if char=='B':
                    map_[i][j]= BaseStation(i,j)
                    self.BaseStation = map_[i][j]
                elif char == 'A':
                    agent  = Agent([], i, j, self.BaseStation)
                    map_[i][j]= agent
                    self.agents.append(agent)
                elif char == 'I':
                    #rate=  random.randint(2,10) 
                    rate = initial_rate # with uniform random generation of packets, avergae will be 7 (<transmission rate)
                    #initial_rate += 1
                    iot = IotNodes(rate, defTtl,i,j)
                    map_[i][j]= iot
                    self.Iot_Nodes.append(iot)
                elif char=='X':
                    block= Block((i,j))
                    map_[i][j]=block
                j+=1
                if(j==self.m): break
            i+=1
        for i in range(self.n):
                for j in range(self.m):
                    if map_[i][j].isBase() or map_[i][j].isBlock():
                        continue
                    if(map_[i][j].isUAV()):
                        map_[i][j].targetBaseStation = self.BaseStation
                    # if map_[i,j].isUAV: # commenting this because IoT nodes also need neighbours
                    if i>0 and (map_[i-1][j].isUAV() or map_[i-1][j].isBase()):
                        map_[i][j].addNeighbour(map_[i-1][j])
                    if j>0 and (map_[i][j-1].isUAV() or map_[i][j-1].isBase()):
                        map_[i][j].addNeighbour(map_[i][j-1])
                    if i<self.n-1 and (map_[i+1][j].isUAV() or map_[i+1][j].isBase()):
                        map_[i][j].addNeighbour(map_[i+1][j])
                    if j<self.m-1 and (map_[i][j+1].isUAV() or map_[i][j+1].isBase()):
                        map_[i][j].addNeighbour(map_[i][j+1])

        self.map = map_ 

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
                prob=random.uniform(0,1)
                if(prob<=self.p):
                    agent  = Agent([], i, j, self.BaseStation)
                    map_[i][j]= agent
                    self.agents.append(agent)
                else:
                    # rate=  random.randint(0,10) # TODO: add actual rate
                    rate = 10 # with uniform random generation of packets, avergae will be 7 (<transmission rate)
                    iot = IotNodes(rate, defTtl,i,j) 
                    map_[i][j]= iot
                    self.Iot_Nodes.append(iot)  

        # populate neightbours for each agent
        for i in range(self.n):
            for j in range(self.m):
                if map_[i][j].isBase():
                    continue
                # if map_[i,j].isUAV: # commenting this because IoT nodes also need neighbours
                if i>0 and (map_[i-1][j].isUAV() or map_[i-1][j].isBase()):
                    map_[i][j].addNeighbour(map_[i-1][j])
                if j>0 and (map_[i][j-1].isUAV() or map_[i][j-1].isBase()):
                    map_[i][j].addNeighbour(map_[i][j-1])
                if i<self.n-1 and (map_[i+1][j].isUAV() or map_[i+1][j].isBase()):
                    map_[i][j].addNeighbour(map_[i+1][j])
                if j<self.m-1 and (map_[i][j+1].isUAV() or map_[i][j+1].isBase()):
                    map_[i][j].addNeighbour(map_[i][j+1])

        self.map = map_ 
        # print("map created of length: ", len(self.map))

    def getBaseStation(self):
        return self.BaseStation
    
    def getAgents(self):
        return self.agents
     
    def getIotNodes(self):
        return self.Iot_Nodes
        

    def renderMap(self):
        for i in range(self.m):
            print('----',end="")
        print()
        for i in range(self.n):
            print('|',end="")
            for j in range(self.m):
                if self.map[i][j].isBlock():
                    print(' |',end="")
                    print('X',end="")
                    print('| ',end="")
                elif self.map[i][j].isBase():
                    print(' |',end="")
                    print(self.map[i][j].getVal(),end="")
                    print('| ',end="")
                elif self.map[i][j].isIot():
                    print(' -',end="")
                    print(self.map[i][j].getVal(),end="")
                    print('- ',end="")
                else:
                    print('  ',end="")
                    print(self.map[i][j].getVal(),end="")
                    print('  ',end="")
                print('|',end="")
            print()
            for j in range(self.m):
                print('----',end="")
            print()
        print()


    def dummyMap(self):  ## 1*3 map
        map_= map_=[['-' for i in range(3)] for j in range(1)]
        map_[0][0] = BaseStation(0,0)
        self.BaseStation = map_[0][0]

        agent  = Agent([], 0, 1, self.BaseStation)
        map_[0][1]= agent
        self.agents.append(agent)

        #rate=  random.randint(0,10) # TODO: add actual rate
        rate = 10
        iot = IotNodes(rate, defTtl,0,2) 
        map_[0][2]= iot
        self.Iot_Nodes.append(iot)  


        map_[0][1].addNeighbour(map_[0][0])
        map_[0][2].addNeighbour(map_[0][1])
        self.map = map_ 

    def resetAll(self):
        for i in range(self.n):
            for j in range(self.m):
                self.map[i][j].reset()

    def loadModel(self,foldername):
        for i in range(self.n):
            for j in range(self.m):
                if(self.map[i][j].isUAV()):
                    self.map[i][j].loadModel("./{}/agent_at_{}".format(foldername,(i,j)))
   
    def initModels (self,device):
        for agent in self.agents:
            agent.initDQN(device)
