import shutil
import os
import random
import string

from dmai.game.game import Game
from dmai.ui.ui import UserInterface
from dmai.nlg.nlg import NLG
from dmai.utils.config import Config
from dmai.utils.output_builder import OutputBuilder
from dmai.utils.logger import get_logger

logger = get_logger(__name__)

def init(root_path: str, rasa_host: str = "localhost", rasa_port: int = 5005, saved_state: dict = None, session_id: str = None) -> None:
    if not session_id:
        session_id = create_session_id()
        logger.debug("(SESSION: {s}) Initialising game".format(s=session_id))
    Config.set_uuid()
    Config.set_root(root_path)
    Config.hosts.set_rasa_host(rasa_host)
    Config.hosts.set_rasa_port(rasa_port)
    game = start(char_class="fighter", session_id=session_id, saved_state=saved_state)
    if not saved_state:
        game.output_builder.append(
            "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nWelcome to the Dungeon Master AI!\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        )
        game.output_builder.append(
            "This is an MSc project created by Katie Baker at Heriot-Watt University. You are reminded not to input any identifying or confidential information. This interaction will be logged for analysis."
        )
        game.output_builder.append("Your unique ID for filling in the questionnaire is {s}. Please make a note of it.".format(s=session_id))
        game.output_builder.append(
            "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n{t}".format(t=NLG.get_title(game.dm.adventure.title)))
    ui = UserInterface(game)

    return (ui, session_id)


def  create_session_id(chars = string.ascii_uppercase, n=10):
    # create a session id
    return "".join(random.choice(chars) for _ in range(n))


def start(char_class: str = None,
          char_name: str = None,
          skip_intro: bool = False,
          adventure: str = "the_tomb_of_baradin_stormfury",
          session_id: str = "",
          saved_state: dict = None) -> Game:
    """Initialise the game"""
    game = Game(char_class=char_class,
                char_name=char_name,
                skip_intro=skip_intro,
                adventure=adventure,
                session_id=session_id)
    game.load()
    if saved_state:
        game.state.load(saved_state)
    
    # return the game instance
    return game


def run(game: Game) -> None:
    """Run the game via CLI"""
    game.output_builder.append(
        "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n{t}".format(t=NLG.get_title(game.dm.adventure.title)))
    ui = UserInterface(game)
    ui.execute()


def gameover(output_builder: OutputBuilder, session: str = None) -> None:
    """Gracefully exit the game"""
    output_builder.append(
        "Thanks for playing! Don't forget to complete your feedback, in fact, why don't you do it now? :-)"
    )
    if Config.cleanup:
        shutil.rmtree(Config.directory.planning)
        os.remove("dmai.log")
    if not session:
        output_builder.print()
        exit_game()
    else:
        output_builder.append("Your unique ID for filling in the questionnaire is {s}.".format(s=session))
        output_builder.append("Exiting game...")
        return output_builder.format()


def exit_game(exit_str: str = None) -> None:
    """Exit the game"""
    if exit_str:
        exit(exit_str)
    else:
        exit("Exiting game...")
