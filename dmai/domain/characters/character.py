from abc import ABC, abstractmethod

class Character(ABC):
    
    def __init__(self, character_data: dict) -> None:
        '''Character abstract class'''
        try:
            self.name = character_data["name"]
        except KeyError as e:
            print("Cannot create character, incorrect key: {e}".format(e=e))
            raise