import random 
from constants import *
from action import Action
from state import State
from state_action_values import run as get_state_action_pairs_average_values

# observação é a unidade mínima de informação dentro de um episódio. é o conjunto de propriedades 
OBSERVATIONS = [] 
#epsilon = 1
epsilon = 0.85

# associadas à um determinado estado (estado, estado-ação, estado seguinte, recompensa, observação adicional)
episodes = []

# Example: { ((x, y), (ax, ay)): 233.64 } 
def pick_action(state_action_values : dict[tuple[tuple[int, int], tuple[int, int]], float], curr_state : tuple[int, int]) -> Action: 

    # ACTIONS:
    # [(0, 1), (1, 0), (0, -1), (-1, 0)]
    # ACTIONS = [(0,1), (1, 0), (0, -1), (-1, 0)]  # up, right, down, left

    chance = random.random()
    action = None
    if (chance <= epsilon):
        action = random.choice(ACTIONS) 
    else:
        population_average_qsa : dict[tuple[tuple[int, int], tuple[int, int]], float] = { }
        for state_action_pair in [(curr_state, a) for a in ACTIONS]: 
            average_qsa = state_action_values.get(state_action_pair) 
            population_average_qsa[state_action_pair] = average_qsa if average_qsa is not None else 0

        average_qsa_arr = list(population_average_qsa.values())
        min_point = min(average_qsa_arr)
        max_point = max(average_qsa_arr)
        sample_space = max_point - min_point
        if sample_space == 0:
            action_tuple = random.choice(ACTIONS)
            return Action(action_tuple[0], action_tuple[1])

        #potentials = [sample_space / (value if value > 0 else 1) for value in average_qsa_arr] 
        population_less_effort_potentials = { key: (sample_space / (value if value > 0 else 1)) for key, value in population_average_qsa.items() } # dictionaty comprehension
        # weight goes up as effort goes down
        potentials_sum_up = sum(list(population_less_effort_potentials.values()))
        weights = { key: (value / potentials_sum_up) for key, value in population_less_effort_potentials.items() }
    
        print(f"weights: {weights}")
        # action = random.choices(list(weights.keys()), list(weights.values()))[0] ??
        action = random.choices(ACTIONS, list(weights.values()))[0]

    if action is None:
        raise Exception
    
    return Action(action[0], action[1])
    
def resume_episode(episode_number : int):
    import csv

    with open(f'./episodes/epsilon_0_85/episode_{episode_number}.csv', 'w', newline='') as episodefile:
        observation_writer = csv.writer(episodefile, delimiter=',')
        observation_writer.writerow(["current_state", "action", "reward", "q(s, a)", "next_state", "additional_observation"])
        
        # current_state, action, reward, qsa, next_state, monte_carlo_reward, observation 
        for i in range(len(OBSERVATIONS)):
            _observations = OBSERVATIONS[i:] 
            qsa = calculate_qsa(_observations, 1) 
            observation_writer.writerow(
                [str(OBSERVATIONS[i][0]), str(OBSERVATIONS[i][1]), OBSERVATIONS[i][2], str(qsa), str(OBSERVATIONS[i][3]), OBSERVATIONS[i][4]])
    
    episodes.append(OBSERVATIONS.copy())
    OBSERVATIONS.clear()


def calculate_qsa(observations, curr_gama) -> int:
    # current_state, action, reward, next_state, monte_carlo_reward, observation 
    gt = observations[0][2]
    if len(observations[0:]) == 1:
        return curr_gama * gt 

    progressive_gama = curr_gama * GAMA
    return (gt * curr_gama) + calculate_qsa(observations[1:], progressive_gama)

# Example: { ((x, y), (ax, ay)): 233.64 } 
state_action_values = get_state_action_pairs_average_values()

curr_state = INITIAL_STATE
overall_counter = 1
episode_size_counter = 1
while overall_counter <= TRAINING_SIZE:

    action = pick_action(state_action_values, (curr_state.x, curr_state.y)) 
    print(f"Moving {action}") # Error here
    print(f"Now i am in the State: {curr_state}")

    next_state = curr_state + action 
    if not WALLS.__contains__(next_state) and ( (0 <= next_state.x <= WIDTH -1) and (0 <= next_state.y <= HEIGHT -1) ):
        if next_state == TERMINAL_STATE: # do it should be explictly revealed? 
            OBSERVATIONS.append(
                (curr_state, action, 0, next_state, "Successfully reached the maze’s exit."))
            
            resume_episode(overall_counter)

            episode_size_counter = 0
            overall_counter += 1
            curr_state = INITIAL_STATE
            continue
        else:
            OBSERVATIONS.append(
                (curr_state, action, -1, next_state, "Move accepted"))
        
        curr_state = next_state
    else:
        OBSERVATIONS.append(
            (curr_state, action, -100, curr_state, "Attempted to move into a wall or beyond the maze’s boundaries"))
        
    if episode_size_counter == EPISODE_SIZE:
        resume_episode(overall_counter)
        episode_size_counter = 1
        overall_counter += 1
        curr_state = INITIAL_STATE
    else:
        episode_size_counter += 1

