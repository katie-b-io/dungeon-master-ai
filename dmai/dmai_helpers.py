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
        logger.debug("(SESSION {s}) Initialising game".format(s=session_id))
    Config.set_root(root_path)
    Config.hosts.set_rasa_host(rasa_host)
    Config.hosts.set_rasa_port(rasa_port)
    game = start(char_class="fighter", session_id=session_id, saved_state=saved_state)
    ui = UserInterface(game)
    if not saved_state:
        ui.game.output_builder.clear()
        ui.game.output_builder.append(
            "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nWelcome to the Dungeon Master AI!\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        )
        ui.game.output_builder.append(
            "This is an MSc project created by Katie Baker at Heriot-Watt University. You are reminded not to input any identifying or confidential information. This interaction will be logged for analysis. By continuing past this point you confirm you consent to participating in the study and have signed the consent form at https://forms.office.com/r/EY4Wu6pAJE."
        )
        ui.game.output_builder.append("Your unique ID for filling in the questionnaire is {s}. Please make a note of it.".format(s=session_id))
        ui.game.output_builder.append(
            "You will enter text into the field below to interact with the DMAI and issues commands. You can use the the dice roller button in the bottom left corner when the game starts for rolling dice when requested to."
        )
        ui.game.output_builder.append(
            "Use the thumbs up and thumbs down buttons for rating responses by the DMAI. You don't need to rate every response, just responses that you particularly like or dislike."
        )
        ui.game.output_builder.append(
            "Refer to the character sheet and player's guide for additional information about your character and the game respectively."
        )
        ui.game.output_builder.append(
            "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n{t}".format(t=NLG.get_title(ui.game.dm.adventure.title)))
        ui.game.output_builder.append("> Press enter to continue...")

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
                session_id=session_id,
                saved_state=saved_state)
    game.load()
    
    # return the game instance
    return game


def run(game: Game) -> None:
    """Run the game via CLI"""
    game.output_builder.append(
        "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n{t}".format(t=NLG.get_title(game.dm.adventure.title)))
    ui = UserInterface(game)
    ui.execute()


def gameover(output_builder: OutputBuilder, session: str = "") -> None:
    """Gracefully exit the game"""
    logger.debug("(SESSION {s}) Gameover".format(s=session))
    if Config.cleanup:
        shutil.rmtree(Config.directory.planning)
        os.remove("dmai.log")
    if not bool(session):
        output_builder.append("Exiting game...")
        output_builder.print()
        exit_game()
    else:
        output_builder.append(
            "Thanks for playing! Don't forget to complete your feedback, in fact, why don't you do it now? :-)"
        )
        output_builder.append("Your unique ID for filling in the questionnaire is {s}. The questionnaire can be found at https://forms.office.com/r/qXwE5Jz3s3.".format(s=session))
        return output_builder.format()


def exit_game(exit_str: str = None) -> None:
    """Exit the game"""
    if exit_str:
        exit(exit_str)
    else:
        exit("Exiting game...")
