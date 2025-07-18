import random 

epsilon = 1

actions = [[0,1], [1, 0], [0, -1], [-1, 0]]  # up, right, down, left
width = 5 # 5 blocks horizontally
height = 5 # 5 blocks vertically
walls = [[0, 3], [2, 3], [4, 3], [1, 1], [3, 1]]

EPISODE_SIZE = 15
TRAINING_ROUNDS = 15
INITIAL_STATE = [0, 0] # test it from a random state (?)
TERMINAL_STATE = [4 ,4] # the agent doesn't know that :D 
DEFAULT_REWARD = -1 # reward shaping --

OBSERVATIONS = [] # observação é a unidade mínima de informação dentro de um episódio. é o conjunto de propriedades 
# associadas à um determinado estado (estado, estado-ação, estado seguinte, recompensa, observação adicional)
episodes = []

def pick_move():
    chance = random.random()
    if (chance <= epsilon):
        return random.choice(actions)
    
    random.choices
    return [0, 0] # don't do anything

# ;e ch
def resume_episode(episode_number : int):
    import csv
    
    print(f"resuming episode number {episode_number}")

    with open(f'./episodes/random/episode_{episode_number}.csv', 'w', newline='') as episodefile:
        #observation_writer = csv.writer(episodefile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        observation_writer = csv.writer(episodefile, delimiter=',')
        observation_writer.writerow(["current_state", "action", "reward", "next_state", "additional_observation"])
        
        # current_state, action, reward, next_state, observation : tuple
        for observation in OBSERVATIONS:
            print(f"observation: {observation}")
            observation_writer.writerow([observation[0], observation[1], observation[2], observation[3], observation[4]])
    
    episodes.append(OBSERVATIONS.copy())
    OBSERVATIONS.clear()

#score = 0
current_state = INITIAL_STATE
counter = 1
episode_counter = 1
while counter <= TRAINING_ROUNDS:

    move = pick_move()
    next_state = [current_state[0]+move[0], current_state[1]+move[1]] 
    if not walls.__contains__(next_state) and ( (0 <= next_state[0] <= width -1) and (0 <= next_state[1] <= height -1) ):
        if next_state == TERMINAL_STATE:
            OBSERVATIONS.append(
                (current_state, (move[0], move[1]), 0, next_state, "Successfully reached the maze’s exit."))
            resume_episode(counter)
            episode_counter = 0
            counter += 1
            current_state = INITIAL_STATE
            continue
        else:
            OBSERVATIONS.append(
                (current_state, (move[0], move[1]), -1, next_state, "Move accepted"))
        
        current_state = next_state
    else:
        OBSERVATIONS.append(
            (current_state, (move[0], move[1]), -100, current_state, "Attempted to move into a wall or beyond the maze’s boundaries"))
        
    if episode_counter == EPISODE_SIZE:
        resume_episode(counter)
        episode_counter = 1
        counter += 1
        current_state = INITIAL_STATE
    else:
        episode_counter += 1

for episode in episodes:
    print(f"ep: {episode}")