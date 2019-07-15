import time
from datetime import timedelta
from multiprocessing import Process, Queue, Value

from graph import Graph

def expand(wid, G, K, cand, fini, max_clique, q_out):

    if len(cand) == 0 and len(fini) == 0:
        with max_clique.get_lock():
            if len(K) > max_clique.value:
                max_clique.value = len(K)
                q_out.put((wid, K.copy()))
        return

    pivot = max(cand | fini, key=lambda u: len(cand & set(G.neighbors(u))))

    ext = cand - set(G.neighbors(pivot))

    for q in ext:

        Kq = K | {q}

        candq = cand & set(G.neighbors(q))
        finiq = fini & set(G.neighbors(q))

        cand = cand - {q}
        fini = fini | {q}

        expand(wid, G, Kq, candq, finiq, max_clique, q_out)

def calc_max_clique(wid, G, max_clique, q_in, q_out):

    quit = False

    while not quit:

        item = q_in.get()

        if item == None:
            quit = True
            continue

        if G.degree(item) >= max_clique.value:

            print("wid: {}, node: {}".format(wid, item))

            CAND = {item}

            # check if the vertexes
            # verify the clique condition
            for neighbor in G.neighbors(item):
                if G.degree(neighbor) >= max_clique.value:
                    CAND.add(neighbor)

            expand(wid, G, set(), CAND, set(), max_clique, q_out)

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
    
    # Order nodes by its degree
    nodes = list(map(lambda x: (x, G.degree(x)), nodes))
    nodes = sorted(nodes, key=lambda x: x[1])
    nodes = list(map(lambda x: x[0], nodes))

    for v in range(len(nodes)):
        queues[v % work_num].put(nodes[v])

    for w in range(work_num):
        p = Process(target=calc_max_clique, args=(w, G, val, queues[w], outq,))
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


