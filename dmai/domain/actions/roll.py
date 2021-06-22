from dmai.utils.dice_roller import DiceRoller
from dmai.utils.output_builder import OutputBuilder
from dmai.utils.exceptions import DiceFormatError
from dmai.game.state import State
from dmai.nlg.nlg import NLG
from dmai.domain.actions.action import Action
from dmai.game.state import Combat
import dmai


class Roll(Action):
    def __init__(self, roll_type: str, die: str, nlu_entities: dict) -> None:
        """Roll class"""
        Action.__init__(self)
        self.roll_type = roll_type
        self.die = die
        self.nlu_entities = nlu_entities
        self.roll_map = {
            "attack": self._attack_roll
        }

    def __repr__(self) -> str:
        return "{c}".format(c=self.__class__.__name__)

    def execute(self, **kwargs) -> bool:
        return self._roll()
    
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
            if self.roll_type in self.roll_map:
                can_roll = self.roll_map[self.roll_type]()
            else:
                return False
            return can_roll
        else:
            OutputBuilder.append("Can't roll!")
            return can_roll

    def _attack_roll(self) -> bool:
        """Execute an attack roll.
        Returns a bool to indicate whether the action was successful"""

        # set initiative order
        if State.get_combat_status() == Combat.INITIATIVE:
            State.set_initiative_order()
        
        # get attack roll from player
        if State.get_combat_status() == Combat.ATTACK_ROLL:
            OutputBuilder.append(NLG.perform_attack_roll())
            
        elif State.get_combat_status() == Combat.WAIT:
            # monster(s) have their go now
            OutputBuilder.append("{e} is having a go!".format(e=State.get_currently_acting_entity()))
            monster = State.get_entity(State.get_currently_acting_entity())
            monster.perform_next_move()
        
        # update the initiative order
        State.update_initiative_order()
        