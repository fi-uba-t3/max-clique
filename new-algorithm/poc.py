import networkx as NX

class Triangles():
    def __init__(self):
        self.current_list = 0
        self.current_place = 0
        self.T = []

    def add(self, node, triangles):
        while len(self.T) <= triangles:
            self.T.append([])
        self.T[triangles].append(node)
        self.current_list = 0
        self.current_place = 0

    def get_t_n(self):
        print(self.T)
        while self.current_place >= len(self.T[self.current_list]):
            self.current_list += 1
            self.current_place = 0
        if self.current_list > len(self.T):
            return None, None

        print(self.current_list)
        print(self.current_place)

        next_neighbor = self.T[self.current_list][self.current_place]
        self.current_place +=1
        return self.current_list, next_neighbor
        

def compute_triangles(node, graph):
    T = Triangles()
    for n in graph.neighbors(node):
        edges = graph.degree(n)
        t = edges - 1 # Hmmm, no estoy seguro de que estos sean los triangulos
        T.add(n, t)
    return T

def verify_clique(node, graph):
    clique = []
    d = graph.degree(node)
    clique_edges = d * (d - 1) / 2
    if len(graph.edges()) == clique_edges:
        clique = list(graph.neighbors(node)).append(node)
    return clique    

def explore (node, father, _graph):
    graph = _graph.subgraph(list(_graph.neighbors(node)).append(node)) 
    print(node)
    triangles = compute_triangles (node, graph)
    clique = verify_clique (node, graph)
    k_triangles, next_neighbor = triangles.get_t_n()
    while k_triangles > len(clique) or next_neighbor != None:
        clique = explore (next_neighbor, node, graph)
        k_triangles, next_neighbor = triangles.get_t_n()
        return clique

def main (graph):
    # graph := compute_2-core (graph)   # esto es una optimizacion 
    max_clique = set()
    for node in graph:
        # k_triangles, next_neighbor = triangles.get_t_n()

        clique = explore (node, node, graph)
        if (len(clique) > len(max_clique)):
            max_clique = clique
    return max_clique

if __name__ == '__main__':
    G = NX.cycle_graph(20)
    print(main(G))