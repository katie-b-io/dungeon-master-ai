from dmai.game.world import Room
from dmai.utils import UnrecognisedEntityError, UnrecognisedRoomError


class State:
    def __init__(self, adventure) -> None:
        """Main class for the game state"""
        self.adventure = adventure
        self.current_room = {"player": adventure.get_init_room()}

    def get_current_room(self, entity: str) -> Room:
        """Method to get the current room for specified entity."""
        if entity not in self.current_room:
            msg = "Entity not recognised: {e}".format(e=entity)
            raise UnrecognisedEntityError(msg)
        
        try:
            return self.adventure.get_room(self.current_room[entity])
        except UnrecognisedRoomError:
            raise

    def set_current_room(self, entity: str, room_id: str) -> None:
        """Method to set the current room for specified entity."""
        if entity not in self.current_room:
            msg = "Entity not recognised: {e}".format(e=entity)
            raise UnrecognisedEntityError(msg)
        
        if room_id not in self.adventure.rooms:
            msg = "Room not recognised: {r}".format(r=room_id)
            raise UnrecognisedRoomError(msg)
        
        self.current_room[entity] = room_id

    def get_current_room_id(self, entity: str) -> str:
        """Method to get the current room id for specified entity."""
        try:
            return self.current_room[entity]
        except KeyError:
            msg = "Entity not recognised: {e}".format(e=entity)
            raise UnrecognisedEntityError(msg)

    def travel_allowed(self, current_id: str, destination_id: str) -> bool:
        """Method to determine if travel is allowed between specified rooms."""
        if destination_id not in self.adventure.rooms:
            msg = "Room not recognised: {d}".format(d=destination_id)
            raise UnrecognisedRoomError(msg)
        
        try: 
            current = self.adventure.rooms[current_id]
            if destination_id not in current.connections:
                return False
            return current.connections[destination_id]
        except KeyError as e:
            msg = "Room not recognised: {e}".format(e=e)
            raise UnrecognisedRoomError(msg)
        
    def lock(self, room_id1: str, room_id2: str) -> None:
        """Method to lock the connection between two given rooms."""
        for (r1, r2) in [(room_id1, room_id2), (room_id2, room_id1)]:
            if r1 not in self.adventure.rooms:
                msg = "Room not recognised: {r}".format(r=r1)
            elif r2 not in self.adventure.rooms[r1].connections:
                msg = "Connection not recognised: {r}".format(r=r2)
        if msg:
            raise UnrecognisedRoomError(msg)
        
        self.adventure.rooms[room_id1].connections[room_id2] = False
        self.adventure.rooms[room_id2].connections[room_id1] = False

    def unlock(self, room_id1: str, room_id2: str) -> None:
        """Method to unlock the connection between two given rooms."""
        for (r1, r2) in [(room_id1, room_id2), (room_id2, room_id1)]:
            if r1 not in self.adventure.rooms:
                msg = "Room not recognised: {r}".format(r=r1)
            elif r2 not in self.adventure.rooms[r1].connections:
                msg = "Connection not recognised: {r}".format(r=r2)
        if msg:
            raise UnrecognisedRoomError(msg)
        
        self.adventure.rooms[room_id1].connections[room_id2] = True
        self.adventure.rooms[room_id2].connections[room_id1] = True
