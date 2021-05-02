from dmai import DM
from dmai import domain
from dmai.game import Player
from dmai.domain import Domain

class Game():
    
    def __init__(self):
        '''Main class for the game'''
        self.player = None
        self.dm = DM()
        self.domain = Domain()
        
        # Load the domain data
        self.domain.load_all()
    
    def input(self, player_utter: str) -> None:
        '''Receive a player input'''
        
        # the player variable is not set at the beginning of the game
        if not self.player:
            # player is selecting a class
            player_utter = player_utter.lower()
            char_class = self.domain.get_character(player_utter)
            self.player = Player(char_class)
            
        else:
            # relay the player utterance to the dm
            self.dm.input(player_utter)
        
    def output(self) -> str:
        '''Return an output for the player'''
        if not self.player:
            print("here")
            return self.domain.char_class_select
        return self.dm.output
