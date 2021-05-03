from dmai.utils import Loader

class Conditions():
    
    # class variables
    condition_data = dict()
    
    def __init__(self) -> None:
        '''Conditions class'''
        self.conditions = dict()
        self._load_condition_data()
        
    def __repr__(self) -> str:
        return "Conditions:\n{a}".format(a=self.conditions)
    
    @classmethod
    def _load_condition_data(self) -> None:
        '''Set the self.condition_data class variable data'''
        self.condition_data = Loader.load_json("data/conditions.json")
        