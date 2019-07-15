#!/usr/bin/env python3

"""
    Etsuji Tomita, Akira Tanaka, Haruhisa Takahashi,
       
       "The worst-case time complexity for generating all maximal
       cliques and computational experiments",
       
       *Theoretical Computer Science*, Volume 363, Issue 1,
       Computing and Combinatorics,
       
       10th Annual International Conference on
       
       Computing and Combinatorics (COCOON 2004), 25 October 2006, Pages 28--42
       
       <https://doi.org/10.1016/j.tcs.2006.06.015>
"""

import sys
import time
import networkx as NX

Q = set()
CLIQUE = set()

def expand(G, SUBG, CAND):

    global Q
    global CLIQUE

    if len(SUBG) == 0:
        if len(Q) > len(CLIQUE):
            CLIQUE = Q.copy()
    else:

        u = max(SUBG, key=lambda u: len(CAND & set(G.neighbors(u))))

        while len(CAND - set(G.neighbors(u))) > 0:

            q = (CAND - set(G.neighbors(u))).pop()

            Q = Q | {q}

            SUBGq = SUBG & set(G.neighbors(q))
            CANDq = CAND & set(G.neighbors(q))

            expand(G, SUBGq, CANDq)

            CAND = CAND - {q}
            
            Q = Q - {q}

def max_clique(G):

    global Q

    nodes = G.nodes()

    # Order nodes by its degree
    nodes = list(map(lambda x: (x, G.degree(x)), nodes))
    nodes = sorted(nodes, key=lambda x: x[1], reverse=True)
    nodes = list(map(lambda x: x[0], nodes))

    print("max-clique - nodes: {}".format(nodes))

    for v in nodes:

        if G.degree(v) >= len(CLIQUE):

            print("node: {}".format(v))

            subn = set(G.neighbors(v)) | {v}

            Q.clear()

            expand(G, subn, subn)

def test_graph(G):

    start = time.time()
    max_clique(G)
    end = time.time()

    print("Result: {}, size: {}".format(CLIQUE, len(CLIQUE)))
    
    delta_own = end - start

    start = time.time()
    nx_clique = NX.graph_clique_number(G)
    end = time.time()

    print("Size NX: {}".format(nx_clique))

    delta_nx = end - start

    print("Time - Own: {}, NX: {}".format(delta_own, delta_nx))

def load_graph(path):

    edges = []

    with open(path) as f:
        lines = f.readlines()

    edges = list(map(lambda x: tuple(x.strip("\n").split(" ")), lines))
    edges = list(map(lambda y: (int(y[0]), int(y[1])), edges))

    g = NX.Graph()
    g.add_edges_from(edges)

    return g

def main():

    # Tests
    if len(sys.argv) <= 1:
        g = NX.complete_graph(10)
        test_graph(g)
        return
    
    # Load a graph
    g = load_graph(sys.argv[1])
    test_graph(g)

if __name__ == "__main__":
    main()

