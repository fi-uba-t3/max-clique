
class Graph(object):

    def __init__(self):
        self._nodes = dict()
        self._edges = set()
    
    def load(self, path):

        edges = []

        with open(path) as f:
            lines = f.readlines()

        edges = list(map(lambda x: tuple(x.strip("\n").split(" ")), lines))
        edges = list(map(lambda y: (int(y[0]), int(y[1])), edges))

        for e in edges:
            self.add_edge(e)

    def edges(self):
        return list(self._edges)

    def nodes(self):
        return list(self._nodes.keys())

    def degree(self, x):
        return len(self.neighbors(x))

    def neighbors(self, x):

        ngbs = {k: v for k, v in self._nodes[x].items() if v}
        
        return list(ngbs.keys())

    def add_edge(self, e):
        
        v1, v2 = e

        if v1 not in self._nodes:
            self._nodes[v1] = dict()

        self._nodes[v1][v2] = True

        if v2 not in self._nodes:
            self._nodes[v2] = dict()

        self._nodes[v2][v1] = True

        self._edges.add(e)

    def add_node(self, v):
        self._nodes[v] = dict()

    def remove_node(self, x):
        
        ngbs = self.neighbors(x)    

        for n in ngbs:
            self._nodes[n][x] = False

        del self._nodes[x]

        self._edges = set(filter(lambda e: e[0] != x and e[1] != x, self._edges))
    
    def remove_edge(self, e):

        v1, v2 = e

        self._edges.remove(e)

        self._nodes[v1][v2] = False

        self._nodes[v2][v1] = False

