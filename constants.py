from state import State

# Graphics vars
WIDTH = 5 # 5 blocks horizontally
HEIGHT = 5 # 5 blocks vertically
WALLS = [State(0, 3), State(2, 3), State(4, 3), State(1, 1), State(3, 1)]

# Logic vars
ACTIONS = [(0,1), (1, 0), (0, -1), (-1, 0)]  # up, right, down, left
EPISODE_SIZE = 20
TRAINING_EPISODES_TOTAL_QUANTITY = 100
INITIAL_EPSILON = 0.75 

INITIAL_STATE = State(0, 0)
TERMINAL_STATE = State(4, 4) 

# RL vars
ALPHA = 0.01 # ?
GAMA = 0.25
REWARD = -1 # reward shaping --
