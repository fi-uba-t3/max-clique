import sys
import time
from os import path
import networkx as NX

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from algorithms.triangles import Triangles

def compute_triangles(graph, main_node, nodes_to_ignore):
    
    T = Triangles(nodes_to_ignore)
    degree_sum = 0
    
    for node in graph.nodes():
        
        degree = graph.degree(node)
        triangles = degree - 1 # Agregar de nuevo el nodo
        degree_sum += degree
        
        if node != main_node:
            T.add(node, triangles)
    
    return T, degree_sum 

def verify_clique(graph, node, degree_sum):
    
    d = graph.degree(node)
    clique_edges = d * (d + 1)
    
    return degree_sum == clique_edges

# Returns the max clique size if it is bigger max_already_found_clique 
# already_accounted_nodes no cuenta node
def explore(node, _graph, visited, max_already_found_clique_size):
    
    subgraph_freezed = _graph.subgraph(list(_graph.neighbors(node)) + [node])
    triangles, degree_sum = compute_triangles (subgraph_freezed, node, visited)

    if verify_clique(subgraph_freezed, node, degree_sum):
        return list(subgraph_freezed.nodes())        
    
    visited[node] = True
    subgraph = NX.Graph(subgraph_freezed)
    
    clique = []
    
    for max_expected_clique_size, next_neighbor in triangles.get_t_n_iterator():
        
        if max_expected_clique_size <= max_already_found_clique_size:
            break
        
        new_clique = explore (next_neighbor, subgraph, visited, max_already_found_clique_size)
        
        if len(clique) < len(new_clique):
            clique = new_clique
            if max_already_found_clique_size < len(new_clique):
                max_already_found_clique_size = len(new_clique)
        
        subgraph.remove_node(next_neighbor)

    visited[node] = False
    
    return clique

def main(graph):
    
    graph = graph.copy()
    visited = {}
    
    for node in graph.nodes():
        visited[node] = False
    
    max_clique = []
    
    for node in list(graph.nodes()):
        
        if len(max_clique) < graph.degree(node)  + 1:
            
            new_clique = explore (node, graph, visited, len(max_clique))
            
            if len(max_clique) < len(new_clique):
                max_clique = new_clique

        graph.remove_node(node)
    
    return max_clique

