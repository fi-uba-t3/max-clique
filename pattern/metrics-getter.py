#!/usr/bin/env python3

import sys
import networkx as NX

import os
from os import path

grandfather_dir = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(grandfather_dir)

from src.algorithms.TTT.parallel import maxclique

directory = grandfather_dir + '/pattern/graphs/own-graphs'

PATH = "metrics-pattern.txt"

with open(PATH, "w") as f:
    f.write("name,nodes,edges,cliques,calls,time\n")

for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        print("graph: {}".format(filename))
        G = NX.read_edgelist(directory + '/' + filename)
        maxclique(G, 4, loaded=True, metrics=True, name=filename)

