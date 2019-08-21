import numpy as np
import torch
import pulp
import graph 
import runner
import networkx as nx

"""
This file contains the definition of the environment
in which the agents are run.
"""


class Environment:
    def __init__(self,graph,pre_rewards):
        self.graph = graph
        self.pre_rewards = pre_rewards

    def reset(self):
        self.graph_init = self.graph
        self.nodes = self.graph_init.nodes()
        #print (self.nodes)
        self.nbr_of_nodes = 0
        self.edge_add_old = 0
        self.last_reward = 0
        self.observation = torch.zeros(1,self.nodes,1,dtype=torch.float)

    def observe(self, node):
        """Returns the current observation that the agent can make
                 of the environment, if applicable.
        """
        ego = []
        ego_2 = []

        for n in nx.all_neighbors(self.graph, node):
            ego.append(n)
        print (ego)
        for n in nx.generators.ego.ego_graph(self.graph, node, 2):
            ego_2.append(n)
        print (ego_2)
        
        return ego_2
        #return self.observation

    def act(self,node, preferences):
        
        #self.observation[:,node,:]=1
        reward = self.get_reward(self.observation, preferences, node)
        return reward

    def get_reward(self, observation, preferences, node):
        # utilities before
        bridging_capital = self.graph.bridging_capital()
        #print ("****************** ",self.graph.bonding_capital(node))
        
        utility_after_acting = preferences[node] * self.graph.bonding_capital(node) + \
                           (1 - preferences[node]) * bridging_capital[node]
        after_rewards = utility_after_acting - self.pre_rewards[node]

        return after_rewards

    def update(self, actions):
        for i in range(0,100):
            self.graph.add_edge(i, actions[i])