from collections import Counter
from enum import Enum
import operator

from dmai.utils.text import Text
from dmai.utils.output_builder import OutputBuilder
from dmai.utils.exceptions import UnrecognisedEntityError, UnrecognisedRoomError, RoomConnectionError
from dmai.nlg.nlg import NLG
from dmai.utils.config import Config
from dmai.utils.logger import get_logger
import dmai

logger = get_logger(__name__, Config.session.session_id)


class GameMode(Enum):
    COMBAT = "combat"
    EXPLORE = "explore"
    ROLEPLAY = "roleplay"


class Status(Enum):
    ALIVE = "alive"
    DEAD = "dead"
    HIDDEN = "hidden"


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
    in_combat_with_door = False
    door_target = None
    roleplaying = False
    torch_lit = False
    stationary = False
    current_conversation = None
    current_room = {}
    current_status = {}
    current_hp = {}
    current_hp_door = {}
    current_game_mode = GameMode.EXPLORE
    current_intent = None
    stored_intent = {}
    current_target = {}
    current_goal = ("at", "player", "southern_corridor")
    current_items = {}
    current_attitude = {}
    attacked_by_player = []
    current_combat_status = {}
    expected_intent = []
    expected_entities = []
    initiative_order = []
    stored_ability_check = None
    stored_skill_check = None
    ales = 0

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
            cls.in_combat_with_door = False
            cls.set_target(target, attacker)
            cls.clear_conversation()
            cls.set_expected_entities(["monster"])
            cls.set_expected_intent(["roll"])
            cls.clear_expected_entities()
            OutputBuilder.append(NLG.transition_to_combat())
        else:
            cls.set_target(target, attacker)
            State.set_expected_intent(["roll"])
            OutputBuilder.append(NLG.perform_attack_roll())
            cls.progress_combat_status()
                
    @classmethod
    def combat_with_door(cls, target: str) -> None:
        cls.door_target = target
        if not cls.in_combat_with_door:
            cls.in_combat_with_door = True
            cls.in_combat = False
            cls.roleplaying = False
            cls.clear_expected_entities()
            cls.set_combat_status(3)
            OutputBuilder.append(NLG.perform_attack_roll())
        else:
            cls.set_combat_status(3)
            OutputBuilder.append(NLG.perform_attack_roll())

    @classmethod
    def explore(cls) -> None:
        if cls.current_game_mode != GameMode.EXPLORE:
            cls.set_current_game_mode("explore")
            cls.in_combat = False
            cls.roleplaying = False
            cls.initiative_order = []
            cls.clear_target()
            cls.clear_conversation()
            cls.clear_expected_intent()
            cls.clear_expected_entities()
            cls.door_target = None

    @classmethod
    def roleplay(cls, target: str) -> None:
        if not cls.roleplaying:
            cls.set_current_game_mode("roleplay")
            cls.in_combat = False
            cls.roleplaying = True
            cls.initiative_order = []
            cls.clear_target()
            cls.set_conversation_target(target)
            cls.clear_expected_intent()
            cls.clear_expected_entities()
            cls.door_target = None

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
        cls.current_room["player"] = init_room
        for room in cls.dm.adventure.get_all_rooms():
            for connected_room in room.get_connected_rooms():
                if room.can_attack_door(connected_room):
                    cls.current_hp_door[connected_room] = room.get_door_hp(connected_room)
        
        # register room triggers
        for room in cls.dm.adventure.get_all_rooms():
             if hasattr(room, "trigger"):
                cls.dm.register_trigger(room)
        # register monster triggers
        for monster in cls.dm.npcs.get_all_monsters():
            if hasattr(monster, "trigger"):
                cls.dm.register_trigger(monster)
        # register npc triggers
        for npc in cls.dm.npcs.get_all_npcs():
            if hasattr(npc, "trigger"):
                cls.dm.register_trigger(npc)

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
    def get_entity_name(cls, entity: str = "player") -> str:
        """Method to return name of entity"""
        try:
            if entity == "player":
                return cls.get_player().name
            else:
                if hasattr(cls.get_dm().npcs.get_entity(entity), "unique_name"):
                    return cls.get_dm().npcs.get_entity(entity).unique_name
                else:
                    return cls.get_dm().npcs.get_entity(entity).name
        except UnrecognisedEntityError:
            logger.debug("Unrecognised entity: {e}".format(e=entity))
            return ""
    
    @classmethod
    def get_entity(cls, entity: str = "player"):
        """Method to return entity"""
        try:
            if entity == "player":
                return cls.get_player()
            else:
                return cls.get_dm().npcs.get_entity(entity)
        except UnrecognisedEntityError:
            logger.debug("Unrecognised entity: {e}".format(e=entity))
            return None
    
    ############################################################
    # METHODS RELATING TO STATUS AND ATTITUDE
    @classmethod
    def set_init_monster(cls, unique_id: str, room_id: str, status: str, hp: int):
        """Method to set the init status for data objects where 
        no initial value is required"""
        cls.current_target[unique_id] = None
        cls.current_hp[unique_id] = hp
        cls.set_init_room(unique_id, room_id)
        cls.set_init_status(unique_id, status)
    
    @classmethod
    def set_init_npc(cls, npc_data: dict):
        """Method to set the init status for data objects where 
        no initial value is required"""
        cls.current_target[npc_data["id"]] = None
        cls.set_init_status(npc_data["id"], npc_data["status"])
        cls.set_init_attitude(npc_data["id"], npc_data["attitude"])
        
    @classmethod
    def set_init_attitude(cls, entity: str, attitude: str) -> None:
        """Method to set the initial attitude towards player for specifed entity."""
        cls.current_attitude[entity] = Attitude(attitude)
    
    @classmethod
    def set_init_status(cls, entity: str, status: str) -> str:
        """Method to set the initial status for specified entity."""
        cls.current_status[entity] = Status(status)

    @classmethod
    def set_init_room(cls, entity: str, room_id: str) -> str:
        """Method to set the initial room for specified entity."""
        cls.current_room[entity] = room_id
        
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
    def is_dead(cls, entity: str = "player") -> bool:
        """Method to determine whether the specified entity is dead"""
        return cls.get_current_status(entity) == Status("dead")
    
    @classmethod
    def is_hidden(cls, entity: str = "player") -> bool:
        """Method to determine whether the specified entity is hidden"""
        return cls.get_current_status(entity) == Status("hidden")

    @classmethod
    def all_dead(cls, entity: str = "player") -> bool:
        """Method to determine whether all the monsters are dead"""
        count = 0
        dead = 0
        for monster in cls.get_dm().npcs.get_all_monster_ids():
            if cls.get_current_room_id() == cls.get_current_room_id(monster):
                count += 1
                if cls.is_dead(monster):
                    dead += 1
        return count == dead
    
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
        cls.expected_intent = []
    
    @classmethod
    def set_expected_entities(cls, entities: list) -> None:
        """Method to set the expected entities"""
        cls.expected_entities = entities

    @classmethod
    def clear_expected_entities(cls) -> None:
        """Method to clear the expected entities"""
        cls.expected_entities = []
        
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
    
    @classmethod
    def heal(cls, hp: int, hp_max: int = None, entity: str = "player") -> None:
        """Method to heal a number of hit points, up to a max"""
        current_hp = cls.get_current_hp(entity)
        new_hp = current_hp + hp
        if hp_max:
            if new_hp > hp_max:
                hp = hp_max - current_hp
            new_hp = min(hp_max, new_hp) 
        cls.current_hp[entity] = new_hp
        OutputBuilder.append(NLG.heal(hp, new_hp))
    
    @classmethod
    def drink_ale(cls) -> None:
        """Method to drink ale"""
        cls.ales += 1

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

    @classmethod
    def maintain_current_target(cls) -> None:
        """Check if current targets are still valid"""
        for entity in cls.current_target:
            target = cls.get_current_target_id(entity)
            if target:
                if not cls.get_current_room_id(
                        entity) == cls.get_current_room_id(target):
                    cls.clear_target(entity)

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
            if next_value == 4:
                cls.update_initiative_order()
        except KeyError:
            msg = "Entity not recognised: {e}".format(e=entity)
            raise UnrecognisedEntityError(msg)
    
    @classmethod
    def set_initiative_order(cls) -> None:
        """Method to set the initative order"""
        rolls = {}

        # get player initiative
        player_result = State.get_player().initiative_roll()
        OutputBuilder.append(NLG.roll_reaction(player_result))
        rolls["player"] = player_result
        
        # initiative rolls for monsters in the room
        monsters = cls.get_possible_monster_targets()
        for monster in monsters:
            rolls[monster.unique_id] = monster.initiative_roll()
        
        # order the rolls dict and set keys as initiative order
        sorted_rolls = dict(sorted(rolls.items(), key=operator.itemgetter(1), reverse=True))
        cls.initiative_order = list(sorted_rolls.keys())
        
        # set combat status depending on player initiative
        if cls.initiative_order.index("player") == 0:
            # get the target from the player
            cls.set_combat_status(1)
            cls.set_expected_intent(["attack"])
        else:
            # player doesn't go first - wait til their turn
            cls.set_combat_status(4)
            cls.clear_target()
            OutputBuilder.append("You'll have to wait your turn.")
            # don't allow player input
            cls.pause()
    
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
            current_target = cls.get_current_target_id(entity)
            if current_target:
                return cls.get_entity(current_target)
        except UnrecognisedEntityError:
            raise

    @classmethod
    def set_target(cls, target: str, entity: str = "player") -> None:
        """Method to set the current target for an entity"""
        if entity not in cls.current_target:
            msg = "Entity not recognised: {e}".format(e=entity)
            raise UnrecognisedEntityError(msg)

        logger.debug("Setting current target: {t}".format(t=target))
        # first, deregister any triggers from original target
        if cls.get_current_target_id(entity):
            current_target_obj = cls.get_entity(cls.get_current_target_id(entity))
            cls.dm.deregister_trigger(current_target_obj)
            
        # set new target
        cls.current_target[entity] = target
        
        # register any triggers for new target
        target_obj = cls.get_entity(target)
        if hasattr(target_obj, "trigger"):
            cls.dm.register_trigger(target_obj)
        
        # append target to attacked_by_player list
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
                cls.get_entity(cls.get_current_target_id(entity)))
            cls.current_target[entity] = None

    @classmethod
    def was_attacked(cls, monster_id: str) -> bool:
        """Method to determine if monster was attacked by player"""
        return monster_id in cls.attacked_by_player
    
    @classmethod
    def take_damage(cls, damage: int, attacker: str, entity: str = "player") -> int:
        """Method to apply damage to specified entity.
        Returns the updated hp value"""
        try:
            cls.current_hp[entity] = cls.current_hp[entity] - damage
            if cls.current_hp[entity] <= 0:
                if entity == "player":
                    # if the entity is player, this is a gameover state
                    attacker = State.get_entity(attacker)
                    death_text = attacker.text["killed_player"]
                    OutputBuilder.append(NLG.hp_end_game(attacker.unique_name, death_text=death_text))
                    OutputBuilder.append(cls.get_dm().get_bad_ending())
                    dmai.dmai_helpers.gameover()
                else:
                    cls.kill_monster(entity)
                    # deregister triggers
                    if hasattr(State.get_entity(entity), "trigger"):
                        cls.dm.register_trigger(State.get_entity(entity))
            return cls.current_hp[entity]
        except KeyError:
            msg = "Entity not recognised: {e}".format(e=entity)
            raise UnrecognisedEntityError(msg)
    
    @classmethod
    def kill_monster(cls, entity: str) -> None:
        # player has killed a monster
        name = State.get_entity_name(entity)
        OutputBuilder.append("You killed {n}!".format(n=name))
        cls.set_current_status(entity, "dead")
        cls.clear_target()
        cls.initiative_order.remove(entity)
        if len(cls.initiative_order) == 1:
            cls.end_fight()

    @classmethod
    def end_fight(cls) -> None:
        OutputBuilder.append(NLG.won_fight())
        cls.explore()
        
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
            if cls.check_room_exists(room_id):
                return cls.dm.adventure.get_room(room_id).name
        except UnrecognisedRoomError:
            logger.info("Room not recognised: {r}".format(r=room_id))
            raise

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
    def check_room_exists(cls, room_id: str) -> bool:
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
                if cls.check_room_exists(room_id):
                    return cls.dm.adventure.get_room(room_id)
        except (UnrecognisedRoomError, UnrecognisedEntityError):
            raise

    @classmethod
    def set_current_room(cls, entity: str, room_id: str) -> None:
        """Method to set the current room for specified entity."""
        try:
            if cls._check_entity_exists(entity) and cls.check_room_exists(
                    room_id):
                logger.debug("Setting current room for {e}: {r}".format(
                    e=entity, r=room_id))
                if entity == "player":
                    cls.stationary = False
                    cls.current_room[entity] = room_id
                else:
                    cls.current_room[entity] = room_id
        except (UnrecognisedRoomError, UnrecognisedEntityError):
            raise

    @classmethod
    def travel_allowed(cls, current_id: str, destination_id: str) -> bool:
        """Method to determine if travel is allowed between specified rooms."""
        try:
            if cls.check_room_exists(current_id) and cls.check_room_exists(
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
            if cls.check_room_exists(current_id) and cls.check_room_exists(
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
            if cls.check_room_exists(room_id1) and cls.check_room_exists(
                    room_id2) and cls._check_connection_exists(
                        room_id1, room_id2):
                cls._update_connection(room_id1, room_id2, "locked", True)
        except (UnrecognisedRoomError, RoomConnectionError):
            raise

    @classmethod
    def unlock_door(cls, room_id1: str, room_id2: str) -> None:
        """Method to unlock the connection between two given rooms."""
        try:
            if cls.check_room_exists(room_id1) and cls.check_room_exists(
                    room_id2) and cls._check_connection_exists(
                        room_id1, room_id2):
                cls._update_connection(room_id1, room_id2, "locked", False)
        except (UnrecognisedRoomError, RoomConnectionError):
            raise

    @classmethod
    def break_door(cls, room_id1: str, room_id2: str) -> None:
        """Method to break the connection between two given rooms."""
        try:
            if cls.check_room_exists(room_id1) and cls.check_room_exists(
                    room_id2) and cls._check_connection_exists(
                        room_id1, room_id2):
                cls._update_connection(room_id1, room_id2, "broken", True)
        except (UnrecognisedRoomError, RoomConnectionError):
            raise

    @classmethod
    def get_possible_npc_targets(cls, entity: str = "player") -> list:
        """Method to get all npcs in a room that specified entity is in"""
        targets = []
        for npc in cls.get_dm().npcs.get_all_npcs():
            if cls.get_current_room_id(npc.id) == cls.get_current_room_id(entity):
                if cls.is_alive(npc.id):
                    targets.append(npc)
        return targets
    
    @classmethod
    def get_possible_door_targets(cls, entity: str = "player") -> list:
        """Method to get all doors in a room that specified entity is in"""
        targets = []
        for room in cls.get_current_room().get_connected_rooms():
            if not State.travel_allowed(State.get_current_room_id(), room):
                targets.append(room)
        return targets
    
    @classmethod
    def get_formatted_possible_door_targets(cls, entity: str = "player") -> str:
        """Method to return a formatted string of possible door targets"""
        rooms = cls.get_possible_door_targets(entity)
        possible_targets = [State.get_room_name(room) for room in rooms]
        formatted_str = "You could try to find a way to open the door to {a}.".format(a=Text.properly_format_list(possible_targets, delimiter=", the ", last_delimiter=" or the "))
        return formatted_str
    
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
        possible_targets = [monster.unique_name for monster in monsters]
        formatted_str = "You could attack {a}.".format(a=Text.properly_format_list(possible_targets, last_delimiter=" or "))
        return formatted_str
    
    @classmethod
    def get_monster_status_summary(cls, location: str) -> dict:
        """Method to return a dictionary of monster status of specified location"""
        monster_status = {"alive": [], "dead": []}
        for monster in cls.get_dm().npcs.get_all_monsters():
            if cls.get_current_room_id(monster.unique_id) == location:
                if cls.is_alive(monster.unique_id):
                    monster_status["alive"].append(monster.name)
                elif cls.is_dead(monster.unique_id):
                    monster_status["dead"].append(monster.name)
        status_count = {}
        for status in monster_status:
            status_count[status] = dict(Counter(monster_status[status]))
        return status_count
    
    @classmethod
    def get_formatted_monster_status_summary(cls, location: str) -> str:
        """Method to return a formatted string of monster status of specified location"""
        monster_status = cls.get_monster_status_summary(location)
        # format alive monsters
        formatted_monsters = {"alive": [], "dead": []}
        for status in monster_status:
            for monster in monster_status[status]:
                count = monster_status[status][monster]
                if count > 1:
                    formatted_monsters[status].append("{c} {m}s".format(c=count, m=monster))
                else:
                    formatted_monsters[status].append("a {m}".format(c=count, m=monster))
                  
        if monster_status["alive"] and monster_status["dead"]:
            summary = "We've got {a} alive and {d} dead.".format(
                a=Text.properly_format_list(formatted_monsters["alive"]),
                d=Text.properly_format_list(formatted_monsters["dead"]))
        elif monster_status["alive"]:
            summary = "We've got {a} alive.".format(
                a=Text.properly_format_list(formatted_monsters["alive"]))
        elif monster_status["dead"]:
            summary = "We've got {d} that's dead.".format(
                d=Text.properly_format_list(formatted_monsters["dead"]))
        else:
            summary = ""

        return summary
        
    ############################################################
    # METHODS RELATING TO COMBAT WITH DOORS
    @classmethod
    def take_door_damage(cls, damage: int, target: str, attacker: str = "player") -> int:
        """Method to apply damage to specified door target.
        Returns the updated hp value"""
        try:
            original_hp = cls.current_hp_door[target]
            cls.current_hp_door[target] = cls.current_hp_door[target] - damage
            if cls.current_hp_door[target] <= 0:
                # this destroys the door and unlocks the way
                cls.in_combat_with_door = False
                cls.unlock_door(cls.get_current_room_id(), target)
                OutputBuilder.append(NLG.broke_down_door(State.get_room_name(target)))
            else:
                OutputBuilder.append(NLG.deal_door_damage(damage, original_hp))
            return cls.current_hp_door[target]
        except KeyError:
            msg = "Room not recognised: {e}".format(e=target)
            raise UnrecognisedRoomError(msg)
    
    @classmethod
    def get_door_armor_class(cls, room: str, door: str) -> int:
        """Method to get a specified door's armor class"""
        return cls.get_dm().adventure.get_room(room).get_door_armor_class(door)
    
    @classmethod
    def get_door_hp(cls, door: str) -> int:
        """Method to get a specified door's hp"""
        return cls.current_hp_door[door]

    ############################################################
    # METHODS RELATING TO ABILITY AND SKILL CHECKS
    @classmethod
    def set_ability_check(cls, target: dict) -> None:
        """Method to set the ability check target, where the target is a dict:
        {target: id, puzzle: id, solution: id, success_func: func, success_params: list}"""
        cls.stored_ability_check = target
    
    @classmethod
    def clear_ability_check(cls) -> None:
        """Method to clear the ability check target"""
        cls.stored_ability_check = None
    
    @classmethod
    def set_skill_check(cls, target: dict) -> None:
        """Method to set the skill check target, where the target is a dict:
        {target: id, puzzle: id, solution: id, success_func: func, success_params: list}"""
        cls.stored_skill_check = target
    
    @classmethod
    def clear_skill_check(cls) -> None:
        """Method to clear the skill check target"""
        cls.stored_skill_check = None
        