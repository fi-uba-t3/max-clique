import sys
import time
from os import path
import networkx as NX
from datetime import timedelta
from multiprocessing import Process, Queue, Value

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from algorithms.triangles import Triangles

METRICS = "metrics-new.txt"

def compute_triangles(graph, main_node, nodes_to_ignore):

    T = Triangles(nodes_to_ignore)
    degree_sum = 0
    
    for node in graph.nodes():
        
        degree = graph.degree(node)
        # Adds the node again
        triangles = degree - 1 
        degree_sum += degree
        
        if node != main_node:
            T.add(node, triangles)
    
    return T, degree_sum 

def verify_clique(graph, node, degree_sum):
    
    degree = graph.degree(node)
    clique_edges = degree * (degree + 1)
    
    return degree_sum == clique_edges

# Returns the max clique size if it is bigger max_already_found_clique 
# already_accounted_nodes no cuenta node
def explore(node, _graph, visited, max_already_found_clique_size, calls_made):
    
    if calls_made is not None:
        with calls_made.get_lock():
            calls_made.value += 1
    
    subgraph_freezed = _graph.subgraph(list(_graph.neighbors(node)) + [node])
    triangles, degree_sum = compute_triangles(subgraph_freezed, node, visited)

    if verify_clique(subgraph_freezed, node, degree_sum):
        return list(subgraph_freezed.nodes())        
    
    visited[node] = True
    subgraph = NX.Graph(subgraph_freezed)
    
    clique = []
    
    for max_expected_clique_size, next_neighbor in triangles.get_t_n_iterator():
    
        if max_expected_clique_size <= max_already_found_clique_size:
            break
        
        new_clique = explore(next_neighbor,
                                subgraph,
                                visited,
                                max_already_found_clique_size,
                                calls_made)
        
        if len(clique) < len(new_clique):
            clique = new_clique
            if max_already_found_clique_size < len(new_clique):
                max_already_found_clique_size = len(new_clique)
        
        subgraph.remove_node(next_neighbor)

    visited[node] = False
    
    return clique

def worker_main(worker_id, queue_in, queue_out, max_clique_size, graph, visited, calls_made):
    
    node_to_visit = queue_in.get()
    graph_ordered_nodes = list(graph.nodes())
    graph_ordered_nodes.reverse()
    
    while node_to_visit is not None:

        popped_element = graph_ordered_nodes.pop()
        
        while popped_element != node_to_visit:
            graph.remove_node(popped_element)
            popped_element = graph_ordered_nodes.pop()
        
        if node_to_visit == popped_element and max_clique_size.value < graph.degree(node_to_visit) + 1:
            
            new_clique = explore(node_to_visit,
                                    graph,
                                    visited,
                                    max_clique_size.value,
                                    calls_made)
            
            with max_clique_size.get_lock():
                if max_clique_size.value < len(new_clique):
                    max_clique_size.value = len(new_clique)
                    queue_out.put(new_clique)

        graph.remove_node(popped_element)

        node_to_visit = queue_in.get()


def process_parallel(graph, workers_num, calls_made=None):

    count_of_cliques_received = 0

    visited = {}

    for node in graph.nodes():
        visited[node] = False

    max_clique = []
    max_clique_size = Value('i', 0)

    queue_in = Queue()
    queue_out = Queue()

    workers = []

    for worker_id in range(workers_num):
        p = Process(target=worker_main, args=(worker_id,
                                            queue_in,
                                            queue_out,
                                            max_clique_size,
                                            graph, visited,
                                            calls_made))
        workers.append(p)
        p.start()

    for node in graph.nodes():
        queue_in.put(node)

    # Signal End of queue
    for i in range(workers_num):
        queue_in.put(None) 

    for worker in workers:
        worker.join()

    count_of_cliques_received = queue_out.qsize()
    
    # Exhaust the total of cliques received, until the last one
    while len(max_clique) != max_clique_size.value:
        max_clique = queue_out.get()

    return max_clique, count_of_cliques_received

    

def main(graph, workers_num, metrics=False, name='none'):

    print("Graph - Nodes: {}, Edges: {}".format(
                len(graph.nodes()), len(graph.edges())))

    visited = {}

    for node in graph.nodes():
        visited[node] = False

    # Measure time
    start = time.time()

    max_clique, count_of_cliques_received = process_parallel(graph, workers_num)

    end = time.time()
    time_diff = end - start

    # Writes and prints the metrics
    if metrics:
        
        # Metrics values
        calls_made = Value('i', 0)

        max_clique, count_of_cliques_received = process_parallel(graph, workers_num, calls_made=calls_made)

        result_metrics = "{},{},{},{},{},{}\n".format(
                            name,
                            len(graph.nodes()),
                            len(graph.edges()),
                            count_of_cliques_received,
                            calls_made.value,
                            time_diff)

        with open(METRICS, "a") as f:
            f.write(result_metrics)

    return max_clique

