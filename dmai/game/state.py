from dmai.game.world import Room


class State:
    def __init__(self, adventure) -> None:
        """Main class for the game state"""
        self.rooms = adventure.rooms
        self.current_room = {"player": adventure.get_init_room()}

    def get_current_room(self, entity: str) -> Room:
        """Method to get the current room for specified entity."""
        return self.rooms[self.current_room[entity]]

    def set_current_room(self, entity: str, room: str) -> None:
        """Method to set the current room for specified entity."""
        self.current_room[entity] = room

    def get_current_room_id(self, entity: str) -> str:
        """Method to get the current room id for specified entity."""
        return self.current_room[entity]

    def travel_allowed(self, current: str, destination: str) -> bool:
        """Method to determine if travel is allowed between specified rooms."""
        try:
            if destination not in self.rooms[current].connections:
                return False
            return self.rooms[current].connections[destination]
        except KeyError:
            raise

    def lock(self, room1: str, room2: str) -> None:
        """Method to lock the connection between two given rooms."""
        self.rooms[room1].connections[room2] = False
        self.rooms[room2].connections[room1] = False

    def unlock(self, room1: str, room2: str) -> None:
        """Method to unlock the connection between two given rooms."""
        self.rooms[room1].connections[room2] = True
        self.rooms[room2].connections[room1] = True
