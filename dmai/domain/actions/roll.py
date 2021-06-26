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
        self.roll_map = {"attack": self._attack_roll}

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
                can_roll = False
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
            OutputBuilder.append(
                NLG.entity_turn(State.get_name(State.get_currently_acting_entity()))
            )
        
        # make sure the player can enter input when not waiting
        State.play()
        
        # process exising input before prompting for further input
        if State.get_combat_status() == Combat.WAIT:
            # process the last player input (damage roll)
            if State.get_current_target():
                target = State.get_current_target()
                player = State.get_entity()
                damage = player.damage_roll()
                hp = State.take_damage(damage, "player", entity=target.unique_id)
                OutputBuilder.append("You dealt {d} damage to {m} (hp is now {h})".format(d=damage, m=target.unique_name, h=hp))
                # end the fight if we're not in combat any more
                if not State.in_combat:
                    return True
            OutputBuilder.append("Okay, now the monsters get to have their turn!")
            State.pause()
        elif State.get_combat_status() == Combat.DAMAGE_ROLL:
            # process the last player input (attack roll)
            target = State.get_current_target()
            player = State.get_entity()
            if player.attack_roll() >= target.armor_class:
                # can deal damage
                OutputBuilder.append("Okay that hits, time to deal some damage!")
            else:
                # can't deal damage, clear target
                State.clear_target()
                OutputBuilder.append("That doesn't hit. Monster's turn now.")
                State.pause()

        # see if monster(s) have their go now
        while State.get_combat_status() == Combat.WAIT:
            entity = State.get_currently_acting_entity()
            if entity == "player":
                # progress to declare target
                State.progress_combat_status()
                return True
            else:
                monster = State.get_entity(entity)
                monster.perform_next_move()

        # get target declaration from player if no target,
        if State.get_combat_status() == Combat.DECLARE:
            State.set_expected_intents(["attack"])
            OutputBuilder.append(NLG.declare_attack())
            State.progress_combat_status()
            return True
        
        # get attack roll from player
        if State.get_combat_status() == Combat.ATTACK_ROLL:
            # this is handled by Attack._attack()
            pass

        # get attack roll from player
        if State.get_combat_status() == Combat.DAMAGE_ROLL:
            if State.get_current_target():
                # now return the utterance for getting the next roll
                OutputBuilder.append(NLG.perform_damage_roll())
                State.progress_combat_status()
            else:
                # didn't hit, skip damage roll
                State.progress_combat_status()
        return True