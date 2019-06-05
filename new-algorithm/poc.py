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
        self.current_list = 0
        self.current_place = 0

    def get_t_n(self): # TODO Invert order
        while self.current_list < len(self.T) and self.current_place >= len(self.T[self.current_list]):
            self.current_list += 1
            self.current_place = 0

        # self.current_list <= len(self.T) or self.current_place < len(self.T[self.current_list])
    
        if self.current_list >= len(self.T):
            return None, None

        # self.current_list = or self.
        next_neighbor = self.T[self.current_list][self.current_place]
        self.current_place +=1
        return self.current_list, next_neighbor
        

def compute_triangles(node, graph):
    T = Triangles()
    total_edges = 0
    # for n in graph.neighbors(node):
    for n in graph.nodes():
        edges = graph.degree(n)
        t = edges - 1
        total_edges += edges
        T.add(n, t)
    return T, total_edges

# def verify_clique(node, graph):
def verify_clique(graph):
    clique = []
    d = len(graph.nodes())
    clique_edges = d * (d + 1)
    
    # if len(graph.edges()) == clique_edges:
    #     clique = list(graph.nodes())
    #     clique.append(node)
    # return clique
    return len(graph.edges()) == clique_edges  

def explore (node, _graph):
    subgraph = _graph.subgraph(list(_graph.neighbors(node))) 

    # clique = verify_clique (node, subgraph)
    if verify_clique(subgraph):
        clique = list(subgraph.nodes())
        clique.append(node)
        return clique
    triangles,edges = compute_triangles (node, subgraph)

    k_triangles, next_neighbor = triangles.get_t_n()
    # while k_triangles > len(clique) or next_neighbor != None:
    while next_neighbor != None:
        clique = explore (next_neighbor, subgraph)
        k_triangles, next_neighbor = triangles.get_t_n()
    clique.append(node)
    return clique

def main(graph):
    graph = NX.k_core(graph, 2)
    max_clique = set()
    for node in graph:
        clique = explore (node, graph)
        if (len(clique) > len(max_clique)):
            max_clique = clique
    return max_clique

def calc_and_measure(G):
    start = time.time()
    result = main(G)
    end = time.time()
    print(main(G), end - start)

if __name__ == '__main__':
    # calc_and_measure(NX.cycle_graph(20))
    # calc_and_measure(NX.cycle_graph(200))
    # calc_and_measure(NX.cycle_graph(10))
    # calc_and_measure(NX.cycle_graph(2))
    # calc_and_measure(NX.cycle_graph(3))
    # calc_and_measure(NX.complete_graph(2))
    calc_and_measure(NX.complete_graph(9))
    