from typing import Generator
from dmai.utils import Loader, Text

from dmai.game.world import Room

class Adventure():
    
    # class variables
    adventure_data = dict()

    def __init__(self, adventure: str) -> None:
        '''Main class for the adventure'''
        self.adventure = adventure
        self._load_adventure_data(self.adventure)
        
        try:
            for key in self.adventure_data:
                self.__setattr__(key, self.adventure_data[key])
        except AttributeError as e:
            print("Cannot create adventure, incorrect attribute: {e}".format(
                e=e))
            raise
        
    def __repr__(self) -> str:
        return "Adventure: {a}".format(a=self.title)
    
    @classmethod
    def _load_adventure_data(self, adventure) -> None:
        '''Set the self.adventure_data class variable data'''
        self.adventure_data = Loader.load_json("adventures/{a}.json".format(
            a=adventure))
    
    def build_world(self) -> None:
        '''Method to build the world'''
        self.rooms = dict()
        
        for room_name in self.adventure_data["rooms"]:
            room_data = self.adventure_data["rooms"][room_name]
            room = Room(room_data)
            self.rooms[room_name] = room
    
    @property
    def intro_text(self) -> Generator:
        return Text.yield_text(self.text["intro"], "\n")
    
    def get_init_room(self) -> str:
        '''Method to get the starting room'''
        for room in self.rooms:
            if self.rooms[room].init:
                return room