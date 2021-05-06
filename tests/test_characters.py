import unittest
import sys
import os

p = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, p + "/../")

from dmai.domain.characters import (
    Character,
    CharacterCollection,
    Cleric,
    Fighter,
    Rogue,
    Wizard,
)


class TestCharacterCollection(unittest.TestCase):
    """Test the CharacterCollection class"""

    def setUp(self) -> None:
        self.characters = CharacterCollection()

    def test_character_factory_error(self) -> None:
        with self.assertRaises(ValueError):
            self.characters._character_factory("human")

    def test_get_character_cleric(self) -> None:
        self.assertIsInstance(self.characters.get_character("cleric"), Cleric)
        self.assertIsInstance(self.characters.get_character("CLERIC"), Cleric)

    def test_get_character_fighter(self) -> None:
        self.assertIsInstance(self.characters.get_character("fighter"), Fighter)
        self.assertIsInstance(self.characters.get_character("FIGHTER"), Fighter)

    def test_get_character_rogue(self) -> None:
        self.assertIsInstance(self.characters.get_character("rogue"), Rogue)
        self.assertIsInstance(self.characters.get_character("ROGUE"), Rogue)

    def test_get_character_wizard(self) -> None:
        self.assertIsInstance(self.characters.get_character("wizard"), Wizard)
        self.assertIsInstance(self.characters.get_character("WIZARD"), Wizard)

    def test_get_character_wrong(self) -> None:
        self.assertIsNone(self.characters.get_character("ninja"))


class TestCharacter(unittest.TestCase):
    """Test the Character class and subclasses"""

    def setUp(self) -> None:
        self.characters = CharacterCollection()
        self.fighter = self.characters.get_character("fighter")

    def test_character_malformed(self) -> None:
        bad_character1 = {
            "name": "Fighter",
            "char": {"fighter": {"level": 1, "subclass": ""}},
        }
        bad_character2 = {"name": "Fighter", "race": "human"}
        with self.assertRaises(AttributeError):
            Character(bad_character1)
        with self.assertRaises(AttributeError):
            Character(bad_character2)

    def test_hp_max(self) -> None:
        self.assertEqual(self.fighter.hp_max, 12)


if __name__ == "__main__":
    unittest.main()
