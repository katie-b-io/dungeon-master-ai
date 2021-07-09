from dmai.utils.output_builder import OutputBuilder
from dmai.domain.actions.investigate import Investigate
from dmai.utils.loader import Loader
from dmai.utils.exceptions import UnrecognisedRoomError, UnrecognisedEquipment, UnrecognisedWeapon, UnrecognisedEntityError, UnrecognisedItem
from dmai.game.state import State
from dmai.game.adventure import Adventure
from dmai.nlg.nlg import NLG
from dmai.domain.actions.attack import Attack
from dmai.domain.actions.attack_door import AttackDoor
from dmai.domain.actions.ability_check import AbilityCheck
from dmai.domain.actions.roll import Roll
from dmai.domain.actions.pick_up import PickUp
import dmai


class Actions:

    # class variables
    action_data = dict()
    state = None

    def __init__(self, adventure: Adventure, npcs, state: State, output_builder: OutputBuilder) -> None:
        """Actions class"""
        self.adventure = adventure
        self.npcs = npcs
        self.state = state
        self.output_builder = output_builder
        self.actions = dict()
        self._load_action_data()

    def __repr__(self) -> str:
        return "Actions:\n{a}".format(a=self.actions)

    @classmethod
    def _load_action_data(cls) -> None:
        """Set the cls.action_data class variable data"""
        cls.action_data = Loader.load_domain("actions")

    def _can_move(self, entity: str, destination: str) -> tuple:
        """Check if an entity can be moved to a specified destination.
        Returns tuple (bool, str) to indicate whether movement is possible
        and reason why not if not."""
        try:
            # check if destination is accessible
            current = self.state.get_current_room(entity)
            if current.id == destination:
                return (False, "same")
            
            # check if travel is allowed
            if self.state.travel_allowed(current.id, destination):

                # can't move if can't see
                if not current.visibility:
                    if not self.state.torch_lit or self.state.get_player(
                    ).character.has_darkvision():
                        return (False, "no visibility")
                
                # can't move if in a room with monsters that must be killed
                for monster in self.state.get_dm().npcs.get_all_monsters():
                    if monster.must_kill and self.state.is_alive(monster.unique_id):
                        if self.state.get_current_room_id() == self.state.get_current_room_id(monster.unique_id):
                            return (False, "must kill")
                
                # can't move without quest
                if not self.state.questing:
                    return (False, "no quest")

                # none of the above situations were triggered so allow travel
                return (True, "")
            
            else:
                if destination in self.state.get_current_room().get_connected_rooms():
                    return (False, "locked")
                else:
                    return (False, "not connected")
        except UnrecognisedRoomError:
            return (False, "unknown destination")
        except UnrecognisedEntityError:
            return (False, "unknown entity")

    def move(self, entity: str, destination: str) -> bool:
        """Attempt to move an entity to the specified destination.
        Returns a bool to indicate whether the action was successful"""
        
        # check if entity can move
        (can_move, reason) = self._can_move(entity, destination)
        if can_move:
            self.state.explore()
            self.state.clear_skill_check()
            self.state.set_current_room(entity, destination)
        else:
            try:
                destination = self.state.get_room_name(destination)
            except UnrecognisedRoomError:
                pass
            connected_rooms = self.state.get_current_room().get_connected_rooms()
            if reason == "locked":
                possible_destinations = [self.state.get_room_name(room) for room in connected_rooms if self.state.travel_allowed(self.state.get_current_room_id(), room)]
            else:
                possible_destinations = [self.state.get_room_name(room) for room in connected_rooms]
            self.output_builder.append(NLG.cannot_move(destination, reason, possible_destinations))
        return can_move

    def attack(self, attacker: str, target: str) -> bool:
        """Attempt to attack a specified target.
        Returns a bool to indicate whether the action was successful"""
        attack = Attack(attacker, target, self.state, self.output_builder)
        return attack.execute()

    def attack_door(self, attacker: str, location: str) -> bool:
        """Attempt to attack a door at specified location.
        Returns a bool to indicate whether the action was successful"""
        attack_door = AttackDoor(attacker, location, self.state, self.output_builder)
        return attack_door.execute()
    
    def _can_use_equipment(self, entity, equipment: str) -> tuple:
        """Check if an entity can use specified equipment.
        Returns tuple (bool, str) to indicate whether use is possible
        and reason why not if not."""

        # check if entity has equipment in their Equipment
        try:
            (has_equipment, reason) = entity.has_equipment(equipment)
            if has_equipment:
                return (True, "")
            else:
                return (False, reason)
        except UnrecognisedEquipment:
            return (False, "unknown")

    def _can_use_item(self, entity, item: str) -> tuple:
        """Check if an entity can use specified item.
        Returns tuple (bool, str) to indicate whether use is possible
        and reason why not if not."""

        # check if entity has item in their item
        try:
            (has_item, reason) = entity.has_item(item)
            if has_item:
                return (True, "")
            else:
                return (False, reason)
        except UnrecognisedItem:
            return (False, "unknown item")
        
    def use(self,
            equipment: str = None,
            item: str = None,
            entity: str = "player",
            stop: bool = False) -> bool:
        """Attempt to use a specified equipment.
        Returns a bool to indicate whether the action was successful"""

        # get entity object
        if entity == "player":
            entity = self.state.get_player()
        else:
            entity = self.npcs.get_entity(entity)

        if stop:
            self.state.explore()
            self.state.clear_skill_check()
            can_use = entity.stop_using_equipment(equipment)
        elif equipment:
            # check if equipment can be used
            (can_use, reason) = self._can_use_equipment(entity, equipment)
            if can_use:
                self.state.explore()
                self.state.clear_skill_check()
                return entity.use_equipment(equipment)
            else:
                self.output_builder.append(NLG.cannot_use(equipment, reason))
        elif item:
            # check if item can be used
            (can_use, reason) = self._can_use_item(entity, item)
            if can_use:
                self.state.explore()
                self.state.clear_skill_check()
                return entity.use_item(item)
            else:
                self.output_builder.append(NLG.cannot_use(self.state.get_player().character.items.get_name(item), reason))
        return can_use

    def _can_equip(self, entity, weapon: str) -> tuple:
        """Check if an entity can equip specified weapon.
        Returns tuple (bool, str) to indicate whether equip is possible
        and reason why not if not."""

        # check if entity has weapon in their Weapons
        try:
            (can_equip, reason) = entity.can_equip(weapon)
            if can_equip:
                return (True, "")
            else:
                return (False, reason)
        except UnrecognisedWeapon:
            return (False, "unknown")

    def equip(self, weapon: str, entity: str = "player") -> bool:
        """Attempt to equip a specified weapon.
        Returns a bool to indicate whether the action was successful"""

        # get entity object
        if entity == "player":
            entity = self.state.get_player()
        else:
            entity = self.npcs.get_entity(entity)

        # check if weapon can be equipped
        (can_equip, reason) = self._can_equip(entity, weapon)
        if can_equip:
            entity.equip_weapon(weapon)
            self.output_builder.append(NLG.equip_weapon(weapon))
        else:
            self.output_builder.append(NLG.cannot_equip(weapon, reason))
        return can_equip

    def _can_unequip(self, entity, weapon: str) -> tuple:
        """Check if an entity can unequip specified weapon.
        Returns tuple (bool, str) to indicate whether unequip is possible
        and reason why not if not."""

        # check if entity has weapon equipped
        try:
            (can_unequip, reason) = entity.can_unequip(weapon)
            if can_unequip:
                return (True, "")
            else:
                return (False, reason)
        except UnrecognisedWeapon:
            return (False, "unknown")

    def unequip(self, weapon: str = None, entity: str = "player") -> bool:
        """Attempt to unequip a specified weapon.
        Returns a bool to indicate whether the action was successful"""

        # get entity object
        if entity == "player":
            entity = self.state.get_player()
        else:
            entity = self.npcs.get_entity(entity)

        # check if weapon can be unequipped
        (can_unequip, reason) = self._can_unequip(entity, weapon)
        if can_unequip:
            entity.unequip_weapon(weapon)
            self.output_builder.append(NLG.unequip_weapon(weapon))
        else:
            self.output_builder.append(NLG.cannot_unequip(weapon, reason))
        return can_unequip

    def _can_converse(self, target: str) -> tuple:
        """Check if a target can have a conversation.
        Returns tuple (bool, str) to indicate whether conversation is possible
        and reason why not if not."""

        # check if player and target are within converse range
        try:
            if not self.state.get_current_room() == self.state.get_current_room(target):
                return (False, "different location")
            # check if target is a monster
            if self.npcs.get_type(target) == "monster":
                return (False, "monster")
            return (True, "")
        except UnrecognisedEntityError:
            return (False, "unknown")

    def converse(self, target: str) -> bool:
        """Attempt to converse with a specified target.
        Returns a bool to indicate whether the action was successful"""
        
        # check if conversation can happen
        (can_converse, reason) = self._can_converse(target)
        if can_converse:
            if self.npcs.get_entity(target).dialogue:
                self.state.roleplay(target)
                # TODO make the dialogue options flexible
                if not self.state.quest_received:
                    self.state.set_conversation_target(target)
                    self.state.received_quest()
                    self.output_builder.append(
                        self.npcs.get_entity(target).dialogue["gives_quest"])
                elif not self.state.get_dm().npcs.get_monster_id("giant_rat", status="alive", location="inns_cellar"):
                    # TODO this condition is hardcoded for the baradin tomb quest - don't hardcode it
                    self.state.set_conversation_target(target)
                    self.output_builder.append(
                        self.npcs.get_entity(target).dialogue["turn_in_quest"])
                    self.output_builder.append(self.state.get_dm().get_bad_ending())
                    dmai.dmai_helpers.gameover()
                else:
                    self.output_builder.append(NLG.roleplay(self.state.get_entity_name(target)))
            return can_converse
        else:
            if bool(self.state.get_entity_name(target)):
                target_name = self.state.get_entity_name(target)
            else:
                target_name = target
            self.output_builder.append(NLG.cannot_converse(target_name, reason))
            return can_converse

    def investigate(self, target: str, target_type: str = "") -> bool:
        """Attempt to explore/investigate.
        Returns a bool to indicate whether the action was successful"""
        investigate = Investigate(target, self.state, self.output_builder, target_type=target_type)
        return investigate.execute()

    def roll(self, roll_type: str, nlu_entities: dict, die: str = "d20") -> bool:
        """Attempt to roll a specified type.
        Returns a bool to indicate whether the action was successful"""
        roll = Roll(roll_type, die, nlu_entities, self.state, self.output_builder)
        return roll.execute()

    def pick_up(self, item: str, entity: str = "player") -> bool:
        """Attempt to pick up specified item.
        Returns a bool to indicate whether the action was successful"""
        self.state.explore()
        self.state.clear_skill_check()
        pick_up = PickUp(item, entity, self.state, self.output_builder)
        return pick_up.execute()

    def ability_check(self,
                      ability: str,
                      entity: str = "player",
                      target: str = None,
                      target_type: str = "") -> bool:
        """Attempt to perform an ability check.
        Returns a bool to indicate whether the action was successful"""
        check = AbilityCheck(ability, entity, target, target_type, self.state, self.output_builder)
        return check.execute()
