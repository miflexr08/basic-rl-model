import json
import csv
from glob import glob

def run() -> dict[tuple[tuple, tuple], float]: # Key: ((x, y), (ax, ay))
    # [x, y] -> (x, y)    
    state_action_pairs : dict[tuple[tuple, tuple], float] = {}
    ocurrences : dict[tuple, int] = { }
    for pathFile in glob('./episodes/random/*.csv'): # one path-file per iteration 
        with open(pathFile) as flattencsv: 
            flatten_reader = csv.reader(flattencsv)
            next(flatten_reader) # skip the header
            for line in flatten_reader: 

                # Properties of the found state action pair from the file -> IT IS AN OCURRENCE!
                state : list[int] = json.loads(line[0]) # Desserializing "[x, y]" 
                action : tuple[int, int] = json.loads(line[1]) # Desserializing "(ax, ay)"
                qsa = float(line[3])
                state_action_pair = (state, action)

                # Now we have to look for the pair inside our control structure
                state_action_value_found = state_action_pairs.get((state, action)) # Ex. ([0, 1], (1, 0))
                if state_action_value_found is not None: # 2 structures that are sync every time (ocurrences & state action pairs)
                    qt_ocurrences = ocurrences.get(state_action_pair) # need to update the number of ocurrences
                    if qt_ocurrences is None:
                        raise Exception
                    updated_qt_ocurrences = qt_ocurrences + 1
                    state_action_pairs[state_action_pair] = (state_action_value_found + qsa) / updated_qt_ocurrences
                    ocurrences[state_action_pair] = updated_qt_ocurrences
                else:
                    ocurrences[state_action_pair] = 1
                    state_action_pairs[state_action_pair] = qsa
                    
    print(f"modified state_action_pairs structure: {state_action_pairs}")
    return state_action_pairs





