from dmai.utils.output_builder import OutputBuilder
from dmai.utils.exceptions import UnrecognisedRoomError
from dmai.game.state import State, Status
from dmai.nlg.nlg import NLG
from dmai.domain.actions.action import Action
import dmai


class AttackDoor(Action):
    def __init__(self, attacker: str, target: str) -> None:
        """AttackDoor class"""
        Action.__init__(self)
        self.attacker = attacker
        self.target = target

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
            current = State.get_current_room(self.attacker)
            if not self.target in current.get_connected_rooms():
                return (False, "different location")
            
            # can't attack if can't see
            # TODO change this to blinded condition - disadvantage on attack roll and not knowing whether hit was successful
            if not current.visibility:
                if self.attacker == "player":
                    if (
                        not State.torch_lit
                        or State.get_player().character.has_darkvision()
                    ):
                        return (False, "no visibility")
                    
            # can't attack a destroyed door
            if State.connection_broken(current.id, self.target):
                return (False, "destroyed door")

            # can't attack an unlocked door
            if State.travel_allowed(current.id, self.target):
                return (False, "travel allowed")
            
            # can't attack if no weapon equipped
            if not State.get_player().is_equipped():
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
            State.combat_with_door(self.target)
            return can_attack
        else:
            door_name = "the door to the {t}".format(t=State.get_room_name(self.target))
            OutputBuilder.append(
                NLG.cannot_attack_door(
                    State.get_name(self.attacker),
                    door_name,
                    reason,
                    State.get_formatted_possible_door_targets(),
                )
            )
            return can_attack
        