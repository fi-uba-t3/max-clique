#!/usr/bin/env python3

import os
import sys

from os import path
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from algorithms.PGLC.parallel import maxclique

def main(graph, workers):

    res = maxclique(graph, workers)

    print("Result: {}, size: {}".format(res, len(res)))

if __name__ == "__main__":

    parser = ArgumentParser(
                description='MCP',
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

    main(args.graph, args.workers)

