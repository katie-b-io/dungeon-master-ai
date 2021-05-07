from abc import ABC, abstractmethod

from dmai.domain.abilities import Abilities
from dmai.domain.alignment import Alignment
from dmai.domain.armor import Armor
from dmai.domain.attacks import Attacks
from dmai.domain.conditions import Conditions
from dmai.domain.equipment import Equipment
from dmai.domain.features import Features
from dmai.domain.languages import Languages
from dmai.domain.skills import Skills
from dmai.domain.spells import Spells

class Monster(ABC):
    def __init__(self, monster_data: dict) -> None:
        """Monster abstract class"""
        try:
            for key in monster_data:
                self.__setattr__(key, monster_data[key])

            # replace the attributes values with objects where appropriate
            self.abilities = Abilities(self.abilities)
            self.alignment = Alignment(self.alignment)
            self.armor = Armor(self.armor)
            self.attacks = Attacks(self.attacks)
            self.conditions = Conditions()
            self.equipment = Equipment(self.equipment)
            self.features = Features(features=self.features)
            self.languages = Languages(self.languages)
            self.skills = Skills(abilities=self.abilities, skills=self.skills)
            self.spells = Spells(self.spells)

        except AttributeError as e:
            print("Cannot create monster, incorrect attribute: {e}".format(e=e))
            raise

    def __repr__(self) -> str:
        return "Monster: {n}\nMax HP: {hp}".format(n=self.name, hp=self.hp_max)
