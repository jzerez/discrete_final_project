# Bron–Kerbosch algorithm
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import copy
import pdb



# the max independent set in complement of graph G is a maximal clique in G
def bruteForce(g):
    """
    g: a nx graph

    This is a brute force algorithm that finds all of the subgraphs of g and checks
    if the subgraph is a clique. This is super inefficient
    """
    subGraphs = getSubgraphs(g)
    cliques = []
    for subGraph in subGraphs:
        if isComplete(subGraph):
            cliques.append(subGraph)
    return findMaximalCliques(cliques)



def getSubgraphs(g):
    """
    g: a nx graph

    This is a helper function that finds all of the subgraphs in g
    """
    subgraphs = []
    numSubgraphs = 2**len(g)-1
    for i in range(numSubgraphs):
        binaryString = str(bin(i)[2:])
        # sign extend
        binaryString = "0" * (len(g) - len(binaryString)) + binaryString
        tempG = copy.deepcopy(g)
        for j, character in enumerate(binaryString):
            if character == '0':
                tempG.remove_node(j)
        subgraphs.append(tempG)

    return subgraphs

def isComplete(g):
    """
    g: a nx graph

    Big brain way to see if a graph is complete. You use handshake theorem
    to calculate the number of edges in a complete graph and compare it with
    the number of edges in g.
    """
    e = g.number_of_edges()
    n = g.number_of_nodes()
    return e==n*(n-1)/2

def findMaximalCliques(cliques):
    """
    cliques: takes in a list of all cliques (type nx graph) of a graph G.

    Note that this function is garbage if used on a random list of graphs
    """
    results = copy.deepcopy(cliques)

    nodeSets = [set(clique.nodes) for clique in cliques]
    pdb.set_trace()
    for i, nodeSet1 in enumerate(nodeSets[:-1]):
        print(nodeSet1)
        for j in range(i+1, len(cliques)):
            nodeSet2 = nodeSets[j]
            allNodes = nodeSet1.union(nodeSet2)
            if allNodes == nodeSet1:
                results.remove(cliques[j])
            elif allNodes == nodeSet2:
                results.remove(cliques[i])

    print(results)
    return results
def bk(r,p,x):
    """
    r: disjoint set of vertices of graph g
    p: disjoint set of vertices of graph g
    x: disjoint set of vertices of graph g
    """
    return

# print([g.nodes for g in getSubgraphs(G)])
# G = nx.generators.random_graphs.connected_watts_strogatz_graph(10, 3, 0.4, seed=420)
G = nx.generators.classic.complete_graph(3)

plt.figure("G")
subgraphs = bruteForce(G)[0]
nx.draw_circular(subgraphs, with_labels=True)
plt.show()
# for subgraph in subgraphs:
#     plt.figure()
#     nx.draw_circular(subgraph, with_labels=True)
# plt.show()
