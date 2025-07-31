#from typing import Optional

from state import State
from action import Action

class QsaStats:
        
        def __init__(self, qsa : float):
            print("Initializing QsaStats")
            self.acc_qsa = qsa 
            self.first_ocurrences_acc_qsa = qsa 
            self.ocurrences_num = 1 # approach 1
            self.first_ocurrences_num = 1 # approach 2
        
        def update_stats(self, qsa : float, first = False):
            self.acc_qsa += qsa 
            self.ocurrences_num += 1

            if first:
                self.first_ocurrences_acc_qsa += qsa 
                self.first_ocurrences_num += 1

        
        def get_stats(self):
            return (self.acc_qsa, self.ocurrences_num)
        
        
        def get_first_ocurrences_stats(self):
            return (self.acc_qsa, self.first_ocurrences_num)
        
        
        def get_qsa_mean(self):
            return self.acc_qsa / self.ocurrences_num
        
        
        def get_qsa_first_ocurrences_mean(self):
            return self.first_ocurrences_acc_qsa / self.first_ocurrences_num
        
        
        # How to apply that only for first ocurrences?
        def __add__(self, qsa : float):
            self.acc_qsa += qsa
            self.ocurrences_num += 1

            return self
        

class QsaStatsManager:


    def __init__(self):
        self.__qsa_stats : dict[tuple[State, Action], QsaStats]
        
    def __get_state_action_qsa_stats(self, state_action : tuple[State, Action]) -> QsaStats:
        qsa_stats = self.__qsa_stats.get(state_action)
        if qsa_stats is not None:
            return qsa_stats
        
        return QsaStats(0.)
         

    def update_state_action_qsa_stats(self, state_action : tuple[State, Action], qsa : float):
        # Update example:
        # car = {
        #     "brand": "Ford",
        #     "model": "Mustang",
        #     "year": 1964
        # }
        # car.update({"color": "White"})
        #  
        qsa_stats = { state_action: self.__get_state_action_qsa_stats(state_action) + qsa }
        self.__qsa_stats.update(qsa_stats) 
        
        
        
        
    
    