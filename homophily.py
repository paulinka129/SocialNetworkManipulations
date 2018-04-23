import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import graphviz

class Homophily:

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
        return (n**2 - 1)/2

    def get_node_class(self, node):
        return self.G.node[node]['value']

    def indicate(self, a, b):
        if a == b:
            return 1.0
        else:
            return 0.0

    def local_homophily(self):
        local_homo = []
        for node in self.G.nodes():
            homo = 0.0
            neighbors = len(list(self.G.neighbors(node)))
            neighbors_count = ((neighbors+1)**2 - 1)/2
            for neighbor in self.G.neighbors(node):
                homo = homo + (self.indicate(self.get_node_class(node), self.get_node_class(neighbor))/neighbors_count)
            local_homo.append(homo)
        return local_homo

    def global_homophily(self):
        global_homo = []
        for node in self.G.nodes():
            homo = 0.0
            n_count = ((self.nodes_count()+1)**2 - 1)/2
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



homophily = Homophily('polblogs.gml')
print nx.info(homophily.G)
print '################'
homophily.plot_homophily(homophily.local_homophily(), 'local.png')
homophily.plot_homophily(homophily.global_homophily(), 'global.png')