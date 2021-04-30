from abc import ABC, abstractmethod

class Monster(ABC):
    
    def __init__(self, monster_data: dict) -> None:
        '''Monster abstract class'''
        self.name = monster_data["name"]
    
    def __str__(self) -> str:
        return "Monster: {n}".format(n=self.name)
    