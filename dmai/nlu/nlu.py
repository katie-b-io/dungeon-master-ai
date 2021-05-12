from dmai.utils.exceptions import DiceFormatError, UnrecognisedCommandError
from dmai.utils.dice_roller import DiceRoller
from dmai.nlu.rasa_adapter import RasaAdapter
from dmai.game.state import State
import dmai


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
            "cmd": "print(cls.show_commands())"
        },
        "exit": {
            "text": "/exit",
            "help": "Exit the game",
            "cmd": "dmai.dmai_helpers.exit_game()"
        },
        "roll": {
            "text": "/roll [die]",
            "help": "Roll a specified die, options: d4, d6, d8, d10, d12, d20, d100 (d20 by default)",
            "cmd": "roll_die(cls.param)",
            "default_param": "d20"
        },
        "say": {
            "text": "/say [utterance]",
            "help": "Have your character say specified utterance",
            "cmd": "State.talk()",
            "return": (False, "param")
        },
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
        cmd_str = "\nCommands:\n"
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
        if player_cmd[0] == "/":
            try:
                return cls._regex_and_exec(player_cmd)
            except UnrecognisedCommandError as e:
                print(e)
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
                c=player_cmd
            )
            raise UnrecognisedCommandError(msg)

        # define a local function for wrapping the DiceRoller
        def roll_die(die: str) -> None:
            try:
                DiceRoller.roll(die)
            except DiceFormatError as e:
                print(e)
        
        try:
            exec(command)
        except Exception:
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
        print("I'm thinking...")
        (intent, entities) = RasaAdapter.get_intent(player_utter)
        if entities:
            print(entities)
        if intent == "move":
            return ("move", {"nlu_entities": entities})
        if intent == "attack":
            return ("attack", {"nlu_entities": entities})
        else:
            return (None, {})
