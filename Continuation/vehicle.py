import math
import time
from ant import Ant
import numpy as np
import constants


class Vehicle:
    def __init__(self, start, end, graph, simulation, id):
        self.ants = []
        self.id = id
        self.start = start
        self.end = end
        # self.departureTime =
        self.graph = graph
        self.simulation = simulation
        self.pheromones = np.full((graph.n, graph.n), constants.INITIAL_PHEROMONE_VALUE)
        self.heuristic = np.full((graph.n, graph.n), constants.INITIAL_PHEROMONE_VALUE)
        self.lastDecayed = np.zeros((graph.n, graph.n))
        self.timesDecayed = 0

        for i in range(constants.NUM_ANTS):
            self.ants.append(Ant(self))

        self.bannedVertices = np.zeros(constants.N_VERTICES)

    def iterate(self):
        # start = time.time()

        bestPath = ([], float('inf'), self.id) # First value is the path which stores vertices, second value is path score
        for ant in self.ants:
            path = ant.generatePath()
            if bestPath[1] > path[1] >= 0:
                bestPath = path
        # print(f"Generate paths time: {time.time() - start}")

        # Pheromone Decay
        self.timesDecayed += 1

        # start = time.time()
        # Updates pheromones along the best path
        for i in range(1, len(bestPath[0])):
            v = max(bestPath[0][i-1] - 1, bestPath[0][i] - 1)
            u = min(bestPath[0][i-1] - 1, bestPath[0][i] - 1)

            # Only decays on pheromone updates for paths -> updates all past times missed
            self.pheromones[u][v] *= math.pow(constants.PHEROMONE_DECAY_RATE, self.timesDecayed - self.lastDecayed[u][v])
            self.lastDecayed[u][v] = self.timesDecayed

            # Updates pheromones (uses the formula of best score / current score)
            bestScore = self.simulation.bestSolution[self.id][1]
            if bestScore == float('inf'):
                bestScore = (constants.MAX_PATH_LENGTH / 2) * (constants.MAX_ROAD_LENGTH / 2)
            self.pheromones[u][v] += constants.PHEROMONE_DEPOSIT_CONSTANT * bestScore/bestPath[1]
            # Old formula: constants.PHEROMONE_DEPOSIT_CONSTANT * (constants.MAX_PATH_LENGTH / 2) * (constants.MAX_ROAD_LENGTH / 2)/bestPath[1]

            # print(f"DEPOSITED: {constants.PHEROMONE_DEPOSIT_CONSTANT * bestScore/bestPath[1]}")

            # Limits the range of values of the pheromones:
            self.pheromones[u][v] = max(self.pheromones[u][v], constants.MIN_PHEROMONE_VALUE)
            self.pheromones[u][v] = min(self.pheromones[u][v], constants.MAX_PHEROMONE_VALUE)

        # Deposit extra pheromones for global best solution (basically a copy of above code but I am lazy to find better way)
        if constants.DEPOSIT_PHEROMONES_ON_GLOBAL_BEST and self.simulation.bestSolutionScore != float('inf'):
            for i in range(1, len(self.simulation.bestSolution[self.id][0])):
                v = max(self.simulation.bestSolution[self.id][0][i - 1] - 1, self.simulation.bestSolution[self.id][0][i] - 1)
                u = min(self.simulation.bestSolution[self.id][0][i - 1] - 1, self.simulation.bestSolution[self.id][0][i] - 1)

                # Only decays on pheromone updates for paths -> updates all past times missed
                self.pheromones[u][v] *= math.pow(constants.PHEROMONE_DECAY_RATE, self.timesDecayed - self.lastDecayed[u][v])
                self.lastDecayed[u][v] = self.timesDecayed

                # Updates pheromones
                self.pheromones[u][v] = max(self.pheromones[u][v], constants.MAX_PHEROMONE_FOR_GLOBAL_BEST_PATH)

                # Limits the range of values of the pheromones:
                # self.pheromones[min(u - 1, v - 1)][max(u - 1, v - 1)] = max(
                #     self.pheromones[min(v - 1, u - 1)][max(u - 1, v - 1)], constants.MIN_PHEROMONE_VALUE)
                # self.pheromones[min(u - 1, v - 1)][max(u - 1, v - 1)] = min(
                #     self.pheromones[min(v - 1, u - 1)][max(u - 1, v - 1)], constants.MAX_PHEROMONE_VALUE)

        # print(f"Pheromone update time: {time.time() - start}")

        return bestPath

    def roundPheromones(self):
        self.pheromones = np.round(self.pheromones, 4)