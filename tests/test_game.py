import unittest
import sys
import os

p = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, p + "/../")

from dmai.game.npcs.npc import NPC
from dmai.domain.monsters.monster_collection import MonsterCollection
from dmai.domain.monsters.skeleton import Skeleton
from dmai.domain.monsters.giant_rat import GiantRat
from dmai.game.adventure import Adventure
from dmai.game.state import State
from dmai.game.game import Game
from dmai.game.npcs.npc_collection import NPCCollection
from dmai.utils.exceptions import UnrecognisedEntityError, UnrecognisedRoomError, RoomConnectionError


class TestState(unittest.TestCase):
    """Test the State class"""
    def setUp(self) -> None:
        self.game = Game(char_class="fighter", char_name="Xena", adventure="the_tomb_of_baradin_stormfury")
        self.game.load()
        self.adventure = self.game.dm.adventure

    def test_get_room_name(self) -> None:
        room = "burial_chamber"
        self.assertEqual("Burial Chamber", State.get_room_name(room))
    
    def test_get_room_name_malformed(self) -> None:
        room = "the bar"
        with self.assertRaises(UnrecognisedRoomError):
            State.get_room_name(room)

    def test__check_room_exists(self) -> None:
        room = "burial_chamber"
        self.assertEqual(True, State._check_room_exists(room))

    def test__check_room_exists_malformed(self) -> None:
        room1 = "the bar"
        room2 = "moon"
        with self.assertRaises(UnrecognisedRoomError):
            State._check_room_exists(room1)
        with self.assertRaises(UnrecognisedRoomError):
            State._check_room_exists(room2)

    def test_get_current_room_player(self) -> None:
        entity = "player"
        room = self.adventure.get_room("stout_meal_inn")
        self.assertEqual(room, State.get_current_room(entity))

    def test_get_current_room_malformed(self) -> None:
        entity = "yoda"
        with self.assertRaises(UnrecognisedEntityError):
            State.get_current_room(entity)

    def test_set_current_room_player(self) -> None:
        entity = "player"
        room_id = "inns_cellar"
        room = self.adventure.get_room(room_id)
        State.set_current_room(entity, room_id)
        self.assertEqual(room, State.get_current_room(entity))

    def test_set_current_room_malformed_room(self) -> None:
        entity = "player"
        room_id = "the_moon"
        with self.assertRaises(UnrecognisedRoomError):
            State.set_current_room(entity, room_id)

    def test_set_current_room_malformed_room(self) -> None:
        entity = "yoda"
        room_id = "inns_cellar"
        with self.assertRaises(UnrecognisedEntityError):
            State.set_current_room(entity, room_id)

    def test_get_current_room_id_player(self) -> None:
        entity = "player"
        room = "stout_meal_inn"
        self.assertEqual(room, State.get_current_room_id(entity))

    def test_get_current_room_id_malformed(self) -> None:
        entity = "yoda"
        with self.assertRaises(UnrecognisedEntityError):
            State.get_current_room_id(entity)

    def test_travel_allowed(self) -> None:
        current = "stout_meal_inn"
        destination = "inns_cellar"
        self.assertEqual(True, State.travel_allowed(current, destination))

    def test_travel_allowed_broken_door(self) -> None:
        current = "storage_room"
        destination = "burial_chamber"
        State.break_door(current, destination)
        self.assertEqual(True, State.travel_allowed(current, destination))

    def test_travel_allowed_not_connected(self) -> None:
        current = "stout_meal_inn"
        destination = "antechamber"
        self.assertEqual(False, State.travel_allowed(current, destination))

    def test_travel_allowed_malformed_destination(self) -> None:
        current = "stout_meal_inn"
        destination1 = "the_moon"
        destination2 = "the"
        with self.assertRaises(UnrecognisedRoomError):
            State.travel_allowed(current, destination1)
        with self.assertRaises(UnrecognisedRoomError):
            State.travel_allowed(current, destination2)

    def test_travel_allowed_malformed_current(self) -> None:
        current = "the_moon"
        destination = "inns_cellar"
        with self.assertRaises(UnrecognisedRoomError):
            State.travel_allowed(current, destination)

    def test_lock_no_connection(self) -> None:
        room1 = "stout_meal_inn"
        room2 = "antechamber"
        with self.assertRaises(RoomConnectionError):
            State.lock_door(room1, room2)

    def test_unlock_door_no_connection(self) -> None:
        room1 = "stout_meal_inn"
        room2 = "antechamber"
        with self.assertRaises(RoomConnectionError):
            State.unlock_door(room1, room2)

    def test_break_door_no_connection(self) -> None:
        room1 = "stout_meal_inn"
        room2 = "antechamber"
        with self.assertRaises(RoomConnectionError):
            State.break_door(room1, room2)

    def test_lock_door_malformed(self) -> None:
        room1 = "stout_meal_inn"
        room2 = "the_moon"
        with self.assertRaises(UnrecognisedRoomError):
            State.lock_door(room1, room2)

    def test_unlock_door_malformed(self) -> None:
        room1 = "stout_meal_inn"
        room2 = "the_moon"
        with self.assertRaises(UnrecognisedRoomError):
            State.unlock_door(room1, room2)

    def test_break_door_malformed(self) -> None:
        room1 = "stout_meal_inn"
        room2 = "the_moon"
        with self.assertRaises(UnrecognisedRoomError):
            State.break_door(room1, room2)


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


class TestNPCCollection(unittest.TestCase):
    """Test the NPCCollection class"""
    def setUp(self) -> None:
        self.adventure = Adventure("the_tomb_of_baradin_stormfury")
        self.npc_collection = NPCCollection(self.adventure)
        MonsterCollection.load()
    
    def test__create_npcs(self) -> None:
        npcs = self.npc_collection._create_npcs()
        self.assertListEqual(["corvus", "anvil"], [npc for npc in npcs])
    
    def test__create_monsters(self) -> None:
        monsters = self.npc_collection._create_monsters()
        self.assertListEqual(["giant_rat_1", "giant_rat_2", "giant_rat_3", "giant_rat_4", "zombie_1", "goblin_1", "skeleton_1", "goblin_2", "goblin_3"], [m for m in monsters])
    
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
        self.assertIsNone(self.npc_collection.get_entity("yoda"))
        
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
        self.assertListEqual(["giant_rat_1", "giant_rat_2", "giant_rat_3", "giant_rat_4", "zombie_1", "goblin_1", "skeleton_1", "goblin_2", "goblin_3"], [m.unique_id for m in monsters])

    def test_get_all_monster_ids(self) -> None:
        self.npc_collection.load()
        monsters = self.npc_collection.get_all_monster_ids()
        self.assertListEqual(["giant_rat_1", "giant_rat_2", "giant_rat_3", "giant_rat_4", "zombie_1", "goblin_1", "skeleton_1", "goblin_2", "goblin_3"], [m for m in monsters])
    

if __name__ == "__main__":
    unittest.main()
