import unittest
import networkx as NX

import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from algorithms.parallel import main

seed = 100

for proba in [0.2, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95]:
    for size in [20, 40, 50, 70, 100, 200]:
        print('gnp {} {} {}'.format(size, proba, seed))
        main(NX.gnp_random_graph(size, proba, seed), 4)
        seed += 1

