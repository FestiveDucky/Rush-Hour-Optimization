ITERATIONS = 500

# Graph
SCALE = 2
N_VERTICES = 100 * SCALE
M_EDGES = 200 * SCALE
LOAD_GRAPH_DATA = False # Already precalculated city data
IMPORT_GRAPH_DATA = False # Calculates new city data based on osm data
MAX_ROAD_LENGTH = 1005 # meters
MIN_ROAD_LENGTH = 1 # meters

# Vehicles
SAME_DESTINATION = False # determines whether all the vehicles have the same destination
NUM_VEHICLES = 400
LATEST_DEPARTURE_TIME = 50
MAX_ROAD_SPEED = 30 # m/s
MIN_ROAD_SPEED = 10 # m/s

# Ants
NUM_ANTS = 20 # per vehicle
MAX_PATH_LENGTH = N_VERTICES

# Pheromones
PHEROMONE_DECAY_RATE = 0.8
GLOBAL_PHEROMONE_DECAY_RATE = 0.7
INITIAL_PHEROMONE_VALUE = 1. # need a decimal point after number
PHEROMONE_DEPOSIT_CONSTANT = 1
MIN_PHEROMONE_VALUE = 0.01
MAX_PHEROMONE_VALUE = 20
MAX_PHEROMONE_FOR_GLOBAL_BEST_PATH = 10
DEPOSIT_PHEROMONES_ON_GLOBAL_BEST = True # Whether we deposit extra pheromones along the global best solution ever
DECAY_GLOBAL_PHEROMONES = True # Determines whether we decay global pheromones or just set them to 0 every iteration

# Final cost function (closer to 0 -> greater punishment for smaller number of vehicles)
GLOBAL_PHEROMONE_EXPONENT = 0.9
MAX_GLOBAL_PHEROMONE_MULTIPLIER = 2 # Maximum multiplier as a result of the global traffic
MIN_ROAD_SPACE_PER_CAR = 10 # distance between vehicles (includes vehicle length) at which point there is severe traffic
INCOMPLETE_PENALTY = 1e6 # TODO change to a multiplier on dijkstra cost

# Ant Weights during edge selection
PHEROMONE_EXPONENT = 15 # Pheromone exponent
HEURISTIC_EXPONENT = 40 # Heuristic exponent (you want it higher for times when we ain't reaching the end much
GLOBAL_EXPONENT = 7 # traffic density exponent
p = 0.9 # probability cap for edge selection (only works for p > 0.5)
EDGE_SELECTION_LIMITS = True # Sets a maximum probability for selecting an edge
HEURISTIC_FUNCTION = True # Uses dijkstras algorithm as a heuristic
USE_GLOBAL_PHEROMONE = True # For Ant Weights

# Adaptive constants
PROPORTION_OF_TOTAL_SCORE_TO_ADAPT = 0.3
MINIMUM_NUMBER_OF_SCORES_TO_ADAPT = 8

# Prints
PRINT_DIJKSTRA_PATHS = False # whether we print the paths found by dijkstra
PRINT_ALL_ITERATIONS = True # Whether we print the best paths & scores for the paths for every vehicle every iteration

# Misc
AUTOMATIC_ADJUSTMENT_OF_CONSTANTS = False # when the current solutions become constant we adapt stuff like decay rate

# TODO BELOW vvv (these are not implemented yet)
BEST_PATH_ONLY = True # use the best path to update pheromones or top 20% of paths
MULTIPROCESSING = False

# NOTES
# pheromones are from 0 -> n - 1
# paths are from 1 -> n
# graph is from 1 -> n
# most edge based look ups require smallest vertex value first and largest second