from sklearn import neighbors
from src.Agent import Agent
from src.DDQN.Agent import DQN
from src.BaseStation import BaseStation
from src.Iot_Nodes import Iot_Nodes
from src.Packets import packet


# add these in constraints
tot_episodes = 5
tot_time = 100


#global variables
IOT_Nodes = []
BaseStation_obj = BaseStation()
Agents = []



def read_map():
    pass


def train():
    for episode in range(tot_episodes):
        for time in range(tot_time):
            
            for agent in Agents:
                top_packet = agent.popQueue()
                nextAgent = agent.nextAgent()
                nextAgent.pushQueue(top_packet)
                agent.trainAgent(BaseStation_obj.get_reward())

            for node in Iot_Nodes:
                node.generate_packet()
            for node in Iot_Nodes:
                agent = node.find_neighbour()
                for packet in node.packetQueue:
                    agent.pushQueue(packet)
            




def test():
    pass

if __name__ == "__main__":
    print("started")
    train()
    test()
