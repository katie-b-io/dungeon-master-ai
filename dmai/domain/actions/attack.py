from dmai.utils.output_builder import OutputBuilder
from dmai.utils.exceptions import UnrecognisedEntityError
from dmai.game.state import State, Status
from dmai.nlg.nlg import NLG
from dmai.domain.actions.action import Action
import dmai


class Attack(Action):
    def __init__(self, attacker: str, target: str, target_type: str, state: State, output_builder: OutputBuilder) -> None:
        """Attack class"""
        Action.__init__(self)
        self.attacker = attacker
        self.target = target
        self.target_type = target_type
        self.state = state
        self.output_builder = output_builder

    def __repr__(self) -> str:
        return "{c}".format(c=self.__class__.__name__)

    def execute(self, **kwargs) -> bool:
        return self._attack()

    def _can_attack(self) -> tuple:
        """Check if a target can be attacked by an attacker.
        Returns tuple (bool, str) to indicate whether attack is possible
        and reason why not if not."""

        # check if attacker and target are within attack range
        try:
            current = self.state.get_current_room(self.attacker)

            if self.target_type == "scenery":
                return (False, "target is scenery")
            
            if self.target_type == "puzzle":
                return (False, "target is puzzle")

            if not current == self.state.get_current_room(self.target):
                return (False, "different location")
            
            # can't attack a dead target
            if self.state.get_current_status(self.target) == Status("dead"):
                return (False, "dead target")

            # can't attack if can't see
            # TODO change this to blinded condition - disadvantage on attack roll and not knowing whether hit was successful
            if not current.visibility:
                if self.attacker == "player":
                    if (
                        not self.state.torch_lit
                        and not self.state.get_player().character.has_darkvision()
                    ):
                        return (False, "no visibility")
            
            # can't attack if no weapon equipped
            if not self.state.get_player().is_equipped():
                return (False, "no weapon")

            # none of the above situations were triggered so allow attack
            return (True, "")
        except UnrecognisedEntityError:
            return (False, "unknown target")

    def _attack(self) -> bool:
        """Attempt to attack a specified target.
        Returns a bool to indicate whether the action was successful"""

        # check if attack can happen
        (can_attack, reason) = self._can_attack()
        if can_attack:
            # check if target will end game
            if self.state.get_dm().npcs.get_type(self.target) == "npc":
                npc = self.state.get_entity(self.target)
                if npc.attack_ends_game:
                    # this is a game end condition
                    self.output_builder.append(npc.dialogue["attacked_by_player"])
                    self.output_builder.append(self.state.get_dm().get_bad_ending())
                    self.state.gameover()
                    return False
            self.state.combat(self.attacker, self.target)
        else:
            target_name = self.state.get_entity_name(self.target)
            if not target_name:
                target_name = self.target
            self.output_builder.append(
                NLG.cannot_attack(
                    self.state.get_entity_name(self.attacker),
                    target_name,
                    self.state.char_name,
                    reason,
                    self.state.get_formatted_possible_monster_targets(),
                )
            )
        return can_attack
