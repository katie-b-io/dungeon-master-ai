from dmai.utils.output_builder import OutputBuilder
from enum import Enum

from dmai.utils.exceptions import UnrecognisedEntityError, UnrecognisedRoomError
from dmai.nlg.nlg import NLG
from dmai.utils.logger import get_logger

logger = get_logger(__name__)


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
    dm = None
    player = None
    
    # class state variables
    started = False
    paused = False
    talking = False
    questing = False
    in_combat = False
    torch_lit = False
    stationary = False
    current_room = {}
    current_status = {}
    current_hp = {}
    current_game_mode = GameMode.EXPLORE
    current_intent = {}
    current_target = {}
    
    def __init__(self) -> None:
        """Main class for the game state"""
        pass
    
    @classmethod
    def combat(cls, attacker: str, target: str) -> None:
        if not cls.in_combat:
            cls.set_current_game_mode("combat")
            cls.in_combat = True
            cls.set_target(target)
            OutputBuilder.append(NLG.transition_to_combat())
    
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
    def received_quest(cls) -> None:
        cls.questing = True

    @classmethod
    def talk(cls) -> None:
        cls.talking = True

    @classmethod
    def stop_talking(cls) -> None:
        cls.talking = False
    
    @classmethod
    def set_dm(cls, dm) -> None:
        logger.debug("Setting DM")
        cls.dm = dm
        init_room = cls.dm.adventure.get_init_room()
        cls.dm.register_trigger(cls.dm.adventure.get_room(init_room))
        cls.current_room["player"] = init_room
    
    @classmethod
    def get_dm(cls) -> None:
        """Method to return dm"""
        return cls.dm

    @classmethod
    def set_player(cls, player) -> None:
        cls.player = player
        cls.current_hp["player"] = player.character.hp_max
        cls.current_status["player"] = Status.ALIVE
        cls.current_target["player"] = None

    @classmethod
    def get_player(cls) -> None:
        """Method to return player"""
        return cls.player
    
    ############################################################
    # METHODS RELATING TO STATUS
    @classmethod
    def set_init_status(cls, entity: str, status: str) -> str:
        """Method to set the initial status for specified entity."""
        cls.current_status[entity] = Status(status)

    @classmethod
    def get_current_hp(cls, entity: str = "player") -> int:
        """Method to get the current hp for specified entity."""
        try:
            return cls.current_hp[entity]
        except KeyError:
            msg = "Entity not recognised: {e}".format(e=entity)
            raise UnrecognisedEntityError(msg)
        
    @classmethod
    def get_current_status(cls, entity: str = "player") -> str:
        """Method to get the current status for specified entity."""
        try:
            return cls.current_status[entity]
        except KeyError:
            msg = "Entity not recognised: {e}".format(e=entity)
            raise UnrecognisedEntityError(msg)
    
    @classmethod
    def is_alive(cls, entity: str = "player") -> bool:
        """Method to determine whether the specified entity is alive"""
        return cls.get_current_status(entity) == Status.ALIVE
    
    ############################################################
    # METHODS RELATING TO ACTIONS
    @classmethod
    def light_torch(cls) -> None:
        """Method to light a torch"""
        cls.torch_lit = True
        OutputBuilder.append(NLG.light_torch())
    
    @classmethod
    def extinguish_torch(cls) -> None:
        """Method to extinguish a torch"""
        cls.torch_lit = False
        OutputBuilder.append(NLG.extinguish_torch())
    
    ############################################################
    # METHODS RELATING TO INTENTS
    @classmethod
    def clear_intent(cls,) -> None:
        """Method to clear the current intent"""
        cls.current_intent = {}
        
    @classmethod
    def store_intent(cls, intent: str, params: dict) -> None:
        """Method to set the current intent"""
        cls.current_intent = {
            "intent": intent,
            "params": params
        }

    ############################################################
    # METHODS RELATING TO STATE MAINTENANCE
    @classmethod
    def maintenance(cls) -> None:
        """Method to maintain the state correctly"""
        cls.maintain_current_target()
        cls.maintain_current_game_mode()
    
    @classmethod
    def maintain_current_target(cls) -> None:
        """Check if current targets are still valid"""
        for entity in cls.current_target:
            target = cls.get_current_target_id(entity)
            if target:
                if not cls.get_current_room_id(entity) == cls.get_current_room_id(target):
                    cls.clear_target(entity)

    @classmethod
    def maintain_current_game_mode(cls) -> None:
        """Check if current game mode is still valid"""
        if cls.in_combat:
            if "player" in cls.current_target:
                if not cls.current_target["player"]:
                    cls.explore()

    ############################################################
    # METHODS RELATING TO COMBAT
    @classmethod
    def get_current_target_id(cls, entity: str = "player") -> str:
        """Method to get the current target id for specified entity."""
        try:
            return cls.current_target[entity]
        except KeyError:
            msg = "Entity not recognised: {e}".format(e=entity)
            raise UnrecognisedEntityError(msg)
    
    @classmethod
    def get_current_target(cls, entity: str = "player"):
        """Method to get the current target for specified entity."""
        try:
            return cls.dm.npcs.get_monster(cls.get_current_target_id(entity))
        except UnrecognisedEntityError:
            raise
    
    @classmethod
    def set_target(cls, target: str, entity: str = "player") -> None:
        """Method to set the current target for an entity"""
        if entity not in cls.current_target:
            msg = "Entity not recognised: {e}".format(e=entity)
            raise UnrecognisedEntityError(msg)
        
        logger.debug("Setting current target: {t}".format(t=target))
        if cls.get_current_target_id(entity):
            cls.dm.deregister_trigger(cls.dm.npcs.get_monster(cls.get_current_target_id(entity)))
        cls.current_target[entity] = target
        cls.dm.register_trigger(cls.dm.npcs.get_monster(cls.get_current_target_id(entity)))
    
    @classmethod
    def clear_target(cls, entity: str = "player") -> None:
        """Method to clear the target for an entity"""
        if entity not in cls.current_target:
            msg = "Entity not recognised: {e}".format(e=entity)
            raise UnrecognisedEntityError(msg)
        
        logger.debug("Clearing current target")
        if cls.get_current_target_id(entity):
            cls.dm.deregister_trigger(cls.dm.npcs.get_monster(cls.get_current_target_id(entity)))
            cls.current_target[entity] = None
        
    ############################################################
    # METHODS RELATING TO LOCATION
    @classmethod
    def halt(cls) -> None:
        """Method to set stationary to true"""
        cls.stationary = True
        
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
    def get_current_room(cls, entity: str = "player"):
        """Method to get the current room for specified entity."""
        try:
            return cls.dm.adventure.get_room(cls.get_current_room_id(entity))
        except (UnrecognisedRoomError, UnrecognisedEntityError):
            raise

    @classmethod
    def set_current_room(cls, entity: str, room_id: str) -> None:
        """Method to set the current room for specified entity."""
        if entity not in cls.current_room:
            msg = "Entity not recognised: {e}".format(e=entity)
            raise UnrecognisedEntityError(msg)
        
        if room_id not in cls.dm.adventure.rooms:
            msg = "Room not recognised: {r}".format(r=room_id)
            raise UnrecognisedRoomError(msg)
        
        logger.debug("Setting current room: {r}".format(r=room_id))
        cls.stationary = False
        cls.dm.deregister_trigger(cls.dm.adventure.get_room(cls.get_current_room_id(entity)))
        cls.current_room[entity] = room_id
        cls.dm.register_trigger(cls.dm.adventure.get_room(cls.get_current_room_id(entity)))
    
    @classmethod
    def travel_allowed(cls, current_id: str, destination_id: str) -> bool:
        """Method to determine if travel is allowed between specified rooms."""
        if destination_id not in cls.dm.adventure.rooms:
            msg = "Room not recognised: {d}".format(d=destination_id)
            raise UnrecognisedRoomError(msg)
        
        try: 
            current = cls.dm.adventure.rooms[current_id]
            if destination_id not in current.connections:
                return False
            return current.connections[destination_id]["broken"] or not current.connections[destination_id]["locked"] 
        except KeyError as e:
            msg = "Room not recognised: {e}".format(e=e)
            raise UnrecognisedRoomError(msg)
    
    @classmethod
    def lock_door(cls, room_id1: str, room_id2: str) -> None:
        """Method to lock the connection between two given rooms."""
        msg = None
        for (r1, r2) in [(room_id1, room_id2), (room_id2, room_id1)]:
            if r1 not in cls.dm.adventure.rooms:
                msg = "Room not recognised: {r}".format(r=r1)
            elif r2 not in cls.dm.adventure.rooms[r1].connections:
                msg = "Connection not recognised: {r}".format(r=r2)
        if msg:
            raise UnrecognisedRoomError(msg)
        
        cls.dm.adventure.rooms[room_id1].connections[room_id2]["locked"] = True
        cls.dm.adventure.rooms[room_id2].connections[room_id1]["locked"] = True

    @classmethod
    def unlock_door(cls, room_id1: str, room_id2: str) -> None:
        """Method to unlock the connection between two given rooms."""
        msg = None
        for (r1, r2) in [(room_id1, room_id2), (room_id2, room_id1)]:
            if r1 not in cls.dm.adventure.rooms:
                msg = "Room not recognised: {r}".format(r=r1)
            elif r2 not in cls.dm.adventure.rooms[r1].connections:
                msg = "Connection not recognised: {r}".format(r=r2)
        if msg:
            raise UnrecognisedRoomError(msg)
        
        cls.dm.adventure.rooms[room_id1].connections[room_id2]["locked"] = False
        cls.dm.adventure.rooms[room_id2].connections[room_id1]["locked"] = False

    @classmethod
    def break_door(cls, room_id1: str, room_id2: str) -> None:
        """Method to break the connection between two given rooms."""
        msg = None
        for (r1, r2) in [(room_id1, room_id2), (room_id2, room_id1)]:
            if r1 not in cls.dm.adventure.rooms:
                msg = "Room not recognised: {r}".format(r=r1)
            elif r2 not in cls.dm.adventure.rooms[r1].connections:
                msg = "Connection not recognised: {r}".format(r=r2)
        if msg:
            raise UnrecognisedRoomError(msg)
        
        cls.dm.adventure.rooms[room_id1].connections[room_id2]["broken"] = True
        cls.dm.adventure.rooms[room_id2].connections[room_id1]["broken"] = True