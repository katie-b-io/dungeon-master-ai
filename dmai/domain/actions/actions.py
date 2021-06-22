from dmai.utils.output_builder import OutputBuilder
from dmai.utils.loader import Loader
from dmai.utils.exceptions import UnrecognisedRoomError, UnrecognisedEquipment, UnrecognisedWeapon, UnrecognisedEntityError
from dmai.game.state import State
from dmai.game.adventure import Adventure
from dmai.nlg.nlg import NLG
from dmai.domain.actions.attack import Attack
from dmai.domain.actions.roll import Roll
import dmai


class Actions:

    # class variables
    action_data = dict()

    def __init__(self, adventure: Adventure, npcs) -> None:
        """Actions class"""
        self.adventure = adventure
        self.npcs = npcs
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
            current = State.get_current_room(entity)
            if current.id == destination:
                return (False, "same")
            
            # check if travel is allowed
            if State.travel_allowed(current.id, destination):

                # can't move if can't see
                if not current.visibility:
                    if not State.torch_lit or State.get_player(
                    ).character.has_darkvision():
                        return (False, "no visibility")
                
                # can't move if in a room with monsters that must be killed
                for monster in State.get_dm().npcs.get_all_monsters():
                    if monster.must_kill and State.is_alive(monster.unique_id):
                        if State.get_current_room_id() == State.get_current_room_id(monster.unique_id):
                            return (False, "must kill")
                
                # can't move without quest
                if not State.questing:
                    return (False, "no quest")

                # none of the above situations were triggered so allow travel
                return (True, "")
            
            else:
                if destination in State.get_current_room().get_connected_rooms():
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
            State.set_current_room(entity, destination)
        else:
            try:
                destination = State.get_room_name(destination)
            except UnrecognisedRoomError:
                pass
            connected_rooms = State.get_current_room().get_connected_rooms()
            if reason == "locked":
                possible_destinations = [State.get_room_name(room) for room in connected_rooms if State.travel_allowed(State.get_current_room_id(), room)]
            else:
                possible_destinations = [State.get_room_name(room) for room in connected_rooms]
            OutputBuilder.append(NLG.cannot_move(destination, reason, possible_destinations))
        return can_move

    def attack(self, attacker: str, target: str) -> bool:
        """Attempt to attack a specified target.
        Returns a bool to indicate whether the action was successful"""
        attack = Attack(attacker, target)
        return attack.execute()

    def _can_use(self, entity, equipment: str) -> tuple:
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

    def use(self,
            equipment: str,
            entity: str = "player",
            stop: bool = False) -> bool:
        """Attempt to use a specified equipment.
        Returns a bool to indicate whether the action was successful"""

        # get entity object
        if entity == "player":
            entity = State.get_player()
        else:
            entity = self.npcs.get_entity(entity)

        if stop:
            can_use = entity.stop_using_equipment(equipment)
        else:
            # check if equipment can be used
            (can_use, reason) = self._can_use(entity, equipment)
            if can_use:
                entity.use_equipment(equipment)
            else:
                OutputBuilder.append(NLG.cannot_use(equipment, reason))
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
            entity = State.get_player()
        else:
            entity = self.npcs.get_entity(entity)

        # check if weapon can be equipped
        (can_equip, reason) = self._can_equip(entity, weapon)
        if can_equip:
            entity.equip_weapon(weapon)
            OutputBuilder.append(NLG.equip_weapon(weapon))
        else:
            OutputBuilder.append(NLG.cannot_equip(weapon, reason))
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
            entity = State.get_player()
        else:
            entity = self.npcs.get_entity(entity)

        # check if weapon can be unequipped
        (can_unequip, reason) = self._can_unequip(entity, weapon)
        if can_unequip:
            entity.unequip_weapon(weapon)
            OutputBuilder.append(NLG.unequip_weapon(weapon))
        else:
            OutputBuilder.append(NLG.cannot_unequip(weapon, reason))
        return can_unequip

    def _can_converse(self, target: str) -> tuple:
        """Check if a target can have a conversation.
        Returns tuple (bool, str) to indicate whether conversation is possible
        and reason why not if not."""

        # check if player and target are within converse range
        try:
            if not State.get_current_room() == State.get_current_room(target):
                return (False, "Different location")
            # check if target is a monster
            if self.npcs.get_type(target) == "monster":
                return (False, "monster")
            return (True, "")
        except UnrecognisedEntityError:
            return (False, "Unknown target")

    def converse(self, target: str) -> bool:
        """Attempt to converse with a specified target.
        Returns a bool to indicate whether the action was successful"""
        
        # check if conversation can happen
        (can_converse, reason) = self._can_converse(target)
        if can_converse:
            if self.npcs.get_entity(target).dialogue:
                # TODO make the dialogue options flexible
                if not State.quest_received:
                    State.set_conversation_target(target)
                    State.received_quest()
                    OutputBuilder.append(
                        self.npcs.get_entity(target).dialogue["gives_quest"])
                else:
                    OutputBuilder.append(NLG.roleplay(State.get_name(target)))
                State.roleplay(target)
            return can_converse
        else:
            OutputBuilder.append("You can't converse with {t}!\n{r}".format(
                t=target, r=reason))
            return can_converse

    def _can_investigate(self, target: str) -> tuple:
        """Check if player can investigate target.
        Returns tuple (bool, str) to indicate whether investigation is possible
        and reason why not if not."""
        try:
            # check if target is in same location as player
            if not State.get_current_room_id(
                    target) == State.get_current_room_id():
                return (False, "different location")
            else:
                return (True, "")
        except UnrecognisedEntityError:
            return (False, "unknown entity")

    def investigate(self, target: str) -> bool:
        """Attempt to investigate current location.
        Returns a bool to indicate whether the action was successful"""

        # check if entity can investigate
        (can_investigate, reason) = self._can_investigate(target)
        if can_investigate:
            # TODO add investigation descriptions to entities in adventure
            OutputBuilder.append("You investigate {t}...".format(t=target))
        else:
            OutputBuilder.append(NLG.cannot_investigate(target, reason))
        return can_investigate

    def roll(self, roll_type: str, nlu_entities: dict, die: str = "d20") -> bool:
        """Attempt to roll a specified type.
        Returns a bool to indicate whether the action was successful"""
        roll = Roll(roll_type, die, nlu_entities)
        return roll.execute()

    @staticmethod
    def declare_attack_against_entity(attacker: str, target: str, *args) -> None:
        """Method to delcare attack against entity"""
        attacker = State.get_entity(attacker)
        OutputBuilder.append(NLG.attack(attacker.name, target))
    
    @staticmethod
    def attack_player(*args) -> None:
        print("Attack player")
    
    @staticmethod
    def attack_roll(*args) -> None:
        print("Attack roll")
    
    @staticmethod
    def damage_roll(*args) -> None:
        print("damage roll")