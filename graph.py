import numpy as np
import networkx as nx
import collections


# seed = np.random.seed(120)

class Graph:
    def __init__(self, graph_type, cur_n):

        if graph_type =='cycle_graph':
            self.g = nx.cycle_graph(n=cur_n)

        # power=0.75
        #
        # self.edgedistdict = collections.defaultdict(int)
        # self.nodedistdict = collections.defaultdict(int)
        #
        # for edge in self.g.edges:
        #     self.edgedistdict[tuple(edge[0],edge[1])] = 1.0/float(len(self.g.edges))
        #
        # for node in self.g.nodes:
        #     self.nodedistdict[node]=float(len(nx.neighbors(self.g,node)))**power/float(len(self.g.edges))


    def nodes(self):

        return nx.number_of_nodes(self.g)

    def edges(self):

        return self.g.edges()

    def neighbors(self, node):

        return nx.all_neighbors(self.g,node)

    def average_neighbor_degree(self, node):

        return nx.average_neighbor_degree(self.g, nodes=node)

    def adj(self):

        return nx.adjacency_matrix(self.g)
    
    def bonding_capital(self, root, alpha=0.85):
        avg = 0
        personalization = {i: 0 for i in self.g.nodes()}
        personalization[root] = 1
        pr = np.array(list(nx.pagerank(self.g, alpha, max_iter=200, personalization=personalization).values()))
        neighbors_nodes = [n for n in self.g.neighbors(root)]
        for i in range(0, len(neighbors_nodes)):
            avg += pr[(list(self.g.nodes()).index(neighbors_nodes[i]))]
        return avg
    
    def bridging_capital(self):
        return nx.betweenness_centrality(self.g)
    
    def two_hop_neighbors(self, node):
        ego = []
        ego_2 = []

        for n in nx.all_neighbors(self.g, node):
            ego.append(n)
        print (ego)
        for n in nx.generators.ego.ego_graph(self.g, node, 2):
            ego_2.append(n)
        print (ego_2)
        if (len(set(ego))>=len(set(ego_2))):
            two_hop_neigh = list(set(ego).difference(set(ego_2)))
        else:
            two_hop_neigh = list(set(ego_2).difference(set(ego)))
        print (two_hop_neigh)
        return two_hop_neigh
    
    def add_edge(self, graph, node_x, node_y):
    
        return graph.add_edge(node_x,node_y)
    
    def two_level_ego_network(self, node):
        return nx.generators.ego.ego_graph(self.g, node, 2)