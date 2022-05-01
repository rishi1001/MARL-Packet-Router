from sklearn import neighbors
from src.Agent import Agent
from src.DDQN.Agent import DQN
from src.BaseStation import BaseStation
from src.Iot_Nodes import Iot_Nodes
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
Iot_Nodes = map_.getIotNodes()
BaseStation_obj = map_.getBaseStation()
Agents =map_.getAgents()


def read_map():
    pass


def train():
    for episode in range(tot_episodes):
        for time in range(tot_time):
            
            for agent in Agents:
                top_packet = agent.popQueue()
                top_packet.decrease_ttl()         # ttl of packet decreases

                # TODO: check for 0 ttl ??
                nextAgent = agent.nextAgent()
                nextAgent.pushQueue(top_packet)
                agent.trainAgent(BaseStation_obj.get_reward())

                top_packet.addToPath(nextAgent.getPosition())   # adding the agent to packet path
                

            for node in Iot_Nodes:
                node.generate_packet()
            for node in Iot_Nodes:
                agent = node.find_neighbour()
                for packet in node.packetQueue:
                    agent.pushQueue(packet)
                    packet.addToPath(agent.getPosition())  # adding the agent to packet path
            




def test():
    pass

if __name__ == "__main__":
    print("started")
    train()
    test()
