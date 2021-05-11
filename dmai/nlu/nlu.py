from dmai.utils.exceptions import DiceFormatError, UnrecognisedCommandError
from dmai.utils.dice_roller import DiceRoller
from dmai.nlu.rasa_adapter import RasaAdapter
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

    # class variable
    game = None
    commands = {
        "help": {
            "text": "/help",
            "help": "Show these commands",
            "cmd": "print(cls.show_commands())",
        },
        "exit": {
            "text": "/exit",
            "help": "Exit the game",
            "cmd": "dmai.dmai_helpers.exit_game()",
        },
        "roll": {
            "text": "/roll [die]",
            "help": "Roll a specified die, options: d4, d6, d8, d10, d12, d20, d100 (d20 by default)",
            "cmd": "roll_die(param)",
            "default_param": "d20",
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
            cmd_str += "{c:<16}".format(c=cls.commands[cmd]["text"])
            cmd_str += "{h}\n".format(h=cls.commands[cmd]["help"])
        return cmd_str

    @classmethod
    def process_player_command(cls, player_cmd: str) -> bool:
        """Method to process the player command"""

        # first check if the user is issuing a command
        if player_cmd[0] == "/":
            try:
                cls._regex(player_cmd)
            except UnrecognisedCommandError as e:
                print(e)
            return True

        return False

    @classmethod
    def _regex(cls, player_cmd: str) -> None:
        """Process the player command as a regular expression"""
        cmd_tokens = player_cmd.split()
        cmd = cmd_tokens[0][1:]

        try:
            # setting param here in the local namespace for exec
            if len(cmd_tokens) == 2:
                param = cmd_tokens[1]
            elif "default_param" in cls.commands[cmd]:
                param = cls.commands[cmd]["default_param"]

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
            return

        return True

    @classmethod
    def process_player_utterance(cls, player_utter: str) -> tuple:
        """Method to process the player utterance"""
        return cls._determine_intent(player_utter)

    @classmethod
    def _determine_intent(cls, player_utter: str) -> str:
        """Method to determine the player intent"""
        player_utter = player_utter.lower()
        print("Thinking...")
        (intent, entities) = RasaAdapter.get_intent(player_utter)
        if entities:
            print(entities)
        if intent == "move":
            return ("move", {"nlu_entities": entities})
        if intent == "attack":
            return ("attack", {"nlu_entities": entities})
        else:
            return (None, {})
