from dmai.utils.output_builder import OutputBuilder
from dmai.utils.exceptions import UnrecognisedEntityError
from dmai.game.state import State, Status
from dmai.nlg.nlg import NLG
from dmai.domain.actions.action import Action
import dmai


class Attack(Action):
    def __init__(self, attacker: str, target: str) -> None:
        """Attack class"""
        Action.__init__(self)
        self.attacker = attacker
        self.target = target

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
            current = State.get_current_room(self.attacker)
            if not current == State.get_current_room(self.target):
                return (False, "different location")
            
            # can't attack a dead target
            if State.get_current_status(self.target) == Status("dead"):
                return (False, "dead target")

            # can't attack if can't see
            # TODO change this to blinded condition - disadvantage on attack roll and not knowing whether hit was successful
            if not current.visibility:
                if self.attacker == "player":
                    if (
                        not State.torch_lit
                        or State.get_player().character.has_darkvision()
                    ):
                        return (False, "no visibility")

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
            if State.get_dm().npcs.get_type(self.target) == "npc":
                if State.get_dm().npcs.get_npc(self.target).attack_ends_game:
                    # this is a game end condition
                    OutputBuilder.append(NLG.attack_npc_end_game(self.target))
                    dmai.dmai_helpers.gameover()
            State.combat(self.attacker, self.target)
            return can_attack
        else:
            OutputBuilder.append(
                NLG.cannot_attack(
                    State.get_name(self.attacker),
                    State.get_name(self.target),
                    reason,
                    State.get_formatted_possible_monster_targets(),
                )
            )
            return can_attack
        