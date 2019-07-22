import sys
import networkx as NX

import os
from os import path

grandfather_dir = path.dirname(path.dirname(path.abspath(__file__)))

sys.path.append(grandfather_dir)

from algorithms.TTT.parallel import maxclique

seed = 100

directory = grandfather_dir + '/../graphs/own-graphs'

for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        G = NX.read_edgelist(directory + '/' + filename)
        maxclique(G, 4, True)

