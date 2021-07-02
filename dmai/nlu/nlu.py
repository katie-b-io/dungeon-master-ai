import traceback

import dmai
from dmai.utils.exceptions import DiceFormatError, UnrecognisedCommandError
from dmai.utils.dice_roller import DiceRoller
from dmai.utils.output_builder import OutputBuilder
from dmai.utils.text import Text
from dmai.nlu.rasa_adapter import RasaAdapter
from dmai.game.state import State
from dmai.game.state import Combat
from dmai.utils.logger import get_logger

logger = get_logger(__name__)


class NLUMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs) -> None:
        """NLU static singleton metaclass"""
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class NLU(metaclass=NLUMeta):

    # class variables
    game = None
    param = ""
    commands = {
        "help": {
            "text": "/help",
            "help": "Show these commands",
            "cmd": "OutputBuilder.append(cls.show_commands(), wrap=False)"
        },
        "exit": {
            "text": "/exit",
            "help": "Exit the game",
            "cmd": "dmai.dmai_helpers.gameover()"
        },
        "stats": {
            "text":
            "/stats",
            "help":
            "Show your character stats in a character sheet",
            "cmd":
            "OutputBuilder.append(cls.game.player.get_character_sheet(), wrap=False)"
        }
    }

    def __init__(self) -> None:
        """NLU static class"""
        pass

    @classmethod
    def set_game(cls, game) -> None:
        cls.game = game

    @classmethod
    def show_commands(cls) -> str:
        """Return the command list"""
        cmd_str = "Commands:\n"
        for cmd in cls.commands:
            cmd_str += "{c:<20}".format(c=cls.commands[cmd]["text"])
            cmd_str += "{h}\n".format(h=cls.commands[cmd]["help"])
        return cmd_str

    @classmethod
    def process_player_command(cls, player_cmd: str) -> tuple:
        """Method to process the player command.
        Returns a tuple with (bool, string) where bool indicates if DM output
        should be paused and string is the updated player utterance."""

        # first check if the user is issuing a command
        if player_cmd[0] == "/" or player_cmd[0] == "\\":
            try:
                return cls._regex_and_exec(player_cmd)
            except UnrecognisedCommandError as e:
                logger.error(e)
        return (False, player_cmd)

    @classmethod
    def _regex_and_exec(cls, player_cmd: str) -> None:
        """Process the player command as a regular expression"""
        cmd_tokens = player_cmd.split()
        cmd = cmd_tokens[0][1:]

        try:
            # setting param here in the local namespace for exec
            if len(cmd_tokens) == 2:
                cls.param = cmd_tokens[1]
            elif len(cmd_tokens) > 2:
                cls.param = " ".join(cmd_tokens[2:])
            elif "default_param" in cls.commands[cmd]:
                cls.param = cls.commands[cmd]["default_param"]

            command = cls.commands[cmd]["cmd"]
        except KeyError:
            msg = "Command not recognised: {c}\nUse /help to get list of available commands".format(
                c=player_cmd)
            raise UnrecognisedCommandError(msg)

        # define a local function for wrapping the DiceRoller
        def roll(die: str) -> None:
            try:
                DiceRoller.roll(die)
            except DiceFormatError as e:
                logger.error(e)

        try:
            exec(command)
        except Exception as e:
            traceback.print_exc()
            return (False, "")

        if "return" in cls.commands[cmd]:
            return_vals = []
            for val in cls.commands[cmd]["return"]:
                # check if string refers to class variable
                if type(val) == str and val in cls.__dict__:
                    return_vals.append(cls.__dict__[val])
                else:
                    return_vals.append(val)
            return tuple(return_vals)
        else:
            return (True, "")

    @classmethod
    def process_player_utterance(cls, player_utter: str) -> tuple:
        """Method to process the player utterance"""
        return cls._determine_intent(player_utter)

    @classmethod
    def _determine_intent(cls, player_utter: str) -> tuple:
        """Method to determine the player intent"""
        player_utter = player_utter.lower()
        (intent, entities) = RasaAdapter.get_intent(player_utter)
        State.set_intent(intent)
        if intent:
            print("intent: " + intent)
        if entities:
            print(entities)
            
        # check if there's expected entities
        if State.expected_entities:
            hits = [entity for entity in entities if entity["entity"] in State.expected_entities]
            if hits:
                # if we have a hit for expected entities, use the primary expected intent
                if State.expected_intent:
                    intent = State.expected_intent[0]
                elif State.stored_intent:
                    intent = State.stored_intent["intent"]
                    State.clear_expected_entities()
                
        # check if there's an expected intent
        elif State.expected_intent:
            if intent not in State.expected_intent:
                # TODO make exception for hints or questions
                # TODO this also seems a little broken when input is not recognised and player corrects themselves to roll initiative
                intents = [State.get_dm().player_intent_map[intent]["desc"] for intent in State.expected_intent]
                intent_str = Text.properly_format_list(intents, last_delimiter=" or ")
                OutputBuilder.append("I was expecting you to {i}".format(i=intent_str))
                return (None, {"nlu_entities": entities})

        # check if in combat before allowing any player utterance
        if State.in_combat:
            if State.get_combat_status() == Combat.ATTACK_ROLL:
                return ("attack", {"nlu_entities": entities})
            else:
                return ("roll", {"nlu_entities": entities})
        
        if intent == "move":
            return ("move", {"nlu_entities": entities})
        if intent == "attack" or intent == "ranged_attack":
            return ("attack", {"nlu_entities": entities})
        if intent == "use":
            return ("use", {"nlu_entities": entities})
        if intent == "stop_using":
            return ("stop_using", {"nlu_entities": entities})
        if intent == "hint":
            return ("hint", {})
        if intent == "equip":
            return ("equip", {"nlu_entities": entities})
        if intent == "unequip":
            return ("unequip", {"nlu_entities": entities})
        if intent == "converse":
            return ("converse", {"nlu_entities": entities})
        if intent == "greet":
            return ("converse", {"nlu_entities": entities})
        if intent == "affirm":
            return ("affirm", {})
        if intent == "deny":
            return ("deny", {})
        if intent == "explore":
            return ("explore", {"nlu_entities": entities})
        if intent == "roll":
            return ("roll", {"nlu_entities": entities})
        if intent == "pick_up":
            return ("pick_up", {"nlu_entities": entities})
        if intent == "health":
            return ("health", {})
        if intent == "inventory":
            return ("inventory", {})
        if intent == "force_door":
            return ("force_door", {"nlu_entities": entities})
        if intent == "ability_check":
            return ("ability_check", {"nlu_entities": entities})
        if intent == "skill_check":
            return ("skill_check", {"nlu_entities": entities})
        if intent == "ale":
            return ("ale", {"nlu_entities": entities})
        else:
            # check for stored intent in State
            if State.stored_intent:
                # combine the stored entities with new entities
                if "nlu_entities" in State.stored_intent["params"]:
                    entities.extend(
                        State.stored_intent["params"]["nlu_entities"])
                return (State.stored_intent["intent"], {
                    "nlu_entities": entities
                })

        return (None, {})
