from dmai import DM
from dmai.game import Player
from dmai.domain import Domain
from dmai.nlg import NLG

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
            if char_class:
                self.player = Player(char_class)
        
        elif not self.player.name:
            # player is entering a name
            self.player.set_name(player_utter)
            self.dm.input(player_utter)
            
        else:
            # relay the player utterance to the dm
            self.dm.input(player_utter)
        
    def output(self) -> str:
        '''Return an output for the player'''
        
        # the player variable is not set at the beginning of the game
        if not self.player:
            # get the character options for player
            return NLG.get_char_class()
        
        elif not self.player.name:
            # get the player's name
            return NLG.get_player_name()
        
        return self.dm.output
