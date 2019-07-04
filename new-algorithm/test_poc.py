import unittest
import networkx as NX
from poc import main

def calc_and_compare(G):
    result = len(main(G))
    nx_result = NX.graph_clique_number(G)
    return result == nx_result



class ResultTests(unittest.TestCase):

    def test_result_test_cycle_graph_20(self):
        assert(calc_and_compare(NX.cycle_graph(20)))
    def test_result_test_cycle_graph_200(self):
        assert(calc_and_compare(NX.cycle_graph(200)))
    def test_result_test_cycle_graph_10(self):
        assert(calc_and_compare(NX.cycle_graph(10)))
    def test_result_test_cycle_graph_2(self):
        assert(calc_and_compare(NX.cycle_graph(2)))
    def test_result_test_cycle_graph_3(self):
        assert(calc_and_compare(NX.cycle_graph(3)))
    def test_result_test_complete_graph_2(self):
        assert(calc_and_compare(NX.complete_graph(2)))
    def test_result_test_complete_graph_200(self):
        assert(calc_and_compare(NX.complete_graph(200)))
    def test_result_test_balanced_binary_tree_height_10(self):
        assert(calc_and_compare(NX.balanced_tree(2, 10)))
    def test_result_test_balanced_triary_tree_height_8(self):
        assert(calc_and_compare(NX.balanced_tree(3, 8)))
    def test_result_test_balanced_4ary_tree_height_5(self):
        assert(calc_and_compare(NX.balanced_tree(4, 5)))
    def test_result_test_balanced_5ary_tree_height_10(self):
        assert(calc_and_compare(NX.balanced_tree(5, 4)))
    def test_result_test_balanced_binary_tree_height_15(self):
        assert(calc_and_compare(NX.balanced_tree(2, 15)))
    def test_result_test_barbell_graph_10_2(self):
        assert(calc_and_compare(NX.barbell_graph(10, 2)))
    def test_result_test_barbell_graph_5_5(self):
        assert(calc_and_compare(NX.barbell_graph(5, 5)))
    def test_result_test_barbell_graph_20_10(self):
        assert(calc_and_compare(NX.barbell_graph(20, 10)))
    def test_result_test_k_multipartite_1_1(self):
        assert(calc_and_compare(NX.complete_multipartite_graph([1,1])))
    def test_result_test_k_multipartite_10_5(self):
        assert(calc_and_compare(NX.complete_multipartite_graph([10,5])))
    def test_result_test_k_multipartite_10_10(self):
        assert(calc_and_compare(NX.complete_multipartite_graph([10,10])))
    def test_result_test_k_multipartite_5_5_5_5_5(self):
        assert(calc_and_compare(NX.complete_multipartite_graph([5,5,5,5,5])))
    def test_result_test_circular_ladder_graph_20(self):
        assert(calc_and_compare(NX.circular_ladder_graph(20)))
    def test_result_test_circular_ladder_graph_10(self):
        assert(calc_and_compare(NX.circular_ladder_graph(10)))
    def test_result_test_circular_ladder_graph_5(self):
        assert(calc_and_compare(NX.circular_ladder_graph(5)))
    def test_result_test_gnp_50_0_5(self):
        assert(calc_and_compare(NX.gnp_random_graph(50, 0.5)))
    def test_result_test_gnp_50_0_95(self):
        assert(calc_and_compare(NX.gnp_random_graph(20, 0.95)))

    # calc_and_compare(NX.gnp_random_graph(50, 0.99), 'GNP; N=50, P=0.99')
    # calc_and_compare(NX.gnp_random_graph(50, 0.69), 'GNP; N=50, P=0.69')
    # calc_and_compare(NX.circulant_graph(n, offsets)), 'Cycle graph 200')
    # calc_and_compare(NX.cycle_graph(n)), 'Cycle graph 200')
    # calc_and_compare(NX.dorogovtsev_goltsev_mendes_graph(n)), 'Cycle graph 200')
    # calc_and_compare(NX.empty_graph()), 'Cycle graph 200')
    # calc_and_compare(NX.full_rary_tree(r, n)), 'Cycle graph 200')
    # calc_and_compare(NX.ladder_graph(n)), 'Cycle graph 200')
    # calc_and_compare(NX.lollipop_graph(m, n)), 'Cycle graph 200')
    # calc_and_compare(NX.null_graph()), 'Cycle graph 200')
    # calc_and_compare(NX.path_graph(n)), 'Cycle graph 200')
    # calc_and_compare(NX.star_graph(n)), 'Cycle graph 200')
    # calc_and_compare(NX.trivial_graph()), 'Cycle graph 200')
    # calc_and_compare(NX.turan_graph(n, r), 'Cycle graph 200')
    # calc_and_compare(NX.wheel_graph(n), 'Cycle graph 200')


if __name__ == "__main__":
    unittest.main()