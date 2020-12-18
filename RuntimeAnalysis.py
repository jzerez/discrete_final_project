#!/usr/bin/env python3
import timeit
import random
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import copy
import pdb
from functools import partial
import timeit
import numpy as np
from matplotlib import pyplot

def intersection(lst1,lst2): 
    return list(set(lst1) & set(lst2))

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
    numSubgraphs = 2**len(g)
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
    results = np.array(copy.deepcopy(cliques))
    indsToRemove = set([])
    nodeSets = [set(clique.nodes) for clique in cliques]

    for i, nodeSet1 in enumerate(nodeSets[:-1]):
        for j in range(i+1, len(cliques)):
            nodeSet2 = nodeSets[j]
            allNodes = nodeSet1.union(nodeSet2)

            if allNodes == nodeSet1:
                indsToRemove.add(j)
            elif allNodes == nodeSet2:
                indsToRemove.add(i)
    return np.delete(results, np.array(list(indsToRemove)))

def bk(g,r=set(),p=None,x=set(), depth=0):
    """
    Bron-Kerbosch with pivots
    g: graph
    r: disjoint set of vertices of graph g
    p: disjoint set of vertices of graph g
    x: disjoint set of vertices of graph g
    """
    if p == None:
        p = set(g.nodes)
    if not p and not x:
        return r

    while p:
        node = p.pop()
        neighbors = list(g.neighbors(node))
        bk(g, r.union([node]), p.intersection(neighbors), x.intersection(neighbors), depth=depth+1)
        x = x.union([node])


def bk_p(g,r = set(),p=None,x = set(), counter=0):
    """
    Bron-Kerbosch with pivots
    """
    if p == None:
        p = set(g.nodes)
    pux = p.union(x)
    if not pux:
        return r

    pivot = next(iter(pux))
    neighborsP = list(g.neighbors(pivot))
    counter += 1
    for v in p.difference(neighborsP):
        neighborsV = list(g.neighbors(v))
        bk_p(g, r.union([v]), p.intersection(neighborsV), x.intersection(neighborsV), counter)
        p.remove(v)
        x.add(v)



def plot_time(func, inputs, repeats, n_tests):
    """
    Run timer and plot time complexity of `func` using the iterable `inputs`.

    Run the function `n_tests` times per `repeats`.
    """
    #Create lists to capture x and y values for runtimes
    x, y= [], []

    for i in inputs:

        # Create the graph with i nodes
        gPath = nx.generators.classic.path_graph(i) #Path Graph
        #gWatts = nx.generators.random_graphs.connected_watts_strogatz_graph(i, round(.3*i), 0.4, seed=400) #Watts-Strogatz Graph
        #gComplete = nx.generators.classic.complete_graph(i) #Complete Graph
       
        #Time each function and save time
        timer = timeit.Timer(partial(func, gPath))
        t = timer.repeat(repeat=repeats, number=n_tests)
        x.append(i)
        y.append(np.mean(t))
   
    #Plot scaled runtime values
    pyplot.semilogy(x, y/y[0], '-o',label=func.__name__)

    #Add reference plots linear, n^2 and 2^n time
    if func.__name__ == "bk_p": 
         pyplot.plot(x,[n/x[0] for n in x], label = "n")
         pyplot.plot(x,[(n**2)/(x[0]**2) for n in x], label = "n^2")
         pyplot.plot(x,[(2**n)/(2**x[0]) for n in x], label = "2^n")
         
def plot_times(functions, inputs, repeats=3, n_tests=1, file_name=""):
    """
    Run timer and plot time complexity of all `functions`,
    using the iterable `inputs`.

    Run the functions `n_tests` times per `repeats`.

    Adds a legend containing the labels added by `plot_time`.
    """

    #Generate plots for each function
    for func in functions:
        plot_time(func, inputs, repeats, n_tests)
    
    #Plot all function runtimes
    pyplot.legend()
    pyplot.title("Bron-Kerbosch Algorithm Run Times Complete Graph")
    pyplot.xlabel("Number of Nodes")
    pyplot.ylabel("Time [s]")
    plt.show()
    if not file_name:
        pyplot.show()
    else:
        pyplot.savefig(file_name)
    
if __name__ == "__main__":

    #Plot BruteForce, BK, and BK w/ pivoting
    plot_times([bruteForce,bk, bk_p],
               range(3,10,2), repeats=3)
