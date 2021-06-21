from dmai.utils.dice_roller import DiceRoller
from dmai.utils.output_builder import OutputBuilder
from dmai.utils.exceptions import DiceFormatError
from dmai.game.state import State
from dmai.nlg.nlg import NLG
from dmai.domain.actions.action import Action
import dmai


class Roll(Action):
    def __init__(self, roll_type: str, die: str, nlu_entities: dict) -> None:
        """Roll class"""
        Action.__init__(self)
        self.roll_type = roll_type
        self.die = die
        self.nlu_entities = nlu_entities

    def __repr__(self) -> str:
        return "{c}".format(c=self.__class__.__name__)

    def _can_roll(self) -> tuple:
        """Check if a dice can be rolled.
        Returns tuple (bool, str) to indicate whether roll is possible
        and reason why not if not."""

        # check if dice can be rolled
        try:
            DiceRoller.check(self.die)
        except DiceFormatError:
            return (False, "unknown dice")
        return (True, "")

    def _roll(self) -> bool:
        """Attempt to roll a specified die.
        Returns a bool to indicate whether the action was successful"""

        # check if roll can happen
        (can_roll, reason) = self._can_roll()
        if can_roll:
            result = DiceRoller.roll(self.die)
            return can_roll
        else:
            OutputBuilder.append("Can't roll!")
            return can_roll

    def execute(self, **kwargs) -> bool:
        return self._roll()
