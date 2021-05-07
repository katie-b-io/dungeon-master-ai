from dmai.game.game import Game
from dmai.ui.ui import UserInterface
from dmai.nlg.nlg import NLG
from dmai.nlu.nlu import NLU


def start() -> Game:
    """Initialise the game"""
    game = Game()
    NLG.set_game(game)
    NLU.set_game(game)

    # print some info for the user
    print(
        "This interface is designed for you to communicate with the DMAI using natural language but you also have the following commands at your disposal:"
    )
    print(NLU.show_commands())
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(NLG.get_title())

    # return the game instance
    return game


def run(game: Game) -> None:
    """Run the game via CLI"""
    ui = UserInterface(game)
    ui.execute()


def exit_game(exit_str: str = None) -> None:
    """Exit the game"""
    if exit_str:
        exit(exit_str)
    else:
        exit("Exiting game...")
