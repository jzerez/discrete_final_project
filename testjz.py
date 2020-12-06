import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pdb

def bk(g, r,p,x):
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
        # print(p)
        node = p.pop()
        print(node)
        print(r, p, x)
        # print(r)
        neighbors = g.neighbors(node)
        # pdb.set_trace()
        # r.update([node])
        # p =  p.intersection(neighbors)

        bk(g, r.union([node]), p.intersection(neighbors).union([node]), x.intersection(neighbors))
        x = x.union([node])


G = nx.generators.random_graphs.connected_watts_strogatz_graph(10, 3, 0.4, seed=420)
# G = nx.generators.classic.complete_graph(5)
nx.draw_circular(G, with_labels=True)

bk(G, set([]), set(G.nodes), set([]))

plt.show()
