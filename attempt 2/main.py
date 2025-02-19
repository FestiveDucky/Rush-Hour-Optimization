import random
import time
import matplotlib.pyplot as plt

from simulation import Simulation

random.seed(8324932980)
if __name__ == '__main__':

    s = Simulation()

    start = time.time()
    s.execute(500)
    print(f"Execution time: {time.time() - start}")

# TODO design cost function based on traffic density and road length for paths
# TODO implement traffic density avoidance in the path ranking & edge selection
# TODO add capped pheromones
# TODO add the ability to pheromone update the top 20% of paths
# TODO add matplotlib data analysis (execution time, cost values of the routes

# TODO EXTRA: add heuristic function for ants to help scoring for incomplete paths
# TODO EXTRA: make duplicate vehicles, AKA, 1 vehicle represents 100 vehicles or something
# TODO EXTRA: Fix multiprocessing (make it store variables and faster)
# TODO EXTRA: Have global pheromones be sum of local pheromones
# TODO EXTRA: Make global pheromones time based
# TODO EXTRA: Only update global pheromones during periods (every 10 iterations) (avoids back and forth repetition of paths)
# TODO EXTRA: Code simple brute force + one that does find the shortest paths


# TODO EXTRA: Any time/memory improvements
# TODO EXTRA: Have increasing pheromone decay rates to further increase exploration