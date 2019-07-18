#!/usr/bin/env python3

import os
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

from TTT import maxclique

def main(graph, workers):

    res = maxclique(graph, workers)

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

    main(args.graph, args.workers)

