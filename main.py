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
                        

def train(foldername,graphics=False,):
    
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
        

        if(episode% save_frequency == 0):
            for agent in Agents:
                agent.dqn_object.saveModel('./{}/dqn_model/agent_at_{}'.format(foldername,agent.getPosition()))
#                agent.dqn_object.saveModel('dqn-model')




def test(env, dqn_agent, num_test_eps, seed, results_basepath, render=True):
    """
    Function to test the agent

    Parameters
    ---
    env: gym.Env
        Instance of the environment used for training
    dqn_agent: DQNAgent
        Agent to be trained
    num_test_eps: int
        Number of episodes of testing to be performed
    seed: int
        Value of the seed used for testing
    results_basepath: str
        Location where models and other result files are saved
    render: bool
        Whether to create a pop-up window display the interaction of the agent with the environment

    Returns
    ---
    none
    """

    step_cnt = 0
    reward_history = []

    for ep in range(num_test_eps):
        score = 0
        done = False
        state = env.reset()
        while not done:

            if render:
                env.render()

            action = dqn_agent.select_action(state)
            next_state, reward, done, _ = env.step(action)

            score += reward
            state = next_state
            step_cnt += 1

        reward_history.append(score)
        print('Ep: {}, Score: {}'.format(ep, score))

    with open('{}/test_reward_history_{}.pkl'.format(results_basepath, seed), 'wb') as f:
        pickle.dump(reward_history, f)
        

if __name__ ==  '__main__':


        os.makedirs("model_parameters", exist_ok=True)
        fillMemory()
        train("model_parameters",False)
    # else:
    #         dqn_agent.load_model('{}/dqn_model'.format(args.results_folder))

    #         test(env=env, dqn_agent=dqn_agent, num_test_eps=args.num_test_eps, seed=seed, results_basepath=args.results_folder, render=args.render)

