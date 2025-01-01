N_VERTICES = 100
M_EDGES = 150

PHEROMONE_DECAY_RATE = 0.8
GLOBAL_PHEROMONE_DECAY_RATE = 0.5
INITIAL_PHEROMONE_VALUE = 1. # need a decimal point after number
INCOMPLETE_PENALTY = 10000
MAX_PATH_LENGTH = N_VERTICES
MAX_ROAD_LENGTH = 10
MIN_ROAD_LENGTH = 1
NUM_VEHICLES = 1000
PHEROMONE_DEPOSIT_CONSTANT = 5
NUM_ANTS = 50 # per vehicle
TRAFFIC_MULTIPLIER_EXPONENT = 0.5
MAX_TRAFFIC_MULTIPLIER = 5


EFFICIENT_DECAY_RATES = True
MULTIPROCESSING = False # don't work rn -> none of data is saved after multiprocessing + slower than normal
# TODO BELOW
COST_BASED_ON_TRAFFIC_DENSITY = True # AKA whether we use global pheromones

BEST_PATH_ONLY = True # use the best path to update pheromones or top 20%
CAPPED_PHEROMONES = False # Limit pheromones to max and min values -> each edge has at least x chance of being chosen

