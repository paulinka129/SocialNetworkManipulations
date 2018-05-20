import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from consts import Consts
import utils
import random
from random import choices, uniform
from collections import defaultdict
from scipy import sparse

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

    def create_clas_matrix(self):
        clas_list = self.get_all_clas()
        sorted_clas_list = sorted(clas_list)
        shape = (self.size, len (sorted_clas_list))

        mat = np.zeros(shape)

        for (i,j), _ in np.ndenumerate(mat):
            # i - rows, j - columns
            # iterate over column
            mat.T[j,i] = self.map_class_to_matrix(i, j, sorted_clas_list, self.G.nodes())
        return mat

    def get_manipulate_clas_index(self, manipulate_clas):
        clas_list = self.get_all_clas()
        sorted_clas_list = sorted(clas_list)
        return sorted_clas_list.index(manipulate_clas)

    def map_class_to_matrix(self, i, j, clas_list, nodes):
        nodes_values = [i for i in nodes.items()]
        val = self.get_node_class(nodes_values[i][0])
        is_ok = clas_list[j] == val
        if (is_ok):
            return 1
        else:
            return 0

    def get_adjacency_matrix(self):
        A = nx.adjacency_matrix(self.G)
        return A.todense()

    def evaluate_lbp_100(self):
        lbp_arr = []
        for i in range(1000):
            lbp = self.evaluate_lbp()
            lbp_sum = np.sum(lbp)
            lbp_arr.append(lbp_sum)
        print(lbp_arr)
        mean = np.mean(lbp_arr)
        median = np.median(lbp_arr)
        print('mean', mean)
        print('median ', median)

    def evaluate_lbp_remove_all(self, manipulation_clas):
        percent = 0.1
        for i in range(10):
            print('percent ', percent)
            self.evaluate_lbp_with_remove_manipulation(manipulation_clas, percent, i)
            percent = percent + 0.1

    def evaluate_lbp_change_all(self, manipulation_clas):
        percent = 0.1
        for i in range(10):
            print('percent ', percent)
            self.evaluate_lbp_with_change_class_manipulation(manipulation_clas, percent, i)
            percent = percent + 0.1

    def evaluate_lbp_add_all(self, manipulation_clas):
        percent = 0.1
        for i in range(10):
            print('percent ', percent)
            self.evaluate_lbp_with_add_manipulation(manipulation_clas, percent, i)
            percent = percent + 0.1

    def evaluate_lbp(self):
        clas_matrix = self.create_clas_matrix() # (319, 16)
        nodes_per_class_vector = clas_matrix.sum(axis=0) # wektor - ile węzłów w danej klasie

        adjacency_matrix = self.get_adjacency_matrix() # macierz sąsiedztwa
        result_matrix = np.copy(clas_matrix)

        for i in range(50): 
            for j in range(result_matrix.shape[1]): # 16 kolumn
                result = adjacency_matrix.dot(result_matrix[:, j]) # mnozenie macierzy sąsiedztwa przez kolejne kolumny
                result_matrix[:, j] = result
            self.normalize_columns(result_matrix) # normalizacja w kolumnach
            self.normalize_rows(result_matrix) # normalizacja w wierszach, suma = 1
        
        # nodes_per_class_vector_after_lbp = result_matrix.sum(axis=0)
        # lbp = np.subtract(clas_matrix, result_matrix)
        # lbp = np.absolute(lbp)
        # lbp_sum = lbp.sum(axis=0)

        nodes_per_class_vector_after_lbp = result_matrix.sum(axis=0)
        lbp = np.subtract(nodes_per_class_vector, nodes_per_class_vector_after_lbp)
        lbp = np.absolute(lbp)
        lbp_sum = lbp.sum(axis=0)

        utils.save_to_file_lbp('evaluate_lbp', 0, 0, 'nodes_per_class_vector', nodes_per_class_vector, 'nodes_per_class_vector_after_lbp', nodes_per_class_vector_after_lbp, 'lbp', lbp, 'lbp_sum', lbp_sum)
        print('nodes_per_class_vector\n', nodes_per_class_vector)
        print('nodes_per_class_vector_after_lbp\n', nodes_per_class_vector_after_lbp)
        print('lbp_sum\n', lbp_sum)
        return lbp_sum


    def evaluate_lbp_with_remove_manipulation(self, manipulation_clas, percent, index):
        clas_matrix = self.create_clas_matrix() # (319, 16)
        nodes_per_class_vector = clas_matrix.sum(axis=0) # wektor - ile węzłów w danej klasie

        result_matrix = np.copy(clas_matrix)

        nodes_to_remove = [node for node in self.G.nodes() if self.get_node_class(node) != manipulation_clas]
        batch_size = int(percent*len(nodes_to_remove))
        removed_nodes_indices = []

        removed_nodes_indices = self.remove_node_for_lbp(manipulation_clas, nodes_to_remove, batch_size, result_matrix)

        adjacency_matrix = self.get_adjacency_matrix() # macierz sąsiedztwa
        self.reset_adjacency_matrix_for_removed_nodes(adjacency_matrix, removed_nodes_indices) # wyzerowanie wierszy w macierzy sąsiedztwa dla usunietych wierzcholkow

        for i in range(50): 
            self.reset_result_matrix_for_removed_nodes(result_matrix, removed_nodes_indices) # wyzerowanie wierszy dla usunietych wierzcholkow
            for j in range(result_matrix.shape[1]): # 16 kolumn
                result = adjacency_matrix.dot(result_matrix[:, j]) # mnozenie macierzy sąsiedztwa przez kolejne kolumny
                result_matrix[:, j] = result
            self.normalize_columns(result_matrix) # normalizacja w kolumnach
            self.normalize_rows(result_matrix) # normalizacja w wierszach, suma = 1
        
        nodes_per_class_vector_after_lbp = result_matrix.sum(axis=0)
        lbp = np.subtract(nodes_per_class_vector, nodes_per_class_vector_after_lbp)
        lbp = np.absolute(lbp)
        lbp_sum = lbp.sum(axis=0)

        utils.save_to_file_lbp('evaluate_lbp_with_remove_manipulation', percent, index, 'nodes_per_class_vector', nodes_per_class_vector, 'nodes_per_class_vector_after_lbp', nodes_per_class_vector_after_lbp, 'lbp', lbp, 'lbp_sum', lbp_sum)
        print('nodes_per_class_vector\n', nodes_per_class_vector)
        print('nodes_per_class_vector_after_lbp\n', nodes_per_class_vector_after_lbp)
        print('lbp_sum\n', lbp_sum)
        # print('removed_nodes_indices: ', removed_nodes_indices)

    def evaluate_lbp_with_add_manipulation(self, manipulation_clas, percent, index):
        clas_matrix = self.create_clas_matrix() # (319, 16)
        nodes_per_class_vector = clas_matrix.sum(axis=0) # wektor - ile węzłów w danej klasie

        result_matrix = np.copy(clas_matrix)

        # nodes_to_add = [node for node in self.G.nodes() if self.get_node_class(node) != manipulation_clas]
        number_of_edges = int(np.ceil(0.2 * self.average_degree))
        batch_size = int(percent*self.size)
        added_nodes_indices = []
        last_added_index = 0

        added_nodes_indices, result_matrix, last_added_index = self.add_node_for_lbp(manipulation_clas, batch_size, result_matrix, number_of_edges, last_added_index)
        new_adjacency_matrix = self.get_adjacency_matrix() # pobieranie nowej macierzy sąsiedztwa po dodaniu nowego wierzchołka
        print('size ', len(list(self.G.nodes())))
        for i in range(50): 
            
            
            self.reset_result_matrix_for_added_nodes(result_matrix, added_nodes_indices, manipulation_clas) # wyzerowanie wierszy dla usunietych wierzcholkow
            for j in range(result_matrix.shape[1]): # 16 kolumn
                result = new_adjacency_matrix.dot(result_matrix[:, j]) # mnozenie macierzy sąsiedztwa przez kolejne kolumny
                result_matrix[:, j] = result

            self.normalize_columns(result_matrix) # normalizacja w kolumnach
            self.normalize_rows(result_matrix) # normalizacja w wierszach, suma = 1
        
        # nodes_per_class_vector_after_lbp = result_matrix.sum(axis=0)
        # lbp = np.subtract(clas_matrix, result_matrix)
        # lbp = np.absolute(lbp)
        # lbp_sum = lbp.sum(axis=0)

        nodes_per_class_vector_after_lbp = result_matrix.sum(axis=0)
        lbp = np.subtract(nodes_per_class_vector, nodes_per_class_vector_after_lbp)
        lbp = np.absolute(lbp)
        lbp_sum = lbp.sum(axis=0)

        utils.save_to_file_lbp('evaluate_lbp_with_add_manipulation', percent, index, 'nodes_per_class_vector', nodes_per_class_vector, 'nodes_per_class_vector_after_lbp', nodes_per_class_vector_after_lbp, 'lbp', lbp, 'lbp_sum', lbp_sum)
        print('nodes_per_class_vector\n', nodes_per_class_vector)
        print('nodes_per_class_vector_after_lbp\n', nodes_per_class_vector_after_lbp)
        print('lbp_sum\n', lbp_sum)

    def evaluate_lbp_with_change_class_manipulation(self, manipulation_clas, percent, index):
        clas_matrix = self.create_clas_matrix() # (319, 16)
        nodes_per_class_vector = clas_matrix.sum(axis=0) # wektor - ile węzłów w danej klasie

        adjacency_matrix = self.get_adjacency_matrix() # macierz sąsiedztwa
        result_matrix = np.copy(clas_matrix)

        nodes_to_change = [node for node in self.G.nodes() if self.get_node_class(node) != manipulation_clas]
        batch_size = int(percent*len(nodes_to_change))
        changed_nodes_indices = []

        changed_nodes_indices = self.change_node_for_lbp(manipulation_clas, nodes_to_change, batch_size, result_matrix)

        for i in range(50):
            self.reset_result_matrix_for_changed_nodes(result_matrix, changed_nodes_indices, manipulation_clas)
            for j in range(result_matrix.shape[1]): # 16 kolumn
                result = adjacency_matrix.dot(result_matrix[:, j]) # mnozenie macierzy sąsiedztwa przez kolejne kolumny
                result_matrix[:, j] = result
            self.normalize_columns(result_matrix) # normalizacja w kolumnach
            self.normalize_rows(result_matrix) # normalizacja w wierszach, suma = 1
        
        # nodes_per_class_vector_after_lbp = result_matrix.sum(axis=0)
        # lbp = np.subtract(clas_matrix, result_matrix)
        # lbp = np.absolute(lbp)
        # lbp_sum = lbp.sum(axis=0)

        nodes_per_class_vector_after_lbp = result_matrix.sum(axis=0)
        lbp = np.subtract(nodes_per_class_vector, nodes_per_class_vector_after_lbp)
        lbp = np.absolute(lbp)
        lbp_sum = lbp.sum(axis=0)

        utils.save_to_file_lbp('evaluate_lbp_with_change_class_manipulation', percent, index, 'nodes_per_class_vector', nodes_per_class_vector, 'nodes_per_class_vector_after_lbp', nodes_per_class_vector_after_lbp, 'lbp', lbp, 'lbp_sum', lbp_sum)
        print('nodes_per_class_vector\n', nodes_per_class_vector)
        print('nodes_per_class_vector_after_lbp\n', nodes_per_class_vector_after_lbp)
        print('lbp_sum\n', lbp_sum)


    def evaluate_lbp_old(self, manipulation_clas):
        clas_matrix = self.create_clas_matrix()
        clas_matrix_before = np.copy(clas_matrix)
        sum_before = clas_matrix_before.sum(axis=0)
        print('before manipulation')
        ### before manipulation
        adjacency_matrix_before = self.get_adjacency_matrix()
        result_shape = (clas_matrix.shape)
        result_matrix_before = np.copy(clas_matrix)
        

        for j in range(result_shape[1]):
            result = adjacency_matrix_before.dot(result_matrix_before[:, j])
            result_matrix_before[:, j] = result
        self.normalize_columns(result_matrix_before)
        ### end before manipulation
        
        print('end before manipulation')
        
        print('manipulation')
        ### manipulation

        np.savetxt('lbp-amd/clas_matrix_before', clas_matrix)
        # self.remove_node_for_lbp(manipulation_clas, clas_matrix, 1)
        np.savetxt('lbp-amd/clas_matrix_after', clas_matrix)
        adjacency_matrix_after = self.get_adjacency_matrix()
        result_shape = (clas_matrix.shape)
        result_matrix = np.copy(clas_matrix)
        for i in range (50):
            for j in range(result_shape[1]):
                # np.savetxt('lbp/result_matrix.{0}.{1}'.format(i,j), result_matrix)
                result = adjacency_matrix_after.dot(result_matrix[:, j])
                # np.savetxt('lbp/result.{0}.{1}'.format(i,j), result)
                result_matrix[:, j] = result                
            self.normalize_columns(result_matrix)
            for l in range(result_matrix.shape[0]):
                #normalizacja per wiersz (suma w wierszu =1)
                #zdarza sie ze juz w result_matrix ma wiecej niz jedną jedynkę, dlatego trzeba losować z nich do której klasy nalezy

                result_matrix[l,np.argmax(result_matrix[l,:])]=1
                result_matrix[l,:]= [0  if m!=1 else 1 for m in result_matrix[l,:]]
                print(np.argmax(result_matrix[l,:]))
                print(result_matrix[l,:])
        
            # np.savetxt('lbp/result_matrix_trololo.{0}'.format(i), result_matrix)
        ### end manipulation
        
        
        print('end manipulation')

        print('after lbp ',result_matrix.sum(axis=0))

        lbp = np.subtract(clas_matrix_before, result_matrix)
        lbp = np.absolute(lbp)
        sum_after = lbp.sum(axis=0)




        np.savetxt('lbp-amd/adjacency_matrix_before', adjacency_matrix_before)
        np.savetxt('lbp-amd/result_matrix_before', result_matrix_before)
        np.savetxt('lbp-amd/adjacency_matrix_after', adjacency_matrix_after)
        np.savetxt('lbp-amd/result_matrix', result_matrix)
        np.savetxt('lbp-amd/lbp', lbp)

        print(sum_before)
        print(sum_after)

    def normalize_columns(self, matrix):
        _, cols = matrix.shape
        for col in range(cols):
            max = abs(matrix[:,col]).max()
            if (max !=0):
                matrix[:,col] /= max
            else:
                matrix[:,col] = 0
        # print('normalize_columns\n', matrix)

    def normalize_rows(self, matrix):
        # print('normalize_rows')
        rows = matrix.shape[0] # liczba wierszy
        for row in range(rows):
            #normalizacja per wiersz (suma w wierszu =1)
            #zdarza sie ze juz w result_matrix ma wiecej niz jedną jedynkę, dlatego trzeba losować z nich do której klasy nalezy
            max_val_indeces = np.argwhere(matrix[row] == np.amax(matrix[row])).flatten().tolist() # lista indeksów z max wartościami
            random_chosen_index = random.choice(max_val_indeces) # losowo wybrany 
            # random_chosen_index = max_val_indeces[0]
            
            matrix[row] = [0 for el in matrix[row]] # wstaw same 0
            matrix[row][random_chosen_index] = 1 # wstaw 1 pod zadanym indeksem  
            # print('matrix[row]: ', matrix[row])  


 
    def remove_node_for_lbp(self, manipulation_clas, nodes_to_remove, batch_size, result_matrix):
        removed_nodes_indices = []
        if (nodes_to_remove):
            for i in range(batch_size):
                try:
                    # node = self.pick_by_ranking(manipulation_clas, nodes_to_remove, 0)
                    # node = self.pick_by_pagerank(manipulation_clas, nodes_to_remove, 0)                    
                    # node = self.pick_random(manipulation_clas, nodes_to_remove, 0)                    
                    node = self.pick_with_probability(manipulation_clas, nodes_to_remove, 0)                    
                    nodes_to_remove.remove(node)
                    node_index = self.get_index(node)
                    removed_nodes_indices.append(node_index)
                    result_matrix[node_index] = 0 # zerujemy cały wiersz danego węzła (nie przynależy do żadnej klasy)
                    edges_to_remove = [edge for edge in self.G.edges() if (edge[0] == node or edge[1] == node)]
                    self.G.remove_edges_from(edges_to_remove)
                except Exception:
                    print('cannot remove, probably empty array')
        return removed_nodes_indices

    def add_node_for_lbp(self, manipulation_clas, batch_size, result_matrix, number_of_edges, i):
        added_nodes_indices = []
        manipulate_clas_index = self.get_manipulate_clas_index(manipulation_clas)
        last_added_index = i
        for b in range(batch_size):
            new_node = (last_added_index+10000)
            for n in range(number_of_edges):
                node = self.pick_random(manipulation_clas, list(self.G.nodes()), last_added_index)                         
                self.add_node(node, new_node, manipulation_clas)           
            new_node_index = self.get_index(new_node)
            added_nodes_indices.append(new_node_index)  
            new_result_matrix_row = np.zeros((1, result_matrix.shape[1])) # stworzenie nowego wiersza dla result_matrix
            new_result_matrix_row[0, manipulate_clas_index] = 1 # ustalamy klasę manipulującą dla nowego wiersza
            result_matrix = np.vstack((result_matrix, new_result_matrix_row)) # dodanie wiersza do result_matrix
            last_added_index += 1
            # print('shape ', result_matrix.shape)

        return added_nodes_indices, result_matrix, last_added_index

    def change_node_for_lbp(self, manipulation_clas, nodes_to_change, batch_size, result_matrix):
        changed_nodes_indices = []
        manipulate_clas_index = self.get_manipulate_clas_index(manipulation_clas)
        if (nodes_to_change):
            for i in range(batch_size):
                try:
                    # node = self.pick_by_ranking(manipulation_clas, nodes_to_change, 0)
                    # node = self.pick_by_pagerank(manipulation_clas, nodes_to_change, 0)
                    # node = self.pick_random(manipulation_clas, nodes_to_change, 0)
                    node = self.pick_with_probability(manipulation_clas, nodes_to_change, 0)
                    nodes_to_change.remove(node)
                    node_index = self.get_index(node)
                    changed_nodes_indices.append(node_index)
                    result_matrix[node_index] = 0 # zerujemy cały wiersz danego węzła
                    result_matrix[node_index, manipulate_clas_index] = 1 # ustawiamy 1 dla danego wezla (wiersza) w kolumnie klasy manipulowanej
                except Exception:
                    print('cannot remove, probably empty array')
        return changed_nodes_indices

    def print_matrix(self, matrix):
        rows,cols = matrix.shape
        for row in range(rows):
            print(matrix[row])

    def reset_adjacency_matrix_for_removed_nodes(self, adjacency_matrix, removed_nodes_indices):
        for index in removed_nodes_indices:
            adjacency_matrix[index] = 0

    def reset_result_matrix_for_removed_nodes(self, result_matrix, removed_nodes_indices):
        for index in removed_nodes_indices:
            result_matrix[index] = 0

    def reset_result_matrix_for_changed_nodes(self, result_matrix, changed_nodes_indices, manipulation_clas):
        manipulate_clas_index = self.get_manipulate_clas_index(manipulation_clas)
        for index in changed_nodes_indices:
            result_matrix[index] = 0
            result_matrix[index, manipulate_clas_index] = 1

    def reset_result_matrix_for_added_nodes(self, result_matrix, added_nodes_indices, manipulation_clas):
        manipulate_clas_index = self.get_manipulate_clas_index(manipulation_clas)
        for index in added_nodes_indices:
            # print('reset_result_matrix_for_added_nodes ', result_matrix.shape)
            # print('result_matrix[index] ', result_matrix[index])
            result_matrix[index] = 0
            result_matrix[index, manipulate_clas_index] = 1

    def get_index(self, node):
        i = 0
        for n in self.G.nodes():    
            if (n == node):
                return i
            i +=1
        return 0