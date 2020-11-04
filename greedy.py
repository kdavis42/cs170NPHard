import networkx as nx
from networkx.algorithms.approximation import min_weighted_dominating_set, min_edge_dominating_set
from parse import read_input_file, write_output_file
from utils import is_valid_network, average_pairwise_distance, average_pairwise_distance_fast
import sys
import matplotlib.pyplot as plt
import queue
import os
import copy
from collections import deque

def solve(G):

	# nx.draw(G, with_labels=True)
	# plt.savefig("pathT.png")
	# plt.clf()	

	#At beginning, do basic check to see if any node has degree n-1?

	#Step 1: Get node with maximum degree
	start = sorted(dict(G.degree).items(), key=lambda x: x[1], reverse=True)[0][0]
	min_nodes = {start}

	#Step 2: Get neighbors of start, descending order of degree
	neighbors = G.neighbors(start)
	sorted_neighbors = sorted(G.degree(neighbors), key=lambda x: x[1], reverse=True)
	sorted_neighbors = [s[0] for s in sorted_neighbors]

	pq = deque(sorted_neighbors)
	curr_set = set(sorted_neighbors + [start])

	while pq: #Go through every node in PQ
		node = pq.pop()

		new_graph = copy.deepcopy(G)
		new_graph.remove_node(node)

		if len(new_graph)!=0 and nx.is_connected(new_graph): #Not needed
			G.remove_node(node)
		else: #Add node to set, add it's neighbords to PQ
			min_nodes.add(node)
			new_neighbors = set(G.neighbors(node)) - curr_set
			sorted_new_neighbors = sorted(G.degree(new_neighbors), key=lambda x: x[1], reverse=True)
			sorted_new_neighbors = [s[0] for s in sorted_new_neighbors]

			pq.extend(sorted_new_neighbors)
			curr_set.update(sorted_new_neighbors)

	sol = G.subgraph(min_nodes)

	# print(min_nodes)
	# nx.draw(sol, with_labels=True)
	# plt.savefig("pathT'.png")

	return sol

#Use this if you want to run on just one input
#python3 greedy.py test2.in
# if __name__ == '__main__':
#     assert len(sys.argv) == 2
#     path = sys.argv[1]
#     G = read_input_file(path)
#     T = solve(G)
#     #assert is_valid_network(G, T)
#     print("Average  pairwise distance: {}".format(average_pairwise_distance(T)))
#     write_output_file(T, 'out/test.out')

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