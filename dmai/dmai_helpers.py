from dmai.game import Game
from dmai.ui import UserInterface
from dmai.nlg import NLG
    
def start() -> Game:
    '''Initialise the game'''
    game = Game()
    NLG.set_game(game)
    print(NLG.get_title())
    return game
    
def run(game: Game) -> None:
    '''Run the game via CLI'''
    ui = UserInterface(game)
    ui.execute()