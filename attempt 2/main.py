import random
import time

from simulation import Simulation

random.seed(8324932980)
if __name__ == '__main__':

    s = Simulation()

    start = time.time()
    s.execute(500)
    print(f"Execution time: {time.time() - start}")

# Utilized data/code outside of python: https://www.openstreetmap.org/#map=7/39.436/-79.958, matplotlib, lxml, numpy, heapdict, geopy

# TODO: Any time/memory improvements
# TODO Store running average of past ~10 scores / differences among them and if they are close together ->
#       - also increase decay rate over time/ decrease heuristic assistance
# TODO debug/tune program
# For abstract -> look at decrease in density of vehicles per any road

# Increasing decay rates actually keeps ants on same path as it deletes all alternate paths and just keeps the current one
# Adjust p to be higher than 80% as if your road is very long (80%) means that there is a very low probability of selecting every edge

# TODO Maybe MAKE THE VEHICLES NOT BE AFFECTED BY THEIR OWN GLOBAL PHEROMONES (but rn it kinda acts as a push away from current path)
# TODO add the ability to pheromone update the top 20% of paths
# TODO make duplicate vehicles, AKA, 1 vehicle represents 100 vehicles or something (not very necessary, just increase traffic penalty per vehicle)

# TODO EXTRA: Fix multiprocessing (make it store variables and faster)
# TODO EXTRA: Have global pheromones be sum of local pheromones
# TODO EXTRA: Make global pheromones time based
# TODO EXTRA: Only update global pheromones during periods (every 10 iterations) (avoids back and forth repetition of paths)
# Above might not be needed as the decay rate already spreads it out

# TODO EXTRA: Any time/memory improvements
