# Maximal Clique Finding
## MTH2110 Final Project
*Jack Mao, Sander Miller, Jonathan Zerez*

*Fall, 2020*

## Introduction
Cliques are fully connected subgraphs of a larger graph. If you imagine a social network, if there is a friend-group where each person within the group is friends with every other person in the group, then that friend-group would be called a clique. A clique is considered to be maximal if no additional nodes can be added to the subgraph while keeping the subgraph a clique.

Finding cliques and maximal cliques has a lot of real world applications, for exampled **[INSERT EXAMPLE HERE]** and is generally a really interesting problem to solve.

In our project, we focused on implementing a number of different techniques to find the maximal cliques within a given graph G. We started off with a brute force algorithm that processes each and every possible unique subgraph and checks whether or not it is a maximal clique. From there, we implemented a few different versions of the Bron-Kerbosch algorithm, a recursive backtracking algorithm that is able to find the maximal cliques of a graph much more efficiently than a brute force method.

## Real life Examples of Cliques


## Explanation of Algorithm
The Bron-Kerbosch algorithm is a recursive backtracking algorithm that is able to return the maximal cliques of a graph `G` in **ADD RUNTIME** time. This section will detail how the algorithm works and more importantly, why it works.

We begin by defining three sets of nodes, `R`, `P` and `X`. These sets are defined to be completely disjoint from each other, meaning that an element found in one set must not also be found in any of the other sets, and will contain various nodes of the graph `G`.

* `R` is defined as the set that contains nodes that are **certainly** contained within the current maximal clique that is being considered
* `P` is defined as the set that contains nodes that **might** be contained within the current maximal clique that is being considered
* `X` is defined as the set that contains nodes that are **definitely not** contained within the current maximal clique that is being considered

The pseudocode for the algorithm looks something like this, where `N(n)` returns the set of nodes that are neighbors of node `n`:
```
Bron_Kerbosch(R, P, X):
  if P is empty AND X is empty:
    return R as a maximal clique

  for each node n in P:
    Bron_Kerbosch(R + n, P ∩ N(n), X ∩ N(n))
    P = P - n
    X = X + n
```

At the highest level, this pseudocode is essentially saying, "*for each node in a graph `G`, find a maximal clique that contains that node*". We will now explain why that is the case in more detail.

For the sake of convenience, we will consider graph `G` to be the graph below. There may be nodes other than `a`, `b`, `c`, and `d`, but we will only iterate over these nodes for the sake of simplicity. We will call the set of all nodes `Q`

**[INSERT GRAPH IMAGE HERE]**

When the function is first called, `R` and `X` are empty since we have not explored any nodes and therefore cannot definitively say whether any particular node is or is not in the maximal clique. Therefore `P` is set equal to `Q` as we are unsure about all of the nodes included in the current maximal clique. We set `n = a`, as `a` is the first element of `P`. Supposing that this node is part of a maximal clique, we will call the algorithm again, but this time, `a` will be a member of `R`. Because the nodes in a clique must be connected to every other node in a clique, the new set of possible clique nodes, `P`, is set to the intersection between `P` and the neighbors of `a`, `N(a)`. By the definition of a clique, all member nodes must be neighbors of every other node, therefore all possible clique members must be a neighbor of `a`. We find the intersection between `X` and `N(a)` for similar reasons: `X` only needs to keep track of nodes that are definitely not in the clique or nodes that have already shared a maximal clique with the current node.

So when we call `Bron_Kerbosch` for the second time, we find that `R = {a}`, `P = Q  ∩ N(a) = N(a) = {b,c}`, and `X = {}`. Now our goal is to find the maximal cliques of the graph that certainly contain `a` and could potentially contain `b` and `c`. We iterate through the nodes of `P` again, this time,  `n = b`. We call the function yet again.

In the third call to the function, `R = {a,b}`, `P = {c}` and `X = {}`. Now our goal is to find the maximal cliques of the graph that certainly contain `a` and `b`, and could potentially contain `c`. We iterate through the nodes of `P` again, this time, `n = c`. We finally call the function again.

In this fourth call to the function, `R = {a,b,c}`, `P = {}` and `X = {}`. When the function is called again, we find that both `P` and `X` are empty, so `R = {a,b,c}` is returned as a maximal clique. Checking with the graph visually, we find that this is indeed a maximal clique of the graph!

We now go back up to the third call of the function, when `R = {a,b}`, `P = {c}` and `X = {}`. We already chose to iterate on `c`, so now we remove `c` from `P` and add `c` to `X`. We leave the function with `R = {a,b}`, `P = {}` and `X = {c}`. The function now ends and we don't return anything.

We now go back up to the second call of the function, when `R = {a}`, `P = {b,c}`, and `X = {}`. Previously, `n = b`, so we'll add `b` to `X` and take `b` out of `P`. We'll then run the algorithm again with `n = c`.

Now, we're in the fifth call of the function at depth ##. `R = {a,c}`, `P = {}`, and `X = {b}`. In this case, there are no nodes in `P` to iterate over, and so the function ends and we don't return anything.

We're now back in the second call of the function at depth ##. `R = {a}`, `P = {c}`, and `X = {c}`. Because `n = c`, we remove `c` from `P` and add it to `X`. Now, because there are no nodes in `P` to iterate over the function ends and we don't return anything.

Finally, we go back up to the first call of the function at depth ##. `R = {}`, `P = {a,b,c}` and `X = {}`. Because `n = a`, we will remove `a` from `P` and add it to `X`. Now `R = {}`, `P = {b,c}` and `X = {a}`. We have successfully found a maximal clique that contains `a`. Now the algorithm will continue in a similar manner to find the maximal cliques that contain `b`, then `c`, and so on.

<!-- <img src="https://latex.codecogs.com/gif.latex?O_t=\text { Onset event at time bin } t " />  -->

## Bron_Kerbosch with Pivot

In the previous algorithm, we essentially iterated through all of the nodes in g given graph `G`. Although this will definitively give you all of the maximal cliques in `G`, the implementation repeats itself by checking for nodes that we know to have been in a maximal clique. To optimize our algorithm, we introduce an idea called a pivot. Given the same conditions in the previous implementation of Bron_Kerbosch algorithm, we define a pivot as an arbitrary node chosen from the union of the sets `P` and `X`, which we call `PUX`. In our implementation, we simply chose the first element in `PUX`, which we designate as `u`.

The new algorithm starts off the same way as the previous algorithm by checking if `P` and `X` are both empty. If this is true, then we return `R` as a maximal clique. If this is not true, we carry on with our algorithm by assigning our pivot. Then, we iterate through every node in `P - N(u)`. Let's call the first node in this iteration `v`. We recursively call the algorithm, except we set `R` to `R` union `v`, `P` to `P` intersection `N(v)`, and `X` to `X` intersection `N(v)`. After the recursion, we remove `v` from `P` and add it to `X`.    

**Insert Pseudocode/Image Here**

## Resources
* [An Overview of Algorithms for Network Survivability](https://www.hindawi.com/journals/isrn/2012/932456/)
* [https://www.math.arizona.edu/~glickenstein/math443f14/sadeghi.pdf](Survivable Network Design with Vertex and Edge Connectivity Constraints)
* [Tutorialspoint Cut set and cut vertex of graph](https://www.tutorialspoint.com/cut-set-and-cut-vertex-of-graph)
* [An efficient algorithm for cut vertex detection in wirelss sensor networks](https://ieeexplore.ieee.org/document/5541668)
* [Review of the Bron-Kerbosch algorithm and variations](https://arxiv.org/pdf/1605.03871.pdf)

## Previous Resources (Stochastic Graph Traversal)
* [Proof of Dijstra's correctness](https://web.engr.oregonstate.edu/~glencora/wiki/uploads/dijkstra-proof.pdf)
* [Another proof of Dijkstra's](https://www.cs.auckland.ac.nz/software/AlgAnim/dij-proof.html)
* [Learning to Solve Stochastic Shortest Path Problems](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.85.3901&rep=rep1&type=pdf)
* [Stochastic Graph Exploration](http://aris.me/pubs/stochastic-graph-exploration.pdf)
* [Generic Algorithm for approximating solutions to stochastic shortest path](https://link.springer.com/chapter/10.1007/978-3-642-04944-6_8)

### Meeting Notes 11/29
* Spend monday's class getting familair with the problem of stochastic graphs. What are they? What are real life things that they can model? Are there closed form solutions to finding the shortest path through one?
* Ditch the car analogy for now. To start, we will create an arbitrary stochastic graph in networkx with a small number of nodes and edges for more manageable testing
* Talk through our project with Sarah to ensure that we are on a good path and that there is good rigourous math to be had. Also see if she has any suggestions
* Use Jupyter notebooks with atom or vscode for the project and writeup

### Schedule
* 12/6 Finish implementing bk algorithm
* 12/7 Write a proof of why bk algorithm works + ask sarah about the slides/video
* 12/9 Applications of clique finding alg
* 12/16 Final Presentation12 Day (3:05pm)
* 12/17 Project Document Due (7:00pm)
