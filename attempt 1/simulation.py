from graph import UndirectedGraph
from random import *


class Simulation:
    def __init__(self):
        self.graphs = [UndirectedGraph()]
        self.pairs = {}

    def getGraph(self, index):
        if index >= len(self.graphs):
            self.graphs.append(UndirectedGraph())
        return self.graphs[index]

    def saveGraphs(self):
        pass

    def loadGraphs(self):
        pass

    def initiate(self):
        # Create pairs of vertices
        # Dijkstra the entire graph -> find distance from
        pass

    def tick(self):
        pass
