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

CLIQUE = set()

def expand(G, K, cand, fini):

    global CLIQUE

    if len(cand) == 0 and len(fini) == 0:
        if len(K) > len(CLIQUE):
            CLIQUE = K.copy()
        return

    pivot = max(cand | fini, key=lambda u: len(cand & set(G.neighbors(u))))

    ext = cand - set(G.neighbors(pivot))

    for q in ext:

        Kq = K | {q}

        candq = cand & set(G.neighbors(q))
        finiq = fini & set(G.neighbors(q))

        cand = cand - {q}
        fini = fini | {q}

        expand(G, Kq, candq, finiq)

def max_clique(G):

    nodes = G.nodes()

    print("max-clique - nodes: {}".format(nodes))

    # Order nodes by its degree
    nodes = list(map(lambda x: (x, G.degree(x)), nodes))
    nodes = sorted(nodes, key=lambda x: x[1])
    nodes = list(map(lambda x: x[0], nodes))

    for v in nodes:

        if G.degree(v) >= len(CLIQUE):

            print("node: {}".format(v))

            subn = set(G.neighbors(v)) | {v}
            
            expand(G, set(), subn, set())

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

