
from dmai.game.adventure import Adventure

class State():
    
    def __init__(self, adventure: Adventure) -> None:
        '''Main class for the game state'''
        self.current_room = adventure.get_init_room()
    
    def set_current_room(self, room: str) -> None:
        '''Method to set the current room'''
        self.current_room = room
    
    
    