"""
Script containing the training and testing loop for DQNAgent
"""

import os
import sys
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)
from configparser import ConfigParser

torch.cuda.empty_cache()
if(len(sys.argv) <= 1):
    print("Please provide the config file folder name")
    exit()


folder_name = sys.argv[1]

import builtins
builtins.current_filename = "{}/config.ini".format(folder_name)
configur = ConfigParser()
configur.read(builtins.current_filename)


num_memory_fill_eps = int(configur.get('train_model','num_memory_fill_eps'))
tot_episodes = int(configur.get('train_model','tot_episodes'))
tot_time = int(configur.get('train_model','tot_time'))
update_frequency = int(configur.get('train_model','update_frequency'))
save_frequency = int(configur.get('train_model','save_frequency'))
generate_packets_till = int(configur.get('test_model','generate_packets_till'))
gap_time= int(configur.get('train_model','gap_time'))

n = int(configur.get('map','n'))
m = int(configur.get('map','m'))
p = float(configur.get('map','p'))

# map
from src.Map import Map
map_ = Map(n,m,p)
# map_.generate()
#grid_map = map_.generate()

## Initially
#grid_map = map_.dummyMap()
map_.read()


#global variables
IotNodes = map_.getIotNodes()
BaseStation_obj = map_.getBaseStation()
Agents = map_.getAgents()


def fillMemory():

    for _ in range(num_memory_fill_eps):

        for time in range(tot_time):

            if(time%gap_time==0):
                for node in IotNodes:
                    node.run()

            for agent in Agents:
                agent.randomRun()

            for agent in Agents:
                agent.update_state()

        map_.resetAll()             # make queues empty for agents, Recv Packets for BS = 0


def train(foldername,graphics=False):

    step_cnt = 0

    for episode in tqdm(range(tot_episodes), position=0, leave=True):

        # if graphics:
            # print("Episode Number : ", episode)

        if step_cnt % update_frequency == 0 and step_cnt!=0:
            for agent in Agents:                    # update the target net after update_frequency steps
                agent.dqn_object.updateTargetNet()

        for time in range(tot_time):

            if(time%gap_time==0):
                for node in IotNodes:
                    node.run()

            ##TODO agent order affects current state reason : agent x->y and y->z can transmit same packet in single timestamp(if order is x,y,z)
            for agent in Agents:
                agent.run()

            for agent in Agents:
                agent.update_state()

            if graphics and episode == tot_episodes-1 :
                map_.renderMap()


        step_cnt += 1
        # print("Episode Num : ", episode)
        for agent in Agents:
            agent.dqn_object.updateEpsilon()
            agent.saveLoss()
            # print("Loss :", agent.latest_loss)
        print("Episode Number:",episode,"Packet reached:",BaseStation_obj.packetRecv)
        # print("Packet reached:",BaseStation_obj.packetRecv)
        map_.resetAll()             # make queues empty for agents, Recv Packets for BS = 0


        if(episode% save_frequency == 0):
            for agent in Agents:
                agent.dqn_object.saveModel('./{}/agent_at_{}'.format(foldername,agent.getPosition()))
#                agent.dqn_object.saveModel('dqn-model')




def test(folder_name,render=True):
    """
    Function to test the agent

    Parameters
    ---
    render: bool
        Whether to create a pop-up window display the interaction of the agent with the environment

    Returns
    ---
    none

    idea: generate packets at iot till some time step
    stop the simulation only when each packet is either dropped or reaches the base station
    metrics: average ttl over all the packets? (indicates both latency and throughout in some sense)

    #TODO can also calculate latency only on packets that reached the base station and throughput overall
    """

    # reset all agents
    map_.resetAll()
    BaseStation_obj.reset()
    # no need to load model here as train was previously called. so last updated model is the model to be used

    # turn off exploration for agents now
    for agent in Agents:
            agent.dqn_object.turn_off_exploration()

    step_cnt = 0
    num_packets=[]
    total_ttl=[]
    time=[]
    t=0
    while True:

        if(t%gap_time==0):
            step_cnt += 1
            if step_cnt <= generate_packets_till:
                for node in IotNodes:
                    node.run()

        for agent in Agents:
            agent.run(False)

        for agent in Agents:
            agent.update_state()

        if render :
            map_.renderMap()

        # check if all iot and uavs have sent out all packets
        num_packets.append(BaseStation_obj.packetRecv)
        total_ttl.append(BaseStation_obj.totalTtl)
        time.append(t)
        t+=1
        end = True
        for agent in Agents:
            if agent.getVal() != 0:
                end = False
                break

        for iot in IotNodes:
            if iot.getQueueSize() !=0:
                end = False
                break

        if end:
            break
    os.makedirs("{}/Plots".format(folder_name), exist_ok=True)
    plt.plot(time,num_packets , color ='blue', label ='Packets Received')
    plt.savefig('{}/Plots/Packet_Received.png'.format(folder_name))
    plt.close()

    plt.plot(time,total_ttl , color ='blue', label ='Sum of TTL')
    plt.savefig('{}/Plots/SumOfTtl.png'.format(folder_name))
    plt.close()


def meanTtl():
    packets = map_.getBaseStation().packets_received
    if len(packets)==0:
        return -1
    return sum([packet.get_ttl() for packet in packets])/len(packets)

def generatePlot(folder_name):
    os.makedirs("{}/Plots".format(folder_name), exist_ok=True)
    for agent in Agents:
        loss = agent.getLoss()
        epi_list = list(range(1,len(loss)+1))
        plt.plot(epi_list, loss, color ='orange', label ='Agent Loss')
        plt.savefig('{}/Plots/agent_at_{}.png'.format(folder_name,agent.getPosition()))
        plt.close()




if __name__ ==  '__main__':


        os.makedirs("{}/model_parameters".format(folder_name), exist_ok=True)
        map_.initModels(device)
        # fillMemory()
        # train("model_parameters",False)
        if configur.get('train_model','train') == 'True':
            fillMemory()
            train("{}/model_parameters".format(folder_name),False)
        map_.loadModel("{}/model_parameters".format(folder_name))
        test(folder_name)
        generatePlot(folder_name)

        print('Mean ttl of all packets received by base station: ',meanTtl())

