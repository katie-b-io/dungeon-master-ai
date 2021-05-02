from dmai import DM
from dmai.game import Game
from dmai.ui import UserInterface
    
def start() -> Game:
    '''Initialise the game'''
    game = Game()
    return game
    
def run(game: Game) -> None:
    '''Run the game via CLI'''
    ui = UserInterface(game)
    ui.execute()