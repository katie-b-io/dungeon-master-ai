from dmai.utils.output_builder import OutputBuilder
from dmai.utils.dice_roller import DiceRoller
from dmai.utils.exceptions import DiceFormatError
from dmai.game.state import State
from dmai.nlg.nlg import NLG
from dmai.domain.actions.action import Action
from dmai.game.state import Combat
from dmai.utils.logger import get_logger

logger = get_logger(__name__)



class Roll(Action):
    def __init__(self, roll_type: str, die: str, nlu_entities: dict, state: State, output_builder: OutputBuilder) -> None:
        """Roll class"""
        Action.__init__(self)
        self.roll_type = roll_type
        self.die = die
        self.nlu_entities = nlu_entities
        self.state = state
        self.output_builder = output_builder
        self.roll_map = {
            "attack": self._attack_roll,
            "door_attack": self._door_attack_roll,
            "ability_check": self._ability_roll,
            "skill_check": self._skill_roll
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
                (roll_str, dice_val) = DiceRoller.roll(self.die)
                self.output_builder.append(roll_str)
                self.output_builder.append(NLG.no_reason_roll())
                can_roll = True
        else:
            (roll_str, dice_val) = DiceRoller.roll("d20")
            self.output_builder.append(roll_str)
            self.output_builder.append(NLG.no_reason_roll())
            can_roll = True
        return can_roll
    
    def _door_attack_roll(self) -> bool:
        """Execute an attack roll against door.
        Returns a bool to indicate whether the action was successful"""
        if self.state.get_combat_status() == Combat.ATTACK_ROLL:
            # process the last player input (damage roll)
            if self.state.door_target:
                target = self.state.door_target
                player = self.state.get_entity()
                damage = player.damage_roll()
                hp = self.state.take_door_damage(damage, target)
                self.output_builder.append("You dealt {d} damage to {t} door (hp is now {h})".format(d=damage, t=self.state.get_room_name(target), h=hp))
                # end the fight if we're not in combat any more
                if not self.state.in_combat_with_door:
                    return True
        elif self.state.get_combat_status() == Combat.DAMAGE_ROLL:
            # process the last player input (attack roll)
            target = self.state.door_target
            player = self.state.get_entity()
            if player.attack_roll() >= self.state.get_door_armor_class(self.state.get_current_room_id(), target):
                # can deal damage
                self.output_builder.append("Okay that hits, try and deal some damage!")
            else:
                # can't deal damage, clear target
                self.state.door_target = None
                self.state.in_combat_with_door = False
                self.output_builder.append("That doesn't hit. Declare attack against door again if you want to try again.")
                return True
                
        # get attack roll from player
        if self.state.get_combat_status() == Combat.ATTACK_ROLL:
            # this is handled by AttackDoor._attack()
            pass

        # get attack roll from player
        if self.state.get_combat_status() == Combat.DAMAGE_ROLL:
            if self.state.door_target:
                # now return the utterance for getting the next roll
                self.output_builder.append(NLG.perform_damage_roll())
                self.state.set_combat_status(2)
        return True

    def _attack_roll(self) -> bool:
        """Execute an attack roll.
        Returns a bool to indicate whether the action was successful"""
        first_turn = False

        # set initiative order
        if self.state.get_combat_status() == Combat.INITIATIVE:
            first_turn = True
            self.state.set_initiative_order()
            self.output_builder.append(
                NLG.first_turn(self.state.get_entity_name(self.state.get_currently_acting_entity()))
            )
        
        # make sure the player can enter input when not waiting
        self.state.play()
        
        # process exising input before prompting for further input
        if self.state.get_combat_status() == Combat.WAIT:
            # process the last player input (damage roll)
            if self.state.get_current_target():
                target = self.state.get_current_target()
                player = self.state.get_entity()
                damage = player.damage_roll()
                hp = max(0, self.state.take_damage(damage, "player", entity=target.unique_id))
                if self.state.game_ended:
                    return
                # end the fight if we're not in combat any more
                if not self.state.in_combat:
                    return True
                if not first_turn:
                    self.output_builder.append("Okay, now the monsters get to have their turn!")
            self.state.pause()
        elif self.state.get_combat_status() == Combat.DAMAGE_ROLL:
            # process the last player input (attack roll)
            target = self.state.get_current_target()
            player = self.state.get_entity()
            if player.attack_roll() >= target.armor_class:
                # can deal damage
                self.output_builder.append("Okay that hits, time to deal some damage!")
            else:
                # can't deal damage, clear target
                self.state.clear_target()
                self.output_builder.append("That doesn't hit. Monster's turn now.")
                self.state.pause()

        # see if monster(s) have their go now
        while self.state.get_combat_status() == Combat.WAIT:
            entity = self.state.get_currently_acting_entity()
            if entity == "player":
                # progress to declare target
                self.state.progress_combat_status()
                return True
            else:
                monster = self.state.get_entity(entity)
                monster.perform_next_move()

        # get target declaration from player if no target,
        if self.state.get_combat_status() == Combat.DECLARE:
            self.state.set_expected_entities(["monster"])
            self.state.set_expected_intent(["attack"])
            self.output_builder.append(NLG.declare_attack())
            self.state.progress_combat_status()
            return True
        
        # get attack roll from player
        if self.state.get_combat_status() == Combat.ATTACK_ROLL:
            # this is handled by Attack._attack()
            pass

        # get attack roll from player
        if self.state.get_combat_status() == Combat.DAMAGE_ROLL:
            if self.state.get_current_target():
                # now return the utterance for getting the next roll
                self.output_builder.append(NLG.perform_damage_roll())
                self.state.progress_combat_status()
            else:
                # didn't hit, skip damage roll
                self.state.progress_combat_status()
        return True
    
    def _ability_roll(self) -> bool:
        """Execute an ability roll.
        Returns a bool to indicate whether the ability check was successful"""
        logger.debug("(SESSION {s}) Roll _ability_roll State.__dict__".format(s=self.state.session.session_id))

        player = self.state.get_entity()
        roll = player.ability_roll(self.state.stored_ability_check["solution"])
        puzzle = self.state.get_current_room().puzzles.get_puzzle(self.state.stored_ability_check["puzzle"])
        dc = puzzle.get_difficulty_class(self.state.stored_ability_check["solution"])
        if roll >= dc:
            self.output_builder.append(NLG.succeed_check())
            success_func = puzzle.get_success_func(self.state.stored_ability_check["success_func"])
            success_func(*self.state.stored_ability_check["success_params"])
            self.state.clear_ability_check()
        else:
            self.output_builder.append(NLG.fail_check(self.state.stored_ability_check["allow_repeat"]))
            if not self.state.stored_ability_check["allow_repeat"]:
                self.state.clear_ability_check()
        self.state.clear_expected_intent()
        self.state.clear_ability_check()
        return True
    
    def _skill_roll(self) -> bool:
        """Execute an skill roll.
        Returns a bool to indicate whether the skill check was successful"""
        logger.debug("(SESSION {s}) Roll _skill_roll State.__dict__".format(s=self.state.session.session_id))

        player = self.state.get_entity()
        roll = player.skill_roll(self.state.stored_skill_check["solution"])
        puzzle = self.state.get_current_room().puzzles.get_puzzle(self.state.stored_skill_check["puzzle"])
        dc = puzzle.get_difficulty_class(self.state.stored_skill_check["solution"])
        if roll >= dc:
            self.output_builder.append(NLG.succeed_check())
            success_func = puzzle.get_success_func(self.state.stored_skill_check["success_func"])
            success_func(*self.state.stored_skill_check["success_params"])
            self.state.clear_skill_check()
        else:
            self.output_builder.append(NLG.fail_check(self.state.stored_skill_check["allow_repeat"]))
            if not self.state.stored_skill_check["allow_repeat"]:
                self.state.clear_skill_check()
        self.state.clear_expected_intent()
        return True