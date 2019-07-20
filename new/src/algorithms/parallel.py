import sys
import uuid
import time
from os import path
import networkx as NX
from datetime import timedelta
from multiprocessing import Process, Queue, Value

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from algorithms.triangles import Triangles

METRICS = "metrics-new-{}.txt"

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
def explore(node, _graph, visited, max_already_found_clique_size, calls_made, hits_triangle):
    
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
            with hits_triangle.get_lock():
                hits_triangle.value += 1
            break
        
        new_clique = explore(next_neighbor,
                                subgraph,
                                visited,
                                max_already_found_clique_size,
                                calls_made, hits_triangle)
        
        if len(clique) < len(new_clique):
            clique = new_clique
            if max_already_found_clique_size < len(new_clique):
                max_already_found_clique_size = len(new_clique)
        
        subgraph.remove_node(next_neighbor)

    visited[node] = False
    
    return clique

def worker_main(worker_id, queue_in, queue_out, max_clique_size, graph, visited, calls_made, hits_triangle):
    
    node_to_visit = queue_in.get()
    graph_ordered_nodes = list(graph.nodes())
    graph_ordered_nodes.reverse()
    
    while node_to_visit is not None:

        print("wid: {}, node: {}".format(worker_id, node_to_visit))

        popped_element = graph_ordered_nodes.pop()
        
        while popped_element != node_to_visit:
            graph.remove_node(popped_element)
            popped_element = graph_ordered_nodes.pop()
        
        if node_to_visit == popped_element and max_clique_size.value < graph.degree(node_to_visit) + 1:
            
            new_clique = explore(node_to_visit,
                                    graph,
                                    visited,
                                    max_clique_size.value,
                                    calls_made, hits_triangle)
            
            with max_clique_size.get_lock():
                if max_clique_size.value < len(new_clique):
                    max_clique_size.value = len(new_clique)
                    queue_out.put(new_clique)

        graph.remove_node(popped_element)

        node_to_visit = queue_in.get()

def main(graph, work_num):

    print("Graph - Nodes: {}, Edges: {}".format(
                len(graph.nodes()), len(graph.edges())))

    visited = {}

    for node in graph.nodes():
        visited[node] = False
    
    max_clique = []
    max_clique_size = Value('i', 0)

    queue_in = Queue()
    queue_out = Queue()

    # Metrics values
    calls_made = Value('i', 0)
    hits_triangle = Value('i', 0)
    count_of_cliques_received = 0
    
    workers = []

    start = time.time()

    for worker_id in range(work_num):
        p = Process(target=worker_main, args=(worker_id,
                                            queue_in,
                                            queue_out,
                                            max_clique_size,
                                            graph, visited,
                                            calls_made,
                                            hits_triangle))
        workers.append(p)
        p.start()

    for node in graph.nodes():
        queue_in.put(node)

    # Signal End of queue
    for i in range(work_num):
        queue_in.put(None) 

    for worker in workers:
        worker.join()

    end = time.time()

    # Exhaust the total of cliques received, until the last one
    while len(max_clique) != max_clique_size.value:
        max_clique = queue_out.get()
        count_of_cliques_received += 1

    d = end - start
    dt = time.strptime(str(timedelta(seconds=d)).split(".")[0], "%H:%M:%S")

    print("Delta time: hour: {}, min: {}, sec: {}".format(
                                        dt.tm_hour,
                                        dt.tm_min,
                                        dt.tm_sec))

    print('Cliques found: {}, Calls made: {}, Hits Tri: {}'.format(
        count_of_cliques_received, calls_made.value, hits_triangle.value))

    with open(METRICS.format(uuid.uuid4()), "w") as f:
        f.write(str((count_of_cliques_received,
                        calls_made.value,
                        hits_triangle.value)))

    return max_clique

