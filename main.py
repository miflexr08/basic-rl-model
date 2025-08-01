import random 
from constants import *
from action import Action
from qsa_stats import QsaStatsManager
# from state import State
# from state_action_values import run as get_state_action_pairs_average_values

# observação é a unidade mínima de informação dentro de um episódio. é o conjunto de propriedades 
_observations = [] # observations being made (it always add an observation being currently evaluated) 
episodes = [] # all episodes (now with diff epsilon values)

# Example: { ((x, y), (ax, ay)): 233.64 } 
qsa_stats_manager = QsaStatsManager()
def pick_action(curr_state : tuple[int, int], epsilon : float) -> Action: 

    # ACTIONS = [(0,1), (1, 0), (0, -1), (-1, 0)]  # up, right, down, left
    chance = random.random()
    action = None
    if (chance <= epsilon):
        action = random.choice(ACTIONS) 
    else:
        qsa_mean_population = []
        for state_action_pair in [(State(curr_state[0], curr_state[1]), Action(a[0], a[1])) for a in ACTIONS]:
            qsa_stats = qsa_stats_manager.__get_state_action_qsa_stats(state_action_pair) 
            
            # That is a qsa stats for the specific state action pair being iterated. It only considers
            # the ocurrences from past experiences. experiences from the current episode are inserted
            # at the end of it inside the method 'resume_episode' 
            qsa_mean_population.append(qsa_stats.get_qsa_mean())

        print(f"Qsa mean Population: {qsa_mean_population}")

        min_point = min(qsa_mean_population)
        max_point = max(qsa_mean_population)
        energy_landscape_sample = max_point - min_point
        if energy_landscape_sample == 0:
            action_tuple = random.choice(ACTIONS)
            return Action(action_tuple[0], action_tuple[1])

        # Divide the sample space for each of the qsa's means
        energy_potentials = [energy_landscape_sample / (mean if mean > 0 else 1) for mean in qsa_mean_population]
        total_energy = sum(energy_potentials)
        # weight goes up as effort goes down (bigger weights for bigger energy potential values)
        weights = [w / total_energy for w in energy_potentials]
        print(f"weights: {weights}")

        # The actions must be in order with weights (how come, review it)
        action = random.choices(ACTIONS, weights)[0]

    if action is None:
        raise Exception
    
    return Action(action[0], action[1])
    

def resume_episode(episode_number, epsilon, terminal=False):
    import csv

    with open(f'./episodes/episode{episode_number}_{epsilon}.csv', 'w', newline='') as episodefile:
        observation_writer = csv.writer(episodefile, delimiter=',')
        observation_writer.writerow(["current_state", "action", "reward", "q(s, a)", "next_state", "additional_observation"])
        
        for i in range(len(_observations)):
            observations_ = _observations[i:] 
            qsa = calculate_qsa(observations_, 1) 

            # current_state [0], action [1], reward [2], q(s, a), next_state [3], additional_observation [4]
            curr_state = _observations[i][0]
            action = _observations[i][1]
            observation_writer.writerow(
                [
                    str(curr_state), 
                    str(action), 
                    str(_observations[i][2]), 
                    str(qsa), 
                    str(_observations[i][3]), 
                    str(_observations[i][4])
                ])
            
            qsa_stats_manager.update_state_action_qsa_stats(
                (
                    State(curr_state[0], curr_state[1]), 
                    Action(action[0], action[1])
                ), qsa)
            
            if terminal:
                print("terminal report")
    
    episodes.append(_observations.copy())
    _observations.clear()


def calculate_qsa(observations, curr_gama) -> int:
    gt = observations[0][2]
    if len(observations[0:]) == 1:
        return curr_gama * gt 

    progressive_gama = curr_gama * GAMA
    return (gt * curr_gama) + calculate_qsa(observations[1:], progressive_gama)


curr_state = INITIAL_STATE
overall_episodes_counter = 1
episode_size_counter = 1
terminal_state = False
is_training = overall_episodes_counter <= TRAINING_EPISODES_TOTAL_QUANTITY and not terminal_state

while is_training:
    
    epsilon = INITIAL_EPSILON - (INITIAL_EPSILON * (overall_episodes_counter / TRAINING_EPISODES_TOTAL_QUANTITY))
    end_training = not is_training
    
    action = pick_action((curr_state.x, curr_state.y), epsilon) 
    
    # print(f"Moving {action.get_graphics()}") 
    # print(f"Now i am in the State: {curr_state}")

    next_candidate_state = curr_state + action
    is_valid_move = ( not WALLS.__contains__(next_candidate_state) and 
                        ( (0 <= next_candidate_state.x <= WIDTH -1) and (0 <= next_candidate_state.y <= HEIGHT -1) ) )
    
    is_forbidden_move = not is_valid_move
    if is_valid_move:
        next_state = next_candidate_state

        # 3 base cases (casos de parada)
        # 1. Terminal state
        # 2. Training is over (has reached the number of episodes desired)
        # training state verification
        #  
        if next_state == TERMINAL_STATE: # do it should be explictly revealed? 
            _observations.append(
                (curr_state, action, +10, next_state, "Successfully reached the maze’s exit."))
            
            terminal_state = True 
            continue 
        elif episode_size_counter == EPISODE_SIZE:
            resume_episode(overall_episodes_counter, epsilon)
            episode_size_counter = 1
            overall_episodes_counter += 1
            curr_state = INITIAL_STATE
        
        # It is not a terminal state
        _observations.append(
            (curr_state, action, -1, next_state, "Move accepted"))
        curr_state = next_state

    elif is_forbidden_move:
        _observations.append(
            (curr_state, action, -10, curr_state, "Attempted to move into a wall or beyond the maze’s boundaries"))

    
    
    else:
        episode_size_counter += 1

    end_training = not (overall_episodes_counter <= TRAINING_EPISODES_TOTAL_QUANTITY)    
    resume_episode(overall_episodes_counter, epsilon, terminal=(terminal_state or end_training))

