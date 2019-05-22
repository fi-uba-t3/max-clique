import networkx as nx

def compute_triangles(graph):
    triangles = {}
    for node, number_triangles in graph.items():
        triangles[node] = number_triangles / 3
    return nx.triangles(graph)

def get_t_n(triangles):
    max = 0
    max_node = None
    for node, number_triangles in triangles.items():
        if max < number_triangles:
            max = number_triangles
            max_node = node
    return max, max_node

def is_clique(graph):
    n = graph.number_of_nodes()
    return graph.number_of_edges() == n * (n - 1) / 2  


def explore(node, father, _graph, max_computed_cl):
    if is_clique(_graph):
        return _graph
    graph = _graph.intersect(graph.neighbors(node)) 
    triangles = compute_triangles (graph)
    k_triangles, next_neighbor = get_t_n (triangles)
    while k_triangles > len(clique) or next_neighbor != None:
        clique = explore(next_neighbor, node, graph)
        k_triangles,next_neighbor = get_t_n (triangles) 
    return clique

def main(graph):
    graph = nx(graph, 2)   # esto es una optimizacion 
    max_clique = set()
    for node in graph:
        k_triangles, next_neighbor = get_t_n (triangles)
        clique = explore (node, node, graph)
        if (len(clique) > len(max_clique)):
            max_clique = clique
    return max_clique
