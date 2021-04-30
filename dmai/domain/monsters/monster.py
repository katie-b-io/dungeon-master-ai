from abc import ABC, abstractmethod

from dmai.utils import DiceRoller
from dmai.domain import Abilities

class Monster(ABC):
    
    def __init__(self, monster_data: dict) -> None:
        '''Monster abstract class'''
        self.name = monster_data["name"]
        self.type = monster_data["type"]
        self.size = monster_data["size"]
        self.alignment = monster_data["alignment"]
        self.ac = monster_data["ac"]
        self.hit_dice = monster_data["hit_dice"]
        self.hp_max = self._calculate_hp()
        self.speed = monster_data["speed"]
        self.climb = monster_data["climb"]
        self.cr = monster_data["cr"]
        self.abilities = Abilities(monster_data["abilities"])
    
    def __str__(self) -> str:
        return "Monster: {n}\nHP: {hp}".format(n=self.name, hp=self.hp)
    
    def _calculate_hp(self) -> int:
        return DiceRoller.roll_dice(self.hit_dice)