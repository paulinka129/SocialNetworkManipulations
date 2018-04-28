from __future__ import division
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import graphviz

def read_graph_from_gml_file():
    pass

def read_graph_from_txt_file():
    pass

def plot_homophily(homo_list, filename):
    num_bins = 10
    fig, ax = plt.subplots()
    ax.hist(homo_list, num_bins, density=1)
    ax.set_xlabel('homofilia')
    ax.set_ylabel('funkcja masy prawdopodobienstwa')
    fig.tight_layout()
    plt.savefig('figures/global/'+filename)


def plot_global_homophily(global_homophilies, filename):
    fig, ax = plt.subplots()
    ax.plot(range(1,len(global_homophilies)+1), global_homophilies)
    ax.set_xlabel('liczba usunietych wierzcholkow')
    ax.set_ylabel('homofilia globalna')
    plt.savefig('figures/global/'+filename)

def plot_local_homophily(homo_list_before, homo_list_after, filename):
    plt.style.use('seaborn-deep')
    bins = np.linspace(0, 1, 10)
    fig, ax = plt.subplots()

    ax.hist([homo_list_before, homo_list_after], bins, label=['before', 'after'], density=True)
    ax.set_xlabel('homofilia lokalna')
    ax.set_ylabel('funkcja masy prawdopodobienstwa')
    for i, v in enumerate(homo_list_before):
        strVal = str(v)
        ax.text(v + 3, i + .25,  str(strVal), horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
    # plt.hist(homo_list_before, bins, alpha=0.5, label='before')
    # plt.hist(homo_list_after, bins, alpha=0.5, label='after')
    ax.legend(loc='upper left')
    plt.savefig('figures/local/'+filename)

def read_node_list():
    node_dict = {}
    with open('datasets/amd_network_class.txt', "r") as f:
        for line in f:
            node_class = line.split()
            node_dict[node_class[0]] = node_class[1]
    return node_dict

def read_edge_list():
    edge_dict = []
    with open('datasets/amd_network_network.txt', "r") as f:
        for line in f:
            edge_class = line.split()
            edge_dict.append((edge_class[0], edge_class[1]))
    return edge_dict


def write_gml_file(node_dict, edge_dict):
    with open('datasets/amd_network_class.gml', "w") as f:
        f.write('Creator ' + '"Paulina Brzechffa"' +"\n")
        f.write('graph [' +"\n")
        f.write('  multigraph 1' +"\n")
        for val in node_dict:
            f.write('  node [' +"\n")
            f.write('    id ' + val +"\n")
            f.write('    label ' + val +"\n")
            f.write('    value ' + '"{}"'.format(node_dict[val]) +"\n")
            f.write('  ]' +"\n")
        print edge_dict
        for val in edge_dict:
            f.write('  edge [' +"\n")
            f.write('    source ' + val[0] +"\n")
            f.write('    target ' + val[1] +"\n")
            f.write('  ]' +"\n")
        f.write(']')

def save_to_file(results, filename):
    with open('results/'+filename, "w") as f:
        for s in results:
            f.write(str(s) +"\n")

def read_from_file(filename):
    results = []
    with open('results/'+filename, "r") as f:
        for line in f:
            results.append(float(line.strip()))
    return results