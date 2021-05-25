import unittest
import sys
import os

p = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, p + "/../")

from dmai.domain.actions import Actions
from dmai.game.game import Game
from dmai.utils.exceptions import UnrecognisedRoomError


class TestActions(unittest.TestCase):
    """Test the Actions class"""
    
    def setUp(self) -> None:
        self.game = Game()
        self.game.load()
        self.actions = self.game.dm.actions
        
    def test_move_good_destination(self) -> None:
        entity = "player"
        destination = "inns_cellar"
        moved = self.actions.move(entity, destination)
        self.assertEqual(moved, True)
    
    def test_move_bad_destination(self) -> None:
        entity = "player"
        destination = "the_moon"
        with self.assertRaises(UnrecognisedRoomError):
            self.actions.move(entity, destination)

if __name__ == "__main__":
    unittest.main()
