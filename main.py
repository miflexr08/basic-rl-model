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
state_action_values : dict[tuple, float] = {}

def pick_move(state_action_values : dict[tuple, float], curr_state):
    chance = random.random()
    action = None
    if (chance <= epsilon):
        action = random.choice(ACTIONS)
    else:

        # 1. find all possible future states for each avaiable action on current state
        population = []
        average_qsa_arr = []
        for curr_state_action in [((curr_state[0], curr_state[1]), (a[0], a[1])) for a in ACTIONS]: # ([current_state], [all possible actions])
            population.append(curr_state_action)

            # the qsa sum divided by the quantity of a certain state action occurrences
            # is nothing to do with the probability distribution
            # wich is: the percentage of every possible action for that certain state (current state 'here')

            # UNHASHABLE TYPE: 'LIST'! -> Key is probaly being composed by a list 
            average_qsa = state_action_values.get(curr_state_action) # it must return a float representing the average 
            # about the average: this average is measured by taking all qsa values for a certain state action value and 
            # divide it by the number of times it appears in the sample (right?) 
            if average_qsa is not None:
                average_qsa_arr.append(average_qsa)
            else:
                average_qsa_arr.append(0)

        print(f"population: {population}")
        print(f"average_qsa_arr: {average_qsa_arr}")
        
        total_sum = sum(average_qsa_arr) if len(average_qsa_arr) > 0 else 1

        # ValueError: Total of weights must be greater than zero
        action = random.choices(population, weights=[w / (total_sum if total_sum > 0 else 1) for w in average_qsa_arr]) 

    if action is None:
        raise Exception
    
    return action
    
def resume_episode(episode_number : int):
    import csv
    
    print(f"resuming episode number {episode_number}")

    with open(f'./episodes/epsilon_0.9/episode_{episode_number}.csv', 'w', newline='') as episodefile:
        observation_writer = csv.writer(episodefile, delimiter=',')
        observation_writer.writerow(["current_state", "action", "reward", "q(s, a)", "next_state", "additional_observation"])
        
        # current_state, action, reward, next_state, observation : tuple
        for i in range(len(OBSERVATIONS)):
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

# this function only modifies the referenced structure
get_acc_state_action_values(state_action_values)

#score = 0
curr_state = INITIAL_STATE
overall_counter = 1
episode_size_counter = 1
while overall_counter <= TRAINING_ROUNDS:

    move = pick_move(state_action_values, curr_state)
    next_state = [curr_state[0]+move[0], curr_state[1]+move[1]] 
    if not WALLS.__contains__(next_state) and ( (0 <= next_state[0] <= WIDTH -1) and (0 <= next_state[1] <= HEIGHT -1) ):
        if next_state == TERMINAL_STATE:
            OBSERVATIONS.append(
                (curr_state, (move[0], move[1]), 0, next_state, "Successfully reached the maze’s exit."))
            resume_episode(overall_counter)
            episode_size_counter = 0
            overall_counter += 1
            curr_state = INITIAL_STATE
            continue
        else:
            OBSERVATIONS.append(
                (curr_state, (move[0], move[1]), -1, next_state, "Move accepted"))
        
        curr_state = next_state
    else:
        OBSERVATIONS.append(
            (curr_state, (move[0], move[1]), -100, curr_state, "Attempted to move into a wall or beyond the maze’s boundaries"))
        
    if episode_size_counter == EPISODE_SIZE:
        resume_episode(overall_counter)
        episode_size_counter = 1
        overall_counter += 1
        curr_state = INITIAL_STATE
    else:
        episode_size_counter += 1

for episode in episodes:
    print(f"ep: {episode}")