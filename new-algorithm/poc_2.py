import networkx as NX
import time
class Triangles():
    def __init__(self):
        self.current_list = 0
        self.current_place = 0
        self.T = []

    def add(self, node, triangles):
        while len(self.T) <= triangles + 1:
            self.T.append([])
        self.T[triangles].append(node)
        # Restart , necessary?
        self.current_list = len(self.T) - 1
        self.current_place = 0

    def get_t_n(self):
        while self.current_list >= 0 and self.current_place >= len(self.T[self.current_list]):
            self.current_list -= 1
            self.current_place = 0


        if self.current_list < 0:
            return None, None

        next_neighbor = self.T[self.current_list][self.current_place]
        self.current_place +=1
        triangles_belonging = self.current_list + 1 # +2
        return triangles_belonging, next_neighbor
    

def compute_triangles(graph):
    T = Triangles()
    total_edges = 0
    for n in graph.nodes():
        edges = graph.degree(n)
        t = edges # -1
        total_edges += edges
        T.add(n, t)
    return T, total_edges

def verify_clique(graph):
    clique = []
    d = len(graph.nodes())
    clique_edges = d * (d - 1) / 2
    print len(graph.edges()), clique_edges
    return len(graph.edges()) == clique_edges

def explore (node, _graph, max_already_found_clique, already_accounted_nodes):
    print('Original')
    if verify_clique(_graph):
        return list(_graph.nodes())

    subgraph = NX.Graph(_graph.subgraph(_graph.neighbors(node)))
    if verify_clique(subgraph): # Why is this necessary?
        print('Second')

        clique = list(subgraph.nodes())
        clique.append(node)
        return clique
    triangles, edges = compute_triangles (subgraph)
    clique = []
    max_expected_clique_size, next_neighbor = triangles.get_t_n()

    while subgraph is not None and next_neighbor is not None and max_expected_clique_size + already_accounted_nodes > max_already_found_clique:
        new_clique = explore (next_neighbor, subgraph, max_already_found_clique, already_accounted_nodes + 1)
        if new_clique is not len(new_clique) > max_already_found_clique:
            clique = new_clique
            max_already_found_clique = len(clique)
        subgraph = subgraph.remove_node(next_neighbor) # Biggest clique has already been found for next_neighbor, if bigger is found it will not include next_neighbor

        max_expected_clique_size, next_neighbor = triangles.get_t_n()
    clique.append(node)
    return clique

def main(graph):
    graph = graph.copy()
    max_clique = []
    while len(graph.nodes()):
        max_degree = -1
        for node in graph.nodes():
            new_degree = graph.degree(node)
            if max_degree < new_degree:
                max_degree_node = node
                max_degree = new_degree



        if len(max_clique) > graph.degree(max_degree_node): # nodes_left_to_visit, se puede hacer algo? No, porque los que ya visitamos, los sacamos; entonces siempre nodes_left_to_visit + degree_ahora >= degree_original; si pruebo probaria con total - nodes_left_to_visit <= max_clique =>??
            break
        new_clique = explore (max_degree_node, graph, len(max_clique), 0)
        graph.remove_node(max_degree_node)

        # Explore devuelve el clique mas grande al que pertenece el nodo;
        # por lo tanto el clique que encontremos no tendra al nodo, si es mas grande

        if len(new_clique) > len(max_clique):
            max_clique = new_clique
            graph = NX.k_core(graph, len(max_clique))
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
    calc_measure_and_compare(NX.cycle_graph(20), 'Cycle graph 20')
    calc_measure_and_compare(NX.cycle_graph(200), 'Cycle graph 200')
    calc_measure_and_compare(NX.cycle_graph(10), 'Cycle graph 10')
    calc_measure_and_compare(NX.cycle_graph(2), 'Cycle graph 2')
    calc_measure_and_compare(NX.cycle_graph(3), 'Cycle graph 3')
    calc_measure_and_compare(NX.complete_graph(2), 'Complete graph 2')
    calc_measure_and_compare(NX.complete_graph(200), 'Complete graph 200')
    calc_measure_and_compare(NX.balanced_tree(2, 10), 'Balanced binary tree-Height 10')
    calc_measure_and_compare(NX.balanced_tree(3, 8), 'Balanced triary tree-Height 8')
    calc_measure_and_compare(NX.balanced_tree(4, 5), 'Balanced 4-ary tree-Height 5')
    calc_measure_and_compare(NX.balanced_tree(5, 4), 'Balanced 5-ary tree-Height 4')
    calc_measure_and_compare(NX.balanced_tree(2, 15), 'Balanced binary tree-Height 15')
    calc_measure_and_compare(NX.barbell_graph(10, 2), 'Barbell graph 10-2')
    calc_measure_and_compare(NX.barbell_graph(5, 5), 'Barbell graph 5-5')
    calc_measure_and_compare(NX.barbell_graph(20, 10), 'Barbell graph 20-10')
    calc_measure_and_compare(NX.complete_multipartite_graph([1,1]), 'K-Multipartite 1-1')
    calc_measure_and_compare(NX.complete_multipartite_graph([10,5]), 'K-Multipartite 10-5')
    calc_measure_and_compare(NX.complete_multipartite_graph([10,10]), 'K-Multipartite 10-10')
    calc_measure_and_compare(NX.complete_multipartite_graph([5,5,5,5,5]), 'K-Multipartite 5-5-5-5-5')
    calc_measure_and_compare(NX.circular_ladder_graph(20), 'Circular ladder graph 20')
    calc_measure_and_compare(NX.circular_ladder_graph(10), 'Circular ladder graph 10')
    calc_measure_and_compare(NX.circular_ladder_graph(5), 'Circular ladder graph 5')
    calc_measure_and_compare(NX.gnp_random_graph(50, 0.5), 'GNP; N=50, P=0.5')
    calc_measure_and_compare(NX.gnp_random_graph(20, 0.95), 'GNP; N=20, P=0.95')
    calc_measure_and_compare(NX.gnp_random_graph(50, 0.99), 'GNP; N=50, P=0.99')
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