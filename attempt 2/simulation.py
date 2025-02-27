import time
import multiprocessing
import matplotlib.pyplot as plt
import heapdict
import numpy as np
import math
import sys
from graph import Graph
import random
import constants
from vehicle import Vehicle


class Simulation:
    def __init__(self):
        self.graph = None
        self.vehicles = []

        # Generate random graph
        self.generateGraph()

        self.bestSolution = {}
        self.bestSolutionScore = float('inf')

        self.destinations = set()
        # Generate vehicles
        self.vehicles = []
        for i in range(constants.NUM_VEHICLES):
            self.vehicles.append(
                Vehicle(random.randint(1, constants.N_VERTICES), random.randint(1, constants.N_VERTICES), self.graph, self, i))
            self.bestSolution[i] = (None, float('inf'))
            self.destinations.add(self.vehicles[-1].end)
        self.globalTrafficDensity = np.zeros((constants.N_VERTICES, constants.N_VERTICES))

        # Precalculated dijkstra score
        self.baseScore = 0

        # key: destination, value: list of vertices and their distance from the end location
        self.heuristics = {}
        if constants.HEURISTIC_FUNCTION:
            self.dijkstra()

        self.scores = []

    def dijkstra(self):
        parents = {}
        for destination in self.destinations:
            parents[destination] = {}
            unvisited = heapdict.heapdict()
            distances = [float('inf') for x in range(constants.N_VERTICES)]
            # Set up infinite distances for all vertices
            for i in range(1, constants.N_VERTICES + 1):
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

        # Double check that all the vehicles have valid paths and remove the invalid ones
        deletedCount = 0
        for i in reversed(range(constants.NUM_VEHICLES)):
            if self.heuristics[self.vehicles[i].end][self.vehicles[i].start - 1] == float('inf') or self.vehicles[i].start == self.vehicles[i].end:
                self.vehicles.pop(i)
                constants.NUM_VEHICLES -= 1
                deletedCount += 1
        print(f"Deleted {deletedCount} vehicles!")

        # Add up global pheromones
        for i in range(constants.NUM_VEHICLES):
            v = self.vehicles[i].start
            u = parents[self.vehicles[i].end][v]
            while u != -1:
                self.globalTrafficDensity[min(u - 1, v - 1)][max(u - 1, v - 1)] += 1
                v = u
                u = parents[self.vehicles[i].end][v]

        # Calculate costs
        for i in range(constants.NUM_VEHICLES):
            v = self.vehicles[i].start
            u = parents[self.vehicles[i].end][v]

            path = [v, u]
            while u != -1:
                roadLength = self.graph.edgeWeight(u, v)
                globalPheromone = self.globalTrafficDensity[min(u - 1, v - 1)][max(u - 1, v - 1)]
                if constants.COST_BASED_ON_TRAFFIC_DENSITY and globalPheromone != 0:
                    self.baseScore += roadLength * constants.MAX_GLOBAL_PHEROMONE_MULTIPLIER * math.pow(globalPheromone, constants.GLOBAL_PHEROMONE_EXPONENT) / math.pow(
                        roadLength / constants.MIN_ROAD_SPACE_PER_CAR, constants.GLOBAL_PHEROMONE_EXPONENT)
                else:
                    # Cost not based on traffic density
                    self.baseScore += roadLength

                v = u
                u = parents[self.vehicles[i].end][v]

                if constants.PRINT_DIJKSTRA_PATHS:
                    path.append(u)
            if constants.PRINT_DIJKSTRA_PATHS:
                print(f"PATH: {path}, score {self.baseScore}")

        # Reset global pheromones
        self.globalTrafficDensity = np.zeros((constants.N_VERTICES, constants.N_VERTICES))


    def generateGraph(self):
        self.graph = Graph()

        if constants.IMPORT_GRAPH_DATA:
            self.graph.importData()
            constants.N_VERTICES = self.graph.n
            constants.M_EDGES = self.graph.m
            print("--------------------------------------FINISHED--------------------------------------------------")
            return

        if constants.LOAD_GRAPH_DATA:
            self.graph.loadFromFile()
            constants.N_VERTICES = self.graph.n
            constants.M_EDGES = self.graph.m
            return

        # Generates a random graph with random weights
        for i in range(constants.N_VERTICES):
            self.graph.addVertex()

        for i in range(constants.M_EDGES):
            self.graph.addEdge(random.randint(1, constants.N_VERTICES), random.randint(1, constants.N_VERTICES),
                               random.random() * constants.MAX_ROAD_LENGTH + constants.MIN_ROAD_LENGTH)

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
        if constants.MULTIPROCESSING:
            pool = multiprocessing.Pool(processes=8)

        # bestPath = (None, math.inf)
        for i in range(iterations):
            # paths: (path, score, vehicle id)
            if constants.MULTIPROCESSING:
                paths = list(pool.map(self.iterate, self.vehicles))
            else:
                paths = []
                for vehicle in self.vehicles:
                    paths.append(vehicle.iterate())

            # Global pheromones
            temp = None
            if constants.DECAY_GLOBAL_PHEROMONES:
                self.globalTrafficDensity *= constants.GLOBAL_PHEROMONE_DECAY_RATE
                temp = self.globalTrafficDensity.copy()
                self.globalTrafficDensity = np.zeros((constants.N_VERTICES, constants.N_VERTICES))
            else:
                self.globalTrafficDensity = np.zeros((constants.N_VERTICES, constants.N_VERTICES))

            for path in paths:
                for j in range(1, len(path[0])):
                    v = path[0][j - 1]
                    u = path[0][j]
                    self.globalTrafficDensity[min(u - 1, v - 1)][max(u - 1, v - 1)] += 1
                    self.globalTrafficDensity[min(u - 1, v - 1)][max(u - 1, v - 1)] = min(constants.NUM_VEHICLES, self.globalTrafficDensity[min(u - 1, v - 1)][max(u - 1, v - 1)])
                    if constants.DECAY_GLOBAL_PHEROMONES:
                        temp[min(u - 1, v - 1)][max(u - 1, v - 1)] += 1
                        temp[min(u - 1, v - 1)][max(u - 1, v - 1)] = min(constants.NUM_VEHICLES, temp[min(u - 1, v - 1)][max(u - 1, v - 1)])

            if not constants.PRINT_ALL_ITERATIONS:
                sys.stdout.write(f"\rCompleted: {100 * (i + 1) / iterations}%")
                sys.stdout.flush()


            currentSolution = {}
            total = 0
            # Final analysis
            for path in paths:
                # COST FUNCTION NEEDED BECAUSE DURING EXECUTION GLOBAL PHEROMONES ARE NOT UPDATED
                pathScore = 0
                for j in range(1, len(path[0])):
                    v = path[0][j - 1]
                    u = path[0][j]

                    roadLength = self.graph.edgeWeight(u, v)
                    globalPheromone = self.globalTrafficDensity[min(u - 1, v - 1)][max(u - 1, v - 1)]
                    if constants.COST_BASED_ON_TRAFFIC_DENSITY and globalPheromone != 0:
                        pathScore += roadLength * constants.MAX_GLOBAL_PHEROMONE_MULTIPLIER * math.pow(globalPheromone, constants.GLOBAL_PHEROMONE_EXPONENT) / math.pow(
                            roadLength / constants.MIN_ROAD_SPACE_PER_CAR, constants.GLOBAL_PHEROMONE_EXPONENT)
                    else:
                        # Cost not based on traffic density
                        pathScore += roadLength

                if len(path[0]) == 0:
                    pathScore += constants.INCOMPLETE_PENALTY

                total += pathScore
                currentSolution[path[2]] = (path[0], pathScore)

            if constants.PRINT_ALL_ITERATIONS or i == iterations - 1:
                # score: {path[1]}, path: {path[0]},
                print(f"Iter: {i}, dijkstra: {self.baseScore}, global best: {self.bestSolutionScore}, cumulative score: {total}")

            # Update best solution over all time
            if total < self.bestSolutionScore:
                self.bestSolutionScore = total
                self.bestSolution = currentSolution.copy()

            if constants.DECAY_GLOBAL_PHEROMONES:
                self.globalTrafficDensity = temp.copy()

            self.scores.append(total)
            self.plot()



            if constants.AUTOMATIC_ADJUSTMENT_OF_CONSTANTS and len(self.scores) >= constants.MINIMUM_NUMBER_OF_SCORES_TO_ADAPT:
                # Check if the past 10 scores are ~ the same
                maxScore = -1
                minScore = float('inf')
                averageScore = 0

                for j in range(len(self.scores) - constants.MINIMUM_NUMBER_OF_SCORES_TO_ADAPT, len(self.scores)):
                    maxScore = max(maxScore, self.scores[j])
                    minScore = min(minScore, self.scores[j])
                    averageScore += self.scores[j]

                averageScore /= constants.MINIMUM_NUMBER_OF_SCORES_TO_ADAPT
                scoreRange = maxScore - minScore

                # If they are then we enable automatic adaptation
                if scoreRange <= constants.PROPORTION_OF_TOTAL_SCORE_TO_ADAPT * averageScore:
                    print(f"Enabled automatic adaptation on iteration {i}")
                    # constants.PHEROMONE_DECAY_RATE = 0.8
                    constants.HEURISTIC_EXPONENT = 1
                    constants.PHEROMONE_EXPONENT = 5
                    # constants.GLOBAL_EXPONENT = 50
                    # constants.p = 0.6
                # else:
                #     constants.PHEROMONE_DECAY_RATE = 0.85
                #     constants.PHEROMONE_EXPONENT = 50
                #     constants.p = 0.99
                print(f"Iteration: {i}, p: {constants.p}, decay rate: {constants.PHEROMONE_DECAY_RATE}")
        # Permanently show the graph at the end of the simulation
        plt.show()