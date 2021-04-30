from dmai.utils import Loader

class Abilities():
    
    # class variables
    ability_data = dict()
    
    def __init__(self, abilities: dict) -> None:
        '''Abilities class'''
        self.abilities = abilities
        self._load_ability_data()
        self.modifiers = self._calculate_ability_modifiers()
        
    def __str__(self) -> str:
        return "Abilities:\n{a}\nModifiers:\n{m}".format(a=self.abilities,
                                                         m=self.modifiers)
    
    @classmethod
    def _load_ability_data(self) -> None:
        '''Set the self.ability_data class variable data'''
        self.ability_data = Loader.load_json("data/abilities.json")
        
    def _calculate_ability_modifiers(self) -> dict:
        '''Calculate the ability modifiers'''
        modifiers = dict()
        for ability in self.abilities:
            for mod in self.ability_data["modifiers"]:
                mod_min = self.ability_data["modifiers"][mod]["min"]
                mod_max = self.ability_data["modifiers"][mod]["max"]
                if mod_min <= self.abilities[ability] <= mod_max:
                    modifiers[ability] = mod
                    break
        return modifiers