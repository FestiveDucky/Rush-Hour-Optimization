import random
import time

from simulation import Simulation

random.seed(8324932980)
if __name__ == '__main__':

    s = Simulation()

    start = time.time()
    s.execute(500)
    print(f"Execution time: {time.time() - start}")

# TODO Add export/import for graphs and the vehicle paths on the graphs (export best overall path)
# TODO: Any time/memory improvements
# TODO Add something which stores best paths for each vehicle and does new pheromone deposits based on comparison to that
#       - also increase decay rate over time/ decrease heuristic assistance

# TODO Maybe MAKE THE VEHICLES NOT BE AFFECTED BY THEIR OWN GLOBAL PHEROMONES (but rn it kinda acts as a push away from current path)
# TODO add the ability to pheromone update the top 20% of paths
# TODO make duplicate vehicles, AKA, 1 vehicle represents 100 vehicles or something (not very necessary, just increase traffic penalty per vehicle)

# TODO EXTRA: Fix multiprocessing (make it store variables and faster)
# TODO EXTRA: Have global pheromones be sum of local pheromones
# TODO EXTRA: Make global pheromones time based
# TODO EXTRA: Only update global pheromones during periods (every 10 iterations) (avoids back and forth repetition of paths)
# Above might not be needed as the decay rate already spreads it out

# TODO EXTRA: Any time/memory improvements
# TODO EXTRA: Have increasing pheromone decay rates to further increase exploration

