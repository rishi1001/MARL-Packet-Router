"""
Script containing the training and testing loop for DQNAgent
"""

import os
import argparse
import numpy as np
import pickle
from tqdm import tqdm
import time
import matplotlib.pyplot as plt

import torch
from src.Map import Map

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)
from configparser import ConfigParser
  

folder_name = input('Enter folder name : ')

configur = ConfigParser()
print (configur.read('config.ini'))


num_memory_fill_eps = int(configur.get('train_model','num_memory_fill_eps'))
tot_episodes = int(configur.get('train_model','tot_episodes'))
tot_time = int(configur.get('train_model','tot_time'))
update_frequency = int(configur.get('train_model','update_frequency'))
save_frequency = int(configur.get('train_model','save_frequency'))
generate_packets_till = int(configur.get('test_model','generate_packets_till'))

n = int(configur.get('map','n'))
m = int(configur.get('map','m'))
p = float(configur.get('map','p'))

# map
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
            for agent in Agents:
                agent.randomRun()

            for node in IotNodes:
                node.run()
                        

def train(foldername,graphics=False):
    
    step_cnt = 0

    for episode in tqdm(range(tot_episodes), position=0, leave=True):

        # if graphics:
            # print("Episode Number : ", episode)

        if step_cnt % update_frequency == 0 and step_cnt!=0:
            for agent in Agents:                    # update the target net after update_frequency steps   
                agent.dqn_object.updateTargetNet()

        for time in range(tot_time):
            ##TODO agent order affects current state reason : agent x->y and y->z can transmit same packet in single timestamp(if order is x,y,z)
            for agent in Agents:
                agent.run()


            for node in IotNodes:
                node.run()

            if graphics and episode == tot_episodes-1 :
                map_.renderMap()
            
        
        step_cnt += 1
        # print("Episode Num : ", episode)
        for agent in Agents:
            agent.dqn_object.updateEpsilon()
            agent.saveLoss()
            # print("Loss :", agent.latest_loss) 

        map_.resetAll()             # make queues empty for agents, Recv Packets for BS = 0
        

        if(episode% save_frequency == 0):
            for agent in Agents:
                agent.dqn_object.saveModel('./{}/agent_at_{}'.format(foldername,agent.getPosition()))
#                agent.dqn_object.saveModel('dqn-model')




def test(render=True):
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
    
    # no need to load model here as train was previously called. so last updated model is the model to be used

    # turn off exploration for agents now
    for agent in Agents:
            agent.dqn_object.turn_off_exploration()

    step_cnt = 0

    while True:
        step_cnt += 1

        for agent in Agents:
            agent.run(False)

        if step_cnt <= generate_packets_till:
            for node in IotNodes:
                node.run()

        if render :
            map_.renderMap()

        # check if all iot and uavs have sent out all packets
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
            return 


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



        

if __name__ ==  '__main__':

        
        os.makedirs("{}/model_parameters".format(folder_name), exist_ok=True)
        map_.initModels(device)
        # fillMemory()
        # train("model_parameters",False)
        if configur.get('train_model','train') == 'True':
            fillMemory()
            train("{}/model_parameters".format(folder_name),False)
        map_.loadModel("{}/model_parameters".format(folder_name))
        test()
        generatePlot(folder_name)
        
        print('Mean ttl of all packets received by base station: ',meanTtl())
        

    # else:
    #         dqn_agent.load_model('{}/dqn_model'.format(args.results_folder))

    #         test(env=env, dqn_agent=dqn_agent, num_test_eps=args.num_test_eps, seed=seed, results_basepath=args.results_folder, render=args.render)

