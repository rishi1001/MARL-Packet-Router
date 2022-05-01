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
BaseStation = []
UAVs=[]


def read_map(map_name):
    map = open(map_name, 'r')

def train():
    for episode in range(tot_episodes):
        for time in range(tot_time):




def test():
    pass

if __name__ == "__main__":
    print("started")
    train()
    test()
