#!/usr/bin/env python3

import sys
import time
import networkx as NX

from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from algorithms.PGLC.iterative import maxclique

def test_graph(G):

    start = time.time()
    clique = maxclique(G)
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

