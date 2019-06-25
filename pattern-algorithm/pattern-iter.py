import time
import networkx as NX

#
# returns: Clique of v
#
def explore(G, nodes, node_id, max_clique):

    C = set()
    U = set()

    C.add(nodes[node_id])

    ngbs = G.neighbors(nodes[node_id])

    for j in range(len(ngbs) + 1):
        if j > node_id and G.degree(nodes[j]) >= max_clique:
            U.add(nodes[j])


    if len(U) == 0 and len(C) > max_clique:
        return C

    while len(U) > 0:

        Uc = U.copy()

        v = Uc.pop()
        C.add(v)

        Np = set()
        vngbs = G.neighbors(v)

        for wj in vngbs:
            if G.degree(wj) >= max_clique:
                Np.add(wj)

        Ux = Uc.intersection(Np)

        while len(Ux) > 0:

        explore(G, Uc.intersection(Np), C, max_clique, level + 1)

def max_clique(G):

    max_clique = 2
    res = []

    nodes = G.nodes()

    print("max-clique - nodes: {}".format(nodes))

    for v in range(len(nodes)):

        if G.degree(nodes[v]) >= max_clique:
            
            C = explore(G, nodes, v, max_clique)

            if len(C) > max_clique:
                max_clique = len(C)
                res = C.copy()

    return res

def main():

    G = NX.complete_graph(6)
    
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

if __name__ == "__main__":
    main()

