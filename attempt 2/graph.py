# Undirected weighted graph
class Graph:
    def __init__(self):
        # Adjacency list implement
        self.n = 0
        self.m = 0
        self.adjList = {}

    def addVertex(self):
        self.n += 1
        self.adjList[self.n] = {}

    def addEdge(self, u, v, w):
        if u == v:
            return
        self.m += 1
        self.adjList[u][v] = w
        self.adjList[v][u] = w

    def hasEdge(self, u, v):
        return v in self.adjList[u].keys()

    def edgeWeight(self, u, v):
        return self.adjList[u][v]

    def removeEdge(self, u, v):
        self.m -= 1
        self.adjList[u].pop(v)
        self.adjList[v].pop(u)

    def neighbors(self, v):
        return list(self.adjList[v].keys())
