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
        bk(g, r.union([node]), p.intersection(neighbors), x.intersection(neighbors), depth=depth+1)
        x = x.union([node])


def bk_p(g,r,p,x, counter=0):
    """
    Bron-Kerbosch with pivots
    """
    pux = p.union(x)
    if not pux:
        print(r)
        return r

    pivot = next(iter(pux))
    neighborsP = list(g.neighbors(pivot))
    counter += 1
    for v in p.difference(neighborsP):
        neighborsV = list(g.neighbors(v))
        bk_p(g, r.union([v]), p.intersection(neighborsV), x.intersection(neighborsV), counter)
        p.remove(v)
        x.add(v)



# G = nx.generators.random_graphs.connected_watts_strogatz_graph(10, 5, 0.2, seed=420)
# G = nx.generators.classic.complete_graph(3)
G = nx.generators.classic.wheel_graph(5)
# G.add_node(3)
# G.add_edge(2,3)
nx.draw_circular(G, with_labels=True)


bk(G, set([]), set(G.nodes), set([]))
bk_p(G, set([]), set(G.nodes), set([]))
plt.show()
