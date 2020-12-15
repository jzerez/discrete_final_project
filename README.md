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

For the sake of convenience, we will consider graph `G` to be the graph below. There may be nodes other than `a`, `b`, `c`, and `d`, but we will only iterate over these nodes for the sake of simplicity. We will suppose that there is a fully connected subgraph `Z` within `G` where each node in `Z` is connected to `c`. We will call the set of all nodes `Q`

![img](./images/base_graph.png)

When the function is first called, `R` and `X` are empty since we have not explored any nodes and therefore cannot definitively say whether any particular node is or is not in the maximal clique. Therefore `P` is set equal to `Q` as we are unsure about all of the nodes inclusion in the current maximal clique. We set `n = a`, as `a` is the first element of `P`. Supposing that this node is part of a maximal clique, we will call the algorithm again, but this time, `a` will be a member of `R`. Because the nodes in a clique must be connected to every other node in a clique, the new set of possible clique nodes, `P`, is set to the intersection between `P` and the neighbors of `a`, `N(a)`. By the definition of a clique, all member nodes must be neighbors of every other node, therefore all possible clique members must be a neighbor of `a`. We find the intersection between `X` and `N(a)` for similar reasons: `X` only needs to keep track of nodes that are definitely not in the clique but that *could* be. In other words, it doesn't make sense for `X` to keep track of nodes that are obviously not members of the clique.

So when we call `Bron_Kerbosch` for the second time, dropping down to recursion depth 2, we find that `R = {a}`, `P = Q  ∩ N(a) = N(a) = {b,c}`, and `X = {}`. Now our goal is to find the maximal cliques of the graph that certainly contain `a` and could potentially contain `b` and `c`. We iterate through the nodes of `P` again, this time,  `n = b`. We call the function yet again.

In the third call to the function at recursion depth 3, `R = {a,b}`, `P = {c}` and `X = {}`. Now our goal is to find the maximal cliques of the graph that certainly contain `a` and `b`, and could potentially contain `c`. We iterate through the nodes of `P` again, this time, `n = c`. We finally call the function again.

In this fourth call to the function at recursion depth 4, `R = {a,b,c}`, `P = {}` and `X = {}`. When the function is called again, we find that both `P` and `X` are empty, so `R = {a,b,c}` is returned as a maximal clique. Checking with the graph visually, we find that this is indeed a maximal clique of the graph!

To see the steps to recurse back up the graph, see [Appendix A](#Appendix-A).

Once the program has recursed back to the first call of the algorithm, we find that `R = {}`, `P = {b,c,d,z}` and `X = {a}`. The algorithm will run again, this time starting with `n = b` to find a maximal clique that contains `b`, but does not contain `a`. This happens to be the set `{b,d}`. This demonstrates why nodes `b` and `c` cannot immediately be added to `X`, despite being members of the first maximal clique found, `{a,b,c}`

Once the program recurses back to the first call of the algorithm again after finding a maximal clique that contains `b`, but not `a`, we find that `R = {}`, `P = {c,d,z}` and `X = {a,b}`. The algorithm will run again, this time starting with `n = c` to find the maximal clique that contains `c`, but does not contain `b` or `a`. This happens to be the set `{c,z}`, again, demonstrating that nodes can only be added to `X` one at a time. To assign all nodes from a found maximal clique to `X` would risk missing the opportunity to identify additional maximal cliques.

For a full visual demonstration of the recursive steps that the BK algorithm takes, see [Appendix B](#Appendix-B).

### Appendix A
#### Reverse Recursion to the top of the call stack
We now go back up to the third call of the function at recursion depth 3, when `R = {a,b}`, `P = {c}` and `X = {}`. We already chose to iterate on `c`, so now we remove `c` from `P` and add `c` to `X`. We leave the function with `R = {a,b}`, `P = {}` and `X = {c}`. The function now ends and we don't return anything.

We now go back up to the second call of the function at recursion depth 2, when `R = {a}`, `P = {b,c}`, and `X = {}`. Previously, `n = b`, so we'll add `b` to `X` and take `b` out of `P`. We'll then run the algorithm again with `n = c`.

Now, we're in the fifth call of the function at depth 3. `R = {a,c}`, `P = {}`, and `X = {b}`. In this case, there are no nodes in `P` to iterate over, and so the function ends and we don't return anything.

We're now back in the second call of the function at depth 2. `R = {a}`, `P = {c}`, and `X = {c}`. Because `n = c`, we remove `c` from `P` and add it to `X`. Now, because there are no nodes in `P` to iterate over the function ends and we don't return anything.

Finally, we go back up to the first call of the function at depth 1. `R = {}`, `P = {a,b,c}` and `X = {}`. Because `n = a`, we will remove `a` from `P` and add it to `X`. Now `R = {}`, `P = {b,c}` and `X = {a}`. We have successfully found a maximal clique that contains `a`. Now the algorithm will continue in a similar manner to find the maximal cliques that contain `b`, then `c`, and so on.

### Appendix B
#### Visual demonstration of BK algorithm
For a full graphical representation of the steps that the BK algorithm takes while it is running, please refer to the following pdf. Note that nodes in set `R` are colored in green, nodes in set `P` are colored in blue, and nodes in set `X` are colored in red. Nodes with heavy outlines are nodes that are chosen from `P`. 

<object data="./assets/BK-step-by-step.pdf" type="application/pdf" width="700px" height="700px">
    <embed src="http://yoursite.com/BK-step-by-step.pdf">
        <p>This browser does not support PDFs. Please download the PDF to view it: <a href="http://yoursite.com/the.pdf">Download PDF</a>.</p>
    </embed>
</object>

<!-- <img src="https://latex.codecogs.com/gif.latex?O_t=\text { Onset event at time bin } t " />  -->

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
