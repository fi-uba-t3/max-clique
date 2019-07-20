"""
    Algorithm taken from NX python library

    <https://github.com/networkx/networkx/blob/master/networkx/algorithms/clique.py#L103>
"""

import sys
import time
import networkx as NX

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

def maxclique(G):

    # Order nodes by its degree
    nodes = list(map(lambda x: (x, G.degree(x)), nodes))
    nodes = sorted(nodes, key=lambda x: x[1])
    nodes = list(map(lambda x: x[0], nodes))

    MCLIQUE = []

    adj = {u: {v for v in G[u] if v != u} for u in G}
    
    for v in nodes:

        if G.degree(v) >= len(MCLIQUE):

            print("node: {}".format(v))

            subg = set(G.neighbors(v)) | {v}

            for clique in cliques(G, subg, subg, adj):
                if len(clique) > len(MCLIQUE):
                    MCLIQUE = clique

    return MCLIQUE

