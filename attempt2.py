import networkx as nx
from networkx.algorithms.approximation import min_weighted_dominating_set, min_edge_dominating_set
from parse import read_input_file, write_output_file
from utils import is_valid_network, average_pairwise_distance, average_pairwise_distance_fast
import sys
import matplotlib.pyplot as plt
import queue
import os


def solve(G):
    """
    Args:
        G: networkx.Graph

    Returns:
        T: networkx.Graph
    """
    #access node k attribute with Bi.nodes[k]
    #access weight of edge (u, v) with G[u][v]['weight']

    Bi = nx.Graph()
    N = G.order()
    for node in G.nodes():
        Bi.add_node(node, **{'bipartite': 0})
        Bi.add_node(node + N, **{'bipartite': 1})
        Bi.add_edge(node, node+N, weight=0)

    for edge in G.edges:
        u = edge[0]
        v = edge[1]
        Bi.add_edge(u, v + N, weight=G[u][v]['weight'])
        Bi.add_edge(v, u + N, weight=G[u][v]['weight'])


    maxVdegree = maxDegree(Bi)

    pq = queue.PriorityQueue()
    pq.put(maxVdegree)
    minCDS = []

    while isBipartite(Bi):
        u = pq.get()[1]
        neighbors = []
        for edge in Bi.edges(u):
            v = edge[1]
            neighbors.append(v)
        
        Bi.remove_nodes_from(neighbors + [u])
        

        for neighbor in neighbors:
            nodeVal = neighbor - N
            if nodeVal != u:
                degree = Bi.degree([nodeVal])[nodeVal]
                val = (degree, nodeVal)
                pq.put(val)

        minCDS.append(u)

    T = G.subgraph(minCDS)
    return T

def isBipartite(G):
    graphAttributes = nx.get_node_attributes(G, 'bipartite')
    for key in graphAttributes:
        if graphAttributes[key] == 1:
            return True
    return False

def maxDegree(G):
    """
    Input: Graph G

    Output: (d, v) where d is degree of vertex v, which is max degree
    """
    maxD = 0
    maxV = 0
    degrees = G.degree()
    for v_d in degrees:
        tempD = v_d[1]
        tempV = v_d[0]
        if maxD < tempD:
            maxD = tempD
            maxV = tempV
    return (maxD, maxV)



# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

if __name__ == '__main__':
    assert len(sys.argv) == 2
    path = sys.argv[1]
    G = read_input_file(path)
    T = solve(G)
    assert is_valid_network(G, T)
    print("Average  pairwise distance: {}".format(average_pairwise_distance(T)))
    write_output_file(T, 'out/test.out')