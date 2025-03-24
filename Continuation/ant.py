import random

import numpy as np

import constants
import math


class Ant:
    def __init__(self, parent):
        self.parent = parent
        self.vertexFromLastIntersection = None

    def generatePath(self):
        # print("NEWANT")
        path = [self.parent.start]
        visited = np.zeros(constants.N_VERTICES)
        score = 0
        alreadyVisited = False
        while path[-1] != self.parent.end and len(path) < constants.MAX_PATH_LENGTH:
            neighbors = self.parent.graph.neighbors(path[-1])
            weights = []
            largestWeight = 0
            cumulativeTotal = 0
            skippedCuzVisited = 0
            for neighbor in neighbors:
                # Makes the ant never go along same path
                if visited[neighbor-1]:
                    weights.append(0)
                    skippedCuzVisited += 1
                # If the vertex is banned we also skip it
                elif self.parent.bannedVertices[neighbor-1]:
                    weights.append(0)
                else:
                    s, f = neighbor - 1, path[-1] - 1 # Needed for dijkstra heuristic
                    u, v = min(s, f), max(s, f)

                    # Update necessary pheromones
                    self.parent.pheromones[u][v] *= math.pow(constants.PHEROMONE_DECAY_RATE, self.parent.timesDecayed - self.parent.lastDecayed[u][v])
                    self.parent.lastDecayed[u][v] = self.parent.timesDecayed

                    self.parent.pheromones[u][v] = max(self.parent.pheromones[u][v], constants.MIN_PHEROMONE_VALUE)
                    self.parent.pheromones[u][v] = min(self.parent.pheromones[u][v], constants.MAX_PHEROMONE_VALUE)

                    # Calculates the weight of the edge

                    # local pheromone
                    weight = math.pow(1 + self.parent.pheromones[u][v] / constants.MAX_PHEROMONE_VALUE, constants.PHEROMONE_EXPONENT)
                    if constants.HEURISTIC_FUNCTION:
                        # heuristic (current point dist to end - next point dist to end) (how much distance we save)
                        # First 0.5 means that if we move really far away from destination we will scale by 0.5
                        # but if we move really close then we scale by 1.5
                        weight *= math.pow(0.5 + 0.5 + 1e-18 + 0.5 * (self.parent.simulation.heuristics[self.parent.end][f] - self.parent.simulation.heuristics[self.parent.end][s])/constants.MAX_ROAD_LENGTH, constants.HEURISTIC_EXPONENT)
                    if constants.USE_GLOBAL_PHEROMONE:
                        # Global pheromone
                        weight *= math.pow(2 - self.parent.simulation.globalTrafficDensity[u][v] / constants.NUM_VEHICLES, constants.GLOBAL_EXPONENT)

                    weights.append(weight)
                    largestWeight = max(weights[-1], largestWeight)
                    cumulativeTotal += weights[-1]

            # If there is nowhere to go we just stop
            if cumulativeTotal == 0:
                # Greater than 1 because we will always skip the vertex we just came from
                if skippedCuzVisited > 1:
                    alreadyVisited = True
                break

            # Limits maximum value of a pheromone
            if constants.EDGE_SELECTION_LIMITS and largestWeight / cumulativeTotal > constants.p and largestWeight != cumulativeTotal:
                # If the probability of being selected is greater than p and not 100% then we decrease it
                weights[weights.index(largestWeight)] -= (largestWeight - constants.p * cumulativeTotal) / (1 - constants.p)

            # Choose a random edge using the weights
            path.append(random.choices(neighbors, weights)[0])
            visited[path[-1] - 1] = 1

            # If there were more than 1 option for edges to travel to
            if largestWeight != cumulativeTotal:
                self.vertexFromLastIntersection = path[-1]

            # Score calculation
            roadLength = self.parent.graph.edgeWeight(path[-2], path[-1])
            globalPheromone = self.parent.simulation.globalTrafficDensity[min(path[-2] - 1, path[-1] - 1)][
                max(path[-2] - 1, path[-1] - 1)]

            # Exponential traffic cost multiplier (1 + x^exp/n^exp)
            # score += constants.MAX_GLOBAL_PHEROMONE_MULTIPLIER * math.pow(
            #     roadLength / (constants.MIN_ROAD_SPACE_PER_CAR * globalPheromone),
            #     constants.GLOBAL_PHEROMONE_EXPONENT)
            if globalPheromone != 0:
                score += roadLength * constants.MAX_GLOBAL_PHEROMONE_MULTIPLIER * math.pow(globalPheromone, constants.GLOBAL_PHEROMONE_EXPONENT) / math.pow(roadLength/constants.MIN_ROAD_SPACE_PER_CAR, constants.GLOBAL_PHEROMONE_EXPONENT)
            else:
                score += roadLength

        # If the path does not reach the destination
        if path[-1] != self.parent.end:
            score *= -1

            # Assume that we hit a dead end
            if len(path) != constants.MAX_PATH_LENGTH and not alreadyVisited:
                self.parent.bannedVertices[self.vertexFromLastIntersection - 1] = 1

        return path, score, self.parent.id


