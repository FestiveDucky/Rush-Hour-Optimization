import time
import multiprocessing
import heapdict
import numpy as np
import math
import sys
from graph import Graph
import random
from constants import *
from vehicle import Vehicle


class Simulation:
    def __init__(self):
        self.graph = None
        self.vehicles = []

        # Generate random graph
        self.generateGraph()
        print(self.graph.adjList)

        self.destinations = set()
        # Generate vehicles
        self.vehicles = []
        for i in range(NUM_VEHICLES):
            self.vehicles.append(
                Vehicle(random.randint(1, N_VERTICES), random.randint(1, N_VERTICES), self.graph, self))
            self.destinations.add(self.vehicles[-1].end)

        self.globalTrafficDensity = np.zeros((N_VERTICES, N_VERTICES))

        # key: destination, value: list of vertices and their distance from the end location
        self.heuristics = {}
        self.dijkstra()

    def dijkstra(self):
        for destination in self.destinations:
            unvisited = heapdict.heapdict()
            distances = [float('inf') for x in range(N_VERTICES)]
            # Set up infinite distances for all vertices
            for i in range(1, N_VERTICES + 1):
                if i != destination:
                    unvisited[i] = float('inf')

            unvisited[destination] = 0
            distances[destination - 1] = 0

            while True:
                if len(unvisited) == 0:
                    break
                current = unvisited.popitem()
                if current[1] == float('inf'):
                    break

                # Update neighbor distances
                for neighbor in self.graph.neighbors(current[0]):
                    prev = distances[neighbor - 1]
                    distances[neighbor - 1] = min(distances[neighbor - 1], current[1] + self.graph.edgeWeight(current[0], neighbor))
                    if prev != distances[neighbor - 1]:
                        print("CHANGING", neighbor, distances[neighbor - 1])
                        unvisited[neighbor] = distances[neighbor - 1]

            self.heuristics[destination] = distances
        print(self.heuristics)
        print(self.heuristics[self.vehicles[0].end][self.vehicles[0].start - 1])

    def generateGraph(self):
        self.graph = Graph()
        for i in range(N_VERTICES):
            self.graph.addVertex()

        for i in range(M_EDGES):
            self.graph.addEdge(random.randint(1, N_VERTICES), random.randint(1, N_VERTICES),
                               random.random() * MAX_ROAD_LENGTH + MIN_ROAD_LENGTH)

    @staticmethod
    def iterate(v):
        return v.iterate()

    def execute(self, iterations):
        if MULTIPROCESSING:
            pool = multiprocessing.Pool(processes=8)
        bestPath = (None, math.inf)
        for i in range(iterations):
            if MULTIPROCESSING:
                paths = list(pool.map(self.iterate, self.vehicles))

            else:
                paths = []
                for vehicle in self.vehicles:
                    paths.append(vehicle.iterate())

            # Global pheromones
            self.globalTrafficDensity *= GLOBAL_PHEROMONE_DECAY_RATE
            for p in paths:
                for j in range(1, len(p[0])):
                    v = p[0][j - 1]
                    u = p[0][j]
                    self.globalTrafficDensity[min(u - 1, v - 1)][max(u - 1, v - 1)] += 1

            if not PRINT_ALL_ITERATIONS:
                sys.stdout.write(f"\rCompleted: {100 * (i + 1) / iterations}%")
                sys.stdout.flush()

            # Final analysis
            # TODO possibly change the path for final output to be the best path over all iterations
            for p in paths:
                if PRINT_ALL_ITERATIONS or i == iterations - 1:

                    # COST FUNCTION
                    commonScore = 0
                    for j in range(1, len(p[0])):
                        v = p[0][j - 1]
                        u = p[0][j]

                        commonScore += self.graph.edgeWeight(u, v) * (1 + (MAX_TRAFFIC_MULTIPLIER - 1)
                                                                      * math.pow(
                                    self.globalTrafficDensity[min(u - 1, v - 1)][max(u - 1, v - 1)],
                                    TRAFFIC_MULTIPLIER_EXPONENT)
                                                                      / math.pow(NUM_VEHICLES,
                                                                                 TRAFFIC_MULTIPLIER_EXPONENT))

                    print(f"Iter: {i}, score: {p[1]}, path: {p[0]}, common score: {commonScore}")

    # print(bestPath)
