
# Graphics vars
WIDTH = 5 # 5 blocks horizontally
HEIGHT = 5 # 5 blocks vertically
WALLS = [[0, 3], [2, 3], [4, 3], [1, 1], [3, 1]]

# Logic vars
ACTIONS = [(0,1), (1, 0), (0, -1), (-1, 0)]  # up, right, down, left
VISUAL_ACTIONS = { 0: "↑", 1: "→", 2: "↓", 3: "←" }
EPISODE_SIZE = 10
TRAINING_SIZE = 10
INITIAL_STATE = [0, 0] 
TERMINAL_STATE = [4 ,4] 

# RL vars
ALPHA = 0.01 # ?
GAMA = 0.25
REWARD = -1 # reward shaping --
