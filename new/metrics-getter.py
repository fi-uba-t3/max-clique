#!/usr/bin/env python3

import sys
import networkx as NX

import os
from os import path

grandfather_dir = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(grandfather_dir)

from src.algorithms.parallel import main

directory = grandfather_dir + '/new/graphs/own-graphs'

PATH = "metrics-new.txt"

with open(PATH, "w") as f:
    f.write("nodes,edges,cliques,calls,triangles,time\n")

for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        G = NX.read_edgelist(directory + '/' + filename)
        main(G, 4, metrics=True)

