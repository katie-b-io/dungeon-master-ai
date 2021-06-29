from typing import Generator
import unittest
import sys
import os
import shutil

p = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, p + "/../")

from dmai.utils.config import Config
from dmai.game.world.puzzles.puzzle import Puzzle
from dmai.game.world.puzzles.puzzle_collection import PuzzleCollection


class TestPuzzle(unittest.TestCase):
    """Test the Puzzle class"""

    def setUp(self) -> None:
        puzzle_data = {
            "id": "storage_room---burial_chamber",
            "type": "door",
            "name": "Portcullis",
            "solutions": {
                "attack": {
                    "description": "attack door",
                    "intent": "attack",
                    "hp": 27,
                    "ac": 19,
                },
                "force": {"description": "force door", "ability": "str", "dc": 15},
                "switch": {
                    "description": "use switch",
                    "skill": "perception",
                    "dc": 10,
                },
            },
        }
        self.puzzle = Puzzle(puzzle_data)

    def tearDown(self) -> None:
        shutil.rmtree(Config.directory.planning)

    def test_get_armor_class(self) -> None:
        self.assertEqual(19, self.puzzle.get_armor_class())

    def test_get_hp(self) -> None:
        self.assertEqual(27, self.puzzle.get_hp())


class TestPuzzleCollection(unittest.TestCase):
    """Test the PuzzleCollection class"""

    def setUp(self) -> None:
        puzzles_data = {
            "storage_room---burial_chamber": {
                "id": "storage_room---burial_chamber",
                "type": "door",
                "name": "Portcullis",
                "solutions": {
                    "attack": {
                        "description": "attack door",
                        "intent": "attack",
                        "hp": 27,
                        "ac": 19,
                    },
                    "force": {"description": "force door", "ability": "str", "dc": 15},
                    "switch": {
                        "description": "use switch",
                        "skill": "perception",
                        "dc": 10,
                    },
                },
            },
            "storage_room---western_corridor": {
                "id": "storage_room---western_corridor",
                "type": "door",
                "name": "Portcullis",
                "solutions": {
                    "attack": {
                        "description": "attack door",
                        "intent": "attack",
                        "hp": 27,
                        "ac": 19,
                    },
                    "force": {"description": "force door", "ability": "str", "dc": 15},
                    "switch": {
                        "description": "use switch",
                        "skill": "perception",
                        "dc": 10,
                    },
                },
            },
        }
        self.puzzles = PuzzleCollection(puzzles_data)

    def tearDown(self) -> None:
        shutil.rmtree(Config.directory.planning)

    def test_get_armor_class(self) -> None:
        self.assertEqual(19, self.puzzles.get_door_armor_class("storage_room", "burial_chamber"))

    def test_get_hp(self) -> None:
        self.assertEqual(27, self.puzzles.get_door_hp("storage_room", "burial_chamber"))


if __name__ == "__main__":
    unittest.main()


if __name__ == "__main__":
    unittest.main()
