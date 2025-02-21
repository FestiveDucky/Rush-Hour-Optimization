# N_VERTICES = 100
# M_EDGES = 160

N_VERTICES = 100
M_EDGES = 150

PHEROMONE_DECAY_RATE = 0.9
GLOBAL_PHEROMONE_DECAY_RATE = 0.5
INITIAL_PHEROMONE_VALUE = 1. # need a decimal point after number
INCOMPLETE_PENALTY = 10000
MAX_PATH_LENGTH = N_VERTICES
MAX_ROAD_LENGTH = 1005
MIN_ROAD_LENGTH = 1
NUM_VEHICLES = 30
PHEROMONE_DEPOSIT_CONSTANT = 0.1
NUM_ANTS = 10 # per vehicle
MIN_ROAD_SPACE_PER_CAR = 10 # distance between vehicles (includes vehicle length) at which point there is severe traffic

p = 0.8 # probability cap for edge selection
MIN_PHEROMONE_VALUE = 0.01
MAX_PHEROMONE_VALUE = 5

# for cost function (closer to 0 -> greater punishment for smaller number of vehicles)
GLOBAL_PHEROMONE_EXPONENT = 0.1
# for weights during edge selection
PHEROMONE_EXPONENT = 5 # Pheromone exponent
HEURISTIC_EXPONENT = 2 # Heuristic exponent
GLOBAL_EXPONENT = 5 # traffic density exponent

PRINT_ALL_ITERATIONS = False # Whether we print the best paths & scores for the paths for every vehicle every iteration
EFFICIENT_DECAY_RATES = True
EDGE_SELECTION_LIMITS = True # Sets a maximum probability for selecting an edge
HEURISTIC_FUNCTION = True # Uses dijkstras algorithm as a heuristic
COST_BASED_ON_TRAFFIC_DENSITY = False # AKA whether we use global pheromones
USE_GLOBAL_PHEROMONE = True
DECAY_GLOBAL_PHEROMONES = False # Determines whether we decay global pheromones or just set them to 0 every iteration

# TODO BELOW vvv (these are not implemented yet)
BEST_PATH_ONLY = True # use the best path to update pheromones or top 20%
ONLY_DEPOSIT_PHEROMONES_WHEN_BETTER_THAN_PAST_BEST = True

# TODO fix the following
MULTIPROCESSING = False # don't work rn -> none of data is saved after multiprocessing + slower than normal

# NOTES
# pheromones are from 0 -> n - 1
# paths are from 1 -> n
# graph is from 1 -> n