"""
    Algorithm taken from NX python library and converted to a 
    parallel version

    <https://github.com/networkx/networkx/blob/master/networkx/algorithms/clique.py#L103>
"""

import time
from datetime import timedelta
from networkx import Graph
from multiprocessing import Process, Queue, Value

def cliques(G, subg, cand, adj):

    if len(G) == 0:
        return

    Q = [None]

    u = max(subg, key=lambda u: len(cand & adj[u]))
    ext_u = cand - adj[u]
    stack = []

    try:
        while True:
            if ext_u:
                q = ext_u.pop()
                cand.remove(q)
                Q[-1] = q
                adj_q = adj[q]
                subg_q = subg & adj_q
                if not subg_q:
                    yield Q[:]
                else:
                    cand_q = cand & adj_q
                    if cand_q:
                        stack.append((subg, cand, ext_u))
                        Q.append(None)
                        subg = subg_q
                        cand = cand_q
                        u = max(subg, key=lambda u: len(cand & adj[u]))
                        ext_u = cand - adj[u]
            else:
                Q.pop()
                subg, cand, ext_u = stack.pop()
    except IndexError:
        pass

def calc_max_clique(wid, G, max_clique, q_in, q_out):

    quit = False

    adj = {u: {v for v in G[u] if v != u} for u in G}
    
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

            MCLIQUE = []
            
            for clique in cliques(G, CAND, CAND, adj):
                if len(clique) > len(MCLIQUE):
                    MCLIQUE = clique

            with max_clique.get_lock():
                if len(MCLIQUE) > max_clique.value:
                    max_clique.value = len(MCLIQUE)
                    q_out.put((wid, MCLIQUE.copy()))

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


