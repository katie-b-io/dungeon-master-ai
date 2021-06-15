from dmai.utils.output_builder import OutputBuilder
from dmai.game.npcs.npc_collection import NPCCollection
from dmai.utils.loader import Loader
from dmai.utils.exceptions import UnrecognisedRoomError, UnrecognisedEquipment, UnrecognisedWeapon, UnrecognisedEntityError
from dmai.game.state import State
from dmai.game.adventure import Adventure
from dmai.nlg.nlg import NLG
import dmai


class Actions:

    # class variables
    action_data = dict()

    def __init__(self, adventure: Adventure, npcs: NPCCollection) -> None:
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
            current = State.get_current_room_id(entity)
            if current == destination:
                return (False, "same")

            if State.travel_allowed(current, destination):
                return (True, "")
            else:
                return (False, "locked")
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
            OutputBuilder.append(NLG.cannot_move(destination, reason))
        return can_move

    def _can_attack(self, attacker: str, target: str) -> tuple:
        """Check if a target can be attacked by an attacker.
        Returns tuple (bool, str) to indicate whether attack is possible
        and reason why not if not."""

        # check if attacker and target are within attack range
        if not State.get_current_room(attacker) == State.get_current_room(
                target):
            return (False, "Different location")
        return (True, "")

    def attack(self, attacker: str, target: str) -> bool:
        """Attempt to attack a specified target.
        Returns a bool to indicate whether the action was successful"""

        # check if attack can happen
        (can_attack, reason) = self._can_attack(attacker, target)
        if can_attack:
            # check if target will end game
            if self.npcs.get_type(target) == "npc":
                if self.npcs.get_npc(target).attack_ends_game:
                    # this is a game end condition
                    OutputBuilder.append(NLG.attack_npc_end_game(target))
                    dmai.dmai_helpers.gameover()
            attacker = "You" if attacker == "player" else attacker
            OutputBuilder.append("{a} attacked {t}!".format(a=attacker,
                                                            t=target))
            State.combat(attacker, target)
            return can_attack
        else:
            attacker = "You" if attacker == "player" else attacker
            OutputBuilder.append("{a} can't attack {t}!\n{r}".format(
                a=attacker, t=target, r=reason))
            return can_attack

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
            entity.stop_using_equipment(equipment)
            can_use = True

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

    def unequip(self, weapon: str, entity: str = "player") -> bool:
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
        if not State.get_current_room() == State.get_current_room(target):
            return (False, "different location")
        # check if target is a monster
        if self.npcs.get_type(target) == "monster":
            return (False, "monster")
        return (True, "")

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
                State.roleplay(target)
            return can_converse
        else:
            OutputBuilder.append("You can't converse with {t}!\n{r}".format(
                t=target, r=reason))
            return can_converse