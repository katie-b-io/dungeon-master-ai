from enum import Enum

from dmai.game.world.room import Room
from dmai.utils.exceptions import UnrecognisedEntityError, UnrecognisedRoomError
from dmai.nlg.nlg import NLG

class GameMode(Enum):
    COMBAT = "combat"
    EXPLORE = "explore"
    ROLEPLAY = "roleplay"


class Status(Enum):
    ALIVE = "alive"
    DEAD = "dead"

class StateMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs) -> None:
        """State static singleton metaclass"""
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class State(metaclass=StateMeta):
    
    # class variables
    started = False
    paused = False
    talking = False
    in_combat = False
    adventure = None
    player = None
    current_room = {}
    current_status = {}
    current_hp = {}
    current_game_mode = GameMode.EXPLORE
    current_intent = {}
    
    def __init__(self) -> None:
        """Main class for the game state"""
        pass
    
    @classmethod
    def combat(cls) -> None:
        if not cls.in_combat:
            cls.set_current_game_mode("combat")
            cls.in_combat = True
            print(NLG.transition_to_combat())
    
    @classmethod
    def explore(cls) -> None:
        cls.set_current_game_mode("explore")
        cls.in_combat = False

    @classmethod
    def roleplay(cls) -> None:
        cls.set_current_game_mode("roleplay")
        cls.in_combat = False
    
    @classmethod
    def set_current_game_mode(cls, game_mode: str) -> None:
        """Method to set the current game mode."""
        cls.current_game_mode = GameMode(game_mode)
        
    @classmethod
    def start(cls) -> None:
        cls.started = True
        
    @classmethod
    def pause(cls) -> None:
        cls.paused = True
    
    @classmethod
    def play(cls) -> None:
        cls.paused = False

    @classmethod
    def talk(cls) -> None:
        cls.talking = True

    @classmethod
    def stop_talking(cls) -> None:
        cls.talking = False
    
    @classmethod
    def set_adventure(cls, adventure) -> None:
        cls.adventure = adventure
        cls.current_room["player"] = adventure.get_init_room()
    
    @classmethod
    def set_player(cls, player) -> None:
        cls.player = player
        cls.current_hp["player"] = player.character.hp_max
        cls.current_status["player"] = Status.ALIVE

    @classmethod
    def set_init_status(cls, entity: str, status: str) -> str:
        """Method to set the initial status for specified entity."""
        cls.current_status[entity] = Status(status)

    @classmethod
    def get_current_hp(cls, entity: str = "player") -> None:
        """Method to get the current hp for specified entity."""
        try:
            return cls.current_hp[entity]
        except KeyError:
            msg = "Entity not recognised: {e}".format(e=entity)
            raise UnrecognisedEntityError(msg)
        
    @classmethod
    def get_current_status(cls, entity: str = "player") -> None:
        """Method to get the current status for specified entity."""
        try:
            return cls.current_status[entity]
        except KeyError:
            msg = "Entity not recognised: {e}".format(e=entity)
            raise UnrecognisedEntityError(msg)
    
    @classmethod
    def clear_intent(cls,) -> None:
        """Method to clera the current intent"""
        cls.current_intent = {}
        
    @classmethod
    def store_intent(cls, intent: str, params: dict) -> None:
        """Method to set the current intent"""
        cls.current_intent = {
            "intent": intent,
            "params": params
        }
        
    ############################################################
    # METHODS RELATING TO LOCATION
    @classmethod
    def set_init_room(cls, entity: str, room_id: str) -> str:
        """Method to set the initial room for specified entity."""
        cls.current_room[entity] = room_id
        
    @classmethod
    def get_current_room_id(cls, entity: str = "player") -> str:
        """Method to get the current room id for specified entity."""
        try:
            return cls.current_room[entity]
        except KeyError:
            msg = "Entity not recognised: {e}".format(e=entity)
            raise UnrecognisedEntityError(msg)
    
    @classmethod
    def get_current_room(cls, entity: str = "player") -> Room:
        """Method to get the current room for specified entity."""
        try:
            return cls.adventure.get_room(cls.get_current_room_id(entity))
        except (UnrecognisedRoomError, UnrecognisedEntityError):
            raise

    @classmethod
    def set_current_room(cls, entity: str, room_id: str) -> None:
        """Method to set the current room for specified entity."""
        if entity not in cls.current_room:
            msg = "Entity not recognised: {e}".format(e=entity)
            raise UnrecognisedEntityError(msg)
        
        if room_id not in cls.adventure.rooms:
            msg = "Room not recognised: {r}".format(r=room_id)
            raise UnrecognisedRoomError(msg)
        
        cls.current_room[entity] = room_id
    
    @classmethod
    def travel_allowed(cls, current_id: str, destination_id: str) -> bool:
        """Method to determine if travel is allowed between specified rooms."""
        if destination_id not in cls.adventure.rooms:
            msg = "Room not recognised: {d}".format(d=destination_id)
            raise UnrecognisedRoomError(msg)
        
        try: 
            current = cls.adventure.rooms[current_id]
            if destination_id not in current.connections:
                return False
            return current.connections[destination_id]
        except KeyError as e:
            msg = "Room not recognised: {e}".format(e=e)
            raise UnrecognisedRoomError(msg)
    
    @classmethod
    def lock(cls, room_id1: str, room_id2: str) -> None:
        """Method to lock the connection between two given rooms."""
        for (r1, r2) in [(room_id1, room_id2), (room_id2, room_id1)]:
            if r1 not in cls.adventure.rooms:
                msg = "Room not recognised: {r}".format(r=r1)
            elif r2 not in cls.adventure.rooms[r1].connections:
                msg = "Connection not recognised: {r}".format(r=r2)
        if msg:
            raise UnrecognisedRoomError(msg)
        
        cls.adventure.rooms[room_id1].connections[room_id2] = False
        cls.adventure.rooms[room_id2].connections[room_id1] = False

    @classmethod
    def unlock(cls, room_id1: str, room_id2: str) -> None:
        """Method to unlock the connection between two given rooms."""
        for (r1, r2) in [(room_id1, room_id2), (room_id2, room_id1)]:
            if r1 not in cls.adventure.rooms:
                msg = "Room not recognised: {r}".format(r=r1)
            elif r2 not in cls.adventure.rooms[r1].connections:
                msg = "Connection not recognised: {r}".format(r=r2)
        if msg:
            raise UnrecognisedRoomError(msg)
        
        cls.adventure.rooms[room_id1].connections[room_id2] = True
        cls.adventure.rooms[room_id2].connections[room_id1] = True
