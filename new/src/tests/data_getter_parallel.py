import networkx as NX

import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from algorithms.parallel import main

seed = 10

for size in [100, 200, 300, 400, 500, 600]:
    for edges in map(lambda x: x * size, [5, 10, 15, 20, 25, 30]):
        print('dense gnm {} {} {}\n'.format(size, edges, seed))
        main(NX.dense_gnm_random_graph(size, edges, seed), 4)
        seed += 1

