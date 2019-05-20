def get_triangles():
    # TODO


def explore (node, father, graph):
    graph := node.neighbors \intersection graph 
    triangles = compute_triangles (graph)
    clique = verify_clique (graph)
    (k_triangles,next_neighbor) = get_t_n (triangles)
    while ( k_triangles > |clique|  ||  next_neighbor != NUL ) do
        clique = explore (next_neighbor, node, graph)
        (k_triangles,next_neighbor) = get_t_n (triangles) 
        return (clique)

def main (graph):
    # graph := compute_2-core (graph)   # esto es una optimización 
    #     mclique := {}
    for node in graph:
        (k_triangles,next_neighbor) = get_t_n (triangles)
        clique = explore (node, node, graph)
        if (|clique| > |mclique|):
            mclique := clique
    return (mclique)