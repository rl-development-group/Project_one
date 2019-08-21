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
        self.graphs = graph
        self.pre_rewards = pre_rewards

    def reset(self):
        self.graph_init = self.graphs
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

        for n in nx.all_neighbors(self.graphs, node):
            ego.append(n)
        print (ego)
        for n in nx.generators.ego.ego_graph(self.graphs, node, 2):
            ego_2.append(n)
        print (ego_2)
        return ego_2
        #return self.observation

    def act(self,node, preferences):
        
        self.observation[:,node,:]=1
        reward = self.get_reward(self.observation, preferences, node)
        return reward

    def get_reward(self, observation, preferences, node):
        # utilities before
        bridging_capital = self.graphs.bridging_capital()
        #print ("****************** ",self.graphs.bonding_capital(node))
        utility_after_acting = {}  # rewards for all nodes after acting
        utility_before_acting = {}  # rewards for all nodes before acting
        rewards = {} # rewards after acting
        utility_before_acting[node] = preferences[node] * self.graphs.bonding_capital(node) + \
                            (1 - preferences[node]) * bridging_capital[node]
        
        utility_after_acting[node] = preferences[node] * self.graphs.bonding_capital(node) + \
                           (1 - preferences[node]) * bridging_capital[node]
        rewards[node] = utility_after_acting[node] - utility_before_acting[node]

        return (rewards[node])

    def update(self, node):
        two_hop_neigh = []
        
        two_hop_neigh = self.graphs.two_hop_neighbors(node)
        print(two_hop_neigh)
        
        #two_hop_neigh = two_hop_neigh.remove(node)
        print (two_hop_neigh)
        for i in two_hop_neigh:
            if node != i:
                print("node: ",node)
                print("i: ",i)
                self.graphs.add_edge(node,i)
        
        return self.graphs