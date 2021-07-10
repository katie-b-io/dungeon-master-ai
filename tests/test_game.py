from typing import Generator
import unittest
import sys
import os

p = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, p + "/../")

from dmai.game.state import State
from dmai.utils.output_builder import OutputBuilder
from dmai.game.npcs.npc import NPC
from dmai.domain.monsters.monster_collection import MonsterCollection
from dmai.domain.monsters.skeleton import Skeleton
from dmai.game.adventure import Adventure
from dmai.game.game import Game
from dmai.game.npcs.npc_collection import NPCCollection
from dmai.utils.exceptions import UnrecognisedEntityError, UnrecognisedRoomError, RoomConnectionError


class TestGame(unittest.TestCase):
    """Test the Game class"""
    def setUp(self) -> None:
        self.game = Game(char_class="fighter", char_name="Xena", adventure="the_tomb_of_baradin_stormfury")
        self.game.load()
    


class TestState(unittest.TestCase):
    """Test the State class"""
    def setUp(self) -> None:
        self.game = Game(char_class="fighter", char_name="Xena", adventure="the_tomb_of_baradin_stormfury")
        self.game.load()
        self.adventure = self.game.dm.adventure

    def test_save_state(self) -> None:
        self.game.state.light_torch()
        self.game.state.set_current_room("player", "antechamber")
        saved_state = self.game.state.save()
        self.assertIn("torch_lit", saved_state)
        self.assertEqual("Fighter", saved_state["char_class"])
    
    def test_load_state(self) -> None:
        saved_state = {
            "paused": True,
            "char_class": "Fighter",
            "started": True,
            "char_name": "Xena",
            "torch_lit": True,
            "current_room": {"player": "western_corridor"}
        }
        self.game.state.load(saved_state)
        self.assertEqual("western_corridor", self.game.state.get_current_room_id())

    def test_get_room_name(self) -> None:
        room = "burial_chamber"
        self.assertEqual("Burial Chamber", self.game.state.get_room_name(room))
    
    def test_get_room_name_malformed(self) -> None:
        room = "the bar"
        with self.assertRaises(UnrecognisedRoomError):
            self.game.state.get_room_name(room)

    def test__check_room_exists(self) -> None:
        room = "burial_chamber"
        self.assertEqual(True, self.game.state.check_room_exists(room))

    def test__check_room_exists_malformed(self) -> None:
        room1 = "the bar"
        room2 = "moon"
        with self.assertRaises(UnrecognisedRoomError):
            self.game.state.check_room_exists(room1)
        with self.assertRaises(UnrecognisedRoomError):
            self.game.state.check_room_exists(room2)

    def test_get_current_room_player(self) -> None:
        entity = "player"
        room = self.adventure.get_room("stout_meal_inn")
        self.assertEqual(room, self.game.state.get_current_room(entity))

    def test_get_current_room_malformed(self) -> None:
        entity = "yoda"
        with self.assertRaises(UnrecognisedEntityError):
            self.game.state.get_current_room(entity)

    def test_set_current_room_player(self) -> None:
        entity = "player"
        room_id = "inns_cellar"
        room = self.adventure.get_room(room_id)
        self.game.state.set_current_room(entity, room_id)
        self.assertEqual(room, self.game.state.get_current_room(entity))

    def test_set_current_room_malformed_room(self) -> None:
        entity = "player"
        room_id = "the_moon"
        with self.assertRaises(UnrecognisedRoomError):
            self.game.state.set_current_room(entity, room_id)

    def test_set_current_room_malformed_room(self) -> None:
        entity = "yoda"
        room_id = "inns_cellar"
        with self.assertRaises(UnrecognisedEntityError):
            self.game.state.set_current_room(entity, room_id)

    def test_get_current_room_id_player(self) -> None:
        entity = "player"
        room = "stout_meal_inn"
        self.assertEqual(room, self.game.state.get_current_room_id(entity))

    def test_get_current_room_id_malformed(self) -> None:
        entity = "yoda"
        with self.assertRaises(UnrecognisedEntityError):
            self.game.state.get_current_room_id(entity)

    def test_travel_allowed(self) -> None:
        current = "stout_meal_inn"
        destination = "inns_cellar"
        self.assertEqual(True, self.game.state.travel_allowed(current, destination))

    def test_travel_allowed_broken_door(self) -> None:
        current = "storage_room"
        destination = "burial_chamber"
        self.game.state.break_door(current, destination)
        self.assertEqual(True, self.game.state.travel_allowed(current, destination))

    def test_travel_allowed_not_connected(self) -> None:
        current = "stout_meal_inn"
        destination = "antechamber"
        self.assertEqual(False, self.game.state.travel_allowed(current, destination))

    def test_travel_allowed_malformed_destination(self) -> None:
        current = "stout_meal_inn"
        destination1 = "the_moon"
        destination2 = "the"
        with self.assertRaises(UnrecognisedRoomError):
            self.game.state.travel_allowed(current, destination1)
        with self.assertRaises(UnrecognisedRoomError):
            self.game.state.travel_allowed(current, destination2)

    def test_travel_allowed_malformed_current(self) -> None:
        current = "the_moon"
        destination = "inns_cellar"
        with self.assertRaises(UnrecognisedRoomError):
            self.game.state.travel_allowed(current, destination)

    def test_lock_no_connection(self) -> None:
        room1 = "stout_meal_inn"
        room2 = "antechamber"
        with self.assertRaises(RoomConnectionError):
            self.game.state.lock_door(room1, room2)

    def test_unlock_door_no_connection(self) -> None:
        room1 = "stout_meal_inn"
        room2 = "antechamber"
        with self.assertRaises(RoomConnectionError):
            self.game.state.unlock_door(room1, room2)

    def test_break_door_no_connection(self) -> None:
        room1 = "stout_meal_inn"
        room2 = "antechamber"
        with self.assertRaises(RoomConnectionError):
            self.game.state.break_door(room1, room2)

    def test_lock_door_malformed(self) -> None:
        room1 = "stout_meal_inn"
        room2 = "the_moon"
        with self.assertRaises(UnrecognisedRoomError):
            self.game.state.lock_door(room1, room2)

    def test_unlock_door_malformed(self) -> None:
        room1 = "stout_meal_inn"
        room2 = "the_moon"
        with self.assertRaises(UnrecognisedRoomError):
            self.game.state.unlock_door(room1, room2)

    def test_break_door_malformed(self) -> None:
        room1 = "stout_meal_inn"
        room2 = "the_moon"
        with self.assertRaises(UnrecognisedRoomError):
            self.game.state.break_door(room1, room2)
    
    def test_get_formatted_possible_monster_targets(self) -> None:
        entity = "player"
        self.game.state.set_current_room(entity, "inns_cellar")
        self.game.state.light_torch()
        self.assertEqual(self.game.state.get_formatted_possible_monster_targets(entity), "You could attack Giant Rat 1 or Giant Rat 2.")


class TestAdventure(unittest.TestCase):
    """Test the Adventure class"""
    def setUp(self) -> None:
        self.game = Game(char_class="fighter", char_name="Xena", adventure="the_tomb_of_baradin_stormfury")
        self.game.load()
        self.adventure = self.game.dm.adventure

    def test_get_init_room(self) -> None:
        room = "stout_meal_inn"
        self.assertEqual(room, self.adventure.get_init_room())

    def test_get_room(self) -> None:
        room = "inns_cellar"
        self.assertEqual(self.adventure.get_room(room),
                         self.adventure.rooms[room])

    def test_get_room_malformed(self) -> None:
        room = "the"
        with self.assertRaises(UnrecognisedRoomError):
            self.adventure.get_room(room)
    
    def test_get_all_rooms(self) -> None:
        room_ids = ["stout_meal_inn", "inns_cellar", "storage_room", "burial_chamber", "western_corridor", "antechamber", "southern_corridor", "baradins_crypt"]
        rooms = self.adventure.get_all_rooms()
        self.assertListEqual(room_ids, [room.id for room in rooms])
    
    def test_get_intro_text_generator(self) -> None:
        intro = self.adventure.intro_text_generator()
        text = "Greyforge, the mountain city in the north of the Kaldarian lands is home to the proud dwarves who settled in the area over 8,000 years ago, led by a silver dragon, according to some stories."
        self.assertIsInstance(intro, Generator)
        self.assertEqual(next(intro), text)

class TestNPCCollection(unittest.TestCase):
    """Test the NPCCollection class"""
    def setUp(self) -> None:
        self.output_builder = OutputBuilder()
        self.state = State(self.output_builder)
        self.adventure = Adventure("the_tomb_of_baradin_stormfury", self.state, self.output_builder)
        self.npc_collection = NPCCollection(self.adventure, self.state, self.output_builder)
        MonsterCollection.load()
    
    def test__create_npcs(self) -> None:
        npcs = self.npc_collection._create_npcs()
        self.assertListEqual(["corvus", "anvil"], [npc for npc in npcs])
    
    def test__create_monsters(self) -> None:
        monsters = self.npc_collection._create_monsters()
        self.assertListEqual(["giant_rat_1", "giant_rat_2", "zombie_1", "goblin_1", "skeleton_1", "goblin_2", "goblin_3"], [m for m in monsters])
    
    def test_get_type(self) -> None:
        self.npc_collection.load()
        self.assertEqual(self.npc_collection.get_type("corvus"), "npc")
        self.assertEqual(self.npc_collection.get_type("goblin_2"), "monster")
        self.assertIsNone(self.npc_collection.get_type("yoda"))

    def test_get_entity(self) -> None:
        self.npc_collection.load()
        self.assertIsInstance(self.npc_collection.get_entity("corvus"), NPC)
        self.assertEqual(self.npc_collection.get_entity("corvus").long_name, "Corvus Stouthammer")
        self.assertIsInstance(self.npc_collection.get_entity("skeleton_1"), Skeleton)
        self.assertEqual(self.npc_collection.get_entity("skeleton_1").name, "Skeleton")
        with self.assertRaises(UnrecognisedEntityError):
            self.npc_collection.get_npc("yoda")
        
    def test_get_npc(self) -> None:
        self.npc_collection.load()
        self.assertIsInstance(self.npc_collection.get_npc("corvus"), NPC)
        self.assertEqual(self.npc_collection.get_npc("corvus").long_name, "Corvus Stouthammer")
        with self.assertRaises(UnrecognisedEntityError):
            self.npc_collection.get_npc("yoda")

    def test_get_monster(self) -> None:
        self.npc_collection.load()
        self.assertIsInstance(self.npc_collection.get_monster("skeleton_1"), Skeleton)
        self.assertEqual(self.npc_collection.get_monster("skeleton_1").name, "Skeleton")
        with self.assertRaises(UnrecognisedEntityError):
            self.npc_collection.get_monster("yoda")

    def test_get_monster_id(self) -> None:
        self.npc_collection.load()
        monster_1 = self.npc_collection.get_monster_id(monster_type="giant_rat", status="alive", location="inns_cellar")
        monster_2 = self.npc_collection.get_monster_id(monster_type="goblin", location="antechamber")
        monster_3 = self.npc_collection.get_monster_id(monster_type="goblin", status="dead")
        monster_4 = self.npc_collection.get_monster_id(monster_type="skeleton")
        self.assertEqual(monster_1, "giant_rat_1")
        self.assertEqual(monster_2, "goblin_2")
        self.assertEqual(monster_3, "goblin_1")
        self.assertEqual(monster_4, "skeleton_1")

    def test_get_all_npcs(self) -> None:
        self.npc_collection.load()
        npcs = self.npc_collection.get_all_npcs()
        self.assertListEqual(["corvus", "anvil"], [npc.id for npc in npcs])

    def test_get_all_npc_ids(self) -> None:
        self.npc_collection.load()
        npcs = self.npc_collection.get_all_npc_ids()
        self.assertListEqual(["corvus", "anvil"], [npc for npc in npcs])

    def test_get_all_monsters(self) -> None:
        self.npc_collection.load()
        monsters = self.npc_collection.get_all_monsters()
        self.assertListEqual(["giant_rat_1", "giant_rat_2", "zombie_1", "goblin_1", "skeleton_1", "goblin_2", "goblin_3"], [m.unique_id for m in monsters])

    def test_get_all_monster_ids(self) -> None:
        self.npc_collection.load()
        monsters = self.npc_collection.get_all_monster_ids()
        self.assertListEqual(["giant_rat_1", "giant_rat_2", "zombie_1", "goblin_1", "skeleton_1", "goblin_2", "goblin_3"], [m for m in monsters])
    

if __name__ == "__main__":
    unittest.main()
