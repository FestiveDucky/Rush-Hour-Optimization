# N_VERTICES = 100
# M_EDGES = 160

N_VERTICES = 10000
M_EDGES = 15000

PHEROMONE_DECAY_RATE = 0.99
GLOBAL_PHEROMONE_DECAY_RATE = 0.5
INITIAL_PHEROMONE_VALUE = 1. # need a decimal point after number
INCOMPLETE_PENALTY = 10000
MAX_PATH_LENGTH = N_VERTICES
MAX_ROAD_LENGTH = 1005
MIN_ROAD_LENGTH = 1
NUM_VEHICLES = 1
PHEROMONE_DEPOSIT_CONSTANT = 500
NUM_ANTS = 50 # per vehicle

p = 0.8 # probability cap for edge selection
MIN_PHEROMONE_VALUE = 0.01
MAX_PHEROMONE_VALUE = 5

MAX_TRAFFIC_MULTIPLIER = 5 # maximum multiplier for the cost function for the paths of the ants
# Cost function exponents
GLOBAL_PHEROMONE_EXPONENT = 0.5


PRINT_ALL_ITERATIONS = True # Whether we print the best paths and scores for the paths for every vehicle every iteration
EFFICIENT_DECAY_RATES = True
EDGE_SELECTION_LIMITS = True # Sets a maximum probability for selecting an edge
HEURISTIC_FUNCTION = True # Uses dijkstras algorithm as a heuristic

# TODO BELOW vvv (these are not implemented yet)
BEST_PATH_ONLY = True # use the best path to update pheromones or top 20%
CAPPED_PHEROMONES = False # Limit pheromones to max and min values -> each edge has at least x chance of being chosen

# TODO fix the following
MULTIPROCESSING = False # don't work rn -> none of data is saved after multiprocessing + slower than normal
COST_BASED_ON_TRAFFIC_DENSITY = False # AKA whether we use global pheromones


# NOTES
# pheromones are from 0 -> n - 1
# paths are from 1 -> n
# graph is from 1 -> n