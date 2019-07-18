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

    reduce_items = {}
    map_items = []

    while len(reduce_items) != 1:

        ## MAP

        map_items.clear()
        
        for k,v in adj.items():
            for val in v:
                if type(k) is int:
                    k = {k}
                else:
                    k = {*k}
                map_items.append({
                    "k": tuple(k | {val}),
                    "v": v - {val}
                })

        ## REDUCE

        reduce_items.clear()

        for item in map_items:
            if item["k"] not in reduce_items:
                reduce_items[item["k"]] = item["v"]
            else:
                reduce_items[item["k"]] = reduce_items[item["k"]] & item["v"]

        adj.clear()

        for k,v in reduce_items.items():
            adj[k] = v

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

