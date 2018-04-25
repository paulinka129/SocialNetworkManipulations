from __future__ import division
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import graphviz
from consts import Consts
import random
from random import choice

class Homophily:

    class0 = '0'
    class1 = '1'

    def __init__(self, filename):
        self.G = self.load_graph(filename)
        self.remove_nodes_without_edges()
        self.sum = self.count_sum()

    def function(self):
        print ("message inside the class.")

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

    def count_sum(self):
        n = self.nodes_count()
        return (n**2 - 1)//2

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
            neighbors = len(list(self.G.neighbors(node)))
            neighbors_count = ((neighbors+1)**2 - 1)//2
            for neighbor in self.G.neighbors(node):
                homo = homo + (self.indicate(self.get_node_class(node), self.get_node_class(neighbor))/neighbors_count)
            local_homo.append(homo)
        return local_homo

    def global_homophily(self):
        global_homo = []
        for node in self.G.nodes():
            homo = 0.0
            n_count = ((self.nodes_count()+1)**2 - 1)//2
            for inner in self.G.nodes():
                if node != inner:
                    homo = homo + (self.indicate(self.get_node_class(node), self.get_node_class(inner))/n_count)
            global_homo.append(homo)
        return global_homo

    def plot_homophily(self, homo_list, filename):
        num_bins = 10
        fig, ax = plt.subplots()
        ax.hist(homo_list, num_bins, density=1)
        ax.set_xlabel('homofilia')
        ax.set_ylabel('funkcja masy prawdopodobienstwa')
        fig.tight_layout()
        plt.savefig(filename)

    def add_random_node(self, index): 
        # print len(self.G.nodes())
        self.G.add_node(index, value=Consts.class1)
        print '*****'
        print index
        # print self.G.node[index]
        # print nx.get_node_attributes(self.G, index)
        random_node = choice(list(self.G.nodes()))
        # print random_node
        # print self.G.node[random_node]
        self.G.add_edge(index, random_node)
        # print len(self.G.nodes())

    def add_random_nodes(self, count):
        self.plot_homophily(self.local_homophily(), 'local_start' )
        for i in range(count):
            self.add_random_node(i)
        self.plot_homophily(self.local_homophily(), 'local_end')

    def remove_random_node(self):
        random_node = choice(list(self.G.nodes()))
        self.G.remove_node(random_node)

    def remove_random_nodes(self, count):
        self.plot_homophily(self.local_homophily(), 'local_start_remove' )
        for i in range(count):
            self.remove_random_node()
        self.plot_homophily(self.local_homophily(), 'local_end_remove')

    def get_probabilities(self):
        # sum_degree = [self.G.degree(node) for node in self.G.nodes()]
        sum_degree = 0
        for node in self.G.nodes():
            sum_degree = sum_degree + self.G.degree(node)
        probabilities = [(self.G.degree(node) / sum_degree) for node in self.G.nodes()]
        return probabilities


    def random_pick(self, probabilities):
        x = random.uniform(0, 1)
        cumulative_probability = 0.0        
        for item, item_probability in zip(list(self.G.nodes()), probabilities):
            cumulative_probability += item_probability
            if x < cumulative_probability: break
        return item, item_probability

    def pick_with_probability(self, count):
        probabilities = self.get_probabilities()
        print '************************'
        picked_nodes = []
        picked_prob = []
        for i in range(count):
            picked, prob = self.random_pick(probabilities)
            picked_nodes.append(picked)
            picked_prob.append(prob)
        print picked_nodes


homophily = Homophily('polblogs.gml')
print nx.info(homophily.G)
print '################'
# homophily.remove_random_nodes(100)
homophily.pick_with_probability(20)
# print 'koniec'
print nx.info(homophily.G)
# homophily.plot_homophily(homophily.local_homophily(), 'local.png')
# homophily.plot_homophily(homophily.global_homophily(), 'global.png')