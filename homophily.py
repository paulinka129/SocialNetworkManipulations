from __future__ import division
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import graphviz
from consts import Consts
import utils
import random
from random import choice

class Homophily:

    class0 = '0'
    class1 = '1'

    def __init__(self, filename):
        self.G = self.load_graph(filename)
        self.remove_nodes_without_edges()
        self.size = self.nodes_count()
        self.global_homophilies  = []

    def add_random(self, count, clas):
        self.global_homophilies  = []
        homo_list_before = self.local_homophily()
        utils.save_to_file(homo_list_before, 'add_random_homo_list_before')
        nodes_with_clas = [node for node in self.G.nodes() if self.get_node_class(node) == clas]
        for i in range(len(nodes_with_clas)):
            random_node = choice(list(self.G.nodes()))
            self.add_node(random_node, i, clas)
            self.global_homophily()
        homo_list_after = self.local_homophily()
        utils.save_to_file(homo_list_after, 'add_random_homo_list_after')
        utils.save_to_file(self.global_homophilies, 'add_random_global_homophilies')
        utils.plot_local_homophily(homo_list_before, homo_list_after, 'add_random')


    def add_with_probability(self, count, clas):
        self.global_homophilies  = []
        probabilities = self.get_graph_probabilities()
        homo_list_before = self.local_homophily()
        utils.save_to_file(homo_list_before, 'add_with_probability_homo_list_before')
        nodes_with_clas = [node for node in self.G.nodes() if self.get_node_class(node) == clas]
        for i in range(len(nodes_with_clas)):
            node = self.pick_with_probability(self.G.nodes(), probabilities)
            self.add_node(node, i, clas)
            self.global_homophily()
        homo_list_after = self.local_homophily()
        utils.save_to_file(homo_list_after, 'add_with_probability_homo_list_after')
        utils.save_to_file(self.global_homophilies, 'add_with_probability_global_homophilies')
        utils.plot_local_homophily(homo_list_before, homo_list_after, 'add_with_probability')
        utils.plot_global_homophily(self.global_homophilies, 'add_with_probability')

    def add_by_ranking(self, count, clas):
        self.global_homophilies  = []
        sorted_by_degree = sorted(self.G.degree, key=lambda x: x[1], reverse=True)
        homo_list_before = self.local_homophily()
        utils.save_to_file(homo_list_before, 'add_by_ranking_list_before')
        nodes_with_clas = [node for node in self.G.nodes() if self.get_node_class(node) == clas]
        for i in range(len(nodes_with_clas)):
            node = sorted_by_degree[i][0]
            self.add_node(node, i, clas)
            self.global_homophily()
        homo_list_after = self.local_homophily()
        utils.save_to_file(homo_list_after, 'add_by_ranking_homo_list_after')
        utils.save_to_file(self.global_homophilies, 'add_by_ranking_global_homophilies')
        utils.plot_local_homophily(homo_list_before, homo_list_after, 'add_by_ranking')
        utils.plot_global_homophily(self.global_homophilies, 'add_by_ranking')

    def remove_random(self, count, clas):
        self.global_homophilies  = []
        homo_list_before = self.local_homophily()
        nodes_with_clas = [node for node in self.G.nodes() if self.get_node_class(node) == clas]
        utils.save_to_file(homo_list_before, 'remove_random_homo_list_before')
        for _ in range(count-1):
            random_node = choice(nodes_with_clas)
            try:
                self.G.remove_node(random_node)
                self.global_homophily()
            except nx.NetworkXError:
                print 'node does not exist in graph'
            
        homo_list_after = self.local_homophily()
        utils.save_to_file(homo_list_after, 'remove_random_homo_list_after')
        utils.save_to_file(self.global_homophilies, 'remove_random_global_homophilies')
        utils.plot_local_homophily(homo_list_before, homo_list_after, 'remove_random')
        utils.plot_global_homophily(self.global_homophilies, 'remove_random')


    def remove_with_probability(self, count, clas):
        self.global_homophilies  = []
        nodes_with_clas = [node for node in self.G.nodes() if self.get_node_class(node) == clas]
        probabilities = self.get_probabilities(nodes_with_clas)
        homo_list_before = self.local_homophily()
        utils.save_to_file(homo_list_before, 'remove_with_probability_homo_list_before')
        for _ in range(count-1):
            node = self.pick_with_probability(nodes_with_clas, probabilities)
            try:
                self.G.remove_node(node)
                self.global_homophily()
            except nx.NetworkXError:
                print 'node does not exist in graph'          
        homo_list_after = self.local_homophily()
        utils.save_to_file(homo_list_after, 'remove_with_probability_homo_list_after')
        utils.save_to_file(self.global_homophilies, 'remove_with_probability_global_homophilies')        
        utils.plot_local_homophily(homo_list_before, homo_list_after, 'remove_with_probability')
        utils.plot_global_homophily(self.global_homophilies, 'remove_with_probability')


    def remove_by_ranking(self, count, clas):
        self.global_homophilies  = []
        sorted_by_degree = sorted(self.G.degree, key=lambda x: x[1], reverse=True)
        nodes_with_clas = [node for node in sorted_by_degree if self.get_node_class(node[0]) == clas]
        homo_list_before = self.local_homophily()
        utils.save_to_file(homo_list_before, 'remove_by_ranking_homo_list_before')
        for i in range(len(nodes_with_clas)):
            print i
            node = nodes_with_clas[i][0]
            try:
                self.G.remove_node(node)
                self.global_homophily()
            except nx.NetworkXError:
                print 'node does not exist in graph'
        homo_list_after = self.local_homophily()
        utils.save_to_file(homo_list_after, 'remove_by_ranking_homo_list_after')
        utils.save_to_file(self.global_homophilies, 'remove_by_ranking_global_homophilies')   
        utils.plot_local_homophily(homo_list_before, homo_list_after, 'remove_by_ranking')
        utils.plot_global_homophily(self.global_homophilies, 'remove_by_ranking')

    def load_graph(self, filename):
        G = nx.read_gml(filename)
        return G
    
    def print_classes(self):
        for node in self.G.nodes():
            print self.G.node[node]['value']

    def print_nodes_with_class(self, value):
        nodeWithClass = [n for n in self.G.nodes() if self.G.node[n]['value'] == value]
        for node in nodeWithClass:
            print "{0}, {1}".format(node, self.G.node[node]['value'])

    def remove_nodes_without_edges(self):
        outdeg = self.G.degree()
        to_remove = [n[0] for n in outdeg if n[1] < 1]
        self.G.remove_nodes_from(to_remove)

    def nodes_count(self):
        return len(self.G.nodes())

    def print_graph(self):
        nx.draw(self.G)
        plt.show()

    def get_node_class(self, node):
        return self.G.node[node]['value']

    def indicate(self, a, b):
        if a == b:
            return 1
        else:
            return 0

    def local_homophily(self):
        local_homo = []
        for node in self.G.nodes():
            homo = 0.0
            neighbors_count = len(list(self.G.neighbors(node)))
            for neighbor in self.G.neighbors(node):
                homo += (self.indicate(self.get_node_class(node), self.get_node_class(neighbor))/neighbors_count)
            local_homo.append(homo)
        return local_homo

    def global_homophily(self):
        global_homo = 0.0
        edges_count = len(list(self.G.edges()))
        for edge in self.G.edges():
            global_homo += (self.indicate(self.get_node_class(edge[0]), self.get_node_class(edge[1]))/edges_count)
        # for node in self.G.nodes():
        #     homo = 0.0
        #     n_count = ((self.nodes_count()+1)**2 - 1)//2
        #     for inner in self.G.nodes():
        #         if node != inner:
        #             homo = homo + (self.indicate(self.get_node_class(node), self.get_node_class(inner))/n_count)
        #     global_homo.append(homo)
        # return global_homo
        self.global_homophilies.append(global_homo)

    def add_random_node(self, index, clas): 
        self.G.add_node(index, value=clas)
        random_node = choice(list(self.G.nodes()))
        self.G.add_edge(index, random_node)

    def add_node(self, node, index, clas):
        self.G.add_node(index, value=clas)
        self.G.add_edge(index, node)

    def add_random_nodes(self, count, clas):
        utils.plot_homophily(self.local_homophily(), 'local_start' )
        for i in range(count):
            self.add_random_node(i, clas)
        utils.plot_homophily(self.local_homophily(), 'local_end')

    def remove_random_node(self):
        random_node = choice(list(self.G.nodes()))
        self.G.remove_node(random_node)

    def remove_random_nodes(self, count):
        utils.plot_homophily(self.local_homophily(), 'local_start_remove' )
        for _ in range(count):
            self.remove_random_node()
        utils.plot_homophily(self.local_homophily(), 'local_end_remove')

    def get_graph_probabilities(self):
        sum_degree = 0
        for node in self.G.nodes():
            sum_degree = sum_degree + self.G.degree(node)
        probabilities = [(self.G.degree(node) / sum_degree) for node in self.G.nodes()]
        return probabilities

    def get_probabilities(self, nodes_list):
        sum_degree = 0
        for node in nodes_list:
            sum_degree = sum_degree + self.G.degree(node)
        probabilities = [(self.G.degree(node) / sum_degree) for node in self.G.nodes()]
        return probabilities


    def pick_with_probability(self, nodes, probabilities):
        x = random.uniform(0, 1)
        cumulative_probability = 0.0        
        for item, item_probability in zip(list(nodes), probabilities):
            cumulative_probability += item_probability
            if x < cumulative_probability: break
        return item

    def pick_nodes_with_probability(self, count):
        probabilities = self.get_graph_probabilities()
        picked_nodes = []
        for _ in range(count):
            picked = self.pick_with_probability(self.G.nodes(), probabilities)
            picked_nodes.append(picked)