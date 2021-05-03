from dmai.utils import Loader

class Spells():
    
    # class variables
    spell_data = dict()
    
    def __init__(self, spells: dict) -> None:
        '''Spells class'''
        self.spells = spells
        self._load_spell_data()
        
    def __str__(self) -> str:
        return "Spells:\n{a}".format(a=self.spells)
    
    @classmethod
    def _load_spell_data(self) -> None:
        '''Set the self.spell_data class variable data'''
        self.spell_data = Loader.load_json("data/spells.json")
        