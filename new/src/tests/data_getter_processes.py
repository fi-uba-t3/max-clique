import unittest
import networkx as NX

import sys
from os import path

grandfather_dir = path.dirname(path.dirname(path.abspath(__file__)))

sys.path.append(grandfather_dir)

from algorithms.parallel import main

seed = 100

import os
directory = grandfather_dir + '/../graphs/own-graphs'

for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        G = NX.read_edgelist(directory + '/' + filename)
        main(G, 4)
