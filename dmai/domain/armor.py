from dmai.utils import Loader

class Armor():
    
    # class variables
    armor_data = dict()
    
    def __init__(self, armor: str) -> None:
        '''Armor class'''
        self.armor = armor
        self._load_armor_data()
        
    def __str__(self) -> str:
        return "Armor:\n{a}".format(a=self.armor)
    
    @classmethod
    def _load_armor_data(self) -> None:
        '''Set the self.armor_data class variable data'''
        self.armor_data = Loader.load_json("data/armor.json")
        