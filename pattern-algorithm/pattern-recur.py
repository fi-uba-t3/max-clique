#!/usr/bin/env python3

"""
    Bharath Pattabiraman, Assefaw H. Gebremedhin, Wei-keng Liao, Alok Choudhary
        
        "Fast Algorithms for the Maximum Clique Problem on
            Massive Sparse Graphs"
        
        Northwestern University, Evanston, IL 60208
        Purdue University, West Lafayette, IN 47907

        <https://arxiv.org/abs/1209.5818>
"""

import sys
import time
import networkx as NX

MAX_CLIQUE = 2
CLIQUE = {}

def explore(G, U, C, size):

    global MAX_CLIQUE
    global CLIQUE

    if len(U) == 0:
        if size > MAX_CLIQUE:
            MAX_CLIQUE = size
            CLIQUE = C.copy()
        return

    while len(U) > 0:

        if size + len(U) <= MAX_CLIQUE:
            return
        
        v = U.pop()

        Np = set()
        vngbs = G.neighbors(v)

        for wj in vngbs:
            if G.degree(wj) >= MAX_CLIQUE:
                Np.add(wj)

        explore(G, U & Np, C | {v}, size + 1)

def max_clique(G):

    nodes = G.nodes()

    print("max-clique - nodes: {}".format(nodes))

    global MAX_CLIQUE

    for v in range(len(nodes)):
        
        if G.degree(nodes[v]) >= MAX_CLIQUE:
           
            print("node: {}".format(nodes[v]))

            U = set()
            C = set()

            C.add(nodes[v])

            ngbs = G.neighbors(nodes[v])
           
            for j in range(len(ngbs)):
                if G.degree(ngbs[j]) >= MAX_CLIQUE:
                    U.add(ngbs[j])
            
            explore(G, U, C, 1)

    print("max_clique: {}".format(MAX_CLIQUE))

def test_graph(G):

    start = time.time()
    max_clique(G)
    end = time.time()

    print("Result: {}, size: {}".format(CLIQUE, MAX_CLIQUE))
    
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

