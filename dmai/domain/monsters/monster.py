from abc import ABC, abstractmethod

from dmai.utils import DiceRoller
from dmai.domain import Abilities, Actions, Alignment, Armor, Attacks, \
    Conditions, Equipment, Features, Languages, Skills, Spells

class Monster(ABC):
    
    def __init__(self, monster_data: dict) -> None:
        '''Monster abstract class'''
        try:
            for key in monster_data:
                self.__setattr__(key, monster_data[key])
            
            # replace the attributes values with objects where appropriate
            self.abilities = Abilities(self.abilities)
            self.actions = Actions()
            self.alignment = Alignment(self.alignment)
            self.armor = Armor(self.armor)
            self.attacks = Attacks(self.attacks)
            self.conditions = Conditions()
            self.equipment = Equipment(self.equipment)
            self.features = Features(self.features)
            self.languages = Languages(self.languages)
            self.skills = Skills(self.skills)
            self.spells = Spells(self.spells)
            
        except AttributeError as e:
            print("Cannot create monster, incorrect attribute: {e}".format(e=e))
            raise
    
    def __str__(self) -> str:
        return "Monster: {n}\nMax HP: {hp}".format(n=self.name, hp=self.hp_max)
    
    def _calculate_hp(self) -> int:
        return DiceRoller.roll_dice(self.hit_dice)