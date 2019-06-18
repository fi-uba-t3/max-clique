import networkx as NX
from triangles import Triangles
import time

def compute_triangles(graph):
    T = Triangles()
    degree_sum = 0
    for node in graph.nodes():
        print graph.edges()
        degree = graph.degree(node)
        triangles = degree - 1 # Agregar de nuevo el nodo
        print(triangles)
        degree_sum += degree
        T.add(node, triangles)
    return T, degree_sum 

def verify_clique(graph, node, degree_sum):
    d = graph.degree(node)
    clique_edges = d * (d + 1)
    return degree_sum == clique_edges

# Returns the max clique size if it is bigger max_already_found_clique 
# already_accounted_nodes no cuenta node
def explore (node, _graph, visited):
    print(node)
    print(_graph.nodes())
    print(_graph.edges())
    subgraph_freezed = _graph.subgraph(list(_graph.neighbors(node)) + [node])
    triangles, degree_sum = compute_triangles (subgraph_freezed)

    if verify_clique(subgraph_freezed, node, degree_sum):
        return list(subgraph_freezed.nodes())        
    
    visited[node] = True
    subgraph = NX.Graph(subgraph_freezed)
    
    clique = []
    for max_expected_clique_size, next_neighbor in triangles.get_t_n_iterator():
        print ('m', max_expected_clique_size)
        if not visited[next_neighbor]:
            print('m', max_expected_clique_size)
            if max_expected_clique_size <= len(clique):
                break
            new_clique = explore (next_neighbor, subgraph, visited)
            if len(new_clique) > len(clique):
                clique = new_clique

    visited[node] = False
    return clique

def main(graph):
    visited = {}
    for node in graph.nodes():
        visited[node] = False
    max_clique = []
    for node in graph.nodes():
        if len(max_clique) < graph.degree(node)  + 1:
            new_clique = explore (node, graph, visited)
            if len(max_clique) < len(new_clique):
                max_clique = new_clique
    return max_clique

def calc_measure_and_compare(G, msg):
    start = time.time()
    result = len(main(G))
    end = time.time()

    start2 = time.time()
    nx_result = NX.graph_clique_number(G)
    end2 = time.time()

    own_time = end - start
    nx_time = end2 - start2
    print(msg)
    print '{}\t\t{}\t\t{}\t\t{}\t\t{}'.format(\
        result,\
        own_time,\
        nx_time,\
        'OK' if result == nx_result else 'XXX',\
        ':(' if own_time > nx_time else ':)'\
        )

if __name__ == '__main__':
    # calc_measure_and_compare(NX.cycle_graph(20), 'Cycle graph 20')
    # calc_measure_and_compare(NX.cycle_graph(200), 'Cycle graph 200')
    # calc_measure_and_compare(NX.cycle_graph(10), 'Cycle graph 10')
    # calc_measure_and_compare(NX.cycle_graph(2), 'Cycle graph 2')
    # calc_measure_and_compare(NX.cycle_graph(3), 'Cycle graph 3')
    # calc_measure_and_compare(NX.complete_graph(2), 'Complete graph 2')
    # calc_measure_and_compare(NX.complete_graph(200), 'Complete graph 200')
    # calc_measure_and_compare(NX.balanced_tree(2, 10), 'Balanced binary tree-Height 10')
    # calc_measure_and_compare(NX.balanced_tree(3, 8), 'Balanced triary tree-Height 8')
    # calc_measure_and_compare(NX.balanced_tree(4, 5), 'Balanced 4-ary tree-Height 5')
    # calc_measure_and_compare(NX.balanced_tree(5, 4), 'Balanced 5-ary tree-Height 4')
    # calc_measure_and_compare(NX.balanced_tree(2, 15), 'Balanced binary tree-Height 15')
    # calc_measure_and_compare(NX.barbell_graph(10, 2), 'Barbell graph 10-2')
    # calc_measure_and_compare(NX.barbell_graph(5, 5), 'Barbell graph 5-5')
    # calc_measure_and_compare(NX.barbell_graph(20, 10), 'Barbell graph 20-10')
    calc_measure_and_compare(NX.complete_multipartite_graph([1,1]), 'K-Multipartite 1-1')
    # calc_measure_and_compare(NX.complete_multipartite_graph([10,5]), 'K-Multipartite 10-5')
    # calc_measure_and_compare(NX.complete_multipartite_graph([10,10]), 'K-Multipartite 10-10')
    # calc_measure_and_compare(NX.complete_multipartite_graph([5,5,5,5,5]), 'K-Multipartite 5-5-5-5-5')
    # calc_measure_and_compare(NX.circular_ladder_graph(20), 'Circular ladder graph 20')
    # calc_measure_and_compare(NX.circular_ladder_graph(10), 'Circular ladder graph 10')
    # calc_measure_and_compare(NX.circular_ladder_graph(5), 'Circular ladder graph 5')
    # calc_measure_and_compare(NX.gnp_random_graph(50, 0.5), 'GNP; N=50, P=0.5')
    # calc_measure_and_compare(NX.gnp_random_graph(20, 0.95), 'GNP; N=20, P=0.95')
    # calc_measure_and_compare(NX.gnp_random_graph(50, 0.99), 'GNP; N=50, P=0.99')
    # calc_measure_and_compare(NX.gnp_random_graph(50, 0.69), 'GNP; N=50, P=0.69')
    # calc_measure_and_compare(NX.circulant_graph(n, offsets)), 'Cycle graph 200')
    # calc_measure_and_compare(NX.cycle_graph(n)), 'Cycle graph 200')
    # calc_measure_and_compare(NX.dorogovtsev_goltsev_mendes_graph(n)), 'Cycle graph 200')
    # calc_measure_and_compare(NX.empty_graph()), 'Cycle graph 200')
    # calc_measure_and_compare(NX.full_rary_tree(r, n)), 'Cycle graph 200')
    # calc_measure_and_compare(NX.ladder_graph(n)), 'Cycle graph 200')
    # calc_measure_and_compare(NX.lollipop_graph(m, n)), 'Cycle graph 200')
    # calc_measure_and_compare(NX.null_graph()), 'Cycle graph 200')
    # calc_measure_and_compare(NX.path_graph(n)), 'Cycle graph 200')
    # calc_measure_and_compare(NX.star_graph(n)), 'Cycle graph 200')
    # calc_measure_and_compare(NX.trivial_graph()), 'Cycle graph 200')
    # calc_measure_and_compare(NX.turan_graph(n, r), 'Cycle graph 200')
    # calc_measure_and_compare(NX.wheel_graph(n), 'Cycle graph 200')