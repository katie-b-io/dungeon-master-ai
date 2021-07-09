import unittest
import sys
import os

p = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, p + "/../")

from dmai.nlu.nlu import NLU
from dmai.game.state import State
from dmai.utils.output_builder import OutputBuilder
from dmai.utils.exceptions import UnrecognisedCommandError


class TestNLU(unittest.TestCase):
    """Test the NLU class"""
    def setUp(self) -> None:
        self.output_builder = OutputBuilder()
        self.state = State(self.output_builder)
        self.nlu = NLU(self.state, self.output_builder)
        self.roll_cmd1 = "/roll d20"
        self.help_cmd = "/help"
        self.exit_cmd = "/exit"
        self.bad_cmd1 = "roll d20"
        self.bad_cmd2 = "/unknown"

    def test_show_commands(self) -> None:
        actual = "Commands:\n"
        actual += "/help               Show these commands\n"
        actual += "/exit               Exit the game\n"
        actual += "/stats              Show your character stats in a character sheet\n"

        self.assertEqual(self.nlu.show_commands(), actual)

    def test_process_player_command_help(self) -> None:
        self.assertEqual(self.nlu.process_player_command(self.help_cmd), (True, ""))

    def test_process_player_command_exit(self) -> None:
        with self.assertRaises(SystemExit):
            self.nlu.process_player_command(self.exit_cmd)

    def test_process_player_command_malformed(self) -> None:
        self.assertEqual(self.nlu.process_player_command(self.bad_cmd1),
                         (False, "roll d20"))
        self.assertEqual(self.nlu.process_player_command(self.bad_cmd2),
                         (False, "/unknown"))

    def test_regex_help(self) -> None:
        self.assertEqual(self.nlu._regex_and_exec(self.help_cmd), (True, ""))

    def test_regex_exit(self) -> None:
        with self.assertRaises(SystemExit):
            self.nlu._regex_and_exec(self.exit_cmd)

    def test_regex_malformed(self) -> None:
        with self.assertRaises(UnrecognisedCommandError):
            self.nlu._regex_and_exec(self.bad_cmd1)
        with self.assertRaises(UnrecognisedCommandError):
            self.nlu._regex_and_exec(self.bad_cmd2)


if __name__ == "__main__":
    unittest.main()
