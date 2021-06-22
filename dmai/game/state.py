from collections import Counter
from enum import Enum
import operator

from dmai.utils.output_builder import OutputBuilder
from dmai.utils.exceptions import UnrecognisedEntityError, UnrecognisedRoomError, RoomConnectionError
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


class Attitude(Enum):
    FRIENDLY = "friendly"
    INDIFFERENT = "indifferent"
    HOSTILE = "hostile"


class Combat(Enum):
    INITIATIVE = 0
    DECLARE = 1
    ATTACK_ROLL = 2
    DAMAGE_ROLL = 3
    WAIT = 4


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
    quest_received = False
    questing = False
    complete = False
    in_combat = False
    roleplaying = False
    torch_lit = False
    stationary = False
    current_conversation = None
    current_room = {}
    current_status = {}
    current_hp = {}
    current_game_mode = GameMode.EXPLORE
    current_intent = None
    stored_intent = {}
    current_target = {}
    current_goal = ("at", "player", "southern_corridor")
    current_items = {}
    current_attitude = {}
    attacked_by_player = []
    current_combat_status = {}
    expected_intent = None
    initiative_order = []

    def __init__(self) -> None:
        """Main class for the game state"""
        pass

    @classmethod
    def combat(cls, attacker: str, target: str) -> None:
        if not cls.in_combat:
            cls.reset_combat_status()
            cls.set_current_game_mode("combat")
            cls.in_combat = True
            cls.roleplaying = False
            cls.set_target(target, attacker)
            cls.clear_conversation()
            OutputBuilder.append(NLG.transition_to_combat())
            cls.set_expected_intent("roll_die") #TODO change to "roll"
        else:
            cls.progress_combat_status()
            OutputBuilder.append(NLG.attack(attacker, target))
            if cls.current_combat_status == Combat(2) or cls.current_combat_status == Combat(3):
                cls.set_expected_intent("roll_die")

    @classmethod
    def explore(cls) -> None:
        cls.set_current_game_mode("explore")
        cls.in_combat = False
        cls.roleplaying = False
        cls.clear_target()
        cls.clear_conversation()
        cls.clear_expected_intent()

    @classmethod
    def roleplay(cls, target: str) -> None:
        if not cls.roleplaying:
            cls.set_current_game_mode("roleplay")
            cls.in_combat = False
            cls.roleplaying = True
            cls.clear_target()
            cls.set_conversation_target(target)
            cls.clear_expected_intent()

    @classmethod
    def set_current_game_mode(cls, game_mode: str) -> None:
        """Method to set the current game mode."""
        cls.current_game_mode = GameMode(game_mode)
    
    @classmethod
    def set_current_goal(cls, goal: tuple) -> None:
        """Method to set the current goal"""
        cls.current_goal = goal

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
        cls.quest_received = True
    
    @classmethod
    def quest(cls) -> None:
        cls.questing = True
    
    @classmethod
    def complete_quest(cls) -> None:
        cls.complete = True

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
        cls.current_combat_status["player"] = Combat.INITIATIVE

    @classmethod
    def get_player(cls):
        """Method to return player"""
        return cls.player
    
    @classmethod
    def get_name(cls, entity: str = None) -> str:
        """Method to return name of entity"""
        try:
            if not entity or entity == "player":
                return cls.get_player().name
            else:
                return cls.get_dm().npcs.get_entity(entity).name
        except UnrecognisedEntityError:
            logger.error("Unrecognised entity: {e}".format(e=entity))
            return ""
    
    @classmethod
    def get_entity(cls, entity: str = None):
        """Method to return entity"""
        try:
            return cls.get_dm().npcs.get_entity(entity)
        except UnrecognisedEntityError:
            logger.error("Unrecognised entity: {e}".format(e=entity))
            return None
    
    ############################################################
    # METHODS RELATING TO STATUS AND ATTITUDE
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
    def set_current_status(cls, entity: str = "player", status: str = "alive") -> str:
        """Method to set the current status for specified entity."""
        try:
            cls.current_status[entity] = Status(status)
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
        return cls.get_current_status(entity) == Status("alive")

    @classmethod
    def set_init_attitude(cls, entity: str, attitude: str) -> None:
        """Method to set the initial attitude towards player for specifed entity."""
        cls.current_attitude[entity] = Attitude(attitude)
    
    @classmethod
    def set_current_attitude(cls, entity: str = "player", attitude: str = "indifferent") -> str:
        """Method to set the current attitude towards player for specified entity."""
        try:
            cls.current_attitude[entity] = Attitude(attitude)
        except KeyError:
            msg = "Entity not recognised: {e}".format(e=entity)
            raise UnrecognisedEntityError(msg)

    @classmethod
    def get_current_attitude(cls, entity: str = "player") -> str:
        """Method to get the current attitude towards player for specified entity."""
        try:
            return cls.current_attitude[entity]
        except KeyError:
            msg = "Entity not recognised: {e}".format(e=entity)
            raise UnrecognisedEntityError(msg)
    
    @classmethod
    def set_expected_intent(cls, intent: str) -> None:
        """Method to set the expected intent"""
        cls.expected_intent = intent

    @classmethod
    def clear_expected_intent(cls) -> None:
        """Method to clear the expected intent"""
        cls.expected_intent = None

    ############################################################
    # METHODS RELATING TO CONVERSATION
    @classmethod
    def set_conversation_target(cls, target: str) -> None:
        """Method to set the current target for a conversation"""
        logger.debug("Setting current conversation target: {t}".format(t=target))
        cls.current_conversation = target

    @classmethod
    def clear_conversation(cls, entity: str = "player") -> None:
        """Method to clear the conversation for an entity"""
        logger.debug("Clearing current conversation")
        cls.current_conversation = None

    ############################################################
    # METHODS RELATING TO ITEMS
    @classmethod
    def add_item(cls, item: str) -> None:
        """Method to add item"""
        if item in cls.current_items:
            cls.current_items[item] = cls.current_items[item] + 1
        else:
            cls.current_items[item] = 1
    
    @classmethod
    def remove_item(cls, item: str) -> None:
        """Method to remove item"""
        if item in cls.current_items:
            cls.current_items[item] = cls.current_items[item] - 1
        if cls.current_items[item] == 0:
            del cls.current_items[item]
    
    @classmethod
    def get_all_item_ids(cls) -> list:
        """Method to return all item IDs in list"""
        return list(cls.current_items.keys())

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
    def clear_intent(cls, ) -> None:
        """Method to clear the stored intent"""
        cls.stored_intent = {}

    @classmethod
    def store_intent(cls, intent: str, params: dict) -> None:
        """Method to set the stored intent"""
        cls.stored_intent = {"intent": intent, "params": params}
    
    @classmethod
    def set_intent(cls, intent: str) -> None:
        """Method to set the current intent"""
        cls.current_intent = intent

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
                if not cls.get_current_room_id(
                        entity) == cls.get_current_room_id(target):
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
    def get_combat_status(cls, entity: str = "player") -> Combat:
        """Method to set the combat status for specified entity."""
        try:
            return cls.current_combat_status[entity]
        except KeyError:
            msg = "Entity not recognised: {e}".format(e=entity)
            raise UnrecognisedEntityError(msg)
        
    @classmethod
    def set_combat_status(cls, status: int, entity: str = "player") -> None:
        """Method to set the combat status for specified entity."""
        cls.current_combat_status[entity] = Combat(status)
    
    @classmethod
    def reset_combat_status(cls, entity: str = "player") -> None:
        """Method to set the combat status for specified entity."""
        cls.current_combat_status[entity] = Combat(0)
    
    @classmethod
    def progress_combat_status(cls, entity: str = "player", can_reset: bool = False) -> str:
        """Method to progress the combat status for specified entity."""
        try:
            next_value = cls.current_combat_status[entity].value + 1
            max_value = max([e.value for e in Combat])
            if next_value > max_value:
                next_value = 0 if can_reset else 1
            cls.set_combat_status(next_value, entity)
        except KeyError:
            msg = "Entity not recognised: {e}".format(e=entity)
            raise UnrecognisedEntityError(msg)
    
    @classmethod
    def set_initiative_order(cls) -> None:
        """Method to set the initative order"""
        rolls = {}

        # get player initiative
        player_result = State.get_player().roll_initiative()
        if player_result == 1 or player_result == 20:
            OutputBuilder.append(NLG.roll_reaction(player_result))
        rolls["player"] = player_result
        
        # initiative rolls for monsters in the room
        monsters = cls.get_possible_monster_targets()
        for monster in monsters:
            rolls[monster.unique_id] = monster.roll_initiative()
        
        # order the rolls dict and set keys as initiative order
        sorted_rolls = dict(sorted(rolls.items(), key=operator.itemgetter(1), reverse=True))
        cls.initiative_order = list(sorted_rolls.keys())
        
        # set combat status depending on player initiative
        print(cls.initiative_order)
        print(cls.current_target)
        if cls.initiative_order.index("player") == 0:
            # we have a target, so get an attack roll from player
            cls.set_combat_status(2)
        else:
            # player doesn't go first - wait til their turn
            cls.set_combat_status(4)
            OutputBuilder.append("You'll have to wait your turn.")
    
    @classmethod
    def update_initiative_order(cls, *args) -> None:
        """Method to update the initiative order by popping from front of list
        and appending to end"""
        logger.debug("Updating initiative order")
        cls.initiative_order.append(cls.initiative_order.pop(0))
    
    @classmethod
    def get_currently_acting_entity(cls) -> str:
        """Method to return the id of the entity at the front of the initiative
        order"""
        return cls.initiative_order[0]
        
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
            return cls.dm.npcs.get_entity(cls.get_current_target_id(entity))
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
            cls.dm.deregister_trigger(
                cls.dm.npcs.get_entity(cls.get_current_target_id(entity)))
        cls.current_target[entity] = target
        cls.dm.register_trigger(
            cls.dm.npcs.get_entity(cls.get_current_target_id(entity)))
        if target != "player" and target not in cls.attacked_by_player:
            cls.attacked_by_player.append(target)

    @classmethod
    def clear_target(cls, entity: str = "player") -> None:
        """Method to clear the target for an entity"""
        if entity not in cls.current_target:
            msg = "Entity not recognised: {e}".format(e=entity)
            raise UnrecognisedEntityError(msg)

        logger.debug("Clearing current target")
        if cls.get_current_target_id(entity):
            cls.dm.deregister_trigger(
                cls.dm.npcs.get_entity(cls.get_current_target_id(entity)))
            cls.current_target[entity] = None

    @classmethod
    def was_attacked(cls, monster_id: str) -> bool:
        """Method to determine if monster was attacked by player"""
        return monster_id in cls.attacked_by_player
    
    ############################################################
    # METHODS RELATING TO LOCATION
    @classmethod
    def halt(cls) -> None:
        """Method to set stationary to true"""
        cls.stationary = True
    
    @classmethod
    def get_room_name(cls, room_id: str) -> str:
        """Method to return the name of a room."""
        try:
            if cls._check_room_exists(room_id):
                return cls.dm.adventure.get_room(room_id).name
        except UnrecognisedRoomError:
            raise

    @classmethod
    def set_init_room(cls, entity: str, room_id: str) -> str:
        """Method to set the initial room for specified entity."""
        cls.current_room[entity] = room_id

    @classmethod
    def _check_entity_exists(cls, entity_id: str) -> bool:
        """Method to check entity exists.
        Raises UnrecognisedEntityError exception if not"""
        try:
            return bool(cls.current_room[entity_id])
        except KeyError:
            msg = "Entity not recognised: {e}".format(e=entity_id)
            raise UnrecognisedEntityError(msg)

    @classmethod
    def _check_room_exists(cls, room_id: str) -> bool:
        """Method to check room exists.
        Raises UnrecognisedRoomError exception if not"""
        try:
            return bool(cls.dm.adventure.get_room(room_id))
        except UnrecognisedRoomError:
            raise

    @classmethod
    def _check_connection_exists(cls, room_id1: str, room_id2: str) -> bool:
        """Method to check connection exists.
        Raises UnrecognisedRoomError exception if not"""
        r1, r2 = "", ""
        try:
            for (r1, r2) in [(room_id1, room_id2), (room_id2, room_id1)]:
                cls.dm.adventure.rooms[r1].connections[r2]
            return True
        except KeyError:
            msg = "Connection does not exist: {r1}-{r2}".format(r1=r1, r2=r2)
            raise RoomConnectionError(msg)

    @classmethod
    def get_current_room_id(cls, entity: str = "player") -> str:
        """Method to get the current room id for specified entity."""
        try:
            if cls._check_entity_exists(entity):
                return cls.current_room[entity]
        except UnrecognisedEntityError:
            raise

    @classmethod
    def get_current_room(cls, entity: str = "player"):
        """Method to get the current room for specified entity."""
        try:
            if cls._check_entity_exists(entity):
                room_id = cls.get_current_room_id(entity)
                if cls._check_room_exists(room_id):
                    return cls.dm.adventure.get_room(room_id)
        except (UnrecognisedRoomError, UnrecognisedEntityError):
            raise

    @classmethod
    def set_current_room(cls, entity: str, room_id: str) -> None:
        """Method to set the current room for specified entity."""
        try:
            if cls._check_entity_exists(entity) and cls._check_room_exists(
                    room_id):
                logger.debug("Setting current room for {e}: {r}".format(
                    e=entity, r=room_id))
                cls.stationary = False
                cls.dm.deregister_trigger(cls.get_current_room(entity))
                cls.current_room[entity] = room_id
                cls.dm.register_trigger(cls.get_current_room(entity))
        except (UnrecognisedRoomError, UnrecognisedEntityError):
            raise

    @classmethod
    def travel_allowed(cls, current_id: str, destination_id: str) -> bool:
        """Method to determine if travel is allowed between specified rooms."""
        try:
            if cls._check_room_exists(current_id) and cls._check_room_exists(
                    destination_id) and cls._check_connection_exists(
                        current_id, destination_id):
                current = cls.dm.adventure.get_room(current_id)
                return current.connections[destination_id][
                    "broken"] or not current.connections[destination_id][
                        "locked"]
        except UnrecognisedRoomError:
            raise
        except RoomConnectionError:
            return False

    @classmethod
    def connection_broken(cls, current_id: str, destination_id: str) -> bool:
        """Method to determine if connection between specified rooms is broken."""
        try:
            if cls._check_room_exists(current_id) and cls._check_room_exists(
                    destination_id) and cls._check_connection_exists(
                        current_id, destination_id):
                current = cls.dm.adventure.rooms[current_id]
                return current.connections[destination_id]["broken"]
        except UnrecognisedRoomError:
            raise
        except RoomConnectionError:
            return False

    @classmethod
    def _update_connection(cls, r1: str, r2: str, status: str,
                           state: bool) -> None:
        cls.dm.adventure.rooms[r1].connections[r2][status] = state
        cls.dm.adventure.rooms[r2].connections[r1][status] = state

    @classmethod
    def lock_door(cls, room_id1: str, room_id2: str) -> None:
        """Method to lock the connection between two given rooms."""
        try:
            if cls._check_room_exists(room_id1) and cls._check_room_exists(
                    room_id2) and cls._check_connection_exists(
                        room_id1, room_id2):
                cls._update_connection(room_id1, room_id2, "locked", True)
        except (UnrecognisedRoomError, RoomConnectionError):
            raise

    @classmethod
    def unlock_door(cls, room_id1: str, room_id2: str) -> None:
        """Method to unlock the connection between two given rooms."""
        try:
            if cls._check_room_exists(room_id1) and cls._check_room_exists(
                    room_id2) and cls._check_connection_exists(
                        room_id1, room_id2):
                cls._update_connection(room_id1, room_id2, "locked", False)
        except (UnrecognisedRoomError, RoomConnectionError):
            raise

    @classmethod
    def break_door(cls, room_id1: str, room_id2: str) -> None:
        """Method to break the connection between two given rooms."""
        try:
            if cls._check_room_exists(room_id1) and cls._check_room_exists(
                    room_id2) and cls._check_connection_exists(
                        room_id1, room_id2):
                cls._update_connection(room_id1, room_id2, "broken", True)
        except (UnrecognisedRoomError, RoomConnectionError):
            raise

    @classmethod
    def get_possible_monster_targets(cls, entity: str = "player") -> list:
        """Method to get all monsters in a room that specified entity is in"""
        targets = []
        for monster in cls.get_dm().npcs.get_all_monsters():
            if cls.get_current_room_id(monster.unique_id) == cls.get_current_room_id(entity):
                if cls.is_alive(monster.unique_id):
                    targets.append(monster)
        return targets
    
    @classmethod
    def get_formatted_possible_monster_targets(cls, entity: str = "player") -> str:
        """Method to return a formatted string of possible monster targets"""
        monsters = cls.get_possible_monster_targets(entity)
        possible_targets = [monster.name for monster in monsters]
        count_targets = dict(Counter(possible_targets))
        if monsters:
            formatted_array = []
            for t in count_targets:
                c = count_targets.get(t)
                if c > 1:
                    formatted_array.append("the {c} {t}s".format(c=c, t=t))
                else:
                    formatted_array.append("the {t}".format(t=t))
            if len(formatted_array) == 1:
                formatted_str = "You could attack {a}.".format(a=formatted_array[0])
            else:
                formatted_str = "You could attack {a}".format(a=", ".join(formatted_array[0:-1]))
                formatted_str += " or {a}.".format(a=formatted_array[-1])
            return formatted_str
        else:
            return ""