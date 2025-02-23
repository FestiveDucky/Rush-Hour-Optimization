import math
import time
from json.encoder import INFINITY

from ant import Ant
import numpy as np
import constants


class Vehicle:
    def __init__(self, start, end, graph, simulation):
        self.ants = []
        self.start = start
        self.end = end
        self.graph = graph
        self.simulation = simulation
        self.pheromones = np.full((graph.n, graph.n), constants.INITIAL_PHEROMONE_VALUE)
        self.heuristic = np.full((graph.n, graph.n), constants.INITIAL_PHEROMONE_VALUE)
        self.lastDecayed = np.zeros((graph.n, graph.n))
        self.timesDecayed = 0
        self.best = float('inf')

        for i in range(constants.NUM_ANTS):
            self.ants.append(Ant(self))

        self.bannedVertices = np.zeros(constants.N_VERTICES)

    def iterate(self):
        # start = time.time()

        bestPath = ([], float('inf')) # First value is the path which stores vertices, second value is path score
        for ant in self.ants:
            path = ant.generatePath()
            if bestPath[1] > path[1] >= 0:
                bestPath = path

        # print(f"Generate paths time: {time.time() - start}")

        # start = time.time()

        # Pheromone Decay
        self.timesDecayed += 1
        if not constants.EFFICIENT_DECAY_RATES:
            self.pheromones *= constants.PHEROMONE_DECAY_RATE

            # Limits the range of pheromone values
            np.clip(self.pheromones, constants.MIN_PHEROMONE_VALUE, constants.MAX_PHEROMONE_VALUE)

        # print(f"Decay time: {time.time() - start}")

        # start = time.time()
        # Updates pheromones along the best path
        for i in range(1, len(bestPath[0])):
            v = bestPath[0][i-1]
            u = bestPath[0][i]

            # Only decays on pheromone updates for paths -> updates all past times missed
            if constants.EFFICIENT_DECAY_RATES:
                self.pheromones[min(u - 1, v - 1)][max(u - 1, v - 1)] *= math.pow(constants.PHEROMONE_DECAY_RATE, self.timesDecayed - self.lastDecayed[min(u - 1, v - 1)][max(u - 1, v - 1)])
                self.lastDecayed[min(u - 1, v - 1)][max(u - 1, v - 1)] = self.timesDecayed

            # Updates pheromones
            # if ONLY_DEPOSIT_PHEROMONES_WHEN_BETTER_THAN_GLOBAL_BEST:
            self.pheromones[min(u - 1, v - 1)][max(u - 1, v - 1)] += constants.PHEROMONE_DEPOSIT_CONSTANT * (constants.MAX_PATH_LENGTH / 2) * (constants.MAX_ROAD_LENGTH / 2)/bestPath[1]

            # Limits the range of values of the pheromones:
            self.pheromones[min(u - 1, v - 1)][max(u - 1, v - 1)] = max(
                self.pheromones[min(v - 1, u - 1)][max(u - 1, v - 1)], constants.MIN_PHEROMONE_VALUE)
            self.pheromones[min(u - 1, v - 1)][max(u - 1, v - 1)] = min(
                self.pheromones[min(v - 1, u - 1)][max(u - 1, v - 1)], constants.MAX_PHEROMONE_VALUE)

        # print(f"Pheromone update time: {time.time() - start}")

        return bestPath

    def roundPheromones(self):
        self.pheromones = np.round(self.pheromones, 4)