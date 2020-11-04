import networkx as nx
from networkx.algorithms.approximation import min_weighted_dominating_set, min_edge_dominating_set
from parse import read_input_file, write_output_file
from utils import is_valid_network, average_pairwise_distance
import sys
import matplotlib.pyplot as plt
import os

def solve(G):
    """
    Args:
        G: networkx.Graph

    Returns:
        T: networkx.Graph
    """

    # Right now attempt is to make an MST of the graph and take out heaviest edges that won't violate conditions for T
    # Issue right now is that nodeDegrees stays up to date with vertex Degree so can't handle more complicated Graph
    # Going to try and solve tomorrow is to get a fixed number for degree at start of MST.

    N = G.number_of_nodes()
    for node in G.nodes:
        if G.degree[node] == N - 1:
            T = nx.Graph()
            T.add_node(node)
            return T
    T = nx.minimum_spanning_tree(G)
    nodeNumbers = [i for i in range(N)]
    nodeDegrees = T.degree(nodeNumbers)
    degOfT = [k[1] for k in nodeDegrees]
    edges = sorted(T.edges(data=True), key=lambda t: t[2].get('weight', 1))[::-1]

    nx.draw(T, with_labels=True)
    #plt.savefig("pathT.png")
    plt.clf()

    for edge in edges:
        u = edge[0]
        v = edge[1]
        uDegree = degOfT[u]
        vDegree = degOfT[v]

        if uDegree > 1 and vDegree < 2:
            T.remove_node(v)
        elif uDegree < 2 and vDegree > 1:
            T.remove_node(u)

    nx.draw(T, with_labels=True)
    #plt.savefig("pathT'.png")
    return T



# if __name__ == '__main__':
#     assert len(sys.argv) == 2
#     path = sys.argv[1]
#     G = read_input_file(path)
#     T = solve(G)
#     assert is_valid_network(G, T)
#     print("Average  pairwise distance: {}".format(average_pairwise_distance(T)))
#     write_output_file(T, 'out/test.out')


# Usage: python3 multi-solve.py inputs
if __name__ == '__main__':
    assert len(sys.argv) == 2
    directory = sys.argv[1]
    for filename in sorted(os.listdir(directory), reverse = True):
        path = os.path.join(directory, filename)
        name = filename[:-3]

        print("SOLVING FOR INPUT: {}".format(name))
        G = read_input_file(path)
        T = solve(G)
        assert is_valid_network(G, T)

        print("Average  pairwise distance for input {}: {}".format(name,average_pairwise_distance(T)))
        write_output_file(T, 'out/{}.out'.format(name))




