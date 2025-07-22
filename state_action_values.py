
import csv
from glob import glob

def run(state_action_values : dict):

    for path in glob('/episodes/random/*.csv'):
        with open(path) as flattencsv: 
            flatten_reader = csv.reader(flattencsv)
            next(flatten_reader)
            for line in flatten_reader:
                current_state = line[0]
                action = line[1]
                qsa = line[3]

                # it returns a array with different qsa's for the same (current_state, action)
                current_state_action_value : list[int] | None = state_action_values.get((current_state, action))
                # if nothing is inside 'there' create it  
                if current_state_action_value is None:
                    state_action_values[(current_state, action)] = [qsa] 
                elif current_state_action_value is not None:
                    current_state_action_value.append(qsa)





