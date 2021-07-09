import shutil
import os
import random
import string

from dmai.game.game import Game
from dmai.ui.ui import UserInterface
from dmai.nlg.nlg import NLG
from dmai.nlu.nlu import NLU
from dmai.utils.output_builder import OutputBuilder
from dmai.utils.config import Config
from dmai.utils.logger import get_logger

logger = get_logger(__name__)

def init(root_path: str, rasa_host: str = "localhost", rasa_port: int = 5005) -> None:
    session_id = create_session_id()
    logger.debug("(SESSION: {s}) Initialising game".format(s=session_id))
    Config.set_uuid()
    Config.set_root(root_path)
    Config.hosts.set_rasa_host(rasa_host)
    Config.hosts.set_rasa_port(rasa_port)
    OutputBuilder.append(
        "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nWelcome to the Dungeon Master AI!\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    )
    OutputBuilder.append(
        "This is an MSc project created by Katie Baker at Heriot-Watt University. You are reminded not to input any identifying or confidential information. This interaction will be logged for analysis."
    )
    game = start(char_class="fighter", session_id=session_id)
    ui = UserInterface(game)

    
    return (ui, session_id)


def  create_session_id(chars = string.ascii_uppercase, n=10):
    # create a session id
    return "".join(random.choice(chars) for _ in range(n))


def start(char_class: str = None,
          char_name: str = None,
          skip_intro: bool = False,
          adventure: str = "the_tomb_of_baradin_stormfury",
          session_id: str = "") -> Game:
    """Initialise the game"""
    game = Game(char_class=char_class,
                char_name=char_name,
                skip_intro=skip_intro,
                adventure=adventure,
                session_id=session_id)
    game.load()
    NLG.set_game(game)
    NLU.set_game(game)

    # print some info for the user
    OutputBuilder.append(
        "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n{t}".format(t=NLG.get_title()))
    
    # return the game instance
    return game


def run(game: Game) -> None:
    """Run the game via CLI"""
    ui = UserInterface(game)
    ui.execute()


def gameover(session: str = None) -> None:
    """Gracefully exit the game"""
    OutputBuilder.append(
        "Thanks for playing! Don't forget to complete your feedback, in fact, why don't you do it now? :-)"
    )
    if Config.cleanup:
        shutil.rmtree(Config.directory.planning)
        os.remove("dmai.log")
    if not session:
        OutputBuilder.print()
        exit_game()
    else:
        OutputBuilder.append("Your unique ID for filling in the questionnaire is {s}.".format(s=session))
        return OutputBuilder.format()


def exit_game(exit_str: str = None) -> None:
    """Exit the game"""
    if exit_str:
        exit(exit_str)
    else:
        exit("Exiting game...")
