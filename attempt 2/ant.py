import random
from constants import *
import math


class Ant:
    def __init__(self, parent):
        self.parent = parent

    def generatePath(self):
        path = [self.parent.start]
        score = 0
        while path[-1] != self.parent.end and len(path) < MAX_PATH_LENGTH:
            neighbors = self.parent.graph.neighbors(path[-1])
            weights = []
            largestWeight = 0
            cumulativeTotal = 0
            for neighbor in neighbors:
                # Makes the ant never go backwards
                if len(path) >= 2 and neighbor == path[-2]:
                    weights.append(0)
                else:
                    u, v = neighbor, path[-1]

                    # Update necessary pheromones
                    if EFFICIENT_DECAY_RATES:
                        self.parent.pheromones[min(u - 1, v - 1)][max(u - 1, v - 1)] *= math.pow(PHEROMONE_DECAY_RATE,
                                                                                          self.parent.timesDecayed -
                                                                                          self.parent.lastDecayed[
                                                                                              min(u - 1, v - 1)][
                                                                                              max(u - 1, v - 1)])
                        self.parent.lastDecayed[min(u - 1, v - 1)][max(u - 1, v - 1)] = self.parent.timesDecayed

                    self.parent.pheromones[min(u - 1, v - 1)][max(u - 1, v - 1)] = max(
                        self.parent.pheromones[min(v - 1, u - 1)][max(u - 1, v - 1)], MIN_PHEROMONE_VALUE)
                    self.parent.pheromones[min(u - 1, v - 1)][max(u - 1, v - 1)] = min(
                        self.parent.pheromones[min(v - 1, u - 1)][max(u - 1, v - 1)], MAX_PHEROMONE_VALUE)

                    # Calculates the weight of the edge

                    # local pheromone
                    weight = math.pow(1 + self.parent.pheromones[min(u - 1, v - 1)][max(u - 1, v - 1)] / MAX_PHEROMONE_VALUE, PHEROMONE_EXPONENT)
                    if HEURISTIC_FUNCTION:
                        # heuristic (current point dist to end - next point dist to end) (how much distance we save)
                        # First 0.5 means that if we move really far away from destination we will scale by 0.5
                        # but if we move really close then we scale by 1.5
                        weight *= math.pow(0.5 + 0.5 + 1e-18 + 0.5 * (self.parent.simulation.heuristics[self.parent.end][v - 1] - self.parent.simulation.heuristics[self.parent.end][u - 1])/MAX_ROAD_LENGTH, HEURISTIC_EXPONENT)
                    if USE_GLOBAL_PHEROMONE:
                        # Global pheromone
                        weight *= math.pow(2 - self.parent.simulation.globalTrafficDensity[min(u - 1, v - 1)][max(u - 1, v - 1)] / NUM_VEHICLES, GLOBAL_EXPONENT)

                    # print(f"WEIGHT: {weight}, Length {self.parent.graph.edgeWeight(v, u)}, Pheromone {self.parent.pheromones[min(u - 1, v - 1)][max(u - 1, v - 1)]}, Heuristic {(self.parent.simulation.heuristics[self.parent.end][v - 1] - self.parent.simulation.heuristics[self.parent.end][u - 1])}, Global {self.parent.simulation.globalTrafficDensity[min(u - 1, v - 1)][max(u - 1, v - 1)]}")

                    weights.append(weight)
                    largestWeight = max(weights[-1], largestWeight)
                    cumulativeTotal += weights[-1]

            # If there is nowhere to go we just stop
            if cumulativeTotal == 0:
                break

            # Limits maximum value of a pheromone
            if EDGE_SELECTION_LIMITS and largestWeight / cumulativeTotal > p and largestWeight != cumulativeTotal:
                # If the probability of being selected is greater than p and not 100% then we decrease it
                weights[weights.index(largestWeight)] -= (largestWeight - p * cumulativeTotal) / (1 - p)

            # Choose a random edge using the weights
            path.append(random.choices(neighbors, weights)[0])

            roadLength = self.parent.graph.edgeWeight(path[-2], path[-1])
            globalPheromone = self.parent.simulation.globalTrafficDensity[min(path[-2] - 1, path[-1] - 1)][
                max(path[-2] - 1, path[-1] - 1)]
            # Exponential traffic cost multiplier (1 + x^exp/n^exp)
            if COST_BASED_ON_TRAFFIC_DENSITY:
                score += roadLength * math.pow(globalPheromone, GLOBAL_PHEROMONE_EXPONENT) / math.pow(roadLength/MIN_ROAD_SPACE_PER_CAR, GLOBAL_PHEROMONE_EXPONENT)
                # assuming each car needs around 15 m of space -> around 10m of space will result in severe traffic
            else:
                # Cost not based on traffic density
                score += roadLength

        # Add extra penalty if the path does not reach the destination
        if path[-1] != self.parent.end:
            score += INCOMPLETE_PENALTY

        return path, score


