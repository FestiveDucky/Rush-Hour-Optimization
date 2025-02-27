import geopy.distance
from lxml import etree
from pathlib import Path

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

    def importData(self):
        data = etree.parse('map.osm').getroot()
        print("FINISHED LOADING")
        # def prettyprint(element, **kwargs):
        #     xml = etree.tostring(element, pretty_print=True, **kwargs)
        #     print(xml.decode(), end='')

        coords = {}
        i = 1
        while data[i].tag == "node":
            self.n += 1
            self.adjList[data[i].get('id')] = {}
            coords[data[i].get('id')] = (float(data[i].get('lat')), float(data[i].get('lon')))
            i += 1

        while i != len(data) and data[i].tag == "way":
            prevNode = None

            isRoad = False
            for child in data[i]:
                # remove "service" which are driveways
                allowedRoads = ["motorway","trunk", "primary", "secondary", "tertiary", "unclassified", "residential", "living_street", "motorway_link", "trunk_link", "primary_link", "secondary_link", "tertiary_link"]
                print(child.get("v"))
                if child.tag == "tag" and child.get("k") == "highway" and child.get("v") in allowedRoads:
                    isRoad = True
                    break

            if not isRoad:
                i += 1
                continue

            for child in data[i]:
                if child.tag == "nd":
                    curNode = child.get("ref")
                    if prevNode is not None:
                        d = geopy.distance.geodesic(coords[prevNode], coords[curNode]).m
                        self.m += 1
                        self.adjList[prevNode][curNode] = d
                        self.adjList[curNode][prevNode] = d
                    prevNode = curNode
            i += 1
        print(f"Edges {self.m} Nodes {self.n}")

        # Remove redundant edges
        toRemove = []
        for v, neighbors in self.adjList.items():
            if len(neighbors) == 2:
                n1 = list(neighbors.keys())[0]
                n2 = list(neighbors.keys())[1]
                self.adjList[n1].pop(v)
                self.adjList[n2].pop(v)
                d = neighbors[n1] + neighbors[n2]
                self.adjList[n1][n2] = d
                self.adjList[n2][n1] = d
                toRemove.append(v)
                self.m -= 1
            elif len(neighbors) == 0:
                toRemove.append(v)

        for v in toRemove:
            self.adjList.pop(v)
            self.n -= 1

        # Change all indices back to 1 -> n
        newAdjList = {}
        idMappings = {}
        for i, v in enumerate(self.adjList.keys(), 1):
            idMappings[v] = i
            newAdjList[i] = {}

        for v, neighbors in self.adjList.items():
            for neighbor, weight in neighbors.items():
                newAdjList[idMappings[v]][idMappings[neighbor]] = weight

        self.adjList = newAdjList

        self.writeToFile()

    def writeToFile(self):
        with open("graph.txt", 'w') as fout:
            fout.write(f"{self.n} {self.m}\n")
            fout.write(str(self))

    def loadFromFile(self):
        with open("graph.txt", "r") as fin:
            n, m = fin.readline().split(" ")

            for i in range(int(n)):
                self.addVertex()

            # print(self.adjList.items())
            for i in range(int(m)):
                u, v, w = fin.readline().split(" ")
                self.addEdge(int(u), int(v), float(w))


    def __str__(self):
        return "\n".join(["\n".join([f"{v} {u} {w}" for u, w in weights.items()]) for v, weights in self.adjList.items()])