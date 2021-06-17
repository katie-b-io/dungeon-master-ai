from typing import Generator
import unittest
import sys
import os
import shutil

p = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, p + "/../")

from dmai.dm import DM
from dmai.game.game import Game
from dmai.game.state import State
from dmai.utils.config import Config
from dmai.nlg.nlg import NLG
from dmai.utils.output_builder import OutputBuilder


class TestDM(unittest.TestCase):
    """Test the DM class"""

    def setUp(self) -> None:
        self.game = Game(
            char_class="fighter",
            char_name="Xena",
            adventure="the_tomb_of_baradin_stormfury",
        )
        self.game.load()
        NLG.set_game(self.game)
        Config.set_uuid()
        Config.agent.set_player("planning")
        Config.planner.set_player("fd")
        self.dm = self.game.dm

    def tearDown(self) -> None:
        shutil.rmtree(Config.directory.planning)
        
    def test_init(self) -> None:
        self.assertIn("adventure", self.dm.__dict__)
        
    def test_input_utter_type(self) -> None:
        player_utter = ""
        utter_type1 = "start"
        utter_type2 = "name"
        self.assertEqual(True, self.dm.input(player_utter, utter_type=utter_type1))
        self.assertEqual(True, self.dm.input(player_utter, utter_type=utter_type2))

    def test_input_intent_good(self) -> None:
        player_utter = "talk to corvus"
        intent = "converse"
        kwargs = {"nlu_entities": [{"entity": "npc", "confidence": 1, "value": "corvus"}]}
        self.assertEqual(True, self.dm.input(player_utter, intent=intent, kwargs=kwargs))

    def test_input_intent_bad(self) -> None:
        player_utter = "start line dancing"
        intent = "line_dancing"
        with self.assertRaises(KeyError):
            self.dm.input(player_utter, intent=intent)

    def test_output(self) -> None:
        self.dm.input("", utter_type="test")
        OutputBuilder.clear()
        self.dm.input("", utter_type="test")
        utter = "Xena, what do you do?\n"
        self.assertEqual(utter, self.dm.output)

    def test_register_trigger(self) -> None:
        class _trigger(): pass
        self.dm.triggers = []
        self.dm.register_trigger(_trigger)
        self.assertListEqual([_trigger], self.dm.triggers)

    def test_deregister_trigger(self) -> None:
        trigger = self.dm.triggers[0]
        self.dm.deregister_trigger(trigger)
        self.assertListEqual([], self.dm.triggers)

    def test_get_intro_text(self) -> None:
        intro = self.dm.get_intro_text()
        text = "Greyforge, the mountain city in the north of the Kaldarian lands is home to the proud dwarves who settled in the area over 8,000 years ago, led by a silver dragon, according to some stories."
        self.assertIsInstance(intro, Generator)
        self.assertEqual(next(intro), text)

    def test_hint(self) -> None:
        self.dm.input("", utter_type="test")
        self.assertEqual(True, self.dm.hint())

    def test__get_destination(self) -> None:
        nlu_entities = [{"entity": "location", "confidence": 1, "value": "inns_cellar"}]
        self.assertEqual("inns_cellar", self.dm._get_destination(nlu_entities))

    def test__get_target_npc(self) -> None:
        nlu_entities = [{"entity": "npc", "confidence": 1, "value": "corvus"}]
        self.assertEqual("corvus", self.dm._get_target(nlu_entities))

    def test__get_target_monster_wrong_location(self) -> None:
        nlu_entities = [{"entity": "monster", "confidence": 1, "value": "giant_rat"}]
        self.assertEqual(None, self.dm._get_target(nlu_entities))

    def test__get_target_monster_right_location(self) -> None:
        State.set_current_room("player", "inns_cellar")
        nlu_entities = [{"entity": "monster", "confidence": 1, "value": "giant_rat"}]
        self.assertEqual("giant_rat_1", self.dm._get_target(nlu_entities))
        
    def test__get_npc(self) -> None:
        self.assertEqual("corvus", self.dm._get_npc())

    def test__get_equipment(self) -> None:
        nlu_entities = [{"entity": "equipment", "confidence": 1, "value": "torch"}]
        self.assertEqual("torch", self.dm._get_equipment(nlu_entities))

    def test__get_weapon(self) -> None:
        nlu_entities = [{"entity": "weapon", "confidence": 1, "value": "greataxe"}]
        self.assertEqual("greataxe", self.dm._get_weapon(nlu_entities))

    def test_move_destination_good(self) -> None:
        State.quest()
        self.assertEqual(True, self.dm.move(destination="inns_cellar"))

    def test_move_destination_bad(self) -> None:
        State.quest()
        self.assertEqual(False, self.dm.move(destination="the_moon"))

    def test_move_nlu_entities_good(self) -> None:
        State.quest()
        nlu_entities = [{"entity": "location", "confidence": 1, "value": "inns_cellar"}]
        self.assertEqual(True, self.dm.move(nlu_entities=nlu_entities))

    def test_move_nlu_entities_bad(self) -> None:
        State.quest()
        nlu_entities = [{"entity": "location", "confidence": 1, "value": "the_moon"}]
        self.assertEqual(False, self.dm.move(nlu_entities=nlu_entities))
        
    def test_attack_target_npc(self) -> None:
        State.set_current_room("player", "inns_cellar")
        self.assertEqual(True, self.dm.attack(target="anvil"))
    
    def test_attack_target_npc_gameover(self) -> None:
        State.set_current_room("player", "stout_meal_inn")
        with self.assertRaises(SystemExit):
            self.dm.attack(target="corvus")

    def test_attack_target_monster(self) -> None:
        State.set_current_room("player", "inns_cellar")
        self.assertEqual(True, self.dm.attack(target="giant_rat_1"))

    def test_attack_target_bad(self) -> None:
        self.assertEqual(False, self.dm.attack(target="anvil"))
        self.assertEqual(False, self.dm.attack(target="goblin_1"))
        self.assertEqual(False, self.dm.attack(target="yoda"))
    
    def test_attack_nlu_entities_npc_good(self) -> None:
        State.set_current_room("player", "inns_cellar")
        nlu_entities = [{"entity": "npc", "confidence": 1, "value": "anvil"}]
        self.assertEqual(True, self.dm.attack(nlu_entities=nlu_entities))
    
    def test_attack_nlu_entities_monster_good(self) -> None:
        State.set_current_room("player", "inns_cellar")
        nlu_entities = [{"entity": "monster", "confidence": 1, "value": "giant_rat"}]
        self.assertEqual(True, self.dm.attack(nlu_entities=nlu_entities))
    
    def test_attack_nlu_entities_monster_bad(self) -> None:
        nlu_entities1 = [{"entity": "npc", "confidence": 1, "value": "yoda"}]
        nlu_entities2 = [{"entity": "monster", "confidence": 1, "value": "yoda"}]
        self.assertEqual(False, self.dm.attack(nlu_entities=nlu_entities1))
        self.assertEqual(False, self.dm.attack(nlu_entities=nlu_entities2))
        
    def test_use_equipment_good(self) -> None:
        self.assertEqual(True, self.dm.use(equipment="torch"))

    def test_use_equipment_bad(self) -> None:
        self.assertEqual(False, self.dm.use(equipment="thieves_tools"))
        self.assertEqual(False, self.dm.use(equipment="rubber_duck"))
    
    def test_use_nlu_entities_good(self) -> None:
        nlu_entities = [{"entity": "equipment", "confidence": 1, "value": "torch"}]
        self.assertEqual(True, self.dm.use(nlu_entities=nlu_entities))

    def test_use_nlu_entities_bad(self) -> None:
        nlu_entities1 = [{"entity": "equipment", "confidence": 1, "value": "thieves_tools"}]
        nlu_entities2 = [{"entity": "equipment", "confidence": 1, "value": "rubber_duck"}]
        self.assertEqual(False, self.dm.use(nlu_entities=nlu_entities1))
        self.assertEqual(False, self.dm.use(nlu_entities=nlu_entities2))
        
    def test_stop_using_equipment_good(self) -> None:
        State.torch_lit = False
        self.assertEqual(False, self.dm.stop_using(equipment="torch"))
        self.dm.use(equipment="torch")
        self.assertEqual(True, self.dm.stop_using(equipment="torch"))

    def test_stop_using_equipment_bad(self) -> None:
        self.assertEqual(False, self.dm.stop_using(equipment="thieves_tools"))
        self.assertEqual(False, self.dm.stop_using(equipment="rubber_duck"))
    
    def test_stop_using_nlu_entities_good(self) -> None:
        nlu_entities = [{"entity": "equipment", "confidence": 1, "value": "torch"}]
        self.assertEqual(False, self.dm.stop_using(nlu_entities=nlu_entities))
        self.dm.use(equipment="torch")
        self.assertEqual(True, self.dm.stop_using(nlu_entities=nlu_entities))

    def test_stop_using_nlu_entities_bad(self) -> None:
        nlu_entities1 = [{"entity": "equipment", "confidence": 1, "value": "thieves_tools"}]
        nlu_entities2 = [{"entity": "equipment", "confidence": 1, "value": "rubber_duck"}]
        self.assertEqual(False, self.dm.stop_using(nlu_entities=nlu_entities1))
        self.assertEqual(False, self.dm.stop_using(nlu_entities=nlu_entities2))
        
    def test_equip_weapon_good(self) -> None:
        self.dm.unequip()
        self.assertEqual(True, self.dm.equip(weapon="javelin"))
        self.assertEqual(True, self.dm.equip(weapon="javelin"))
        self.dm.unequip()
        self.assertEqual(True, self.dm.equip(weapon="greataxe"))

    def test_equip_weapon_bad(self) -> None:
        self.assertEqual(False, self.dm.equip(weapon="greataxe"))
        self.assertEqual(False, self.dm.equip(weapon="quarterstaff"))
        self.assertEqual(False, self.dm.equip(weapon="rubber_duck"))
    
    def test_equip_nlu_entities_good(self) -> None:
        self.dm.unequip()
        nlu_entities = [{"entity": "weapon", "confidence": 1, "value": "javelin"}]
        self.assertEqual(True, self.dm.equip(nlu_entities=nlu_entities))
        self.dm.unequip()
        nlu_entities = [{"entity": "weapon", "confidence": 1, "value": "greataxe"}]
        self.assertEqual(True, self.dm.equip(nlu_entities=nlu_entities))
        
    def test_equip_nlu_entities_bad(self) -> None:
        nlu_entities1 = [{"entity": "weapon", "confidence": 1, "value": "greataxe"}]
        nlu_entities2 = [{"entity": "weapon", "confidence": 1, "value": "quarterstaff"}]
        nlu_entities3 = [{"entity": "weapon", "confidence": 1, "value": "rubber_duck"}]
        self.assertEqual(False, self.dm.equip(nlu_entities=nlu_entities1))
        self.assertEqual(False, self.dm.equip(nlu_entities=nlu_entities2))
        self.assertEqual(False, self.dm.equip(nlu_entities=nlu_entities3))

    def test_unequip_weapon_good(self) -> None:
        self.assertEqual(True, self.dm.unequip())
        self.dm.equip(weapon="greataxe")
        self.assertEqual(True, self.dm.unequip(weapon="greataxe"))

    def test_unequip_weapon_bad(self) -> None:
        self.assertEqual(False, self.dm.unequip(weapon="javelin"))
        self.assertEqual(False, self.dm.unequip(weapon="quarterstaff"))
        self.assertEqual(False, self.dm.unequip(weapon="rubber_duck"))
    
    def test_unequip_nlu_entities_good(self) -> None:
        nlu_entities = [{"entity": "weapon", "confidence": 1, "value": "greataxe"}]
        self.assertEqual(True, self.dm.unequip(nlu_entities=nlu_entities))
        self.dm.equip(weapon="javelin")
        nlu_entities = [{"entity": "weapon", "confidence": 1, "value": "javelin"}]
        self.assertEqual(True, self.dm.unequip(nlu_entities=nlu_entities))
        
    def test_unequip_nlu_entities_bad(self) -> None:
        nlu_entities1 = [{"entity": "weapon", "confidence": 1, "value": "javelin"}]
        nlu_entities2 = [{"entity": "weapon", "confidence": 1, "value": "quarterstaff"}]
        nlu_entities3 = [{"entity": "weapon", "confidence": 1, "value": "rubber_duck"}]
        self.assertEqual(False, self.dm.unequip(nlu_entities=nlu_entities1))
        self.assertEqual(False, self.dm.unequip(nlu_entities=nlu_entities2))
        self.assertEqual(False, self.dm.unequip(nlu_entities=nlu_entities3))

    def test_converse_target_good(self) -> None:
        State.set_current_room("player", "stout_meal_inn")
        self.assertEqual(True, self.dm.converse(target="corvus"))

    def test_converse_target_bad(self) -> None:
        State.set_current_room("player", "stout_meal_inn")
        self.assertEqual(False, self.dm.converse(target="anvil"))
        self.assertEqual(False, self.dm.converse(target="yoda"))
    
    def test_converse_nlu_entities_good(self) -> None:
        State.set_current_room("player", "stout_meal_inn")
        nlu_entities = [{"entity": "npc", "confidence": 1, "value": "corvus"}]
        self.assertEqual(True, self.dm.converse(nlu_entities=nlu_entities))

    def test_converse_nlu_entities_bad(self) -> None:
        State.set_current_room("player", "stout_meal_inn")
        nlu_entities1 = [{"entity": "npc", "confidence": 1, "value": "anvil"}]
        nlu_entities2 = [{"entity": "unknown", "confidence": 1, "value": "yoda"}]
        self.assertEqual(False, self.dm.converse(nlu_entities=nlu_entities1))
        self.assertEqual(False, self.dm.converse(nlu_entities=nlu_entities2))

    def test_affirm(self) -> None:
        State.roleplay("corvus")
        State.received_quest()
        self.dm.affirm()
        self.assertEqual(True, State.questing)

    def test_deny_gameover(self) -> None:
        State.roleplay("corvus")
        State.received_quest()
        State.questing = False
        with self.assertRaises(SystemExit):
            self.dm.deny()

    def test_explore_target_good(self) -> None:
        State.set_current_room("player", "stout_meal_inn")
        self.assertEqual(True, self.dm.explore(target="corvus"))

    def test_explore_target_bad(self) -> None:
        State.set_current_room("player", "stout_meal_inn")
        self.assertEqual(False, self.dm.explore(target="anvil"))
        self.assertEqual(False, self.dm.explore(target="yoda"))
    
    def test_explore_nlu_entities_good(self) -> None:
        State.set_current_room("player", "stout_meal_inn")
        nlu_entities = [{"entity": "npc", "confidence": 1, "value": "corvus"}]
        self.assertEqual(True, self.dm.explore(nlu_entities=nlu_entities))

    def test_explore_nlu_entities_bad(self) -> None:
        State.set_current_room("player", "stout_meal_inn")
        nlu_entities1 = [{"entity": "npc", "confidence": 1, "value": "anvil"}]
        nlu_entities2 = [{"entity": "npc", "confidence": 1, "value": "yoda"}]
        nlu_entities3 = [{"entity": "monster", "confidence": 1, "value": "goblin"}, {"entity": "id", "confidence": 1, "value": 2}]
        self.assertEqual(False, self.dm.explore(nlu_entities=nlu_entities1))
        self.assertEqual(False, self.dm.explore(nlu_entities=nlu_entities2))
        self.assertEqual(False, self.dm.explore(nlu_entities=nlu_entities3))
        
    def test_explore_monster_different_room(self) -> None:
        nlu_entities4 = [{"entity": "monster", "confidence": 1, "value": "zombie"}]
        self.assertEqual(True, self.dm.explore(nlu_entities=nlu_entities4))
        

if __name__ == "__main__":
    unittest.main()
