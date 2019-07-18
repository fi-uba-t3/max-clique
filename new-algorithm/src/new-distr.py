#!/usr/bin/env python3

import os
import time
import networkx as NX
from datetime import timedelta
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

from parallel import main

def run(graph, workers):

    G = NX.read_edgelist(graph)

    start = time.time()
    res = main(G, workers)
    end = time.time()

    d = end - start
    dt = time.strptime(str(timedelta(seconds=d)).split(".")[0], "%H:%M:%S")

    print("Delta time: hour: {}, min: {}, sec: {}".format(
                                        dt.tm_hour,
                                        dt.tm_min,
                                        dt.tm_sec))

    print("Result: {}, size: {}".format(res, len(res)))

if __name__ == "__main__":

    parser = ArgumentParser(
                description='MCP-TTT',
                formatter_class=ArgumentDefaultsHelpFormatter)
    
    parser.add_argument(
            '--workers',
            default=os.cpu_count(),
            type=int,
            help='MCP workers'
    )

    parser.add_argument(
            '--graph',
            default=None,
            help='MCP graph data'
    )

    args = parser.parse_args()

    run(args.graph, args.workers)

