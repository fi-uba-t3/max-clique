import time
from networkx import Graph
from datetime import timedelta
from multiprocessing import Process, Queue, Value

def explore(wid, G, U, C, max_clique, level):

    if len(U) == 0:
        with max_clique.get_lock():
            if level > max_clique.value:
                max_clique.value = level
        return

    while len(U) > 0:

        with max_clique.get_lock():
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

        U = set()
        C = set()

        if G.degree(item) >= val.value:

            C.add(item)

            ngbs = G.neighbors(item)

            # check if the vertexes
            # verify the clique condition
            for neighbor in ngbs:
                if G.degree(neighbor) >= val.value:
                    U.add(neighbor)

        explore(wid, G, U, C, val, 1)

        with val.get_lock():
            if len(C) >= val.value:
                val.value = len(C)
                res = C.copy()

    q_out.put((res, wid))

def load_graph(path):

    edges = []

    with open(path) as f:
        lines = f.readlines()

    edges = list(map(lambda x: tuple(x.strip("\n").split(" ")), lines))
    edges = list(map(lambda y: (int(y[0]), int(y[1])), edges))

    g = Graph()
    g.add_edges_from(edges)

    return g

def maxclique(graph, work_num):
    
    G = load_graph(graph)

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
    nodes = sorted(nodes, key=lambda x: x[1], reverse=True)
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
        
        clique, wid = outq.get()

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


