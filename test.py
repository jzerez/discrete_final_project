import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import copy

"""
Greedy alg for finding articulation points
1) For every vertex v, do following
…..a) Remove v from graph
..…b) See if the graph remains connected (We can either use BFS or DFS)
…..c) Add v back to the graph
"""
def findArticulations(graph):
    """
    This function returns all nodes within a graph considered
    to be articulation nodes, nodes that if deleted would result
    in a disconnected graph.
    """
    articulationPoints = []
    for i in graph.nodes:
        tempGraph = copy.deepcopy(graph)
        tempGraph.remove_node(i)
        if not nx.is_connected(tempGraph):
            articulationPoints.append(i)

    return articulationPoints


def findLargestClique(graph):
    """

    """
    return
# Create a watts and strogatz graph. Creates a ring of 10 nodes, connected to their 3 nearest neighbors. there is a 0.4 probabilty that any edge will be re-wired.
G = nx.generators.random_graphs.connected_watts_strogatz_graph(10, 3, 0.4, seed=420)
#tempGraph = copy.deepcopy(G)
#tempGraph.remove_node(0)

# plt.figure("tempGraph")
# nx.draw_circular(tempGraph, with_labels=True)
# plt.figure("G")
# nx.draw_circular(G, with_labels=True)
# plt.show()

print(findArticulations(G))
