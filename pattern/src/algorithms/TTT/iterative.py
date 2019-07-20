"""
    Etsuji Tomita, Akira Tanaka, Haruhisa Takahashi,
       
       "The worst-case time complexity for generating all maximal
       cliques and computational experiments",
       
       *Theoretical Computer Science*, Volume 363, Issue 1,
       Computing and Combinatorics,
       
       10th Annual International Conference on
       
       Computing and Combinatorics (COCOON 2004), 25 October 2006, Pages 28--42
       
       <https://doi.org/10.1016/j.tcs.2006.06.015>
"""

CLIQUE = set()

def expand(G, K, cand, fini):

    global CLIQUE

    if len(cand) == 0 and len(fini) == 0:
        if len(K) > len(CLIQUE):
            CLIQUE = K.copy()
        return

    pivot = max(cand | fini, key=lambda u: len(cand & set(G.neighbors(u))))

    ext = cand - set(G.neighbors(pivot))

    for q in ext:

        Kq = K | {q}

        candq = cand & set(G.neighbors(q))
        finiq = fini & set(G.neighbors(q))

        cand = cand - {q}
        fini = fini | {q}

        expand(G, Kq, candq, finiq)

def maxclique(G):

    nodes = G.nodes()

    print("max-clique - nodes: {}".format(nodes))

    # Order nodes by its degree
    nodes = list(map(lambda x: (x, G.degree(x)), nodes))
    nodes = sorted(nodes, key=lambda x: x[1])
    nodes = list(map(lambda x: x[0], nodes))

    for v in nodes:

        if G.degree(v) >= len(CLIQUE):

            print("node: {}".format(v))

            subn = set(G.neighbors(v)) | {v}
            
            expand(G, set(), subn, set())

    return list(CLIQUE)

