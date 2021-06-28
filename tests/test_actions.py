import unittest
import sys
import os

p = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, p + "/../")

from dmai.domain.actions.attack import Attack
from dmai.game.game import Game
from dmai.game.state import State
from dmai.nlg.nlg import NLG
from dmai.utils.output_builder import OutputBuilder


class TestActions(unittest.TestCase):
    """Test the Actions class"""
    def setUp(self) -> None:
        self.game = Game(char_class="fighter", char_name="Xena", adventure="the_tomb_of_baradin_stormfury")
        self.game.load()
        NLG.set_game(self.game)
        self.actions = self.game.dm.actions

    def tearDown(self) -> None:
        State.extinguish_torch()
        
    def test_move_good_destination(self) -> None:
        entity = "player"
        destination = "inns_cellar"
        State.quest()
        moved = self.actions.move(entity, destination)
        self.assertEqual(moved, True)

    def test_move_bad_destination(self) -> None:
        entity = "player"
        destination = "the_moon"
        moved = self.actions.move(entity, destination)
        self.assertEqual(moved, False)

    def test_move_locked(self) -> None:
        OutputBuilder.clear()
        entity = "player"
        State.set_current_room(entity, "western_corridor")
        moved  = self.actions.move(entity, "storage_room")
        self.assertEqual(moved, False)
        self.assertEqual("You cannot move to Storage Room because the way is locked! You should figure out a way to get\nthrough or you could go to the Antechamber.\n", OutputBuilder.format())
        
    def test__can_move_must_kill_monsters(self) -> None:
        entity = "player"
        destination = "stout_meal_inn"
        State.set_current_room(entity, "inns_cellar")
        State.light_torch()
        (moved, reason) = self.actions._can_move(entity, destination)
        self.assertEqual(moved, False)
        self.assertEqual(reason, "must kill")
    
    def test__can_move_same_destination(self) -> None:
        entity = "player"
        destination = "stout_meal_inn"
        State.set_current_room(entity, destination)
        (moved, reason) = self.actions._can_move(entity, destination)
        self.assertEqual(moved, False)
        self.assertEqual(reason, "same")

    def test__can_move_no_quest(self) -> None:
        entity = "player"
        destination = "inns_cellar"
        State.set_current_room(entity, "stout_meal_inn")
        State.questing = False
        (moved, reason) = self.actions._can_move(entity, destination)
        self.assertEqual(moved, False)
        self.assertEqual(reason, "no quest")
        
    def test__can_move_no_visibility(self) -> None:
        entity = "player"
        destination = "stout_meal_inn"
        State.set_current_room(entity, "inns_cellar")
        State.extinguish_torch()
        (moved, reason) = self.actions._can_move(entity, destination)
        self.assertEqual(moved, False)
        self.assertEqual(reason, "no visibility")
        
    def test__can_move_locked(self) -> None:
        entity = "player"
        destination = "storage_room"
        State.set_current_room(entity, "burial_chamber")
        State.light_torch()
        State.quest()
        (moved, reason) = self.actions._can_move(entity, destination)
        self.assertEqual(moved, False)
        self.assertEqual(reason, "locked")
        
    def test__can_move_unrecognised_room(self) -> None:
        entity = "player"
        destination = "the moon"
        State.set_current_room(entity, "stout_meal_inn")
        State.quest()
        (moved, reason) = self.actions._can_move(entity, destination)
        self.assertEqual(moved, False)
        self.assertEqual(reason, "unknown destination")
    
    def test__can_move_unrecognised_entity(self) -> None:
        entity = "yoda"
        destination = "inns_cellar"
        (moved, reason) = self.actions._can_move(entity, destination)
        self.assertEqual(moved, False)
        self.assertEqual(reason, "unknown entity")

    def test__can_move_not_connected(self) -> None:
        entity = "player"
        destination = "antechamber"
        State.set_current_room(entity, "stout_meal_inn")
        State.quest()
        (moved, reason) = self.actions._can_move(entity, destination)
        self.assertEqual(moved, False)
        self.assertEqual(reason, "not connected")
        
    def test_attack_good_target(self) -> None:
        entity = "player"
        target = "giant_rat_1"
        State.quest()
        State.light_torch()
        self.actions.move(entity, "inns_cellar")
        attacked = self.actions.attack(entity, target)
        self.assertEqual(attacked, True)
    
    def test_attack_bad_target(self) -> None:
        entity = "player"
        target = "goblin_1"
        State.quest()
        self.actions.move(entity, "inns_cellar")
        attacked = self.actions.attack(entity, target)
        self.assertEqual(attacked, False)

    def test_use_good_equipment(self) -> None:
        entity = "player"
        equipment = "torch"
        used = self.actions.use(equipment=equipment, entity=entity)
        self.assertEqual(used, True)
    
    def test_use_bad_equipment(self) -> None:
        entity = "player"
        equipment = "computer"
        used = self.actions.use(equipment=equipment, entity=entity)
        self.assertEqual(used, False)
    
    def test_equip_good_weapon(self) -> None:
        entity = "player"
        weapon = "javelin"
        self.actions.unequip()
        equipped = self.actions.equip(weapon, entity)
        self.assertEqual(equipped, True)
    
    def test_equip_bad_weapon(self) -> None:
        entity = "player"
        weapon = "rubber_duck"
        self.actions.unequip()
        equipped = self.actions.equip(weapon, entity)
        self.assertEqual(equipped, False)

    def test_unequip_all(self) -> None:
        unequipped = self.actions.unequip()
        self.assertEqual(unequipped, True)

    def test_unequip_good_weapon(self) -> None:
        entity = "player"
        weapon = "greataxe"
        unequipped = self.actions.unequip(weapon, entity)
        self.assertEqual(unequipped, True)

    def test_unequip_good_weapon(self) -> None:
        entity = "player"
        weapon1 = "rubber_duck"
        weapon2 = "quarterstaff"
        unequipped = self.actions.unequip(weapon1, entity)
        self.assertEqual(unequipped, False)
        unequipped = self.actions.unequip(weapon2, entity)
        self.assertEqual(unequipped, False)
    
    def test_converse_good_target(self) -> None:
        target = "corvus"
        can_converse = self.actions.converse(target)
        self.assertEqual(can_converse, True)

    def test_converse_bad_target(self) -> None:
        target1 = "yoda"
        target2 = "anvil"
        can_converse = self.actions.converse(target1)
        self.assertEqual(can_converse, False)
        can_converse = self.actions.converse(target2)
        self.assertEqual(can_converse, False)

    def test_investigate_good_target(self) -> None:
        target = "corvus"
        can_converse = self.actions.investigate(target)
        self.assertEqual(can_converse, True)

    def test_investigate_bad_target(self) -> None:
        target1 = "yoda"
        target2 = "anvil"
        can_converse = self.actions.investigate(target1)
        self.assertEqual(can_converse, False)
        can_converse = self.actions.investigate(target2)
        self.assertEqual(can_converse, False)


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
