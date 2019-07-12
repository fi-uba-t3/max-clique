#!/usr/bin/env python3

"""
    Map-Reduce implementation for
    the MCP
"""

import sys
import time
import networkx as NX

def clique_map_reduce():

    d = {1:{2,3}, 2:{1,3}, 3:{1,2}}

    nd = []

    ## MAP

    for k,v in d.items():
        print("k: {}, v: {}".format(k,v))
        for val in v:
            print("key: {}".format(tuple({k} | {val})))
            print("val: {}".format(v - {val}))
            nd.append({
                "k": tuple({k} | {val}),
                "v": v - {val}
            })

    print(nd)

    ## REDUCE

    dr = {}

    for item in nd:
        if item["k"] not in dr:
            dr[item["k"]] = item["v"]
        else:
            dr[item["k"]] = dr[item["k"]] & item["v"]

    print(dr)

def main():
    clique_map_reduce()

if __name__ == "__main__":
    main()

