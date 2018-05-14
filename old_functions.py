from __future__ import division
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import graphviz
from consts import Consts
import utils
import random
from random import choices
from collections import defaultdict

class OldHomophily:

    class0 = '0'
    class1 = '1'

    def __init__(self, filename):
        self.G = self.load_graph(filename)
        self.remove_nodes_without_edges()
        self.size = self.nodes_count()
        self.global_homophilies  = []
        self.clas_list = self.get_all_clas()
        self.homophily_per_clas = defaultdict(list)

    def add_random(self, count, clas, network_name):
        self.global_homophilies  = []
        class_partitions = []
        homo_list_before = self.local_homophily()
        utils.save_to_file(homo_list_before, network_name, 'add_random_homo_list_before')
        nodes_with_clas = [node for node in self.G.nodes() if self.get_node_class(node) == clas]
        for i in range(len(nodes_with_clas)):
            random_node = random.choice(list(self.G.nodes()))
            self.add_node(random_node, i, clas)
            self.global_homophily()
            self.count_homophily_per_clas()
            print(i)
        homo_list_after = self.local_homophily()
        utils.save_to_file(homo_list_after, network_name, 'add_random_homo_list_after')
        utils.save_to_file(self.global_homophilies, network_name, 'add_random_global_homophilies')
        utils.plot_global_homophily(self.global_homophilies, network_name, 'add_with_probability')
        utils.plot_local_homophily(homo_list_before, homo_list_after, network_name, 'add_random')
        utils.plot_all(class_partitions, self.global_homophilies, self.homophily_per_clas, 'E', network_name, 'remove_random')


    def add_with_probability(self, count, clas, network_name=None):
        self.global_homophilies  = []
        probabilities = self.get_graph_probabilities()
        homo_list_before = self.local_homophily()
        utils.save_to_file(homo_list_before, network_name, 'add_with_probability_homo_list_before')
        nodes_with_clas = [node for node in self.G.nodes() if self.get_node_class(node) == clas]
        for i in range(len(nodes_with_clas)):
            node = self.pick_with_probability(self.G.nodes())
            self.add_node(node, i, clas)
            self.global_homophily()
            self.count_homophily_per_clas()
        homo_list_after = self.local_homophily()
        utils.save_to_file(homo_list_after, network_name, 'add_with_probability_homo_list_after')
        utils.save_to_file(self.global_homophilies, network_name, 'add_with_probability_global_homophilies')
        utils.plot_local_homophily(homo_list_before, homo_list_after, network_name, 'add_with_probability')
        utils.plot_global_homophily(self.global_homophilies, network_name, 'add_with_probability')

    def add_by_ranking(self, count, clas, network_name):
        self.global_homophilies  = []
        sorted_by_degree = sorted(self.G.degree, key=lambda x: x[1], reverse=True)
        homo_list_before = self.local_homophily()
        utils.save_to_file(homo_list_before, network_name, 'add_by_ranking_list_before')
        nodes_with_clas = [node for node in self.G.nodes() if self.get_node_class(node) == clas]
        for i in range(len(nodes_with_clas)):
            node = sorted_by_degree[i][0]
            self.add_node(node, i, clas)
            self.global_homophily()
            self.count_homophily_per_clas()
        homo_list_after = self.local_homophily()
        utils.save_to_file(homo_list_after, network_name, 'add_by_ranking_homo_list_after')
        utils.save_to_file(self.global_homophilies, network_name, 'add_by_ranking_global_homophilies')
        utils.plot_local_homophily(homo_list_before, homo_list_after, network_name, 'add_by_ranking')
        utils.plot_global_homophily(self.global_homophilies, network_name, 'add_by_ranking')

    def remove_random(self, count, manipulation_clas, clas, network_name):
        self.global_homophilies  = []
        class_partitions = []
        nodes_with_manipulation_clas = [node for node in self.G.nodes() if self.get_node_class(node) == manipulation_clas] 
        class_partitions.append(len(nodes_with_manipulation_clas)/self.size)
        homo_list_before = self.local_homophily()
        # nodes_with_clas = [node for node in self.G.nodes() if self.get_node_class(node) == clas]
        nodes_to_remove = [node for node in self.G.nodes() if self.get_node_class(node) != manipulation_clas]
        utils.save_to_file(homo_list_before, network_name, 'remove_random_homo_list_before')
        count = len(nodes_to_remove)
        for i in range(count):
            random_node = random.choice(nodes_to_remove)
            try:
                self.G.remove_node(random_node)
                nodes_to_remove.remove(random_node)
                class_partitions.append(len(nodes_with_manipulation_clas)/len(list(self.G.nodes())))
                self.global_homophily()
                self.count_homophily_per_clas()
                print(i)
            except nx.NetworkXError:
                print('node does not exist in graph')

        homo_list_after = self.local_homophily()
        utils.save_to_file(homo_list_after, network_name, 'remove_random_homo_list_after')
        utils.save_to_file(self.global_homophilies, network_name, 'remove_random_global_homophilies')
        utils.plot_local_homophily(homo_list_before, homo_list_after, network_name, 'remove_random')
        utils.plot_global_homophily(self.global_homophilies, network_name, 'remove_random')
        utils.plot_all(class_partitions, self.global_homophilies, self.homophily_per_clas, manipulation_clas, network_name, 'remove_random')


    def remove_with_probability(self, count, manipulation_clas, clas, network_name):
        self.global_homophilies  = []
        class_partitions = []
        nodes_with_manipulation_clas = [node for node in self.G.nodes() if self.get_node_class(node) == manipulation_clas] 
        class_partitions.append(len(nodes_with_manipulation_clas)/self.size)
        nodes_with_clas = [node for node in self.G.nodes() if self.get_node_class(node) == clas]
        probabilities = self.get_probabilities(nodes_with_clas)
        homo_list_before = self.local_homophily()
        utils.save_to_file(homo_list_before, network_name, 'remove_with_probability_homo_list_before')
        count = len(nodes_with_clas)
        for i in range(count):
            node = self.pick_with_probability(nodes_with_clas)
            try:
                self.G.remove_node(node)
                nodes_with_clas.remove(node)
                class_partitions.append(len(nodes_with_manipulation_clas)/len(list(self.G.nodes())))
                self.global_homophily()
                self.count_homophily_per_clas()
            except nx.NetworkXError:
                print('node does not exist in graph')        
        homo_list_after = self.local_homophily()
        utils.save_to_file(homo_list_after, network_name, 'remove_with_probability_homo_list_after')
        utils.save_to_file(self.global_homophilies, network_name, 'remove_with_probability_global_homophilies')        
        utils.plot_local_homophily(homo_list_before, homo_list_after, network_name, 'remove_with_probability')
        utils.plot_global_homophily(self.global_homophilies, network_name, 'remove_with_probability')
        utils.plot_all(class_partitions, self.global_homophilies, self.homophily_per_clas, manipulation_clas, network_name, 'remove_with_probability')


    def remove_by_ranking(self, manipulation_clas, count, clas, network_name):
        self.global_homophilies  = []
        class_partitions = []
        nodes_with_manipulation_clas = [node for node in self.G.nodes() if self.get_node_class(node) == manipulation_clas] 
        sorted_by_degree = sorted(self.G.degree, key=lambda x: x[1], reverse=True)
        nodes_with_clas = [node for node in sorted_by_degree if self.get_node_class(node[0]) == clas]
        homo_list_before = self.local_homophily()
        utils.save_to_file(homo_list_before, network_name, 'remove_by_ranking_homo_list_before')
        count = len(nodes_with_clas)
        for i in range(count):
            print(i)
            node = nodes_with_clas[i][0]
            try:
                self.G.remove_node(node)
                class_partitions.append(len(nodes_with_manipulation_clas)/len(list(self.G.nodes())))
                self.global_homophily()
                self.count_homophily_per_clas()
            except nx.NetworkXError:
                print('node does not exist in graph')
        homo_list_after = self.local_homophily()
        utils.save_to_file(homo_list_after, network_name, 'remove_by_ranking_homo_list_after')
        utils.save_to_file(self.global_homophilies, network_name, 'remove_by_ranking_global_homophilies')   
        utils.plot_local_homophily(homo_list_before, homo_list_after, network_name, 'remove_by_ranking')
        utils.plot_global_homophily(self.global_homophilies, network_name, 'remove_by_ranking')
        utils.plot_all(class_partitions, self.global_homophilies, self.homophily_per_clas, manipulation_clas,  network_name, 'remove_by_ranking')

    def change_class_random(self, count, manipulation_clas, clas, network_name):
        self.global_homophilies  = []
        class_partitions = []
        nodes_with_manipulation_clas = [node for node in self.G.nodes() if self.get_node_class(node) == manipulation_clas] 
        class_partitions.append(len(nodes_with_manipulation_clas)/self.size)
        homo_list_before = self.local_homophily()
        nodes_with_clas = [node for node in self.G.nodes() if self.get_node_class(node) != manipulation_clas]
        utils.save_to_file(homo_list_before, network_name, 'change_class_random_homo_list_before')
        count = len(nodes_with_manipulation_clas)
        for i in range(count):
            random_node = random.choice(nodes_with_clas)
            try:
                self.G.node[random_node]['value'] = manipulation_clas
                class_partitions.append(self.get_size_of_manipulated_set(manipulation_clas)/len(list(self.G.nodes())))
                self.global_homophily()
                self.count_homophily_per_clas()
                print(i)
            except nx.NetworkXError:
                print('node does not exist in graph')

        homo_list_after = self.local_homophily()
        utils.save_to_file(homo_list_after, network_name, 'change_class_random_homo_list_after')
        utils.save_to_file(self.global_homophilies, network_name, 'change_class_random_global_homophilies')
        utils.plot_local_homophily(homo_list_before, homo_list_after, network_name, 'change_class_random')
        utils.plot_global_homophily(self.global_homophilies, network_name, 'change_class_random')
        utils.plot_all(class_partitions, self.global_homophilies, self.homophily_per_clas, manipulation_clas, network_name, 'change_class_random')

    def change_class_by_ranking(self, count, manipulation_clas, clas, network_name):
        self.global_homophilies  = []
        class_partitions = []
        sorted_by_degree = sorted(self.G.degree, key=lambda x: x[1], reverse=True)
        nodes_with_manipulation_clas = [node for node in self.G.nodes() if self.get_node_class(node) == manipulation_clas] 
        class_partitions.append(len(nodes_with_manipulation_clas)/self.size)
        homo_list_before = self.local_homophily()
        nodes_with_clas = [node for node in sorted_by_degree if self.get_node_class(node[0]) != manipulation_clas]
        utils.save_to_file(homo_list_before, network_name, 'change_class_by_ranking_homo_list_before')
        count = len(nodes_with_clas)
        for i in range(count):
            node = nodes_with_clas[i][0]
            try:
                self.G.node[node]['value'] = manipulation_clas
                class_partitions.append(self.get_size_of_manipulated_set(manipulation_clas)/len(list(self.G.nodes())))
                self.global_homophily()
                self.count_homophily_per_clas()
                print(i)
            except nx.NetworkXError:
                print('node does not exist in graph')

        homo_list_after = self.local_homophily()
        utils.save_to_file(homo_list_after, network_name, 'change_class_by_ranking_homo_list_after')
        utils.save_to_file(self.global_homophilies, network_name, 'change_class_by_ranking_global_homophilies')
        utils.plot_local_homophily(homo_list_before, homo_list_after, network_name, 'change_class_by_ranking')
        utils.plot_global_homophily(self.global_homophilies, network_name, 'change_class_by_ranking')
        utils.plot_all(class_partitions, self.global_homophilies, self.homophily_per_clas, manipulation_clas, network_name, 'change_class_by_ranking')

    def add_random_nodes(self, count, clas):
        utils.plot_homophily(self.local_homophily(), 'local_start' )
        for i in range(count):
            self.add_random_node(i, clas)
        utils.plot_homophily(self.local_homophily(), 'local_end')

    def remove_random_node(self):
        random_node = random.choice(list(self.G.nodes()))
        self.G.remove_node(random_node)

    def remove_random_nodes(self, count):
        utils.plot_homophily(self.local_homophily(), 'local_start_remove' )
        for _ in range(count):
            self.remove_random_node()
        utils.plot_homophily(self.local_homophily(), 'local_end_remove')

    def pick_nodes_with_probability(self, count):
        probabilities = self.get_graph_probabilities()
        picked_nodes = []
        picked_probes = []
        for i in range(count):
            picked, picked_prob = self.pick_with_probability(self.G.nodes())
            picked_nodes.append(picked)
            picked_probes.append(picked_prob)
        return picked_nodes, picked_probes
