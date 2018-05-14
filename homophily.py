from __future__ import division
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import graphviz
from consts import Consts
import utils
import random
from random import choices, uniform
from collections import defaultdict

class Homophily:

    class0 = '0'
    class1 = '1'

    def __init__(self, filename):
        self.G = self.load_graph(filename)
        self.remove_nodes_without_edges()
        self.size = self.nodes_count()
        self.global_homophilies  = []
        self.clas_list = self.get_all_clas()
        self.homophily_per_clas = defaultdict(list)
        self.average_degree = self.get_average_degree(self.G)
        # self.pagerank = self.evaluate_pagerank()

    def manipulate(self, strategy_func, strategy_name, pick_strategy, manipulation_clas, network_name):
        self.global_homophilies  = []
        class_partitions = []
        nodes_with_manipulation_clas = [node for node in self.G.nodes() if self.get_node_class(node) == manipulation_clas] 
        class_partitions.append(len(nodes_with_manipulation_clas)/self.size)
        homo_list_before = self.local_homophily()
        nodes_to_remove = [node for node in self.G.nodes() if self.get_node_class(node) != manipulation_clas]
        utils.save_to_file(homo_list_before, network_name, '{0}_homo_list_before'.format(strategy_name))

        ''' add, remove or change node ''' 
        strategy_func(nodes_to_remove, nodes_with_manipulation_clas, class_partitions, pick_strategy, manipulation_clas)


        homo_list_after = self.local_homophily()
        utils.save_to_file(homo_list_after, network_name, '{0}_homo_list_after'.format(strategy_name))
        utils.save_to_file(self.global_homophilies, network_name, '{0}_global_homophilies'.format(strategy_name))
        utils.plot_local_homophily(homo_list_before, homo_list_after, network_name, strategy_name)
        utils.plot_global_homophily(self.global_homophilies, network_name, strategy_name)
        utils.plot_all(class_partitions, self.global_homophilies, self.homophily_per_clas, manipulation_clas, network_name, strategy_name)

    def remove_strategy(self, nodes_to_remove, nodes_with_manipulation_clas, class_partitions, pick_strategy, manipulation_clas):
        count = len(nodes_to_remove)
        for i in range(count):

            ''' random, sampling with probability or according to ranking by degree '''
            picked_node = pick_strategy(manipulation_clas, nodes_to_remove, i)
            try:
                self.G.remove_node(picked_node)
                nodes_to_remove.remove(picked_node)
                class_partitions.append(len(nodes_with_manipulation_clas)/len(list(self.G.nodes())))
                self.global_homophily()
                self.count_homophily_per_clas()
                print(i)
            except nx.NetworkXError:
                print('node does not exist in graph')
            except Exception as ex:
                print(ex)

    def add_strategy(self, nodes_to_add, nodes_with_manipulation_clas, class_partitions, pick_strategy, manipulation_clas):
        for i in range(len(nodes_to_add)):

            ''' random, sampling with probability or according to ranking by degree '''
            picked_node = pick_strategy(manipulation_clas, list(self.G.nodes()), i)   
            try:         
                self.add_node(picked_node, i, manipulation_clas)
                nodes_with_manipulation_clas = [node for node in self.G.nodes() if self.get_node_class(node) == manipulation_clas] 
                class_partitions.append(len(nodes_with_manipulation_clas)/len(list(self.G.nodes())))
                self.global_homophily()
                self.count_homophily_per_clas()
                print(i)
            except Exception as ex:
                print(ex)

    def add_while_strategy(self, nodes_to_add, nodes_with_manipulation_clas, class_partitions, pick_strategy, manipulation_clas):
        i = 0
        last_global_homophily = 0
        while (i < 1000 and last_global_homophily < 1):

            ''' random, sampling with probability or according to ranking by degree '''
            picked_node = pick_strategy(manipulation_clas, list(self.G.nodes()), i)   
            try:         
                self.add_node(picked_node, (i+10000), manipulation_clas)
                nodes_with_manipulation_clas = [node for node in self.G.nodes() if self.get_node_class(node) == manipulation_clas] 
                class_partitions.append(len(nodes_with_manipulation_clas)/len(list(self.G.nodes())))
                last_global_homophily = self.global_homophily()
                self.count_homophily_per_clas()
                print(str(i) + ': ' + str(last_global_homophily))
            except Exception as ex:
                print(ex)
            i += 1

    def add_big_strategy(self, nodes_to_add, nodes_with_manipulation_clas, class_partitions, pick_strategy, manipulation_clas):
        number_of_edges = int(np.ceil(5 * self.average_degree))
        i = 0
        last_global_homophily = 0
        max_add = self.size*2
        while (i < max_add and last_global_homophily < 1):

            for n in range(number_of_edges):
                ''' random, sampling with probability or according to ranking by degree '''
                picked_node = pick_strategy(manipulation_clas, list(self.G.nodes()), i)   
                try:         
                    self.add_node(picked_node, (i+10000), manipulation_clas)                    
                except Exception as ex:
                    print(ex)
            nodes_with_manipulation_clas = [node for node in self.G.nodes() if self.get_node_class(node) == manipulation_clas] 
            class_partitions.append(len(nodes_with_manipulation_clas)/len(list(self.G.nodes())))
            last_global_homophily = self.global_homophily()
            self.count_homophily_per_clas()
            print(str(i) + ': ' + str(last_global_homophily))
            i += 1


    def add_medium_strategy(self, nodes_to_add, nodes_with_manipulation_clas, class_partitions, pick_strategy, manipulation_clas):
        pass

    def add_small_strategy(self, nodes_to_add, nodes_with_manipulation_clas, class_partitions, pick_strategy, manipulation_clas):
        pass

    def change_class_strategy(self, nodes_to_change, nodes_with_manipulation_clas, class_partitions, pick_strategy, manipulation_clas):
        count = len(nodes_to_change)
        for i in range(count):

            ''' random, sampling with probability or according to ranking by degree '''
            picked_node = pick_strategy(manipulation_clas, nodes_to_change, i)
            try:
                self.G.node[picked_node]['value'] = manipulation_clas
                nodes_with_manipulation_clas = [node for node in self.G.nodes() if self.get_node_class(node) == manipulation_clas] 
                class_partitions.append(len(nodes_with_manipulation_clas)/len(list(self.G.nodes())))
                nodes_to_change.remove(picked_node)
                self.global_homophily()
                self.count_homophily_per_clas()
                print(i)
            except nx.NetworkXError:
                print('node does not exist in graph')
            except Exception as ex:
                print(ex)

    def pick_random(self, manipulation_clas, nodes, i):
        return random.choice(nodes)

    def pick_with_probability(self, manipulation_clas, nodes, i):
        probabilities = self.get_probabilities(nodes)
        all_zeros = all(elem == 0 for elem in probabilities)
        if (not all_zeros):
            return choices(nodes, probabilities)[0]
        else:
            return self.pick_random(manipulation_clas, nodes, i)

    def pick_with_custom_probability(self, manipulation_clas, nodes, i):
        probabilities = self.generate_probabilities(nodes, manipulation_clas, 0, 0.4, 0.6, 1.0)
        return choices(nodes, probabilities)[0]

    def pick_by_ranking(self, manipulation_clas, nodes, i):
        sorted_by_degree = sorted(self.G.degree, key=lambda x: x[1], reverse=True)
        result = [node[0] for node in sorted_by_degree if node[0] in nodes]
        return result[0]

    def pick_by_pagerank(self, manipulation_clas, nodes, i):
        pr = nx.pagerank(self.G)
        sorted_by_pagerank = sorted(pr.items(), key=lambda x: x[1], reverse=True)
        result = [node[0] for node in sorted_by_pagerank if node[0] in nodes]
        return result[0]

    def pick_by_ranking_for_add(self, manipulation_clas, nodes, i):
        sorted_by_degree = sorted(self.G.degree, key=lambda x: x[1], reverse=True)
        result = [node[0] for node in sorted_by_degree if node[0] in nodes]
        return result[i]

    def load_graph(self, filename):
        G = nx.read_gml(filename)
        return G

    def get_size_of_manipulated_set(self, manipulation_clas):
        nodes_with_manipulation_clas = [node for node in self.G.nodes() if self.get_node_class(node) == manipulation_clas] 
        return len(nodes_with_manipulation_clas)
    
    def print_classes(self):
        for node in self.G.nodes():
            print(self.G.node[node]['value'])

    def print_nodes_with_class(self, value):
        nodeWithClass = [n for n in self.G.nodes() if self.G.node[n]['value'] == value]
        for node in nodeWithClass:
            print("{0}, {1}".format(node, self.G.node[node]['value']))

    def remove_nodes_without_edges(self):
        deg = self.G.degree()
        to_remove = [n[0] for n in deg if n[1] < 1]
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

    def indicate_bool(self, a, b):
        if (a and b):
            return 1
        else:
            return 0

    def evaluate_pagerank(self):
        pg = nx.pagerank(self.G)
        sorted_by_pagerank = sorted(pg, key=lambda x: x[1], reverse=True)
        return sorted_by_pagerank

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
        self.global_homophilies.append(global_homo)
        return global_homo

    def count_homophily_per_clas(self):
        # all_edges = len(list(self.G.edges()))
        for clas in self.clas_list:
            homo = 0.0
            edges_per_clas = [edge for edge in self.G.edges() if (self.get_node_class(edge[0]) == clas or self.get_node_class(edge[1]) == clas)] 
            edge_count = len(edges_per_clas)
            for edge in edges_per_clas:
                homo += (self.indicate(self.get_node_class(edge[0]), self.get_node_class(edge[1]))/edge_count)
            self.homophily_per_clas[clas].append(homo)

    def add_random_node(self, index, clas): 
        self.G.add_node(index, value=clas)
        random_node = random.choice(list(self.G.nodes()))
        self.G.add_edge(index, random_node)

    def add_node(self, node, index, clas):
        self.G.add_node(index, value=clas)
        self.G.add_edge(index, node)

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
        probabilities = [((self.G.degree(node) / sum_degree) if sum_degree != 0 else 0) for node in nodes_list]
        return probabilities

    def get_average_degree(self, graph):
        sum_degree = 0
        for node in graph.nodes():
            sum_degree = sum_degree + graph.degree(node)
        average_degree = sum_degree / len(list(graph.nodes()))
        return average_degree

    def get_all_clas(self):
        clas_list = set()
        for node in self.G.nodes():
            clas = self.get_node_class(node)
            clas_list.add(clas)
        return clas_list

    def generate_probabilities(self, nodes, manipulate_clas, low1, high1, low2, high2):
        prob = []
        for node in nodes:
            if (self.get_node_class(node) == manipulate_clas):
                prob.append(uniform(low1, high1))
            else:
                prob.append(uniform(low2, high2))
        return prob