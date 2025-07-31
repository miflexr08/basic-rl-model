#from typing import Optional

from state import State
from action import Action

class QsaStatsManager:

    class QsaStats:
        def __init__(self):
            print("Initializing QsaStats")

            self.stats = (0., 0)
        
        def update_stats(self):
            pass 

    def __init__(self):
        self.__state_action_pairs_qsa : dict[tuple[State, Action], tuple[float, int]] = {} # tuple[float, int] -> sum of qsa's, 
        # and number of ocurrences 

    def get_state_action_qsa(self, state_action : tuple[State, Action]) -> float | None:
        total_qsa_and_ocurrences_num = self.__state_action_pairs_qsa.get(state_action)
        if total_qsa_and_ocurrences_num is not None:
            total_qsa, ocurrences_num = total_qsa_and_ocurrences_num
            return total_qsa / ocurrences_num
        
        return None 
    
    def __get_qsa_stats(self, state_action: tuple[State, Action]) -> tuple[float, int]:
        qsa_stats = self.__state_action_pairs_qsa.get(state_action)
        if qsa_stats is not None:
            return qsa_stats
        
        return (0.0, 0) 

    def update_state_action_qsa(self, state_action : tuple[State, Action], qsa : float) -> bool:
        try:
            first_count : int = 1
            #qsa_stats = { state_action: (qsa + acc_qsa, ocurrences_num + 1) for acc_qsa, ocurrences_num in self.__get_qsa_stats(state_action) if self.__state_action_pairs_qsa.__contains__(state_action) else state_action: (qsa, 1) }
            qsa_stats = { state_action: self.__get_qsa_stats(state_action) }
            self.__state_action_pairs_qsa.update(qsa_stats) 

            self.__state_action_pairs_qsa[state_action] = (qsa, 1) 

            return True 

            total_qsa_and_ocurrences_num = self.__state_action_pairs_qsa.get(state_action)
            if total_qsa_and_ocurrences_num is None:
                self.__state_action_pairs_qsa[state_action] = (qsa, 1) 
            if total_qsa_and_ocurrences_num is not None:
                # car = {
                #     "brand": "Ford",
                #     "model": "Mustang",
                #     "year": 1964
                # }

                # car.update({"color": "White"})
                total_qsa, ocurrences_num = total_qsa_and_ocurrences_num
                self.__state_action_pairs_qsa.update({ state_action: (total_qsa + qsa, ocurrences_num + 1) })
                #self.__state_action_pairs_qsa[state_action] = (total_qsa + qsa, ocurrences_num + 1)
        except:
            return False     
        
        return True 