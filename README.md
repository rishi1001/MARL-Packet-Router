# MARL Packet Router

## Overview
UAVs, or Unmanned Aerial Vehicles have been increasingly put to use to collect and distribute data among IoT Nodes distributed spatially, especially in remote areas with little to no network access. One particular use case is the deployment of UAVs to collect data from a particular group of nodes and deliver it to a central aggregator. Two major bottlenecks can be identified in this paradigm, as compared to the direct transmission counterpart:

1. Time taken for UAV to travel in space is significantly higher than average data transmission times
2. UAVs are resource constrained devices and can only travel a bounded distance before needing another recharge

Thus, effective UAV path planning and inter UAV packet routing algorithms play a crucial role in the performance of the system. This project focuses on UAV packet routing. In essence, we implemented a MARL (Multi-Agent Reinforcement Learning) technique to route packets among UAVs. The setup is summarised in the next section. 

## Setup
We call the nodes generating data IoT nodes, which are relayed by the UAVs to the aggregator, which is referred to as the Base Station. The map is a grid of size nxm, in which each cell of the grid is occupied by either IoT Nodes, UAVs, or the Base Station (unique). It is assumed that the UAVs are fixed in space, and can only participate in packet routing, i.e transmission of data to other UAVs. The figure below illustrates a 3x3 grid.

<img src="/images/grid_example.png" alt="Map Example" width="400"/>

The data is represented in the form of packets, which are of fixed size. IoT Nodes generate these packets with different rates. Further, a UAV can only transfer a data packet to its neighbours. A is said to be a neigbour of B if it is one hop away from B. Each UAV has a queue of fixed length to store the packets. In each time unit, a UAV can only send out one packet to its neighbour, which would be at the head of the queue (FIFO policy).

## Requirements
The project requires the following packages to be installed:

- matplotlib==3.5.2
- numpy==1.22.3
- tensorflow==2.9.1
- torch==1.11.0
- tqdm==4.64.0

## How to run
The project can be easily setup by using the included MakeFile. The steps below need to be followed:

1. <code> sudo apt install python3-virtualenv </code> , For MAC - <code> pip3 install virtualenv </code>
2. <code> virtualenv environment_name </code>
3. <code> source env/bin/activate </code>
4. <code> make setup </code>
5. <code> make run </code>
 
Now the project is ready to run. To run, follow the steps below:
1. Create a folder in which the results are to be received
2. Add a <code>config.ini</code> file to the folder (details listed below)
3. <code> make run folder = folder_name </code>
4. A progress bar would indicate the progress of the training. Once the execution is completed, the results can be viewed in the results folder created earlier

### About config.ini:
This is the configuration file through which parameters in the project can be configured. It should contain sections: map, train_model, test_model, packet, reward, scaling_factor. A default config file is included in the root directory, which can be editted and added to the results folder. A brief descripiton of the parameters is given below:

map
- **n**: number of rows in the grid
- **m**: number of columns in the grid
- **p**: In case of a random map, probability that a cell would have a UAV (It would have an IoT node with prob. 1-p)

train_model
- **train**: boolean value indicating if the model is to be trained in the next run
- **num_memory_fill_eps**: number of episodes for which to run the code to fill replay memory of DQNs before actual training starts
- **tot_epsiodes**: Total number of episodes to train the DQNs
- **tot_time**: Total time elapsed in each episode
- **update_frequency**: Number of episodes after which to udpdate the target network of agents

test_model
- **num_test_eps**: Total number of episodes to test the model
- **generate_packets_till**: Number of episodes till which IoT Nodes will generate packets

packet
- **def_ttl**: initial ttl of each packet

reward
- **agent_to_agent_scale**: Scaling factor in the reward awarded by one agent to the other while receiving packet
- **scale_base_reward**: Scaling factor in reward provided by Base Station when a packet is delivered
- **ttl_zero_reward**: Reward awarded to agent in case a packet's ttl reduces to zero
- **packet_drop_reward**: Reward awarded to agent for dropping a packet
- **include_distance**: Boolean value indicating if the manhattan distance of the recipient UAV should be considered while computing reward for the forwarding UAV while forwarding a packet

scaling factor
- **type**: Scaling factor in reward based on ttl of packets given to UAVs

While running the code, a map is to be provided. A custom map can be provided to the program, or a map can be randomly spawned. To randomly spawn a map, the n and m parameters are to be provided in the config file. A single Base Station is added to one location at random. Each other location of the map is assigned either a UAV (with probability p) or an IoT Node (with probability 1-p).
A custom map can also be provided. We have added 5 maps in the /Maps directory, for 1x3, 1x4, 1x5, 2x2, 2x4 and 3x3 map sizes. The process of creating is custome map is given below.

### Creating a custom Map
To create a map of size nxm, create a file and name it map_n_m.txt. There need to be n lines in the file, each corresponding to a row in the map. Each line would have m space separated characters. Each charater is either of a B, I, or A. A 'B' in the 3rd line, as the 4th character indicates the base station is at position (2,3), assuming 0-based indexing. Similarly A denotes an agent (UAV) and I and IoT Node.

## References
The code is inspired from [this](https://github.com/saashanair/rl-series) repository.
