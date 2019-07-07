import os
import sys
import time
import networkx as NX

from datetime import timedelta
from multiprocessing import Process, Queue, Value
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

def explore(wid, G, U, C, max_clique, level):

    print("wid: {}, U: {}, C: {}, max_clique: {}, level: {}".format(
                wid, U, C, max_clique.value, level))

    if len(U) == 0:
        with max_clique.get_lock():
            if level > max_clique.value:
                max_clique.value = level
        return

    while len(U) > 0:

        if level + len(U) <= max_clique.value:
            return
        
        v = U.pop()
        Uc = U.copy()
        
        C.add(v)

        Np = set()
        vngbs = G.neighbors(v)

        for wj in vngbs:
            if G.degree(wj) >= max_clique.value:
                Np.add(wj)

        explore(wid, G, Uc.intersection(Np), C, max_clique, level + 1)

def calc_max_clique(wid, q_in, q_out, val, G):

    quit = False
    res = []

    while not quit:
    
        item = q_in.get()

        if item == None:
            quit = True
            continue

        U, C = item

        # check if the vertexes
        # verify the clique condition

        with val.get_lock():
            U = set(filter(lambda x: G.degree(x) >= val.value, U))

        explore(wid, G, U, C, val, 1)

        with val.get_lock():
            if len(C) >= val.value:
                val.value = len(C)
                res = C.copy()

    q_out.put((res, wid))

def test_graph(G, work_num):
    
    workers = []
    queues = []

    val = Value('i', 2)
    outq = Queue()

    for w in range(work_num):
        queues.append(Queue())

    start = time.time()

    nodes = G.nodes()

    print("nodes: {}".format(nodes))

    for v in range(len(nodes)):
        
        if G.degree(nodes[v]) >= val.value:
           
            U = set()
            C = set()

            C.add(nodes[v])
            res = []

            ngbs = G.neighbors(nodes[v])
            
            for j in range(len(ngbs) + 1):
                if j > v and G.degree(nodes[j]) >= val.value:
                    U.add(nodes[j])

            queues[v % work_num].put((U.copy(), C.copy()))

    for w in range(work_num):
        p = Process(target=calc_max_clique, args=(w, queues[w], outq, val, G,))
        workers.append(p)
        p.start()

    for qw in queues:
        qw.put(None)

    for w in workers:
        w.join()

    maxclique = []

    while not outq.empty():
        
        clique, wid = outq.get()

        print("wid: {}, clique: {}".format(wid, clique))

        if len(clique) > len(maxclique):
            maxclique = clique

    print("Result: {}, size: {}".format(maxclique, len(maxclique)))
    
    end = time.time()

    d = end - start
    dt = time.strptime(str(timedelta(seconds=d)).split(".")[0], "%H:%M:%S")

    print("Delta time: hour: {}, min: {}, sec: {}".format(
                                        dt.tm_hour,
                                        dt.tm_min,
                                        dt.tm_sec))
    
def load_graph(path):

    edges = []

    with open(path) as f:
        lines = f.readlines()

    edges = list(map(lambda x: tuple(x.strip("\n").split(" ")), lines))
    edges = list(map(lambda y: (int(y[0]), int(y[1])), edges))

    g = NX.Graph()
    g.add_edges_from(edges)

    return g

def main(workers, graph):

    if graph is None:
        g = NX.complete_graph(10)
        test_graph(g, workers)
        return
    
    # Load a graph
    g = load_graph(graph)
    test_graph(g, workers)

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

    main(args.workers, args.graph)

