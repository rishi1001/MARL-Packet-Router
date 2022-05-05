#from sklearn import neighbors
from src.Agent import Agent
from src.DDQN.Agent import DQN
from src.BaseStation import BaseStation
from IotNodes import IotNodes
from src.Packets import packet
from src.Map import Map


# add these in constraints
tot_episodes = 5
tot_time = 100
n = 50
m = 50
p = 0.8

# map
map_ = Map(n,m,p)
grid_map = map_.generate()

#global variables
IotNodes = map_.getIotNodes()
BaseStation_obj = map_.getBaseStation()
Agents =map_.getAgents()


def read_map(map_name):
    map = open(map_name, 'r')

def fillMemory():
    pass

def train():

    step_cnt = 0

    for episode in range(tot_episodes):

        for time in range(tot_time):
            ##TODO agent order affects current state
            for agent in Agents:
                agent.run()

                if step_cnt % update_frequency == 0:
                    agent.dqn_agent.update_target_net()


            for node in IotNodes:
                node.run()
        
        step_cnt += 1
        
        for agent in Agents:
            agent.dqn_agent.updateEpsilon()


def test():
    pass

if __name__ == "__main__":
    print("started")
    train()
    test()
