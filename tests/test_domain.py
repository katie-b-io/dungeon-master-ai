import unittest
import sys
import os

p = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, p + "/../")

from dmai.domain.actions import Actions
from dmai.game.state import State
from dmai.game.adventure import Adventure
from dmai.utils.exceptions import UnrecognisedRoomError


class TestActions(unittest.TestCase):
    """Test the Actions class"""
    
    def setUp(self) -> None:
        self.adventure = Adventure("the_tomb_of_baradin_stormfury")
        self.adventure.build_world()
        self.state = State(self.adventure)
        self.actions = Actions(self.state, self.adventure)
        
    def test_move_good_destination(self) -> None:
        entity = "player"
        destination = "inns_cellar"
        (moved, utterance) = self.actions.move(entity, destination)
        self.assertEqual(moved, True)
        self.assertEqual(utterance, "You descend into the dark and damp cellar of the inn. The light from the ground floor above dimly illuminates the landing but the rest of the cellar is covered in complete darkness.\nThe landing in front of you leads left into the main cellar where you can hear the squeaks of rats as they destroy Corvus' stock and the loud protesting meows of Anvil-Jumper, Corvus' cat.")
    
    def test_move_bad_destination(self) -> None:
        entity = "player"
        destination = "the_moon"
        with self.assertRaises(UnrecognisedRoomError):
            self.actions.move(entity, destination)

if __name__ == "__main__":
    unittest.main()
