from dmai.domain.skills import Skills
from dmai.utils.output_builder import OutputBuilder
from dmai.utils.exceptions import UnrecognisedEntityError, UnrecognisedRoomError
from dmai.game.state import State
from dmai.nlg.nlg import NLG
from dmai.domain.actions.action import Action
from dmai.utils.logger import get_logger

logger = get_logger(__name__)



class SkillCheck(Action):
    def __init__(self, skill: str, entity: str, target: str, state: State, output_builder: OutputBuilder, dm_request: bool = False, puzzle: str = None, investigate: bool = False) -> None:
        """SkillCheck class"""
        Action.__init__(self)
        self.skill = skill
        self.entity = entity
        self.target = target
        self.state = state
        self.output_builder = output_builder
        self.dm_request = dm_request
        self.puzzle = puzzle
        self.investigate = investigate
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
            current = self.state.get_current_room(self.entity)
            if self.state.get_entity(self.target):
                # TODO support non-room skill checks
                # if not current == self.state.get_current_room(self.target):
                #     return (False, "different location")
                return (False, "not required")
            elif not self.state.check_room_exists(self.target):
                return (False, "unknown room")
            elif not self.target in current.get_connected_rooms():
                return (False, "different location")

            # can't skill check if can't see
            if not current.visibility:
                if self.entity == "player":
                    if (
                        not self.state.torch_lit
                        and not self.state.get_player().character.has_darkvision()
                    ):
                        return (False, "no visibility")
                    
            # don't need to skill check a door which is already open
            if self.state.travel_allowed(self.state.get_current_room_id(), self.target):
                return (False, "not required")

            # now check if an skill check is required for this situation
            for puzzle in current.puzzles.get_all_puzzles():
                # TODO support non-door puzzles
                if puzzle.id == "{c}---{t}".format(c=current.id, t=self.target):
                    if puzzle.check_solution_skill(self.skill) and puzzle.id not in self.state.solved_puzzles:
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
            self.solution = self.skill
        else:
            (can_check, reason) = self._can_skill_check()
        if can_check:
            if can_check:
                self.output_builder.append(
                    NLG.skill_check(Skills.get_name(self.skill), dm_request=self.dm_request)
                )
                self.state.set_expected_intent(["roll", "skill_check"])
                current = self.state.get_current_room()
                if self.state.current_intent == "explore":
                    if self.investigate:
                        success_func = "investigate"
                        success_params = current.puzzles.get_puzzle(self.puzzle).get_investigate_success_params(self.skill)
                    else:
                        success_func = "explore"
                        success_params = current.puzzles.get_puzzle(self.puzzle).get_explore_success_params(self.skill)
                elif current.puzzles.get_puzzle(self.puzzle).type == "door":
                    success_func = "solution"
                    success_params = current.puzzles.get_puzzle(self.puzzle).get_solution_success_params(self.skill)
                else:
                    # TODO better fallback
                    success_func = print
                    success_params=["Implement something!"]
                self.state.set_skill_check({
                    "target": self.target,
                    "puzzle": self.puzzle,
                    "solution": self.solution,
                    "success_func": success_func,
                    "success_params": success_params,
                    "allow_repeat": False if self.dm_request else True
                })
            return can_check
        else:
            target_name = self.target
            if self.state.get_entity_name(self.target):
                target_name = self.state.get_entity_name(self.target)
            elif reason != "unknown room":
                target_name = self.state.get_room_name(self.target)
            self.output_builder.append(NLG.cannot_skill_check(Skills.get_name(self.skill), target_name, reason))
            return can_check
