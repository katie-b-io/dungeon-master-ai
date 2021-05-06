from abc import ABC, abstractmethod

from dmai.domain import Abilities, Alignment, Armor, Attacks, \
    Conditions, Equipment, Features, Languages, Skills, Spells
from dmai.domain.characters import CharacterClass, Race
from dmai.utils import DiceRoller

class Character(ABC):
    
    def __init__(self, character_data: dict) -> None:
        '''Character abstract class'''
        self.name = None
        
        try:
            for key in character_data:
                self.__setattr__(key, character_data[key])
                
            # replace the attributes values with objects where appropriate
            self.abilities = Abilities(self.abilities)
            self.alignment = Alignment(self.alignment)
            self.armor = Armor(self.armor)
            self.attacks = Attacks()
            self.char_class = CharacterClass(self.char_class)
            self.conditions = Conditions()
            self.equipment = Equipment(self.equipment)
            self.languages = Languages(self.languages)
            self.race = Race(self.race)
            self.skills = Skills(abilities = self.abilities,
                                 pro_bonus = self.proficiency_bonus,
                                 proficiencies = self.proficiencies["skills"])
            self.spells = Spells(self.spells)
            self.features = Features(char_class = self.char_class,
                                     race = self.race)
            
        except AttributeError as e:
            print("Cannot create character, incorrect attribute: {e}".format(
                e=e))
            raise
        
    def __repr__(self) -> str:
        return "Character: {n}\nMax HP: {hp}".format(
            n=self.name,
            hp=self.hp_max)

    @property
    def hp_max(self) -> int:
        hp = DiceRoller.get_max(self.char_class.hit_dice)
        mod = self.abilities.get_modifier("con")
        return hp + mod
    