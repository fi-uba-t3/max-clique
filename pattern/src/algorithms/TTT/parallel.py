import time
import networkx as NX
from datetime import timedelta
from multiprocessing import Process, Queue, Value

METRICS = "metrics-pattern.txt"

def expand(wid, G, K, cand, fini, max_clique_size, calls_made, q_out):

    if calls_made is not None:
        with calls_made.get_lock():
            calls_made.value += 1

    if len(cand) == 0 and len(fini) == 0:
        with max_clique_size.get_lock():
            if len(K) > max_clique_size.value:
                max_clique_size.value = len(K)
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

        expand(wid, G, Kq, candq, finiq,
                max_clique_size, calls_made, q_out)

def calc_max_clique(wid, G, max_clique_size, calls_made, q_in, q_out):

    quit = False

    while not quit:

        item = q_in.get()

        if item == None:
            quit = True
            continue

        if G.degree(item) >= max_clique_size.value:

            CAND = {item}

            # check if the vertexes
            # verify the clique condition
            for neighbor in G.neighbors(item):
                if G.degree(neighbor) >= max_clique_size.value:
                    CAND.add(neighbor)

            expand(wid, G, set(), CAND, set(),
                    max_clique_size, calls_made, q_out)

def process_parallel(G, workers_num, calls_made=None):

    workers = []
    queues = []
    outq = Queue()

    max_clique = []
    max_clique_size = Value('i', 2)

    for w in range(workers_num):
        queues.append(Queue())

    nodes = G.nodes()

    print("nodes: {}".format(nodes))

    # Order nodes by its degree
    nodes = list(map(lambda x: (x, G.degree(x)), nodes))
    nodes = sorted(nodes, key=lambda x: x[1])
    nodes = list(map(lambda x: x[0], nodes))

    for v in range(len(nodes)):
        queues[v % workers_num].put(nodes[v])

    start = time.time()

    for w in range(workers_num):
        p = Process(target=calc_max_clique, args=(w, G,
                                                    max_clique_size,
                                                    calls_made,
                                                    queues[w], outq,))
        workers.append(p)
        p.start()

    for qw in queues:
        qw.put(None)

    for w in workers:
        w.join()


    count_of_cliques_received = outq.qsize()

    # Find the maximum clique
    while not outq.empty():        
        wid, clique = outq.get()

        print("wid: {}, clique: {}".format(wid, clique))

        if len(clique) > len(max_clique):
            max_clique = clique

    return max_clique, count_of_cliques_received
    

def maxclique(graph, workers_num, loaded=False, metrics=False, name='none'):
    
    if not loaded:
        G = NX.read_edgelist(graph)
    else:
        G = graph

    print("Graph - Nodes: {}, Edges: {}".format(
                len(G.nodes()), len(G.edges())))

    start = time.time()

    max_clique, _ = process_parallel(graph, workers_num)
    
    end = time.time()

    d = end - start
    dt = time.strptime(str(timedelta(seconds=d)).split(".")[0], "%H:%M:%S")

    print("Delta time: hour: {}, min: {}, sec: {}".format(
                                        dt.tm_hour,
                                        dt.tm_min,
                                        dt.tm_sec))

    # Writes and prints the metrics
    if metrics:
        # Metrics values
        calls_made = Value('i', 0)
        _, count_of_cliques_received = process_parallel(graph, workers_num, calls_made=calls_made)
    

        print("Cliques found: {}, Calls made: {}".format(
            count_of_cliques_received, calls_made.value))

        result_metrics = "{},{},{},{},{},{}\n".format(
                            name,
                            len(G.nodes()),
                            len(G.edges()),
                            count_of_cliques_received,
                            calls_made.value, d)
        with open(METRICS, "a") as f:
            f.write(result_metrics)

    return list(max_clique)


