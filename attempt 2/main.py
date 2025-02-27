import random
import time

from simulation import Simulation

random.seed(8324932980)
if __name__ == '__main__':

    s = Simulation()

    start = time.time()
    s.execute(500)
    print(f"Execution time: {time.time() - start}")
# NOTES
# Increasing decay rates actually keeps ants on same path as it deletes all alternate paths and just keeps the current one
# Adjust p to be higher than 80% as if your road is very long (80%) means that there is a very low probability of selecting every edge

# Utilized data/code outside of python: https://www.openstreetmap.org/#map=7/39.436/-79.958, matplotlib, lxml, numpy, heapdict, geopy

# TODO change deposit of pheromones based on current path score to be somewhat related to best global path score
#       - (MAYBE NOT) add adaptable MAX_PHEROMONE_FOR_GLOBAL_BEST_PATH -> gets larger for when we deviate upward -> smaller when we get closer
#       - Store how long it have been since previous improvment -> change variab;es based on this and diff between current sol and prev sol
#       - lots of failed to reach destination -> increase heuristic
# TODO Data analysis: look at decrease in # of vehicles on the most dense roads
# TODO Data analysis: look at running time / iterations to reach ~ best solution
# TODO Data analysis: look at random start location (in millburn) all to one destination
#       - Run many iterations of each with random seeds
# TODO: Any time/memory improvements (fix matplotlib laggy graphing)
# TODO debug/tune program

# TODO LATER
# TODO ( Decrease pheromones on trails that result in us looping back on ourselves -> set pheromone to min pheromone amount)
# TODO ADAPTABILITY Store running average of past ~10 scores / differences among them and if they are close together ->
#       - also increase decay rate over time/ decrease heuristic assistance
# TODO make the algorithm prefer better solutions and to try and stay on them

# TODO Maybe MAKE THE VEHICLES NOT BE AFFECTED BY THEIR OWN GLOBAL PHEROMONES (but rn it kinda acts as a push away from current path)
# TODO add the ability to pheromone update the top 20% of paths
# TODO make duplicate vehicles, AKA, 1 vehicle represents 100 vehicles or something (not very necessary, just increase traffic penalty per vehicle)

# TODO eventually figure out what to do with parallel edges
# TODO EXTRA: Fix multiprocessing (make it store variables and faster)
# TODO EXTRA: Have global pheromones be sum of local pheromones
# TODO EXTRA: Make global pheromones time based
# TODO EXTRA: Only update global pheromones during periods (every 10 iterations) (avoids back and forth repetition of paths)
# Above might not be needed as the decay rate already spreads it out

# TODO EXTRA: Any time/memory improvements
# 158885.52607098
# 274393.73139896