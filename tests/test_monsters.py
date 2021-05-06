import unittest
import sys
import os

p = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, p + "/../")

from dmai.domain.monsters import (
    Monster,
    MonsterCollection,
    Cat,
    GiantRat,
    Goblin,
    Skeleton,
    Zombie,
)


class TestMonsterCollection(unittest.TestCase):
    """Test the MonsterCollection class"""

    def setUp(self) -> None:
        self.monsters = MonsterCollection()

    def test_monster_factory_error(self) -> None:
        with self.assertRaises(ValueError):
            self.monsters._monster_factory("human")

    def test_get_monster_cat(self) -> None:
        self.assertIsInstance(self.monsters.get_monster("cat"), Cat)
        self.assertIsInstance(self.monsters.get_monster("CAT"), Cat)

    def test_get_monster_giant_rat(self) -> None:
        self.assertIsInstance(self.monsters.get_monster("giant_rat"), GiantRat)
        self.assertIsInstance(self.monsters.get_monster("GIANT_RAT"), GiantRat)

    def test_get_monster_goblin(self) -> None:
        self.assertIsInstance(self.monsters.get_monster("goblin"), Goblin)
        self.assertIsInstance(self.monsters.get_monster("GOBLIN"), Goblin)

    def test_get_monster_skeleton(self) -> None:
        self.assertIsInstance(self.monsters.get_monster("skeleton"), Skeleton)
        self.assertIsInstance(self.monsters.get_monster("SKELETON"), Skeleton)

    def test_get_monster_zombie(self) -> None:
        self.assertIsInstance(self.monsters.get_monster("zombie"), Zombie)
        self.assertIsInstance(self.monsters.get_monster("ZOMBIE"), Zombie)

    def test_get_monster_wrong(self) -> None:
        self.assertIsNone(self.monsters.get_monster("human"))


class TestMonster(unittest.TestCase):
    """Test the Monster class and subclasses"""

    def setUp(self) -> None:
        self.monsters = MonsterCollection()
        self.cat = self.monsters.get_monster("cat")

    def test_monster_malformed(self) -> None:
        bad_monster1 = {"name": "Cat", "type": "beast", "abilitie": {}}
        bad_monster2 = {"name": "Cat", "type": "beast"}
        with self.assertRaises(AttributeError):
            Monster(bad_monster1)
        with self.assertRaises(AttributeError):
            Monster(bad_monster2)


if __name__ == "__main__":
    unittest.main()
