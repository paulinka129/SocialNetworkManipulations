from __future__ import division
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import graphviz

def plot_local_homophily(homo_list_before, homo_list_after, filename):
    num_bins = 10
    fig, ax = plt.subplots()
    ax.hist(homo_list_before, num_bins, density=1)
    ax.set_xlabel('homofilia lokalna')
    ax.set_ylabel('funkcja masy prawdopodobienstwa')
    fig.tight_layout()
    plt.savefig('figures/local/'+filename)


def plot(homo_list_before, homo_list_after, filename):
    plt.style.use('seaborn-deep')
    bins = np.linspace(0, 1, 10)

    plt.hist([homo_list_before, homo_list_after], bins, label=['before', 'after'])

    # plt.hist(homo_list_before, bins, alpha=0.5, label='before')
    # plt.hist(homo_list_after, bins, alpha=0.5, label='after')
    plt.legend(loc='upper left')
    plt.savefig('figures/local/'+filename)

def read_graph_from_gml_file():
    pass

def read_graph_from_txt_file():
    pass
        