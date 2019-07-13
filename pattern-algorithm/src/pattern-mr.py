#!/usr/bin/env python3

"""
    Map-Reduce implementation for
    the MCP
"""

import sys
import time
import networkx as NX

def clique_map_reduce(G):

    if len(G) == 0:
        return

    adj = {u: {v for v in G[u] if v != u} for u in G}

    dr = {}

    while len(dr) != 1:

        ## MAP

        nd = []
        
        for k,v in adj.items():
            for val in v:
                if type(k) is int:
                    k = {k}
                else:
                    k = {*k}
                nd.append({
                    "k": tuple(k | {val}),
                    "v": v - {val}
                })

        ## REDUCE

        dr = {}

        for item in nd:
            if item["k"] not in dr:
                dr[item["k"]] = item["v"]
            else:
                dr[item["k"]] = dr[item["k"]] & item["v"]

        adj = dr

    return list(*adj.keys())

def test_graph(G):

    print("max-clique - nodes: {}".format(G.nodes()))

    start = time.time()
    
    clique = clique_map_reduce(G)

    end = time.time()

    print("Time: {}".format(end - start))
    print("Result: {}, size: {}".format(clique, len(clique)))

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

