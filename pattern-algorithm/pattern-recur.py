#!/usr/bin/env python3

import sys
import time
import networkx as NX

MAX_CLIQUE = 2

def explore(G, U, C, size):

    global MAX_CLIQUE

    if len(U) == 0:
        if size > MAX_CLIQUE:
            MAX_CLIQUE = size
        return

    while len(U) > 0:

        if size + len(U) <= MAX_CLIQUE:
            return
        
        v = U.pop()
        Uc = U.copy()
        
        C.add(v)

        Np = set()
        vngbs = G.neighbors(v)

        for wj in vngbs:
            if G.degree(wj) >= MAX_CLIQUE:
                Np.add(wj)

        explore(G, Uc.intersection(Np), C, size + 1)

def max_clique(G):

    res = []
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
            
            for j in range(len(ngbs) + 1):
                if j > v and G.degree(nodes[j]) >= MAX_CLIQUE:
                    U.add(nodes[j])
            
            explore(G, U, C, 1)
            
            if len(C) >= MAX_CLIQUE:
                MAX_CLIQUE = len(C)
                res = C.copy()

        print("max_clique: {}".format(MAX_CLIQUE))

    return res

def test_graph(G):

    start = time.time()
    clique = max_clique(G)
    end = time.time()

    print("Result: {}, size: {}".format(clique, len(clique)))
    
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

