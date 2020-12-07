import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pdb

def bk(g, r,p,x, depth=0):
    """
    Bron-Kerbosch with pivots
    g: graph
    r: disjoint set of vertices of graph g
    p: disjoint set of vertices of graph g
    x: disjoint set of vertices of graph g
    """

    if not p and not x:
        print('THIS IS WHAT IT IS:')
        print(r)

    while p:
        node = p.pop()
        neighbors = list(g.neighbors(node))
        n = len(neighbors)
        bk(g, r.union([node]), p.intersection(neighbors), x.intersection(neighbors), depth=depth+1)
        x = x.union([node])


# G = nx.generators.random_graphs.connected_watts_strogatz_graph(10, 3, 0.4, seed=420)
G = nx.generators.classic.complete_graph(3)
G.add_node(3)
G.add_edge(2,3)
nx.draw_circular(G, with_labels=True)

bk(G, set([]), set(G.nodes), set([]))

plt.show()
