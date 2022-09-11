class Graph():

    #to create a graph it is convinient to use an adjancency list
    def __init__(self, num_nodes, edges, ismatrix=False):
        self.num_nodes = num_nodes
        self.edges = edges
        self.data = [[] for i in range(num_nodes)]
        self.ismatrix = ismatrix
        if not ismatrix:
            for i, j in edges:
                self.data[i].append(j)
                self.data[j].append(i)
        else:
            Graph.create_matrix(self)   #see the nodes in a matrix  inform 0's and 1's. 1's --> " ", 0's --> "#"
    def __repr__(self):
        if not self.ismatrix:
            return "\n".join([f"{i}: {j}" for i,j in enumerate(self.data)])
        else:
            return "\n".join(["    "+str([i for i in range(self.num_nodes)]).strip("[").strip("]")]+[f"{i}: {j}" for i,j in enumerate(self.data)])
    def __str__(self):
        return self.__repr__()

    def create_matrix(self):
        for i in range(len(self.data)):
            self.data[i] = [0] * self.num_nodes
        for n1, n2 in self.edges:
            self.data[n1][n2] = 1
            self.data[n2][n1] = 1
