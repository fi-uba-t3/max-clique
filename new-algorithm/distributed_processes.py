from multiprocessing import Process, Queue, Value
import networkx as NX
from triangles import Triangles
import time

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
def explore (node, _graph, visited, max_already_found_clique_size):
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

def worker_main(worker_id, queue_in, queue_out, max_clique_size, graph, visited):
    node_to_visit = queue_in.get()
    graph_ordered_nodes = list(graph.nodes())
    graph_ordered_nodes.reverse()
    while node_to_visit is not None:
        popped_element = graph_ordered_nodes.pop()

        if node_to_visit == popped_element and max_clique_size.value < graph.degree(node_to_visit)  + 1:
            new_clique = explore (node_to_visit, graph, visited, max_clique_size.value)
            with max_clique_size.get_lock():
                if max_clique_size.value < len(new_clique):
                    max_clique_size.value = len(new_clique)
                    queue_out.put(new_clique)

        graph.remove_node(popped_element)


        node_to_visit = queue_in.get()

def main(graph, work_num):

    visited = {}
    for node in graph.nodes():
        visited[node] = False
    max_clique = []

    queue_in = Queue()
    queue_out = Queue()

    max_clique_size = Value('i', 0)
    workers = []


    for worker_id in range(work_num):
        p = Process(target=worker_main, args=(worker_id, queue_in, queue_out, max_clique_size, graph, visited))
        workers.append(p)
        p.start()


    for node in graph.nodes():
        queue_in.put(node)

    for i in range(work_num):
        queue_in.put(None) # Signal End of queue

    for worker in workers:
        worker.join()
    count = 0
    while len(max_clique) != max_clique_size.value:
        max_clique = queue_out.get()
        # print(max_clique)
        count += 1

    # print(count)

    return max_clique


