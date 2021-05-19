from dmai.game.game import Game
from dmai.ui.ui import UserInterface
from dmai.nlg.nlg import NLG
from dmai.nlu.nlu import NLU


def start(char_class: str = None, char_name: str = None, skip_intro: bool = False) -> Game:
    """Initialise the game"""
    game = Game(char_class=char_class, char_name=char_name, skip_intro=skip_intro)
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

def gameover() -> None:
    """Gracefully exit the game"""
    print("Thanks for playing! Don't forget to complete your feedback, in fact, why don't you do it now? :-)")
    exit_game()

def exit_game(exit_str: str = None) -> None:
    """Exit the game"""
    if exit_str:
        exit(exit_str)
    else:
        exit("Exiting game...")
