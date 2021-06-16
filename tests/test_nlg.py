import unittest
import sys
import os

p = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, p + "/../")

from dmai.nlg.nlg import NLG
from dmai.game.game import Game


class TestNLG(unittest.TestCase):
    """Test the NLG class"""
    def setUp(self) -> None:
        self.game = Game(char_class="fighter", char_name="Xena", adventure="the_tomb_of_baradin_stormfury")
        NLG.set_game(self.game)

    def test_enter_room(self) -> None:
        room = "room"
        self.assertEqual("You entered room", NLG.enter_room(room))

    def test_cannot_move(self) -> None:
        room = "room"
        self.assertEqual("You cannot move to room", NLG.cannot_move(room))

    def test_cannot_move_same(self) -> None:
        room = "room"
        reason = "same"
        self.assertEqual(
            "You cannot move to room because you're already there!",
            NLG.cannot_move(room, reason),
        )

    def test_cannot_move_locked(self) -> None:
        room = "room"
        reason = "locked"
        self.assertEqual(
            "You cannot move to room because the way is locked!",
            NLG.cannot_move(room, reason),
        )


if __name__ == "__main__":
    unittest.main()
