from dmai.domain.skills import Skills
from dmai.utils.output_builder import OutputBuilder
from dmai.utils.exceptions import UnrecognisedEntityError, UnrecognisedRoomError
from dmai.game.state import State
from dmai.nlg.nlg import NLG
from dmai.domain.actions.action import Action
import dmai


class SkillCheck(Action):
    def __init__(self, skill: str, entity: str, target: str, dm_request: bool = False, puzzle: str = None) -> None:
        """SkillCheck class"""
        Action.__init__(self)
        self.skill = skill
        self.entity = entity
        self.target = target
        self.dm_request = dm_request
        self.puzzle = puzzle
        self.solution = None

    def __repr__(self) -> str:
        return "{c}".format(c=self.__class__.__name__)

    def execute(self, **kwargs) -> bool:
        return self._skill_check()

    def _can_skill_check(self) -> tuple:
        """Check entity can perform skill check.
        Returns tuple (bool, str) to indicate whether skill check is possible
        and reason why not if not."""

        # check if entity and target are within pick up range
        try:
            current = State.get_current_room(self.entity)
            if State.get_entity(self.target):
                # TODO support non-room skill checks
                # if not current == State.get_current_room(self.target):
                #     return (False, "different location")
                return (False, "not required")
            elif not State.check_room_exists(self.target):
                return (False, "unknown room")
            elif not self.target in current.get_connected_rooms():
                return (False, "different location")

            # can't skill check if can't see
            if not current.visibility:
                if self.entity == "player":
                    if (
                        not State.torch_lit
                        or State.get_player().character.has_darkvision()
                    ):
                        return (False, "no visibility")
                    
            # don't need to skill check a door which is already open
            if State.travel_allowed(State.get_current_room_id(), self.target):
                return (False, "not required")

            # now check if an skill check is required for this situation
            for puzzle in current.puzzles.get_all_puzzles():
                # TODO support non-door puzzles
                if puzzle.id == "{c}---{t}".format(c=current.id, t=self.target):
                    if puzzle.check_solution_skill(self.skill):
                        self.puzzle = puzzle.id
                        self.solution = self.skill
                        return (True, "")
            
            # none of the above situations were triggered so by default don't allow skill check
            return (False, "not required")
        except UnrecognisedEntityError:
            return (False, "unknown entity")
        except UnrecognisedRoomError:
            return (False, "unknown room")

    def _skill_check(self) -> bool:
        """Attempt to perform skill check.
        Returns a bool to indicate whether the action was successful"""

        # check if skill check can happen
        if self.dm_request:
            (can_check, reason) = (True, "")
        else:
            (can_check, reason) = self._can_skill_check()
        if can_check:
            if can_check:
                OutputBuilder.append(
                    NLG.skill_check(Skills.get_name(self.skill), dm_request=self.dm_request)
                )
                State.set_expected_intents(["roll"])
                current = State.get_current_room()
                success_func = print
                success_params = [""]
                if current.puzzles.get_puzzle(self.puzzle).type == "door":
                    success_func = State.unlock_door
                    success_params = [current.id, self.target]
                State.set_skill_check({
                    "target": self.target,
                    "puzzle": self.puzzle,
                    "solution": self.solution,
                    "success_func": success_func,
                    "success_params": success_params
                })
            return can_check
        else:
            target_name = self.target
            if State.get_entity_name(self.target):
                target_name = State.get_entity_name(self.target)
            elif reason != "unknown room":
                target_name = State.get_room_name(self.target)
            OutputBuilder.append(NLG.cannot_skill_check(Skills.get_name(self.skill), target_name, reason))
            return can_check
