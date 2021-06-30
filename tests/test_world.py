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
            "id": "storage_room---western_corridor",
            "type": "door",
            "name": "Portcullis",
            "solutions": {
                "attack": {
                    "description": "attack door",
                    "intent": "attack",
                    "hp": 27,
                    "ac": 19
                },
                "str": {
                    "description": "force door",
                    "ability": "str",
                    "dc": 15
                }
            },
            "explore": {
                "use_switch": {
                    "description": "use switch",
                    "skill": "perception",
                    "dc": 10,
                    "result": "say:You see a switch left of the portcullis"
                }
            },
            "investigate": {}
        }
        self.puzzle = Puzzle(puzzle_data)

    def tearDown(self) -> None:
        shutil.rmtree(Config.directory.planning)

    def test_get_armor_class(self) -> None:
        self.assertEqual(19, self.puzzle.get_armor_class())

    def test_get_hp(self) -> None:
        self.assertEqual(27, self.puzzle.get_hp())

    def test_get_solution_id(self) -> None:
        self.assertEqual("attack", self.puzzle.get_solution_id("attack"))
        self.assertEqual("str", self.puzzle.get_solution_id("str"))


class TestPuzzleCollection(unittest.TestCase):
    """Test the PuzzleCollection class"""

    def setUp(self) -> None:
        puzzles_data = {
            "vault": {
                "id": "vault",
                "type": "vault",
                "name": "Vault",
                "solutions": {
                    "str": {
                        "description": "force lid",
                        "ability": "str",
                        "dc": 15
                    }
                },
                "explore": {},
                "investigate": {}
            },
            "silver_key": {
                "id": "silver_key",
                "type": "item",
                "name": "Silver key",
                "solutions": {},
                "explore": {
                    "pick_up": {
                        "description": "pick up key",
                        "result": "say:You notice the glint of a silver key in the open vault."
                    }
                },
                "investigate": {}
            },
            "altar": {
                "id": "altar",
                "type": "altar",
                "name": "Altar",
                "solutions": {},
                "explore": {},
                "investigate": {
                    "inspect_altar": {
                        "description": "inspect altar",
                        "skill": "religion",
                        "dc": 10,
                        "advantage": {
                            "race": "dwarf"
                        },
                        "result": "say:The dust covered altar is dedicated to Thorogrin, the patron deity of dwarves, the hammer and anvil being his holy symbol."
                    }
                }
            }
        }
        self.puzzles = PuzzleCollection(puzzles_data)

    def tearDown(self) -> None:
        shutil.rmtree(Config.directory.planning)

    def test_get_puzzle(self) -> None:
        self.assertEqual(
            "altar", self.puzzles.get_puzzle("altar").id
        )

    def test_get_all_puzzles(self) -> None:
        puzzles = self.puzzles.get_all_puzzles()
        self.assertListEqual(["vault", "silver_key", "altar"], [puzzle.id for puzzle in puzzles])


if __name__ == "__main__":
    unittest.main()


if __name__ == "__main__":
    unittest.main()
