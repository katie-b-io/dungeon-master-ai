from dmai.utils.output_builder import OutputBuilder
from dmai.utils.exceptions import UnrecognisedRoomError
from dmai.game.state import State
from dmai.nlg.nlg import NLG
from dmai.domain.actions.action import Action
import dmai


class AttackDoor(Action):
    def __init__(self, attacker: str, target: str, state: State, output_builder: OutputBuilder) -> None:
        """AttackDoor class"""
        Action.__init__(self)
        self.attacker = attacker
        self.target = target
        self.state = state
        self.output_builder = output_builder

    def __repr__(self) -> str:
        return "{c}".format(c=self.__class__.__name__)

    def execute(self, **kwargs) -> bool:
        return self._attack_door()

    def _can_attack_door(self) -> tuple:
        """Check if a door can be attacked by an attacker.
        Returns tuple (bool, str) to indicate whether attack is possible
        and reason why not if not."""

        # check if attacker and door are within attack range
        try:
            current = self.state.get_current_room(self.attacker)
            if not self.target in current.get_connected_rooms():
                return (False, "different location")
            
            # can't attack if can't see
            # TODO change this to blinded condition - disadvantage on attack roll and not knowing whether hit was successful
            if not current.visibility:
                if self.attacker == "player":
                    if (
                        not self.state.torch_lit
                        and not self.state.get_player().character.has_darkvision()
                    ):
                        return (False, "no visibility")
                    
            # can't attack a destroyed door
            if self.state.connection_broken(current.id, self.target):
                return (False, "destroyed door")

            # can't attack an unlocked door
            if self.state.travel_allowed(current.id, self.target):
                return (False, "travel allowed")
            
            # can't attack if no weapon equipped
            if not self.state.get_player().is_equipped():
                return (False, "no weapon")

            # none of the above situations were triggered so allow attack
            return (True, "")
        except UnrecognisedRoomError:
            return (False, "unknown target")

    def _attack_door(self) -> bool:
        """Attempt to attack a specified door.
        Returns a bool to indicate whether the action was successful"""

        # check if attack can happen
        (can_attack, reason) = self._can_attack_door()
        if can_attack:
            self.state.combat_with_door(self.target)
            return can_attack
        else:
            door_name = "the door to the {t}".format(t=self.state.get_room_name(self.target))
            self.output_builder.append(
                NLG.cannot_attack_door(
                    self.state.get_entity_name(self.attacker),
                    door_name,
                    self.state.char_name,
                    reason,
                    self.state.get_formatted_possible_door_targets(),
                )
            )
            return can_attack
        