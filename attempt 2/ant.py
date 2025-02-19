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
            cummulativeTotal = 0
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

                    #TODO use global pheromone for these weights && heuristic function

                    # Calculates the weight
                    # 1/distance * local pheromone
                    weights.append(1/self.parent.graph.edgeWeight(v, u) * self.parent.pheromones[min(u - 1, v - 1)][max(u - 1, v - 1)])
                    largestWeight = max(weights[-1], largestWeight)
                    cummulativeTotal += weights[-1]

            # If there is nowhere to go we just stop
            if cummulativeTotal == 0:
                break

            # Limits maximum value of a pheromone
            if EDGE_SELECTION_LIMITS and largestWeight / cummulativeTotal > p and largestWeight != cummulativeTotal: # If the probability of being selected is greater than p and not 100%
                # print(largestWeight)
                weights[weights.index(largestWeight)] -= (largestWeight - p * cummulativeTotal) / (1 - p)

            path.append(random.choices(neighbors, weights)[0])


            # TODO improve cost function to be more accurate

            # Determine the cost to add based on the current edge

            # Exponential traffic cost multiplier (capped at 5x)
            # -> 1 + max(x^exp/n^exp)
            if COST_BASED_ON_TRAFFIC_DENSITY:
                score += self.parent.graph.edgeWeight(path[-2], path[-1]) * (1 + (MAX_TRAFFIC_MULTIPLIER - 1)
                                                                         * math.pow(self.parent.simulation.globalTrafficDensity[min(path[-2] - 1, path[-1] - 1)][max(path[-2] - 1, path[-1] - 1)], TRAFFIC_MULTIPLIER_EXPONENT)
                                                                         / math.pow(NUM_VEHICLES, TRAFFIC_MULTIPLIER_EXPONENT))
            else:
                # Linear traffic cost multiplier
                # score += self.parent.graph.edgeWeight(path[-2], path[-1]) * (1 + self.parent.simulation.globalTrafficDensity[min(path[-2] - 1, path[-1] - 1)][max(path[-2] - 1, path[-1] - 1)] / NUM_VEHICLES)

                # No Traffic cost
                score += self.parent.graph.edgeWeight(path[-2], path[-1])

        # Add extra penalty if the path does not reach destination
        if path[-1] != self.parent.end:
            score += INCOMPLETE_PENALTY

        return path, score


