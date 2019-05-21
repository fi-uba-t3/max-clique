import networkx as nx

def compute_triangles(graph):
    return nx.triangles(graph) # TODO divide by 3

def get_t_n():
    pass
    # TODO

def verify_clique(graph):
    n = graph.number_of_nodes()
    return graph.number_of_edges() == n * (n - 1) / 2  


def explore (node, father, graph):
    graph = graph.keep_only_neighbors(node) 
    triangles = compute_triangles (graph)
    clique = verify_clique (graph)
    k_triangles, next_neighbor = get_t_n (triangles)
    while k_triangles > len(clique) or next_neighbor != None:
        clique = explore (next_neighbor, node, graph)
        (k_triangles,next_neighbor) = get_t_n (triangles) 
        return clique

def main (graph):
    # graph := compute_2-core (graph)   # esto es una optimizacion 
    max_clique = set()
    for node in graph:
        (k_triangles,next_neighbor) = get_t_n (triangles)
        clique = explore (node, node, graph)
        if (len(clique) > len(max_clique)):
            max_clique = clique
    return max_clique