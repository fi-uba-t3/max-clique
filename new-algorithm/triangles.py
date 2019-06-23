class Triangles():
    def __init__(self):
        self.T = []

    def add(self, node, triangles):
        while len(self.T) <= triangles + 1:
            self.T.append([])
        self.T[triangles].append(node)

    def get_max_clique_size(self, degree):
        ## Lists of greater degree should be empty by now
        ## 2 is because of the node in the explore function and the node which we are currently checking in the iterator 
        max_clique_size = degree + 2

        for amount_of_nodes in self.nodes_per_degree:
            if amount_of_nodes + 1 >= max_clique_size: # +1 because of the main_node
                break
            max_clique_size -= 1

        if len(self.nodes_per_degree) == 0:
            return 0

        self.nodes_per_degree = map(lambda x: x - 1, self.nodes_per_degree)
        ## Remove empty degrees list
        while self.nodes_per_degree and self.nodes_per_degree[0] == 0:
            self.nodes_per_degree.pop()
        return max_clique_size
        
    def get_t_n_iterator(self):
        self.nodes_per_degree = []
        self.T.reverse()
        previous_value = 0
        for list_of_nodes in self.T:

            self.nodes_per_degree.append(len(list_of_nodes) + previous_value)
            previous_value = self.nodes_per_degree[-1]
        self.T.reverse()
        current_list = len(self.T) - 1

        current_place = 0
        while current_list >= 0:
            if current_place >= len(self.T[current_list]):
                current_list -= 1
                current_place = 0
                continue

            next_neighbor = self.T[current_list][current_place]
            current_place +=1
            yield self.get_max_clique_size(current_list) , next_neighbor    
