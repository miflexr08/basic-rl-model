
import csv
from glob import glob

def run(state_action_values : dict[tuple, float]):
    
    ocurrences : dict[tuple, int] = { }
    for path in glob('./episodes/random/*.csv'): # one file path per iteration (one file)
        with open(path) as flattencsv: # let's read the current iteration file
            flatten_reader = csv.reader(flattencsv)
            next(flatten_reader) # skip the header
            for line in flatten_reader: # let's read the lines one by one in this file (current iteration path/file)
                current_state = line[0]
                action = line[1]
                qsa = line[3]

                # it returns a array with different qsa's for the same (current_state, action)
                state_action_value = state_action_values.get((current_state, action)) # Ex. ("[0, 1]", "(1, 0)")
                state_action_track : float = state_action_value if state_action_value is not None else 0.0 
                
                if state_action_value is None:
                    state_action_values[(current_state, action)] = state_action_track
                    ocurrences[(current_state, action)] = 1
                else:
                    qt_ocurrences = ocurrences.get((current_state, action)) 
                    divisor = qt_ocurrences if qt_ocurrences is not None else 1
                    state_action_values[(current_state, action)] = (state_action_value + float(qsa)) / divisor
                    
    print(f"modified state_action_values structure: {state_action_values}")





