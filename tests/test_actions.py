import unittest
import sys
import os

p = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, p + "/../")

from dmai.domain.actions.attack import Attack
from dmai.game.game import Game
from dmai.game.state import State
from dmai.nlg.nlg import NLG


class TestAttack(unittest.TestCase):
    """Test the Attack class"""
    def setUp(self) -> None:
        self.game = Game(char_class="fighter", char_name="Xena", adventure="the_tomb_of_baradin_stormfury")
        self.game.load()
        NLG.set_game(self.game)
    
    def test__can_attack_unknown_target(self) -> None:
        entity = "player"
        target = "yoda"
        State.set_current_room(entity, "inns_cellar")
        attack = Attack(entity, target)
        (attacked, reason) = attack._can_attack()
        self.assertEqual(attacked, False)
        self.assertEqual(reason, "unknown target")
    
    def test__can_attack_different_location(self) -> None:
        entity = "player"
        target = "zombie_1"
        State.set_current_room(entity, "inns_cellar")
        State.extinguish_torch()
        attack = Attack(entity, target)
        (attacked, reason) = attack._can_attack()
        self.assertEqual(attacked, False)
        self.assertEqual(reason, "different location")
        
    def test__can_attack_no_visibility(self) -> None:
        entity = "player"
        target = "giant_rat_1"
        State.set_current_room(entity, "inns_cellar")
        State.extinguish_torch()
        attack = Attack(entity, target)
        (attacked, reason) = attack._can_attack()
        self.assertEqual(attacked, False)
        self.assertEqual(reason, "no visibility")


if __name__ == "__main__":
    unittest.main()
