import random 
from constants import *
from state_action_values import run as set_acc_state_action_values

OBSERVATIONS = [] # observação é a unidade mínima de informação dentro de um episódio. é o conjunto de propriedades 
#epsilon = 1
epsilon = 0.85
# associadas à um determinado estado (estado, estado-ação, estado seguinte, recompensa, observação adicional)
episodes = []
state_action_values : dict[str, float] = {}

def pick_move(state_action_values : dict[str, float], curr_state) -> str: # This str it's actually a key!

    # But why the fuck my move is a fucking Key?!

    chance = random.random()
    action = None
    if (chance <= epsilon):
        action = str(random.choice(ACTIONS))
    else:
        population : list[str] = []
        average_qsa_arr = []

        # Build a better solution for this big messy!
        # ((x, y), (ax, ay))
        for state_action_pair in [f"({curr_state[0]}, {curr_state[1]}), {a}" for a in ACTIONS]: 
            population.append(state_action_pair)

            # * [ Must return a float representing the average ] *
            # This average is measured by taking all qsa values for a certain state action value and divide it by the 
            # number of times it appears in the sample 
            average_qsa = state_action_values.get(state_action_pair) # The key must be in format '((x, y), (ax, ay))'
            if average_qsa is not None:
                average_qsa_arr.append(average_qsa)
            else:
                average_qsa_arr.append(0)

        print(f"population: {population}")
        print(f"average_qsa_arr: {average_qsa_arr}")

        min_point = min(average_qsa_arr)
        max_point = max(average_qsa_arr)
        sample_space = max_point - min_point
        if sample_space == 0:
            action = random.choice(ACTIONS)
            return str(action) 
    
        weights = [sample_space / (w if w > 0 else 1) for w in average_qsa_arr] # change this var name
        normalized_w = [w / sum(weights) for w in weights] 

        print(f"weights: {normalized_w}")
        action = random.choices(population, weights)[0]

    if action is None:
        raise Exception
    
    print(f"Selected Action: {action}")
    return action[0]
    
def resume_episode(episode_number : int):
    import csv

    with open(f'./episodes/epsilon_0_85/episode_{episode_number}.csv', 'w', newline='') as episodefile:
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
set_acc_state_action_values(state_action_values)

curr_state = INITIAL_STATE
overall_counter = 1
episode_size_counter = 1
while overall_counter <= TRAINING_SIZE:

    move = pick_move(state_action_values, curr_state) # state_action_values must be a class member

    #print(f"Moving ...{move}\n")
    print(f"move: {move}")
    print(f"Moving {VISUAL_ACTIONS[ACTIONS.index(move)]}")
    print(f"Now i am in the State: {curr_state}")

    next_state = [int(curr_state[0])+int(move[0]), int(curr_state[1])+int(move[1])] 
    if not WALLS.__contains__(next_state) and ( (0 <= next_state[0] <= WIDTH -1) and (0 <= next_state[1] <= HEIGHT -1) ):
        if next_state == TERMINAL_STATE: # do it should be explictly revealed?
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

