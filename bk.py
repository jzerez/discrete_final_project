# Bron–Kerbosch algorithm
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import copy
import pdb


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
    numSubgraphs = 2**len(g)

    for i in range(numSubgraphs):
        # look, we're using bitstrings!
        binaryString = str(bin(i)[2:])
        # pad the bitstring with leading zeros
        binaryString = "0" * (len(g) - len(binaryString)) + binaryString
        tempG = copy.deepcopy(g)
        # Remove nodes corresponding to zeros in the bit string
        for j, character in enumerate(binaryString):
            if character == '0':
                tempG.remove_node(j)
        subgraphs.append(tempG)

    return subgraphs

def isComplete(g):
    """
    g: a nx graph

    Check if a graph is complete. You use handshake theorem to calculate the
    number of edges in a complete graph and compare it with the number of edges
    in g.
    """
    e = g.number_of_edges()
    n = g.number_of_nodes()
    return e==n*(n-1)/2

def findMaximalCliques(cliques):
    """
    cliques: takes in a list of all cliques (type: nx graph) of a graph G.

    Returns the list of  maximal cliques (ie: prunes out non-maximal cliques)
    """
    results = np.array(copy.deepcopy(cliques))
    indsToRemove = set([])
    nodeSets = [set(clique.nodes) for clique in cliques]

    # compare every clique to every other clique
    for i, nodeSet1 in enumerate(nodeSets[:-1]):
        for j in range(i+1, len(cliques)):
            nodeSet2 = nodeSets[j]
            allNodes = nodeSet1.union(nodeSet2)

            # check to see if one clique is fully contained in another
            if allNodes == nodeSet1:
                indsToRemove.add(j)
            elif allNodes == nodeSet2:
                indsToRemove.add(i)

    # Remove non-maximal cliques
    return np.delete(results, np.array(list(indsToRemove)))

def bk(g,r,p,x, depth=0):
    """
    Bron-Kerbosch algorithm without pivots
    g: an nx graph
    r: disjoint set of vertices of graph g
    p: disjoint set of vertices of graph g
    x: disjoint set of vertices of graph g
    """
    # if p and x are empty:
    if not p and not x:
        print('Maximal Clique found: ', r)

    while p:
        # choose and remove a node from p
        node = p.pop()
        neighbors = list(g.neighbors(node))
        bk(g, r.union([node]), p.intersection(neighbors), x.intersection(neighbors), depth=depth+1)
        x = x.union([node])

def bk_p(g,p,r,x, counter):
    """
    Bron-Kerbosch algorithm without pivots
    g: an nx graph
    r: disjoint set of vertices of graph g
    p: disjoint set of vertices of graph g
    x: disjoint set of vertices of graph g
    """
    print("counter:\t", counter)
    print("p:\t", p)
    print("r:\t", r)
    print("x:\t", x)
    result = []
    pux = set(p).union(set(x))
    if len(pux) == 0:
        print("return r: ", r)
        return r
    else:
        pivot = list(pux)[0]
        pN = [n for n in g.neighbors(pivot)]
        p_copy = copy.deepcopy(p)
        print("P_COPY",p_copy)
        print("P_N",pN)
        for n in pN:
            p_copy.remove(n)
        for v in p_copy:
            print("v: ", v)
            vNeighbors = [a for a in g.neighbors(v)]
            print("vNeighbors: \t", vNeighbors)
            # pnnv, ruv, xnnv
            print("================================")
            result.append(bk_p(g, intersection(p,vNeighbors), r+[v], intersection(x, vNeighbors), counter+1))
            print("================================")
            print("result:\t", result, "\tv: ", v)
            p.remove(v)
            x.append(v)
            print("fp:\t", p)
            print("fr:\t", r)
            print("fx:\t", x)
    return result

    def bk_p2(g,r,p,x, counter=0):
        """
        Bron-Kerbosch algorithm without pivots (implemented with python sets)
        g: an nx graph
        r: disjoint set of vertices of graph g
        p: disjoint set of vertices of graph g
        x: disjoint set of vertices of graph g
        """
        pux = p.union(x)
        if not pux:
            print('Maximal clique found: ', r)

        # choose an pivot from pux
        pivot = next(iter(pux))
        neighborsP = list(g.neighbors(pivot))
        for v in p.difference(neighborsP):
            neighborsV = list(g.neighbors(v))
            bk_p(g, r.union([v]), p.intersection(neighborsV), x.intersection(neighborsV), counter+1)
            p.remove(v)
            x.add(v)

            
# print([g.nodes for g in getSubgraphs(G)])
# G = nx.generators.random_graphs.connected_watts_strogatz_graph(10, 3, 0.4, seed=420)
G = nx.generators.classic.complete_graph(5)

plt.figure("G")
subgraphs = bruteForce(G)[0]
nx.draw_circular(subgraphs, with_labels=True)
plt.show()
# for subgraph in subgraphs:
#     plt.figure()
#     nx.draw_circular(subgraph, with_labels=True)
# plt.show()
