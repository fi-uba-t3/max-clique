import sys
import time
import networkx as NX

from multiprocessing import Process, Queue, Value

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

        Uc = U.copy()
        
        v = Uc.pop()
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

        print("wid: {}, U: {}, C: {}".format(wid, U, C))
        
        explore(wid, G, U, C, val, 1)

        print("wid: {}, C: {}".format(wid, C))

        with val.get_lock():
            if len(C) >= val.value:
                val.value = len(C)
                res = C.copy()

        print("wid: {}, res: {}".format(wid, res))
        print("wid: {}, max_clique: {}".format(wid, val.value))
    
    q_out.put(res)

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
        
        clique = outq.get()

        print(clique)

        if len(clique) > len(maxclique):
            maxclique = clique

    print("Result: {}".format(maxclique))
    
    end = time.time()
    
def load_graph(path):

    edges = []

    with open(path) as f:
        lines = f.readlines()

    edges = list(map(lambda x: tuple(x.strip("\n").split(" ")), lines))
    edges = list(map(lambda y: (int(y[0]), int(y[1])), edges))

    g = NX.Graph()
    g.add_edges_from(edges)

    return g

def main():

    WORKERS = 6

    # Tests
    if len(sys.argv) <= 1:
        V = 10
        g = NX.complete_graph(V)
        test_graph(g, 2)
        return
    
    # Load a graph
    g = load_graph(sys.argv[1])
    test_graph(g, WORKERS)

if __name__ == "__main__":
    main()

