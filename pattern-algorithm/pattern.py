import networkx as NX

def explore(G, U, C, low, max_clique, prev):

    if len(U) == 0 and len(C) > max_clique:
        return

    while len(U) > 0:

        if prev + len(U) <= len(C):
            return

        i = min(U)
        
        Uc = U.copy()
        
        Uc.remove(i)
        C.add(i)

        Np = set()
        vngbs = G.neighbors(i)

        for wj in vngbs:
            if G.degree(wj) >= max_clique:
                Np.add(wj)

        explore(G, Uc.intersection(Np), C, low, max_clique, prev + 1)

def max_clique(G):

    low = 2
    max_clique = 2

    nodes = G.nodes()

    print("max-clique - nodes: {}".format(nodes))

    for v in range(len(nodes)):
        
        if G.degree(v) >= max_clique:
            
            U = set()
            C = set()

            C.add(nodes[v])
            res = []

            ngbs = G.neighbors(nodes[v])
            
            for j in range(len(ngbs) + 1):
                if j > v and G.degree(nodes[j]) >= max_clique:
                    U.add(nodes[j])
            
            explore(G, U, C, low, max_clique, 1)
            
            if len(C) > max_clique:
                max_clique = len(C)
                res = C.copy()

    return res

def main():

    G = NX.complete_graph(4)

    clique = max_clique(G)

    print("final result: {}".format(clique))

if __name__ == "__main__":
    main()

