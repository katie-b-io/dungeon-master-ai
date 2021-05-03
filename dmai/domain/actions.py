from dmai.utils import Loader

class Actions():
    
    # class variables
    action_data = dict()
    
    def __init__(self) -> None:
        '''Actions class'''
        self.actions = dict()
        self._load_action_data()
        
    def __str__(self) -> str:
        return "Actions:\n{a}".format(a=self.actions)
    
    @classmethod
    def _load_action_data(self) -> None:
        '''Set the self.action_data class variable data'''
        self.action_data = Loader.load_json("data/actions.json")
        