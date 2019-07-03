import sys
import time
import networkx as NX

from multiprocessing import Process, Queue, Value

def explore(G, U, C, max_clique, level):

    if len(U) == 0 and len(C) > max_clique.value:
        return

    while len(U) > 0:

        if level + len(U) <= len(C):
            return

        Uc = U.copy()
        
        v = Uc.pop()
        C.add(v)

        Np = set()
        vngbs = G.neighbors(v)

        for wj in vngbs:
            if G.degree(wj) >= max_clique.value:
                Np.add(wj)

        explore(G, Uc.intersection(Np), C, max_clique, level + 1)

def calc_max_clique(wid, q_in, q_out, val, G):

    quit = False
    res = []

    while not quit:
    
        item = q_in.get()

        if item == None:
            quit = True
            continue

        U, C = item

        print("U: {}, C: {}".format(U, C))

        # check if the vertexes
        # verify the clique condition

        for v in U:
            if G.degree(v) < val.value:
                U.remove(v)

        explore(G, U, C, val, 1)

        if len(C) > val.value:
            with val.get_lock():
                val.value = len(C)
                res = C.copy()

        print("max_clique: {}".format(val.value))
    
    q_out.put(res)

def test_graph(G):

    WORKERS = 6
    
    workers = []
    queues = []

    val = Value('i', 2)
    outq = Queue()

    for w in range(WORKERS):
        queues.append(Queue())

    start = time.time()
    
    for w in range(WORKERS):
        p = Process(target=calc_max_clique, args=(w, queues[w], outq, val, G,))
        workers.append(p)
        p.start()

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

            queues[v % WORKERS].put((U, C))

    for qw in queues:
        qw.put(None)

    for w in workers:
        w.join()

    maxclique = []

    while not outq.empty():
        
        clique = outq.get()

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

    # Tests
    if len(sys.argv) <= 1:
        g = NX.complete_graph(10)
        test_graph(g)
        return
    
    # Load a graph
    g = load_graph(sys.argv[1])
    test_graph(g)

if __name__ == "__main__":
    main()

