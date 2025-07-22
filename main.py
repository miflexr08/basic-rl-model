import random 
from state_action_values import run as get_acc_state_action_values

GAMA = 0.25
ACTIONS = [[0,1], [1, 0], [0, -1], [-1, 0]]  # up, right, down, left
WIDTH = 5 # 5 blocks horizontally
HEIGHT = 5 # 5 blocks vertically
WALLS = [[0, 3], [2, 3], [4, 3], [1, 1], [3, 1]]
EPISODE_SIZE = 10
TRAINING_ROUNDS = 10
INITIAL_STATE = [0, 0] # test it from a random state (?)
TERMINAL_STATE = [4 ,4] # the agent doesn't know that :D 
DEFAULT_REWARD = -1 # reward shaping --

OBSERVATIONS = [] # observação é a unidade mínima de informação dentro de um episódio. é o conjunto de propriedades 
#epsilon = 1
epsilon = 0.9
# associadas à um determinado estado (estado, estado-ação, estado seguinte, recompensa, observação adicional)
episodes = []
state_action_values : dict[tuple, list[float]] = {}

def pick_move(state_action_values : dict[tuple, list[float]], curr_state):
    chance = random.random()
    action = None
    if (chance <= epsilon):
        action = random.choice(ACTIONS)
    else:

        # 1. find all possible future states for each avaiable action on current state
        population = []
        weights = []
        for curr_state_action in [(curr_state, a) for a in ACTIONS]: # ([current_state], [all possible actions])
            population.append(curr_state_action[1])
            qsa = state_action_values.get(curr_state_action)
            if qsa is not None:
                weights.append(qsa)
            else:
                weights.append(0)

        print(f"population: {population}")
        print(f"weights: {weights}")    

        #action = random.choices(population=[], weights=[]) 
        action = random.choices(population, weights) 

    if action is None:
        raise Exception
    
    return action
    

def resume_episode(episode_number : int):
    import csv
    
    print(f"resuming episode number {episode_number}")

    with open(f'./episodes/random/episode_{episode_number}.csv', 'w', newline='') as episodefile:
        observation_writer = csv.writer(episodefile, delimiter=',')
        observation_writer.writerow(["current_state", "action", "reward", "q(s, a)", "next_state", "additional_observation"])
        
        # current_state, action, reward, next_state, observation : tuple
        print(f"OBSERVATIONS: {OBSERVATIONS}")
        for i in range(len(OBSERVATIONS)):
            print("_observation: {OBSERVATIONS[i]}" )
            _observations = OBSERVATIONS[i:] # the first will be 0:, the second will be 1:
            qsa = calculate_qsa(_observations, 1) # this will not work (it will be ZERO for every single first)
            observation_writer.writerow(
                [OBSERVATIONS[i][0], OBSERVATIONS[i][1], OBSERVATIONS[i][2], str(qsa), OBSERVATIONS[i][3], OBSERVATIONS[i][4]])
    
    episodes.append(OBSERVATIONS.copy())
    OBSERVATIONS.clear()

# Can build a class to keep track of some variables like Obervations or gama for example (make it an abstraction)
def calculate_qsa(observations, curr_gama) -> int:
    # current_state, action, reward, next_state, monte_carlo_reward, observation : tuple
    gt = observations[0][2]
    if len(observations[0:]) == 1:
        return curr_gama * gt 

    progressive_gama = curr_gama * GAMA
    return (gt * curr_gama) + calculate_qsa(observations[1:], progressive_gama)

get_acc_state_action_values(state_action_values)

#score = 0
current_state = INITIAL_STATE
overall_counter = 1
episode_size_counter = 1
while overall_counter <= TRAINING_ROUNDS:

    move = pick_move(state_action_values)
    next_state = [current_state[0]+move[0], current_state[1]+move[1]] 
    if not WALLS.__contains__(next_state) and ( (0 <= next_state[0] <= WIDTH -1) and (0 <= next_state[1] <= HEIGHT -1) ):
        if next_state == TERMINAL_STATE:
            OBSERVATIONS.append(
                (current_state, (move[0], move[1]), 0, next_state, "Successfully reached the maze’s exit."))
            resume_episode(overall_counter)
            episode_size_counter = 0
            overall_counter += 1
            current_state = INITIAL_STATE
            continue
        else:
            OBSERVATIONS.append(
                (current_state, (move[0], move[1]), -1, next_state, "Move accepted"))
        
        current_state = next_state
    else:
        OBSERVATIONS.append(
            (current_state, (move[0], move[1]), -100, current_state, "Attempted to move into a wall or beyond the maze’s boundaries"))
        
    if episode_size_counter == EPISODE_SIZE:
        resume_episode(overall_counter)
        episode_size_counter = 1
        overall_counter += 1
        current_state = INITIAL_STATE
    else:
        episode_size_counter += 1

for episode in episodes:
    print(f"ep: {episode}")