import unittest
import sys
import os

p = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, p + "/../")

from dmai.game import State, Adventure
from dmai.game.world import Room
from dmai.utils import UnrecognisedEntityError, UnrecognisedRoomError

class TestState(unittest.TestCase):
    """Test the State class"""

    def setUp(self) -> None:
        self.adventure = Adventure("the_tomb_of_baradin_stormfury")
        self.adventure.build_world()
        self.state = State(self.adventure)

    def test_get_current_room_player(self) -> None:
        entity = "player"
        room = self.adventure.get_room("stout_meal_inn")
        self.assertEqual(room, self.state.get_current_room(entity))

    def test_get_current_room_malformed(self) -> None:
        entity = "yoda"
        with self.assertRaises(UnrecognisedEntityError):
            self.state.get_current_room(entity)

    def test_set_current_room_player(self) -> None:
        entity = "player"
        room_id = "inns_cellar"
        room = self.adventure.get_room(room_id)
        self.state.set_current_room(entity, room_id)
        self.assertEqual(room, self.state.get_current_room(entity))

    def test_set_current_room_malformed_room(self) -> None:
        entity = "player"
        room_id = "the_moon"
        with self.assertRaises(UnrecognisedRoomError):
            self.state.set_current_room(entity, room_id)
            
    def test_set_current_room_malformed_room(self) -> None:
        entity = "yoda"
        room_id = "inns_cellar"
        with self.assertRaises(UnrecognisedEntityError):
            self.state.set_current_room(entity, room_id)
    
    def test_get_current_room_id_player(self) -> None:
        entity = "player"
        room = "stout_meal_inn"
        self.assertEqual(room, self.state.get_current_room_id(entity))

    def test_get_current_room_id_malformed(self) -> None:
        entity = "yoda"
        with self.assertRaises(UnrecognisedEntityError):
            self.state.get_current_room_id(entity)

    def test_travel_allowed(self) -> None:
        current = "stout_meal_inn"
        destination = "inns_cellar"
        self.assertEqual(True, self.state.travel_allowed(current, destination))
    
    def test_travel_allowed_not_connected(self) -> None:
        current = "stout_meal_inn"
        destination = "antechamber"
        self.assertEqual(False, self.state.travel_allowed(current, destination))
            
    def test_travel_allowed_malformed_destination(self) -> None:
        current = "stout_meal_inn"
        destination = "the_moon"
        with self.assertRaises(UnrecognisedRoomError):
            self.state.travel_allowed(current, destination)

    def test_travel_allowed_malformed_current(self) -> None:
        current = "the_moon"
        destination = "inns_cellar"
        with self.assertRaises(UnrecognisedRoomError):
            self.state.travel_allowed(current, destination)
    
    def test_lock_no_connection(self) -> None:
        room1 = "stout_meal_inn"
        room2 = "antechamber"
        with self.assertRaises(UnrecognisedRoomError):
            self.state.lock(room1, room2)

    def test_unlock_no_connection(self) -> None:
        room1 = "stout_meal_inn"
        room2 = "antechamber"
        with self.assertRaises(UnrecognisedRoomError):
            self.state.unlock(room1, room2)

    def test_lock_malformed(self) -> None:
        room1 = "stout_meal_inn"
        room2 = "the_moon"
        with self.assertRaises(UnrecognisedRoomError):
            self.state.lock(room1, room2)
            
    def test_unlock_malformed(self) -> None:
        room1 = "stout_meal_inn"
        room2 = "the_moon"
        with self.assertRaises(UnrecognisedRoomError):
            self.state.unlock(room1, room2)
            
if __name__ == "__main__":
    unittest.main()
