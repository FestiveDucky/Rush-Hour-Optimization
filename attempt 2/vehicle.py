import math
import time
from json.encoder import INFINITY

from ant import Ant
import numpy as np
from constants import *


class Vehicle:
    def __init__(self, start, end, graph, simulation):
        # print("START", start, "END:", end)
        self.ants = []
        self.start = start
        self.end = end
        self.graph = graph
        self.simulation = simulation
        self.pheromones = np.full((graph.n, graph.n), INITIAL_PHEROMONE_VALUE)
        self.heuristic = np.full((graph.n, graph.n), INITIAL_PHEROMONE_VALUE)
        self.lastDecayed = np.zeros((graph.n, graph.n))
        self.timesDecayed = 0

        for i in range(NUM_ANTS):
            self.ants.append(Ant(self))

    def iterate(self):
        # start = time.time()

        bestPath = (None, math.inf) # First value is the path which stores vertices, second value is path score
        for ant in self.ants:
            p = ant.generatePath()
            if p[1] < bestPath[1]:
                bestPath = p

        # print(f"Generate paths time: {time.time() - start}")

        # start = time.time()

        # Pheromone Decay
        self.timesDecayed += 1
        if not EFFICIENT_DECAY_RATES:
            self.pheromones *= PHEROMONE_DECAY_RATE

            # limits the minimum value of the pheromones
            if PHEROMONE_LIMITS_FLOOR:
                self.pheromones[self.pheromones < MIN_PHEROMONE_VALUE] = MIN_PHEROMONE_VALUE

        # print(f"Decay time: {time.time() - start}")

        # start = time.time()
        # Updates pheromones along the best path
        for i in range(1, len(bestPath[0])):
            v = bestPath[0][i-1]
            u = bestPath[0][i]

            # Only decays on pheromone updates for paths -> updates all past times missed
            if EFFICIENT_DECAY_RATES:
                self.pheromones[min(u - 1, v - 1)][max(u - 1, v - 1)] *= math.pow(PHEROMONE_DECAY_RATE, self.timesDecayed - self.lastDecayed[min(u - 1, v - 1)][max(u - 1, v - 1)])
                self.lastDecayed[min(u - 1, v - 1)][max(u - 1, v - 1)] = self.timesDecayed

                # Limits the minimum value of pheromones
                if PHEROMONE_LIMITS_FLOOR:
                    self.pheromones[min(u - 1, v - 1)][max(u - 1, v - 1)] = max(
                        self.pheromones[min(v - 1, u - 1)][max(u - 1, v - 1)], MIN_PHEROMONE_VALUE)

            # Updates pheromones
            self.pheromones[min(u - 1, v - 1)][max(u - 1, v - 1)] += PHEROMONE_DEPOSIT_CONSTANT/bestPath[1]

        # print(f"Pheromone update time: {time.time() - start}")
        # print(self.pheromones)
        return bestPath

    def roundPheromones(self):
        self.pheromones = np.round(self.pheromones, 4)