"""
    Map-Reduce implementation for
    the MCP
"""

def maxclique(G):

    if len(G) == 0:
        return

    adj = {u: {v for v in G[u] if v != u} for u in G}

    reduce_items = {}
    map_items = []

    while len(reduce_items) != 1:

        ## MAP

        map_items.clear()
        
        for k,v in adj.items():
            for val in v:
                if type(k) is int:
                    k = {k}
                else:
                    k = {*k}
                map_items.append({
                    "k": tuple(k | {val}),
                    "v": v - {val}
                })

        ## REDUCE

        reduce_items.clear()

        for item in map_items:
            if item["k"] not in reduce_items:
                reduce_items[item["k"]] = item["v"]
            else:
                reduce_items[item["k"]] = reduce_items[item["k"]] & item["v"]

        adj.clear()

        for k,v in reduce_items.items():
            adj[k] = v

    return list(*adj.keys())

