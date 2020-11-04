import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_network, average_pairwise_distance, average_pairwise_distance_fast
import sys
import matplotlib.pyplot as plt
import os
import copy
from collections import deque

def solve(G):

	N = G.order()
	checkDegrees = G.degree()
	for d in checkDegrees:
		if d[1] == N - 1:
			oneNodeGraph = nx.Graph()
			oneNodeGraph.add_node(d[0])
			return oneNodeGraph

	V = set(G.nodes())
	F = set()
	copyG = G.copy()
	condition = V.difference(F)
	while condition:
		sortedDegrees = sorted(copyG.degree(condition), key=lambda x: x[1])
		u = sortedDegrees[0][0]
		diff = V.difference([u])
		connection = G.subgraph(diff)
		if nx.is_connected(connection):
			V.remove(u)
			neighbors = set(copyG.neighbors(u))
			copyG.remove_node(u)
			if neighbors.intersection(F) == set():
				maxNeighbor = max(copyG.degree(neighbors), key=lambda x: x[1])
				F.add(maxNeighbor[0])
		else:
			F.add(u)
		condition = V.difference(F)
	T = G.subgraph(V)
	return T

#Use this if you want to run on a folder of inputs
#python3 greedy.py inputs
if __name__ == '__main__':
    assert len(sys.argv) == 2
    directory = sys.argv[1]
    for filename in sorted(os.listdir(directory), reverse = True):
        path = os.path.join(directory, filename)
        name = filename[:-3]

        print("SOLVING FOR INPUT: {}".format(name))
        G = read_input_file(path)
        T = solve(G)
        #assert is_valid_network(G, T)
        #print("Average  pairwise distance for input {}: {}".format(name,average_pairwise_distance(T)))
        write_output_file(T, 'out/{}.out'.format(name))