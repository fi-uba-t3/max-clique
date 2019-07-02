import sys
import time
import networkx as NX

def explore(G, U, C, max_clique, level):

    if len(U) == 0 and len(C) > max_clique:
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
            if G.degree(wj) >= max_clique:
                Np.add(wj)

        explore(G, Uc.intersection(Np), C, max_clique, level + 1)

def max_clique(G):

    max_clique = 2

    nodes = G.nodes()

    print("max-clique - nodes: {}".format(nodes))

    for v in range(len(nodes)):
        
        if G.degree(nodes[v]) >= max_clique:
           
            print("node: {}".format(nodes[v]))

            U = set()
            C = set()

            C.add(nodes[v])
            res = []

            ngbs = G.neighbors(nodes[v])
            
            for j in range(len(ngbs) + 1):
                if j > v and G.degree(nodes[j]) >= max_clique:
                    U.add(nodes[j])
            
            explore(G, U, C, max_clique, 1)
            
            if len(C) > max_clique:
                max_clique = len(C)
                res = C.copy()

        print("max_clique: {}".format(max_clique))

    return res

def test_graph(G):

    start = time.time()
    clique = max_clique(G)
    end = time.time()

    print("Result: {}".format(clique))
    
    delta_own = end - start

    start = time.time()
    NX.graph_clique_number(G)
    end = time.time()

    delta_nx = end - start

    print("Time - Own: {}, NX: {}".format(delta_own, delta_nx))

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

