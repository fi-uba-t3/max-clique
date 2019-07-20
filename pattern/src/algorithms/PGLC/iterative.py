"""
    Bharath Pattabiraman, Assefaw H. Gebremedhin, Wei-keng Liao, Alok Choudhary
        
        "Fast Algorithms for the Maximum Clique Problem on
            Massive Sparse Graphs"
        
        Northwestern University, Evanston, IL 60208
        Purdue University, West Lafayette, IN 47907

        <https://arxiv.org/abs/1209.5818>
"""

MAX_CLIQUE = 2
CLIQUE = {}

def explore(G, U, C, size):

    global MAX_CLIQUE
    global CLIQUE

    if len(U) == 0:
        if size > MAX_CLIQUE:
            MAX_CLIQUE = size
            CLIQUE = C.copy()
        return

    while len(U) > 0:

        if size + len(U) <= MAX_CLIQUE:
            return
        
        v = U.pop()

        Np = set()
        vngbs = G.neighbors(v)

        for wj in vngbs:
            if G.degree(wj) >= MAX_CLIQUE:
                Np.add(wj)

        explore(G, U & Np, C | {v}, size + 1)

def maxclique(G):

    nodes = G.nodes()

    print("max-clique - nodes: {}".format(nodes))

    global MAX_CLIQUE

    for v in range(len(nodes)):
        
        if G.degree(nodes[v]) >= MAX_CLIQUE:
           
            print("node: {}".format(nodes[v]))

            U = set()
            C = set()

            C.add(nodes[v])

            ngbs = G.neighbors(nodes[v])
           
            for j in range(len(ngbs)):
                if G.degree(ngbs[j]) >= MAX_CLIQUE:
                    U.add(ngbs[j])
            
            explore(G, U, C, 1)

    return CLIQUE.copy()

