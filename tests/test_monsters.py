import unittest
import sys
import os

p = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, p + "/../")

from dmai.domain.monsters.monster import Monster
from dmai.domain.monsters.monster_collection import MonsterCollection
from dmai.domain.monsters.cat import Cat
from dmai.domain.monsters.giant_rat import GiantRat
from dmai.domain.monsters.goblin import Goblin
from dmai.domain.monsters.skeleton import Skeleton
from dmai.domain.monsters.zombie import Zombie


class TestMonsterCollection(unittest.TestCase):
    """Test the MonsterCollection class"""
    def setUp(self) -> None:
        self.monsters = MonsterCollection()
        self.monsters.load()

    def test_monster_factory_error(self) -> None:
        with self.assertRaises(ValueError):
            self.monsters._monster_factory("human")

    def test_get_monster_cat(self) -> None:
        self.assertIsInstance(self.monsters.get_monster("cat", "cat_1"), Cat)
        self.assertIsInstance(self.monsters.get_monster("CAT", "cat_1"), Cat)

    def test_get_monster_giant_rat(self) -> None:
        self.assertIsInstance(self.monsters.get_monster("giant_rat", "giant_rat_1"), GiantRat)
        self.assertIsInstance(self.monsters.get_monster("GIANT_RAT", "giant_rat_1"), GiantRat)

    def test_get_monster_goblin(self) -> None:
        self.assertIsInstance(self.monsters.get_monster("goblin", "goblin_1"), Goblin)
        self.assertIsInstance(self.monsters.get_monster("GOBLIN", "goblin_1"), Goblin)

    def test_get_monster_skeleton(self) -> None:
        self.assertIsInstance(self.monsters.get_monster("skeleton", "skeleton_1"), Skeleton)
        self.assertIsInstance(self.monsters.get_monster("SKELETON", "skeleton_1"), Skeleton)

    def test_get_monster_zombie(self) -> None:
        self.assertIsInstance(self.monsters.get_monster("zombie", "zombie_1"), Zombie)
        self.assertIsInstance(self.monsters.get_monster("ZOMBIE", "zombie_1"), Zombie)

    def test_get_monster_wrong(self) -> None:
        self.assertIsNone(self.monsters.get_monster("human", "human_1"))


class TestMonster(unittest.TestCase):
    """Test the Monster class and subclasses"""
    def setUp(self) -> None:
        self.monsters = MonsterCollection()

    def test_monster_malformed(self) -> None:
        bad_monster1 = {
            "id": "cat",
            "name": "Cat",
            "type": "beast",
            "abilitie": {}
        }
        bad_monster2 = {"id": "cat", "name": "Cat", "type": "beast"}
        with self.assertRaises(AttributeError):
            Monster(bad_monster1, unique_name="Cat 1")
        with self.assertRaises(AttributeError):
            Monster(bad_monster2, unique_name="Cat 1")


if __name__ == "__main__":
    unittest.main()
