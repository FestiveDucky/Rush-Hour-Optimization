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

# TODO add matplotlib data analysis (execution time, cost values of the routes
# TODO Compare to shortest paths using dijkstra
# TODO Test global pheromone avoidance and tune cost function variables (for edge selection)

# TODO add the ability to pheromone update the top 20% of paths
# TODO possibly change the path for final output to be the best path over all iterations rather than the last path
# TODO make duplicate vehicles, AKA, 1 vehicle represents 100 vehicles or something

# TODO EXTRA: Fix multiprocessing (make it store variables and faster)
# TODO EXTRA: Have global pheromones be sum of local pheromones
# TODO EXTRA: Make global pheromones time based
# TODO EXTRA: Only update global pheromones during periods (every 10 iterations) (avoids back and forth repetition of paths)
# Above might not be needed as the decay rate already spreads it out

# TODO EXTRA: Any time/memory improvements
# TODO EXTRA: Have increasing pheromone decay rates to further increase exploration

