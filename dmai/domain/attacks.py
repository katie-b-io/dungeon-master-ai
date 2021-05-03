from dmai.utils import Loader

class Attacks():
    
    # class variables
    attack_data = dict()
    
    def __init__(self, attacks: dict = {}) -> None:
        '''Attacks class'''
        self.attacks = attacks
        self._load_attack_data()
        
    def __repr__(self) -> str:
        return "Attacks:\n{a}".format(a=self.attacks)
    
    @classmethod
    def _load_attack_data(self) -> None:
        '''Set the self.attack_data class variable data'''
        self.attack_data = Loader.load_json("data/attacks.json")
        