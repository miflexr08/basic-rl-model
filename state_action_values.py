import json
import csv
from glob import glob

def run() -> dict[tuple[tuple, tuple], float]: # Example: { ((x, y), (ax, ay)): 233.64 } 
    
    state_action_pairs : dict[tuple[tuple, tuple], float] = {}
    ocurrences : dict[tuple, int] = { }
    for pathFile in glob('./episodes/random/*.csv'): # one path-file per iteration 
        with open(pathFile) as flattencsv: 
            flatten_reader = csv.reader(flattencsv)
            next(flatten_reader) # skip the header
            for line in flatten_reader: 
                
                # Properties of the found state action pair from the file -> IT IS AN OCURRENCE!
                state : list[int] = json.loads(line[0]) # Desserializing "[x, y]" 
                formatted_state = (state[0], state[1]) # [x, y] -> (x, y))

                # Ex. "[0, 0]","(-1, 0)",-100,-106.64961242675781,"[0, 0]",Attempted to move into a wall or beyond the maze�s boundaries
                #action : tuple[int, int] = json.loads(line[1]) # Desserializing "(ax, ay)"
                stringfied_action = line[1]
                
                print(f"STRINGFIED ACTION: {stringfied_action}")
                
                stringfied_action_arr = line[1].removeprefix('(').removesuffix(')').replace(' ', '').split(',') # ["(", "x", "y", ")"]
                print(f"stringfied_action_arr: {stringfied_action_arr}")

                action = (int(stringfied_action_arr[0]), int(stringfied_action_arr[1]))
                print(f"ACTION TUPLE: {action}")

                qsa = float(line[3])
                state_action_pair = (formatted_state, action)

                # Now we have to look for the pair inside our control structure
                state_action_value_found = state_action_pairs.get(state_action_pair) 
                if state_action_value_found is not None: # both structures have to be sync every time (ocurrences & state action pairs)
                    qt_ocurrences = ocurrences.get(state_action_pair) # need to update the number of ocurrences
                    
                    if qt_ocurrences is None: 
                        # If a state action pair is found in state_action_pairs and it is not synchronized to ocurrences 
                        # an erro must be raise
                        raise Exception
                    
                    updated_qt_ocurrences = qt_ocurrences + 1
                    state_action_pairs[state_action_pair] = (state_action_value_found + qsa) / updated_qt_ocurrences
                    ocurrences[state_action_pair] = updated_qt_ocurrences
                else:
                    ocurrences[state_action_pair] = 1
                    state_action_pairs[state_action_pair] = qsa
                    
    print(f"State action pairs: {state_action_pairs}")
    return state_action_pairs





