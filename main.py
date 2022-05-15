"""
Script containing the training and testing loop for DQNAgent
"""

import os
import argparse
import numpy as np
import pickle
from tqdm import tqdm
import time

import torch
from src.Map import Map
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

from configparser import ConfigParser
  
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
map_.generate()
#grid_map = map_.generate()

## Initially
# grid_map = map_.dummyMap() 

#global variables
IotNodes = map_.getIotNodes()
BaseStation_obj = map_.getBaseStation()
Agents = map_.getAgents()


def fillMemory():
    for agent in Agents:
        agent.initDQN(device)

    for _ in range(num_memory_fill_eps):
        
        for time in range(tot_time):
            for agent in Agents:
                agent.randomRun()

            for node in IotNodes:
                node.run()
                        

def train(foldername,graphics=False):
    
    step_cnt = 0

    for episode in tqdm(range(tot_episodes)):

        # if graphics:
            # print("Episode Number : ", episode)

        if step_cnt % update_frequency == 0 and step_cnt!=0:
            for agent in Agents:                    # update the target net after update_frequency steps   
                agent.dqn_object.update_target_net()

        for time in range(tot_time):
            ##TODO agent order affects current state reason : agent x->y and y->z can transmit same packet in single timestamp(if order is x,y,z)
            for agent in Agents:
                agent.run()


            for node in IotNodes:
                node.run()

            if graphics and episode == tot_episodes-1 :
                map_.renderMap()
            
        
        step_cnt += 1
        
        for agent in Agents:
            agent.dqn_object.updateEpsilon()
            agent.saveLoss()
        

        if(episode% save_frequency == 0):
            for agent in Agents:
                agent.dqn_object.saveModel('./{}/dqn_model/agent_at_{}'.format(foldername,agent.getPosition()))
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
    return sum([packet.get_ttl() for packet in packets])/len(packets)

        

if __name__ ==  '__main__':


        os.makedirs("model_parameters", exist_ok=True)
        fillMemory()
        train("model_parameters",False)
        test()
        print('Mean ttl of all packets received by base station: {meanTtl()}')
    # else:
    #         dqn_agent.load_model('{}/dqn_model'.format(args.results_folder))

    #         test(env=env, dqn_agent=dqn_agent, num_test_eps=args.num_test_eps, seed=seed, results_basepath=args.results_folder, render=args.render)

