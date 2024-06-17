from graph import UndirectedGraph


class Simulation:
    def __init__(self):
        self.graphs = [UndirectedGraph()]

    def getGraph(self, index):
        if index >= len(self.graphs):
            self.graphs.append(UndirectedGraph())
        return self.graphs[index]

    def saveGraphs(self):
        pass

    def loadGraphs(self):
        pass

    def tick(self):
        pass
