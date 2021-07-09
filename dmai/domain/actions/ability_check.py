from dmai.domain.abilities import Abilities
from dmai.utils.output_builder import OutputBuilder
from dmai.utils.exceptions import UnrecognisedEntityError, UnrecognisedRoomError
from dmai.game.state import State
from dmai.nlg.nlg import NLG
from dmai.domain.actions.action import Action
import dmai


class AbilityCheck(Action):
    def __init__(self, ability: str, entity: str, target: str, target_type: str, state: State, dm_request: bool = False, investigate: bool = False) -> None:
        """AbilityCheck class"""
        Action.__init__(self)
        self.ability = ability
        self.entity = entity
        self.target = target
        self.target_type = target_type
        self.state = state
        self.dm_request = dm_request
        self.investigate = investigate
        self.puzzle = target if target_type == "puzzle" else None

    def __repr__(self) -> str:
        return "{c}".format(c=self.__class__.__name__)

    def execute(self, **kwargs) -> bool:
        return self._ability_check()

    def _can_ability_check(self) -> tuple:
        """Check entity can perform ability check.
        Returns tuple (bool, str) to indicate whether ability check is possible
        and reason why not if not."""

        # check if entity and target are within pick up range
        try:
            current = self.state.get_current_room(self.entity)
            if self.state.get_entity(self.target):
                # TODO support non-room ability checks
                # if not current == self.state.get_current_room(self.target):
                #     return (False, "different location")
                return (False, "not required")
            if self.target_type == "location":
                if not self.state.check_room_exists(self.target):
                    return (False, "unknown room")
                elif not self.target in current.get_connected_rooms():
                    return (False, "different location")

            # can't ability check if can't see
            if not current.visibility:
                if self.entity == "player":
                    if (
                        not self.state.torch_lit
                        and not self.state.get_player().character.has_darkvision()
                    ):
                        return (False, "no visibility")
                    
            # don't need to force open a door which is already open
            if self.target_type == "location" or self.target_type == "door":
                if self.state.travel_allowed(self.state.get_current_room_id(), self.target):
                    return (False, "not required")

            # now check if an ability check is required for this situation
            for puzzle in current.puzzles.get_all_puzzles():
                if puzzle.check_solution_ability(self.ability):
                    self.puzzle = puzzle.id
                    return (True, "")
            
            # none of the above situations were triggered so by default don't allow ability check
            return (False, "not required")
        except UnrecognisedEntityError:
            return (False, "unknown entity")
        except UnrecognisedRoomError:
            return (False, "unknown room")

    def _ability_check(self) -> bool:
        """Attempt to perform ability check.
        Returns a bool to indicate whether the action was successful"""
        
        # check if ability check can happen
        if self.dm_request:
            (can_check, reason) = (True, "")
        else:
            (can_check, reason) = self._can_ability_check()
        if can_check:
            if can_check:
                OutputBuilder.append(
                    NLG.ability_check(Abilities.get_name(self.ability), dm_request=self.dm_request)
                )
                self.state.set_expected_intent(["roll"])
                current = self.state.get_current_room()
                if self.state.current_intent == "explore":
                    if self.investigate:
                        success_func = current.puzzles.get_puzzle(self.puzzle).get_investigate_success_func()
                        success_params = current.puzzles.get_puzzle(self.puzzle).get_investigate_success_params(self.ability)
                    else:
                        success_func = current.puzzles.get_puzzle(self.puzzle).get_explore_success_func()
                        success_params = current.puzzles.get_puzzle(self.puzzle).get_explore_success_params(self.ability)
                elif current.puzzles.get_puzzle(self.puzzle).type == "door":
                    self.target = self.puzzle.split("---")[1]
                    success_func = self.state.unlock_door
                    success_params = [current.id, self.target]
                elif current.puzzles.get_puzzle(self.puzzle).type == "trap":
                    print("IT'S A TRAP")
                    success_func = current.puzzles.get_puzzle(self.puzzle).get_solution_success_func()
                    success_params = current.puzzles.get_puzzle(self.puzzle).get_solution_success_params(self.ability)
                else:
                    # TODO better fallback
                    success_func = print
                    success_params=["Implement something!"]
                self.state.set_ability_check({
                    "target": self.target,
                    "puzzle": self.puzzle,
                    "solution": self.ability,
                    "success_func": success_func,
                    "success_params": success_params
                })
            return can_check
        else:
            target_name = self.target
            if self.state.get_entity_name(self.target):
                target_name = self.state.get_entity_name(self.target)
            try:
                if self.state.get_room_name(self.target):
                    target_name = self.state.get_room_name(self.target)
            except UnrecognisedRoomError:
                target_name = self.target
            OutputBuilder.append(NLG.cannot_ability_check(Abilities.get_name(self.ability), target_name, reason))
            return can_check
