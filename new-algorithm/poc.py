import networkx as nx

def compute_triangles(graph, node):
    T = []
    for n in node.neighbors:
        edges = len(n.neighbors)
        t = edges - 1
        if not t in T:
            T[t] = []
        T[t] = T[t].append(n)
    triangles_L = flatten (T)
	triangles_T = count_triangles_leq (T)
	return triangles_L, triangles_T

def verify_clique(node, graph):
    clique = []
    d = degree(node)
	clique_edges = d * (d - 1) / 2
	if clique_edges == edges:
		clique = node.neighbors + [node]
	return clique

def get_t_n(triangles):
    T, L = triangles
    

def explore (node, father, graph):
    graph = graph.keep_only_neighbors(node) 
    triangles = compute_triangles (graph)
    clique = verify_clique (node, graph)
    k_triangles, next_neighbor = get_t_n (triangles)
    while k_triangles > len(clique) or next_neighbor != None:
        clique = explore (next_neighbor, node, graph)
        k_triangles, next_neighbor = get_t_n (triangles) 
        return clique

def main (graph):
    # graph := compute_2-core (graph)   # esto es una optimizacion 
    max_clique = set()
    for node in graph:
        k_triangles, next_neighbor = get_t_n (triangles)
        clique = explore (node, node, graph)
        if (len(clique) > len(max_clique)):
            max_clique = clique
    return max_clique