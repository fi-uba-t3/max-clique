#!/usr/bin/env python3

import networkx as NX

PATH = "graph-{}.txt"

def generate():

    NX.write_edgelist(NX.cycle_graph(20), PATH.format("cycle-20"), data=False)
    NX.write_edgelist(NX.cycle_graph(200), PATH.format("cycle-200"), data=False)
    NX.write_edgelist(NX.cycle_graph(10), PATH.format("cycle-10"), data=False)
    NX.write_edgelist(NX.cycle_graph(2), PATH.format("cycle-2"), data=False)
    NX.write_edgelist(NX.cycle_graph(3), PATH.format("cycle-3"), data=False)
    NX.write_edgelist(NX.complete_graph(2), PATH.format("complete-2"), data=False)
    NX.write_edgelist(NX.complete_graph(200), PATH.format("complete-200"), data=False)
    NX.write_edgelist(NX.balanced_tree(2, 10), PATH.format("balanced-tree-2-10"), data=False)
    NX.write_edgelist(NX.balanced_tree(3, 8), PATH.format("balanced-tree-3-8"), data=False)
    NX.write_edgelist(NX.balanced_tree(4, 5), PATH.format("balanced-tree-4-5"), data=False)
    NX.write_edgelist(NX.balanced_tree(5, 4), PATH.format("balanced-tree-5-4"), data=False)
    NX.write_edgelist(NX.balanced_tree(2, 15), PATH.format("balanced-tree-2-15"), data=False)
    NX.write_edgelist(NX.barbell_graph(10, 2), PATH.format("barbell-10-2"), data=False)
    NX.write_edgelist(NX.barbell_graph(5, 5), PATH.format("barbell-5-5"), data=False)
    NX.write_edgelist(NX.barbell_graph(20, 10), PATH.format("barbell-20-10"), data=False)
    NX.write_edgelist(NX.circular_ladder_graph(20), PATH.format("circular_ladder_graph-20"), data=False)
    NX.write_edgelist(NX.circular_ladder_graph(10), PATH.format("circular_ladder_graph-10"), data=False)
    NX.write_edgelist(NX.circular_ladder_graph(5), PATH.format("circular_ladder_graph-5"), data=False)
    NX.write_edgelist(NX.full_rary_tree(5, 4), PATH.format("full_rary_tree-5-4"), data=False)
    NX.write_edgelist(NX.ladder_graph(200), PATH.format("ladder_graph-200"), data=False)
    NX.write_edgelist(NX.lollipop_graph(200, 20), PATH.format("lollipop_graph-200-20"), data=False)
    NX.write_edgelist(NX.path_graph(200), PATH.format("path_graph-200"), data=False)
    NX.write_edgelist(NX.star_graph(50), PATH.format("star_graph-50"), data=False)
    NX.write_edgelist(NX.trivial_graph(), PATH.format("trivial_graph"), data=False)
    NX.write_edgelist(NX.wheel_graph(50), PATH.format("wheel_graph-50"), data=False)

if __name__ == "__main__":
    generate()

