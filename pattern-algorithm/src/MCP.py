import time
from datetime import timedelta
from multiprocessing import Process, Queue, Value

from graph import Graph

def explore(wid, G, U, C, max_clique, q_out, size):

    if len(U) == 0:
        with max_clique.get_lock():
            if size > max_clique.value:
                max_clique.value = size
                q_out.put((wid, C.copy()))
        return

    while len(U) > 0:

        with max_clique.get_lock():
            if size + len(U) <= max_clique.value:
                return
        
        v = U.pop()

        Np = set()
        vngbs = G.neighbors(v)

        for wj in vngbs:
            if G.degree(wj) >= max_clique.value:
                Np.add(wj)

        explore(wid, G, U & Np, C | {v}, max_clique, q_out, size + 1)

def calc_max_clique(wid, q_in, q_out, max_clique, G):

    quit = False

    while not quit:

        item = q_in.get()

        if item == None:
            quit = True
            continue

        U = set()
        C = set()

        if G.degree(item) >= max_clique.value:

            print("wid: {}, node: {}".format(wid, item))

            C.add(item)

            ngbs = G.neighbors(item)

            # check if the vertexes
            # verify the clique condition
            for neighbor in ngbs:
                if G.degree(neighbor) >= max_clique.value:
                    U.add(neighbor)

            explore(wid, G, U, C, max_clique, q_out, 1)

def maxclique(graph, work_num):
    
    G = Graph()
    G.load(graph)

    workers = []
    queues = []

    val = Value('i', 2)
    outq = Queue()

    for w in range(work_num):
        queues.append(Queue())

    nodes = G.nodes()

    print("nodes: {}".format(nodes))

    start = time.time()
    
    # Order nodes by the its degree
    nodes = list(map(lambda x: (x, G.degree(x)), nodes))
    nodes = sorted(nodes, key=lambda x: x[1])
    nodes = list(map(lambda x: x[0], nodes))

    for v in range(len(nodes)):
        queues[v % work_num].put(nodes[v])

    for w in range(work_num):
        p = Process(target=calc_max_clique, args=(w, queues[w], outq, val, G,))
        workers.append(p)
        p.start()

    for qw in queues:
        qw.put(None)

    for w in workers:
        w.join()

    max_clique = []

    while not outq.empty():
        
        wid, clique = outq.get()

        print("wid: {}, clique: {}".format(wid, clique))

        if len(clique) > len(max_clique):
            max_clique = clique

    end = time.time()

    d = end - start
    dt = time.strptime(str(timedelta(seconds=d)).split(".")[0], "%H:%M:%S")

    print("Delta time: hour: {}, min: {}, sec: {}".format(
                                        dt.tm_hour,
                                        dt.tm_min,
                                        dt.tm_sec))
    return max_clique


