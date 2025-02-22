import time
import multiprocessing
import matplotlib.pyplot as plt
import pandas as pd
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

        self.destinations = set()
        # Generate vehicles
        self.vehicles = []
        for i in range(NUM_VEHICLES):
            self.vehicles.append(
                Vehicle(random.randint(1, N_VERTICES), random.randint(1, N_VERTICES), self.graph, self))
            self.destinations.add(self.vehicles[-1].end)

        self.globalTrafficDensity = np.zeros((N_VERTICES, N_VERTICES))

        # Precalculated dijkstra score
        self.baseScore = 0

        # key: destination, value: list of vertices and their distance from the end location
        self.heuristics = {}
        if HEURISTIC_FUNCTION:
            self.dijkstra()

        self.scores = []

    def dijkstra(self):
        parents = {}
        for destination in self.destinations:
            parents[destination] = {}
            unvisited = heapdict.heapdict()
            distances = [float('inf') for x in range(N_VERTICES)]
            # Set up infinite distances for all vertices
            for i in range(1, N_VERTICES + 1):
                if i != destination:
                    unvisited[i] = float('inf')

            unvisited[destination] = 0
            distances[destination - 1] = 0
            parents[destination][destination] = -1

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
                        unvisited[neighbor] = distances[neighbor - 1]
                        parents[destination][neighbor] = current[0]

            self.heuristics[destination] = distances

        global NUM_VEHICLES
        # Double check that all the vehicles have valid paths and remove the invalid ones
        for i in reversed(range(NUM_VEHICLES)):
            if self.heuristics[self.vehicles[i].end][self.vehicles[i].start - 1] == float('inf') or self.vehicles[i].start == self.vehicles[i].end:
                self.vehicles.pop(i)
                NUM_VEHICLES -= 1

        # Add up global pheromones
        for i in range(NUM_VEHICLES):
            v = self.vehicles[i].start
            u = parents[self.vehicles[i].end][v]
            while u != -1:
                self.globalTrafficDensity[min(u - 1, v - 1)][max(u - 1, v - 1)] += 1
                v = u
                u = parents[self.vehicles[i].end][v]

        # Calculate costs
        for i in range(NUM_VEHICLES):
            v = self.vehicles[i].start
            u = parents[self.vehicles[i].end][v]
            while u != -1:
                roadLength = self.graph.edgeWeight(u, v)
                globalPheromone = self.globalTrafficDensity[min(u - 1, v - 1)][max(u - 1, v - 1)]
                if COST_BASED_ON_TRAFFIC_DENSITY and globalPheromone != 0:
                    self.baseScore += roadLength * MAX_GLOBAL_PHEROMONE_MULTIPLIER * math.pow(globalPheromone, GLOBAL_PHEROMONE_EXPONENT) / math.pow(
                        roadLength / MIN_ROAD_SPACE_PER_CAR, GLOBAL_PHEROMONE_EXPONENT)
                else:
                    # Cost not based on traffic density
                    self.baseScore += roadLength

                v = u
                u = parents[self.vehicles[i].end][v]

        # Reset global pheromones
        self.globalTrafficDensity = np.zeros((N_VERTICES, N_VERTICES))


    def generateGraph(self):
        # Generates a random graph with random weights
        self.graph = Graph()
        for i in range(N_VERTICES):
            self.graph.addVertex()

        for i in range(M_EDGES):
            self.graph.addEdge(random.randint(1, N_VERTICES), random.randint(1, N_VERTICES),
                               random.random() * MAX_ROAD_LENGTH + MIN_ROAD_LENGTH)

    @staticmethod
    def iterate(v):
        return v.iterate()

    def plot(self):
        # plt.scatter(len(self.scores), self.scores[-1])
        plt.cla()
        plt.plot(range(1, len(self.scores) + 1), [self.baseScore] * len(self.scores))
        plt.plot(range(1, len(self.scores) + 1), self.scores)
        # plt.savefig("graph7.png")
        plt.pause(0.01)

    def execute(self, iterations):
        pool = None
        if MULTIPROCESSING:
            pool = multiprocessing.Pool(processes=8)

        # bestPath = (None, math.inf)
        for i in range(iterations):
            # paths: (path, score)
            if MULTIPROCESSING:
                paths = list(pool.map(self.iterate, self.vehicles))
            else:
                paths = []
                for vehicle in self.vehicles:
                    paths.append(vehicle.iterate())

            # Global pheromones
            if DECAY_GLOBAL_PHEROMONES:
                self.globalTrafficDensity *= GLOBAL_PHEROMONE_DECAY_RATE
            else:
                self.globalTrafficDensity = np.zeros((N_VERTICES, N_VERTICES))

            for path in paths:
                for j in range(1, len(path[0])):
                    v = path[0][j - 1]
                    u = path[0][j]
                    self.globalTrafficDensity[min(u - 1, v - 1)][max(u - 1, v - 1)] += 1
                    self.globalTrafficDensity[min(u - 1, v - 1)][max(u - 1, v - 1)] = min(NUM_VEHICLES, self.globalTrafficDensity[min(u - 1, v - 1)][max(u - 1, v - 1)])


            if not PRINT_ALL_ITERATIONS:
                sys.stdout.write(f"\rCompleted: {100 * (i + 1) / iterations}%")
                sys.stdout.flush()

            total = 0
            # Final analysis
            for path in paths:
                # COST FUNCTION NEEDED BECAUSE DURING EXECUTION GLOBAL PHEROMONES ARE NOT UPDATED
                for j in range(1, len(path[0])):
                    v = path[0][j - 1]
                    u = path[0][j]

                    roadLength = self.graph.edgeWeight(u, v)
                    globalPheromone = self.globalTrafficDensity[min(u - 1, v - 1)][max(u - 1, v - 1)]
                    if COST_BASED_ON_TRAFFIC_DENSITY and globalPheromone != 0:
                        total += roadLength * MAX_GLOBAL_PHEROMONE_MULTIPLIER * math.pow(globalPheromone, GLOBAL_PHEROMONE_EXPONENT) / math.pow(
                            roadLength / MIN_ROAD_SPACE_PER_CAR, GLOBAL_PHEROMONE_EXPONENT)
                    else:
                        # Cost not based on traffic density
                        total += roadLength
                if PRINT_ALL_ITERATIONS or i == iterations - 1:
                    print(f"Iter: {i}, score: {path[1]}, path: {path[0]}, cummulative score: {total}")

            self.scores.append(total)
            self.plot()
        # Permanently show the graph at the end of the simulation
        plt.show()