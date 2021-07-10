from collections import Counter
from enum import Enum
import operator

from dmai.utils.text import Text
from dmai.utils.output_builder import OutputBuilder
from dmai.utils.exceptions import UnrecognisedEntityError, UnrecognisedRoomError, RoomConnectionError
from dmai.nlg.nlg import NLG
from dmai.utils.logger import get_logger
import dmai

logger = get_logger(__name__)


class Session(object):
    session_id = ""
    def set_session_id(self, session_id: str) -> None:
        self.session_id = session_id


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


class State():

    # initialise session
    session = Session()

    # class variables
    dm = None
    player = None

    # class state variables
    intro_read = False
    char_class = None
    char_name = None
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
    # puzzle triggers
    puzzle_trigger_map = {}
    solved_puzzles = []
    # monster triggers
    monster_trigger_map = {}
    # room triggers
    room_trigger_map = {}
    visited_rooms = []
    # treasure
    room_treasure_map = {}
    monster_treasure_map = {}

    def __init__(self, output_builder: OutputBuilder, session_id: str = "") -> None:
        """Main class for the game state"""
        self.session.set_session_id(session_id)
        self.output_builder = output_builder
    
    def set_char_class(self, char_class: str) -> None:
        self.char_class = char_class

    def set_char_name(self, char_name: str) -> None:
        self.char_name = char_name

    def save(self) -> dict:
        """Method to save the game state to dict"""
        return self.__dict__
    
    def load(self, saved_state: dict) -> None:
        """Method to load the game state"""
        self.__dict__ = saved_state
        
    def combat(self, attacker: str, target: str) -> None:
        if not self.in_combat:
            self.reset_combat_status()
            self.set_current_game_mode("combat")
            self.in_combat = True
            self.roleplaying = False
            self.in_combat_with_door = False
            self.set_target(target, attacker)
            self.clear_conversation()
            self.set_expected_entities(["monster"])
            self.set_expected_intent(["roll"])
            self.clear_expected_entities()
            self.output_builder.append(NLG.transition_to_combat())
        else:
            self.set_target(target, attacker)
            self.set_expected_intent(["roll"])
            self.output_builder.append(NLG.perform_attack_roll())
            self.progress_combat_status()
                
    
    def combat_with_door(self, target: str) -> None:
        self.door_target = target
        if not self.in_combat_with_door:
            self.in_combat_with_door = True
            self.in_combat = False
            self.roleplaying = False
            self.clear_expected_entities()
            self.set_combat_status(3)
            self.output_builder.append(NLG.perform_attack_roll())
        else:
            self.set_combat_status(3)
            self.output_builder.append(NLG.perform_attack_roll())

    
    def explore(self) -> None:
        if self.current_game_mode != GameMode.EXPLORE:
            self.set_current_game_mode("explore")
            self.in_combat = False
            self.roleplaying = False
            self.initiative_order = []
            self.clear_target()
            self.clear_conversation()
            self.clear_expected_intent()
            self.clear_expected_entities()
            self.door_target = None

    
    def roleplay(self, target: str) -> None:
        if not self.roleplaying:
            self.set_current_game_mode("roleplay")
            self.in_combat = False
            self.roleplaying = True
            self.initiative_order = []
            self.clear_target()
            self.set_conversation_target(target)
            self.clear_expected_intent()
            self.clear_expected_entities()
            self.door_target = None

    
    def set_current_game_mode(self, game_mode: str) -> None:
        """Method to set the current game mode."""
        self.current_game_mode = GameMode(game_mode)
    
    
    def set_current_goal(self, goal: tuple) -> None:
        """Method to set the current goal"""
        self.current_goal = goal

    def skip_intro(self) -> None:
        self.intro_read = True
    
    def start(self) -> None:
        self.started = True

    
    def pause(self) -> None:
        self.paused = True

    
    def play(self) -> None:
        self.paused = False

    
    def received_quest(self) -> None:
        self.quest_received = True
    
    
    def quest(self) -> None:
        self.questing = True
    
    
    def complete_quest(self) -> None:
        self.complete = True

    
    def talk(self) -> None:
        self.talking = True

    
    def stop_talking(self) -> None:
        self.talking = False

    
    def set_dm(self, dm) -> None:
        logger.debug("Setting DM")
        self.dm = dm
        init_room = self.dm.adventure.get_init_room()
        self.current_room["player"] = init_room
        for room in self.dm.adventure.get_all_rooms():
            for connected_room in room.get_connected_rooms():
                if room.can_attack_door(connected_room):
                    self.current_hp_door[connected_room] = room.get_door_hp(connected_room)
        
        # register room triggers
        for room in self.dm.adventure.get_all_rooms():
             if hasattr(room, "trigger"):
                self.dm.register_trigger(room)
        # register monster triggers
        for monster in self.dm.npcs.get_all_monsters():
            if hasattr(monster, "trigger"):
                self.dm.register_trigger(monster)
        # register npc triggers
        for npc in self.dm.npcs.get_all_npcs():
            if hasattr(npc, "trigger"):
                self.dm.register_trigger(npc)

    
    def get_dm(self) -> None:
        """Method to return dm"""
        return self.dm

    
    def set_player(self, player) -> None:
        self.player = player
        self.current_hp["player"] = player.character.hp_max
        self.current_status["player"] = Status.ALIVE
        self.current_target["player"] = None
        self.current_combat_status["player"] = Combat.INITIATIVE
        self.char_class = player.character.char_class

    
    def get_player(self):
        """Method to return player"""
        return self.player
    
    
    def get_entity_name(self, entity: str = "player") -> str:
        """Method to return name of entity"""
        try:
            if entity == "player":
                return self.char_name
            else:
                if hasattr(self.get_dm().npcs.get_entity(entity), "unique_name"):
                    return self.get_dm().npcs.get_entity(entity).unique_name
                else:
                    return self.get_dm().npcs.get_entity(entity).name
        except UnrecognisedEntityError:
            logger.debug("Unrecognised entity: {e}".format(e=entity))
            return ""
    
    
    def get_entity(self, entity: str = "player"):
        """Method to return entity"""
        try:
            if entity == "player":
                return self.get_player()
            else:
                return self.get_dm().npcs.get_entity(entity)
        except UnrecognisedEntityError:
            logger.debug("Unrecognised entity: {e}".format(e=entity))
            return None
    
    ############################################################
    # METHODS RELATING TO STATUS AND ATTITUDE
    
    def set_init_monster(self, unique_id: str, room_id: str, status: str, hp: int):
        """Method to set the init status for data objects where 
        no initial value is required"""
        self.current_target[unique_id] = None
        self.current_hp[unique_id] = hp
        self.set_init_room(unique_id, room_id)
        self.set_init_status(unique_id, status)
    
    
    def set_init_npc(self, npc_data: dict):
        """Method to set the init status for data objects where 
        no initial value is required"""
        self.current_target[npc_data["id"]] = None
        self.set_init_status(npc_data["id"], npc_data["status"])
        self.set_init_attitude(npc_data["id"], npc_data["attitude"])
        
    
    def set_init_attitude(self, entity: str, attitude: str) -> None:
        """Method to set the initial attitude towards player for specifed entity."""
        self.current_attitude[entity] = Attitude(attitude)
    
    
    def set_init_status(self, entity: str, status: str) -> str:
        """Method to set the initial status for specified entity."""
        self.current_status[entity] = Status(status)

    
    def set_init_room(self, entity: str, room_id: str) -> str:
        """Method to set the initial room for specified entity."""
        self.current_room[entity] = room_id
        
    
    def get_current_hp(self, entity: str = "player") -> int:
        """Method to get the current hp for specified entity."""
        try:
            return self.current_hp[entity]
        except KeyError:
            msg = "Entity not recognised: {e}".format(e=entity)
            raise UnrecognisedEntityError(msg)

    
    def set_current_status(self, entity: str = "player", status: str = "alive") -> str:
        """Method to set the current status for specified entity."""
        try:
            self.current_status[entity] = Status(status)
        except KeyError:
            msg = "Entity not recognised: {e}".format(e=entity)
            raise UnrecognisedEntityError(msg)

    
    def get_current_status(self, entity: str = "player") -> str:
        """Method to get the current status for specified entity."""
        try:
            return self.current_status[entity]
        except KeyError:
            msg = "Entity not recognised: {e}".format(e=entity)
            raise UnrecognisedEntityError(msg)

    
    def is_alive(self, entity: str = "player") -> bool:
        """Method to determine whether the specified entity is alive"""
        return self.get_current_status(entity) == Status("alive")
    
    
    def is_dead(self, entity: str = "player") -> bool:
        """Method to determine whether the specified entity is dead"""
        return self.get_current_status(entity) == Status("dead")
    
    
    def is_hidden(self, entity: str = "player") -> bool:
        """Method to determine whether the specified entity is hidden"""
        return self.get_current_status(entity) == Status("hidden")

    
    def all_dead(self, entity: str = "player") -> bool:
        """Method to determine whether all the monsters are dead"""
        count = 0
        dead = 0
        for monster in self.get_dm().npcs.get_all_monster_ids():
            if self.get_current_room_id() == self.get_current_room_id(monster):
                count += 1
                if self.is_dead(monster):
                    dead += 1
        return count == dead
    
    
    def set_current_attitude(self, entity: str = "player", attitude: str = "indifferent") -> str:
        """Method to set the current attitude towards player for specified entity."""
        try:
            self.current_attitude[entity] = Attitude(attitude)
        except KeyError:
            msg = "Entity not recognised: {e}".format(e=entity)
            raise UnrecognisedEntityError(msg)

    
    def get_current_attitude(self, entity: str = "player") -> str:
        """Method to get the current attitude towards player for specified entity."""
        try:
            return self.current_attitude[entity]
        except KeyError:
            msg = "Entity not recognised: {e}".format(e=entity)
            raise UnrecognisedEntityError(msg)
    
    
    def set_expected_intent(self, intent: str) -> None:
        """Method to set the expected intent"""
        self.expected_intent = intent

    
    def clear_expected_intent(self) -> None:
        """Method to clear the expected intent"""
        self.expected_intent = []
    
    
    def set_expected_entities(self, entities: list) -> None:
        """Method to set the expected entities"""
        self.expected_entities = entities

    
    def clear_expected_entities(self) -> None:
        """Method to clear the expected entities"""
        self.expected_entities = []
        
    ############################################################
    # METHODS RELATING TO CONVERSATION
    
    def set_conversation_target(self, target: str) -> None:
        """Method to set the current target for a conversation"""
        logger.debug("Setting current conversation target: {t}".format(t=target))
        self.current_conversation = target

    
    def clear_conversation(self, entity: str = "player") -> None:
        """Method to clear the conversation for an entity"""
        logger.debug("Clearing current conversation")
        self.current_conversation = None

    ############################################################
    # METHODS RELATING TO ACTIONS
    
    def light_torch(self) -> None:
        """Method to light a torch"""
        self.torch_lit = True
        self.output_builder.append(NLG.light_torch())

    
    def extinguish_torch(self) -> None:
        """Method to extinguish a torch"""
        self.torch_lit = False
        self.output_builder.append(NLG.extinguish_torch())
    
    
    def heal(self, hp: int, hp_max: int = None, entity: str = "player") -> None:
        """Method to heal a number of hit points, up to a max"""
        current_hp = self.get_current_hp(entity)
        new_hp = current_hp + hp
        if hp_max:
            if new_hp > hp_max:
                hp = hp_max - current_hp
            new_hp = min(hp_max, new_hp) 
        self.current_hp[entity] = new_hp
        self.output_builder.append(NLG.heal(hp, new_hp, self.player.character_class))
    
    
    def drink_ale(self) -> None:
        """Method to drink ale"""
        self.ales += 1

    ############################################################
    # METHODS RELATING TO INTENTS
    
    def clear_intent(self, ) -> None:
        """Method to clear the stored intent"""
        self.stored_intent = {}

    
    def store_intent(self, intent: str, params: dict) -> None:
        """Method to set the stored intent"""
        self.stored_intent = {"intent": intent, "params": params}
    
    
    def set_intent(self, intent: str) -> None:
        """Method to set the current intent"""
        self.current_intent = intent

    ############################################################
    # METHODS RELATING TO STATE MAINTENANCE
    
    def maintenance(self) -> None:
        """Method to maintain the state correctly"""
        self.maintain_current_target()

    
    def maintain_current_target(self) -> None:
        """Check if current targets are still valid"""
        for entity in self.current_target:
            target = self.get_current_target_id(entity)
            if target:
                if not self.get_current_room_id(
                        entity) == self.get_current_room_id(target):
                    self.clear_target(entity)

    ############################################################
    # METHODS RELATING TO COMBAT
    
    def get_combat_status(self, entity: str = "player") -> Combat:
        """Method to set the combat status for specified entity."""
        try:
            return self.current_combat_status[entity]
        except KeyError:
            msg = "Entity not recognised: {e}".format(e=entity)
            raise UnrecognisedEntityError(msg)
        
    
    def set_combat_status(self, status: int, entity: str = "player") -> None:
        """Method to set the combat status for specified entity."""
        self.current_combat_status[entity] = Combat(status)
    
    
    def reset_combat_status(self, entity: str = "player") -> None:
        """Method to set the combat status for specified entity."""
        self.current_combat_status[entity] = Combat(0)
    
    
    def progress_combat_status(self, entity: str = "player", can_reset: bool = False) -> str:
        """Method to progress the combat status for specified entity."""
        try:
            next_value = self.current_combat_status[entity].value + 1
            max_value = max([e.value for e in Combat])
            if next_value > max_value:
                next_value = 0 if can_reset else 1
            self.set_combat_status(next_value, entity)
            if next_value == 4:
                self.update_initiative_order()
        except KeyError:
            msg = "Entity not recognised: {e}".format(e=entity)
            raise UnrecognisedEntityError(msg)
    
    
    def set_initiative_order(self) -> None:
        """Method to set the initative order"""
        rolls = {}

        # get player initiative
        player_result = self.get_player().initiative_roll()
        self.output_builder.append(NLG.roll_reaction(player_result))
        rolls["player"] = player_result
        
        # initiative rolls for monsters in the room
        monsters = self.get_possible_monster_targets()
        for monster in monsters:
            rolls[monster.unique_id] = monster.initiative_roll()
        
        # order the rolls dict and set keys as initiative order
        sorted_rolls = dict(sorted(rolls.items(), key=operator.itemgetter(1), reverse=True))
        self.initiative_order = list(sorted_rolls.keys())
        
        # set combat status depending on player initiative
        if self.initiative_order.index("player") == 0:
            # get the target from the player
            self.set_combat_status(1)
            self.set_expected_intent(["attack"])
        else:
            # player doesn't go first - wait til their turn
            self.set_combat_status(4)
            self.clear_target()
            self.output_builder.append("You'll have to wait your turn.")
            # don't allow player input
            self.pause()
    
    
    def update_initiative_order(self, *args) -> None:
        """Method to update the initiative order by popping from front of list
        and appending to end"""
        logger.debug("Updating initiative order")
        self.initiative_order.append(self.initiative_order.pop(0))
    
    
    def get_currently_acting_entity(self) -> str:
        """Method to return the id of the entity at the front of the initiative
        order"""
        return self.initiative_order[0]
        
    
    def get_current_target_id(self, entity: str = "player") -> str:
        """Method to get the current target id for specified entity."""
        try:
            return self.current_target[entity]
        except KeyError:
            msg = "Entity not recognised: {e}".format(e=entity)
            raise UnrecognisedEntityError(msg)

    
    def get_current_target(self, entity: str = "player"):
        """Method to get the current target for specified entity."""
        try:
            current_target = self.get_current_target_id(entity)
            if current_target:
                return self.get_entity(current_target)
        except UnrecognisedEntityError:
            raise

    
    def set_target(self, target: str, entity: str = "player") -> None:
        """Method to set the current target for an entity"""
        if entity not in self.current_target:
            msg = "Entity not recognised: {e}".format(e=entity)
            raise UnrecognisedEntityError(msg)

        logger.debug("Setting current target: {t}".format(t=target))
        # first, deregister any triggers from original target
        if self.get_current_target_id(entity):
            current_target_obj = self.get_entity(self.get_current_target_id(entity))
            self.dm.deregister_trigger(current_target_obj)
            
        # set new target
        self.current_target[entity] = target
        
        # register any triggers for new target
        target_obj = self.get_entity(target)
        if hasattr(target_obj, "trigger"):
            self.dm.register_trigger(target_obj)
        
        # append target to attacked_by_player list
        if target != "player" and target not in self.attacked_by_player:
            self.attacked_by_player.append(target)

    
    def clear_target(self, entity: str = "player") -> None:
        """Method to clear the target for an entity"""
        if entity not in self.current_target:
            msg = "Entity not recognised: {e}".format(e=entity)
            raise UnrecognisedEntityError(msg)

        logger.debug("Clearing current target")
        if self.get_current_target_id(entity):
            self.dm.deregister_trigger(
                self.get_entity(self.get_current_target_id(entity)))
            self.current_target[entity] = None

    
    def was_attacked(self, monster_id: str) -> bool:
        """Method to determine if monster was attacked by player"""
        return monster_id in self.attacked_by_player
    
    
    def take_damage(self, damage: int, attacker: str, entity: str = "player") -> int:
        """Method to apply damage to specified entity.
        Returns the updated hp value"""
        try:
            self.current_hp[entity] = self.current_hp[entity] - damage
            if self.current_hp[entity] <= 0:
                if entity == "player":
                    # if the entity is player, this is a gameover state
                    attacker = self.get_entity(attacker)
                    death_text = attacker.text["killed_player"]
                    self.output_builder.append(NLG.hp_end_game(attacker.unique_name, death_text=death_text))
                    self.output_builder.append(self.get_dm().get_bad_ending())
                    dmai.dmai_helpers.gameover(self.output_builder)
                else:
                    self.kill_monster(entity)
                    # deregister triggers
                    if hasattr(self.get_entity(entity), "trigger"):
                        self.dm.register_trigger(self.get_entity(entity))
            return self.current_hp[entity]
        except KeyError:
            msg = "Entity not recognised: {e}".format(e=entity)
            raise UnrecognisedEntityError(msg)
    
    
    def kill_monster(self, entity: str) -> None:
        # player has killed a monster
        name = self.get_entity_name(entity)
        self.output_builder.append("You killed {n}!".format(n=name))
        self.set_current_status(entity, "dead")
        self.clear_target()
        self.initiative_order.remove(entity)
        if len(self.initiative_order) == 1:
            self.end_fight()

    
    def end_fight(self) -> None:
        self.output_builder.append(NLG.won_fight())
        self.explore()
    
    def declare_attack_against_player(self, attacker: str, target: str, *args) -> None:
        """Method to declare attack against player"""
        self.set_target(target, attacker)
        attacker = self.get_entity_name(attacker)
        self.output_builder.append(NLG.attack(attacker, target))
    
    def attack_roll(self, attacker: str, weapon: str, target: str, *args) -> None:
        """Method to perform an attack roll"""
        # TODO implement advantage/disadvantage
        attacker = self.get_entity(attacker)
        target = self.get_entity(target)
        if attacker.attack_roll(weapon) >= target.armor_class:
            self.output_builder.append("{a} hits!".format(a=attacker.unique_name))
        else:
            self.output_builder.append("{a} misses!".format(a=attacker.unique_name))
            self.update_initiative_order()
        return
    
    def damage_roll(self, attacker: str, weapon: str, target: str, *args) -> None:
        """Method to perform a damage roll"""
        attacker = self.get_entity(attacker)
        target = self.get_entity(target)
        damage = attacker.damage_roll(weapon)
        hp = self.take_damage(damage, attacker.unique_id)
        if target == self.get_player():
            self.output_builder.append(NLG.health_update(hp, hp_max=target.hp_max))
        return
        
    ############################################################
    # METHODS RELATING TO LOCATION
    
    def halt(self) -> None:
        """Method to set stationary to true"""
        self.stationary = True
    
    
    def get_room_name(self, room_id: str) -> str:
        """Method to return the name of a room."""
        try:
            if self.check_room_exists(room_id):
                return self.dm.adventure.get_room(room_id).name
        except UnrecognisedRoomError:
            logger.info("Room not recognised: {r}".format(r=room_id))
            raise

    
    def _check_entity_exists(self, entity_id: str) -> bool:
        """Method to check entity exists.
        Raises UnrecognisedEntityError exception if not"""
        try:
            return bool(self.current_room[entity_id])
        except KeyError:
            msg = "Entity not recognised: {e}".format(e=entity_id)
            raise UnrecognisedEntityError(msg)

    
    def check_room_exists(self, room_id: str) -> bool:
        """Method to check room exists.
        Raises UnrecognisedRoomError exception if not"""
        try:
            return bool(self.dm.adventure.get_room(room_id))
        except UnrecognisedRoomError:
            raise

    
    def _check_connection_exists(self, room_id1: str, room_id2: str) -> bool:
        """Method to check connection exists.
        Raises UnrecognisedRoomError exception if not"""
        r1, r2 = "", ""
        try:
            for (r1, r2) in [(room_id1, room_id2), (room_id2, room_id1)]:
                self.dm.adventure.rooms[r1].connections[r2]
            return True
        except KeyError:
            msg = "Connection does not exist: {r1}-{r2}".format(r1=r1, r2=r2)
            raise RoomConnectionError(msg)

    
    def get_current_room_id(self, entity: str = "player") -> str:
        """Method to get the current room id for specified entity."""
        try:
            if self._check_entity_exists(entity):
                return self.current_room[entity]
        except UnrecognisedEntityError:
            raise

    
    def get_current_room(self, entity: str = "player"):
        """Method to get the current room for specified entity."""
        try:
            if self._check_entity_exists(entity):
                room_id = self.get_current_room_id(entity)
                if self.check_room_exists(room_id):
                    return self.dm.adventure.get_room(room_id)
        except (UnrecognisedRoomError, UnrecognisedEntityError):
            raise

    
    def set_current_room(self, entity: str, room_id: str) -> None:
        """Method to set the current room for specified entity."""
        try:
            if self._check_entity_exists(entity) and self.check_room_exists(
                    room_id):
                logger.debug("Setting current room for {e}: {r}".format(
                    e=entity, r=room_id))
                if entity == "player":
                    self.stationary = False
                    self.current_room[entity] = room_id
                else:
                    self.current_room[entity] = room_id
        except (UnrecognisedRoomError, UnrecognisedEntityError):
            raise

    
    def travel_allowed(self, current_id: str, destination_id: str) -> bool:
        """Method to determine if travel is allowed between specified rooms."""
        try:
            if self.check_room_exists(current_id) and self.check_room_exists(
                    destination_id) and self._check_connection_exists(
                        current_id, destination_id):
                current = self.dm.adventure.get_room(current_id)
                return current.connections[destination_id][
                    "broken"] or not current.connections[destination_id][
                        "locked"]
        except UnrecognisedRoomError:
            raise
        except RoomConnectionError:
            return False

    
    def connection_broken(self, current_id: str, destination_id: str) -> bool:
        """Method to determine if connection between specified rooms is broken."""
        try:
            if self.check_room_exists(current_id) and self.check_room_exists(
                    destination_id) and self._check_connection_exists(
                        current_id, destination_id):
                current = self.dm.adventure.rooms[current_id]
                return current.connections[destination_id]["broken"]
        except UnrecognisedRoomError:
            raise
        except RoomConnectionError:
            return False

    
    def _update_connection(self, r1: str, r2: str, status: str,
                           state: bool) -> None:
        self.dm.adventure.rooms[r1].connections[r2][status] = state
        self.dm.adventure.rooms[r2].connections[r1][status] = state

    
    def lock_door(self, room_id1: str, room_id2: str) -> None:
        """Method to lock the connection between two given rooms."""
        try:
            if self.check_room_exists(room_id1) and self.check_room_exists(
                    room_id2) and self._check_connection_exists(
                        room_id1, room_id2):
                self._update_connection(room_id1, room_id2, "locked", True)
        except (UnrecognisedRoomError, RoomConnectionError):
            raise

    
    def unlock_door(self, room_id1: str, room_id2: str) -> None:
        """Method to unlock the connection between two given rooms."""
        try:
            if self.check_room_exists(room_id1) and self.check_room_exists(
                    room_id2) and self._check_connection_exists(
                        room_id1, room_id2):
                self._update_connection(room_id1, room_id2, "locked", False)
        except (UnrecognisedRoomError, RoomConnectionError):
            raise

    
    def break_door(self, room_id1: str, room_id2: str) -> None:
        """Method to break the connection between two given rooms."""
        try:
            if self.check_room_exists(room_id1) and self.check_room_exists(
                    room_id2) and self._check_connection_exists(
                        room_id1, room_id2):
                self._update_connection(room_id1, room_id2, "broken", True)
        except (UnrecognisedRoomError, RoomConnectionError):
            raise

    
    def get_possible_npc_targets(self, entity: str = "player") -> list:
        """Method to get all npcs in a room that specified entity is in"""
        targets = []
        for npc in self.get_dm().npcs.get_all_npcs():
            if self.get_current_room_id(npc.id) == self.get_current_room_id(entity):
                if self.is_alive(npc.id):
                    targets.append(npc)
        return targets
    
    
    def get_possible_door_targets(self, entity: str = "player") -> list:
        """Method to get all doors in a room that specified entity is in"""
        targets = []
        for room in self.get_current_room().get_connected_rooms():
            if not self.travel_allowed(self.get_current_room_id(), room):
                targets.append(room)
        return targets
    
    
    def get_formatted_possible_door_targets(self, entity: str = "player") -> str:
        """Method to return a formatted string of possible door targets"""
        rooms = self.get_possible_door_targets(entity)
        possible_targets = [self.get_room_name(room) for room in rooms]
        formatted_str = "You could try to find a way to open the door to {a}.".format(a=Text.properly_format_list(possible_targets, delimiter=", the ", last_delimiter=" or the "))
        return formatted_str
    
    
    def get_possible_monster_targets(self, entity: str = "player") -> list:
        """Method to get all monsters in a room that specified entity is in"""
        targets = []
        for monster in self.get_dm().npcs.get_all_monsters():
            if self.get_current_room_id(monster.unique_id) == self.get_current_room_id(entity):
                if self.is_alive(monster.unique_id):
                    targets.append(monster)
        return targets
    
    
    def get_formatted_possible_monster_targets(self, entity: str = "player") -> str:
        """Method to return a formatted string of possible monster targets"""
        monsters = self.get_possible_monster_targets(entity)
        possible_targets = [monster.unique_name for monster in monsters]
        formatted_str = "You could attack {a}.".format(a=Text.properly_format_list(possible_targets, last_delimiter=" or "))
        return formatted_str
    
    
    def get_monster_status_summary(self, location: str) -> dict:
        """Method to return a dictionary of monster status of specified location"""
        monster_status = {"alive": [], "dead": []}
        for monster in self.get_dm().npcs.get_all_monsters():
            if self.get_current_room_id(monster.unique_id) == location:
                if self.is_alive(monster.unique_id):
                    monster_status["alive"].append(monster.name)
                elif self.is_dead(monster.unique_id):
                    monster_status["dead"].append(monster.name)
        status_count = {}
        for status in monster_status:
            status_count[status] = dict(Counter(monster_status[status]))
        return status_count
    
    
    def get_formatted_monster_status_summary(self, location: str) -> str:
        """Method to return a formatted string of monster status of specified location"""
        monster_status = self.get_monster_status_summary(location)
        # format alive monsters
        formatted_monsters = {"alive": [], "dead": []}
        for status in monster_status:
            for monster in monster_status[status]:
                count = monster_status[status][monster]
                if count > 1:
                    formatted_monsters[status].append("{c} {s} {m}s".format(c=count, s=status, m=monster))
                else:
                    formatted_monsters[status].append("a {s} {m}".format(s=status, m=monster))
                  
        if monster_status["alive"] and monster_status["dead"]:
            summary = "We've got {a} alive and {d} dead.".format(
                a=Text.properly_format_list(formatted_monsters["alive"]),
                d=Text.properly_format_list(formatted_monsters["dead"]))
        elif monster_status["alive"]:
            summary = "We've got {a}.".format(
                a=Text.properly_format_list(formatted_monsters["alive"]))
        elif monster_status["dead"]:
            summary = "We've got {d}.".format(
                d=Text.properly_format_list(formatted_monsters["dead"]))
        else:
            summary = ""

        return summary
        
    ############################################################
    # METHODS RELATING TO COMBAT WITH DOORS
    
    def take_door_damage(self, damage: int, target: str, attacker: str = "player") -> int:
        """Method to apply damage to specified door target.
        Returns the updated hp value"""
        try:
            original_hp = self.current_hp_door[target]
            self.current_hp_door[target] = self.current_hp_door[target] - damage
            if self.current_hp_door[target] <= 0:
                # this destroys the door and unlocks the way
                self.in_combat_with_door = False
                self.unlock_door(self.get_current_room_id(), target)
                self.output_builder.append(NLG.broke_down_door(self.get_room_name(target)))
            else:
                self.output_builder.append(NLG.deal_door_damage(damage, original_hp))
            return self.current_hp_door[target]
        except KeyError:
            msg = "Room not recognised: {e}".format(e=target)
            raise UnrecognisedRoomError(msg)
    
    
    def get_door_armor_class(self, room: str, door: str) -> int:
        """Method to get a specified door's armor class"""
        return self.get_dm().adventure.get_room(room).get_door_armor_class(door)
    
    
    def get_door_hp(self, door: str) -> int:
        """Method to get a specified door's hp"""
        return self.current_hp_door[door]

    ############################################################
    # METHODS RELATING TO ABILITY AND SKILL CHECKS
    
    def set_ability_check(self, target: dict) -> None:
        """Method to set the ability check target, where the target is a dict:
        {target: id, puzzle: id, solution: id, success_func: func, success_params: list}"""
        self.stored_ability_check = target
    
    
    def clear_ability_check(self) -> None:
        """Method to clear the ability check target"""
        self.stored_ability_check = None
    
    
    def set_skill_check(self, target: dict) -> None:
        """Method to set the skill check target, where the target is a dict:
        {target: id, puzzle: id, solution: id, success_func: func, success_params: list}"""
        self.stored_skill_check = target
    
    
    def clear_skill_check(self) -> None:
        """Method to clear the skill check target"""
        self.stored_skill_check = None
        