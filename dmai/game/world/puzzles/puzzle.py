from abc import ABC, abstractmethod

from dmai.utils.output_builder import OutputBuilder
from dmai.domain.actions.skill_check import SkillCheck
from dmai.game.state import State
from dmai.utils.logger import get_logger

logger = get_logger(__name__)


class Puzzle(ABC):
    def __init__(self, puzzle_data: dict, state: State, output_builder: OutputBuilder) -> None:
        """Puzzle abstract class"""
        self.state = state
        self.output_builder = output_builder
        try:
            for key in puzzle_data:
                self.__setattr__(key, puzzle_data[key])
        except AttributeError as e:
            logger.error("(SESSION {s}) Cannot create puzzle, incorrect attribute: {e}".format(s=self.state.session.session_id, e=e))
            raise
        
        if self.id not in self.state.puzzle_trigger_map:
            self.state.puzzle_trigger_map[self.id] = {
                    "solution": {},
                    "explore": {},
                    "investigate": {}
                }

        for solution in self.solutions:
            if solution not in self.state.puzzle_trigger_map[self.id]["solution"]:
                self.state.puzzle_trigger_map[self.id]["solution"][solution] = True
            
        for explore in self.explore:
            if explore not in self.state.puzzle_trigger_map[self.id]["explore"]:
                self.state.puzzle_trigger_map[self.id]["explore"][explore] = True

        for investigate in self.investigate:
            if investigate not in self.state.puzzle_trigger_map[self.id]["investigate"]:
                self.state.puzzle_trigger_map[self.id]["investigate"][investigate] = True
            
    def __repr__(self) -> str:
        return "{c}: {n}".format(c=self.__class__.__name__, n=self.name)

    def solve(self) -> None:
        self.state.solved_puzzles.append(self.id)

    def get_solution(self, solution: str) -> dict:
        """Method to return specified solution details"""
        return self.solutions[solution]

    def get_all_solutions(self) -> list:
        """Method to return possible solutions to puzzle"""
        return self.solutions

    def get_solution_id(self, query: str) -> str:
        """Method to return the solution ID depending on the query"""
        if self.check_solution(query):
            return query
        
        solution_type = None
        if self.check_solution_ability(query):
            solution_type = "ability"
        elif self.check_solution_skill(query):
            solution_type = "skill"
        elif self.check_solution_item(query):
            solution_type = "item"
        elif self.check_solution_equipment(query):
            solution_type = "equipment"
        elif self.check_solution_intent(query):
            solution_type = "intent"
        elif self.check_solution_spell(query):
            solution_type = "spell"
        
        for solution in self.solutions:
            if solution_type in self.solutions[solution]:
                if self.solutions[solution] == query:
                    return solution
        
    def check_solution(self, solution: str) -> bool:
        """Method to determine if possible solution exists.
        Returns bool"""
        return solution in self.solutions

    def check_solution_explore(self) -> bool:
        """Method to determine if possible explore solution exists.
        Returns bool"""
        return bool(self.explore)

    def check_solution_ability(self, ability: str) -> bool:
        """Method to determine if possible ability solution exists.
        Returns bool"""
        for s in self.solutions.values():
            if "ability" in s:
                if ability == s["ability"]:
                    return True

    def check_solution_skill(self, skill: str) -> bool:
        """Method to determine if possible skill solution exists.
        Returns bool"""
        for s in self.solutions.values():
            if "skill" in s:
                if skill == s["skill"]:
                    return True

    def check_solution_item(self, item: str) -> bool:
        """Method to determine if possible item solution exists.
        Returns bool"""
        for s in self.solutions.values():
            if "item" in s:
                if item == s["item"]:
                    return True

    def check_solution_equipment(self, equipment: str) -> bool:
        """Method to determine if possible equipment solution exists.
        Returns bool"""
        for s in self.solutions.values():
            if "equipment" in s:
                if equipment == s["equipment"]:
                    return True
    
    def check_solution_intent(self, intent: str) -> bool:
        """Method to determine if possible intent solution exists.
        Returns bool"""
        for s in self.solutions.values():
            if "intent" in s:
                if intent == s["intent"]:
                    return True

    def check_solution_spell(self, spell: str) -> bool:
        """Method to determine if possible spell solution exists.
        Returns bool"""
        for s in self.solutions.values():
            if "spell" in s:
                if spell == s["spell"]:
                    return True
    
    def get_difficulty_class(self, solution: str) -> int:
        """Method to return the difficulty class of specified solution"""
        if solution in self.solutions and "dc" in self.solutions[solution]:
            return self.solutions[solution]["dc"]
        elif solution in self.explore and "dc" in self.explore[solution]:
            return self.explore[solution]["dc"]
        elif solution in self.investigate and "dc" in self.investigate[solution]:
            return self.investigate[solution]["dc"]
        else:
            logger.debug("(SESSION {s}) Solution {so} not in puzzle {p}".format(s=self.state.session.session_id, so=solution, p=self.id))
            return
    
    def get_armor_class(self) -> int:
        """Method to return the armor class of puzzle"""
        if "attack" in self.solutions:
            return self.solutions["attack"]["ac"]
    
    def get_hp(self) -> int:
        """Method to return the hp of puzzle"""
        if "attack" in self.solutions:
            return self.solutions["attack"]["hp"]
    
    def explore_trigger(self) -> None:
        """Method to print any new text if conditions met"""
        if not self.id in self.state.solved_puzzles:
            for explore in self.state.puzzle_trigger_map[self.id]["explore"]:
                if self.state.puzzle_trigger_map[self.id]["explore"][explore]:
                    logger.debug("(SESSION {s}) Explore trigger: {p}".format(s=self.state.session.session_id, p=self.id))
                    if "skill" in self.explore[explore]:
                        self.state.set_expected_intent(["roll", "skill_check"])
                        skill_check = SkillCheck(self.explore[explore]["skill"], "player", self.state.get_current_room_id(), self.state, self.output_builder, dm_request=True, puzzle=self.id)
                        skill_check.execute()
                    else:
                        self.explore_success_func(explore)
                    self.state.puzzle_trigger_map[self.id]["explore"][explore] = False
                    break
    
    def investigate_trigger(self) -> None:
        """Method to print any new text if conditions met"""
        if not self.id in self.state.solved_puzzles:
            for investigate in self.state.puzzle_trigger_map[self.id]["investigate"]:
                if self.state.puzzle_trigger_map[self.id]["investigate"][investigate]:
                    logger.debug("(SESSION {s}) Investigate trigger: {p}".format(s=self.state.session.session_id, p=self.id))
                    if "skill" in self.investigate[investigate]:
                        self.state.set_expected_intent(["roll", "skill_check"])
                        skill_check = SkillCheck(self.investigate[investigate]["skill"], "player", self.state.get_current_room_id(), self.state, self.output_builder, dm_request=True, puzzle=self.id, investigate=True)
                        skill_check.execute()
                    else:
                        self.investigate_success_func(investigate)
                    self.state.puzzle_trigger_map[self.id]["investigate"][investigate] = False
                    break

    def solution_success_func(self, option: str = None) -> None:
        """Method to construct solution success function"""
        # TODO support non-door types
        logger.debug("(SESSION {s}) Puzzle.solution_success_func : {p}".format(s=self.state.session.session_id, p=self.id))
        if not self.id in self.state.solved_puzzles:
            logger.debug("(SESSION {s}) {p} not in state.solved_puzzles".format(s=self.state.session.session_id, p=self.id))
            if self.solutions[option]["say"]:
                self.output_builder.append(self.solutions[option]["say"])
            if self.type == "door":
                room1 = self.id.split("---")[0]
                room2 = self.id.split("---")[1]
                self.state.unlock_door(room1, room2)
            elif self.type == "trap":
                self.state.puzzle_trigger_map[self.id]["solution"][option] = False
                result = self.solutions[option]["result"]
                # TODO support non-monster results
                if self.state.get_entity(result):
                    self.state.set_current_status(result, "alive")
                    self.state.combat(result, "player")
            self.solve()
        logger.debug("(SESSION {s}) Returning from Puzzle.solution_success_func: {p}".format(s=self.state.session.session_id, p=self.id))
        
    def explore_success_func(self, option: str) -> None:
        """Method to construct explore success function"""
        logger.debug("(SESSION {s}) Puzzle.explore_success_func : {p}".format(s=self.state.session.session_id, p=self.id))
        if not self.id in self.state.solved_puzzles:
            logger.debug("(SESSION {s}) {p} not in state.solved_puzzles".format(s=self.state.session.session_id, p=self.id))
            if self.explore[option]["say"]:
                self.output_builder.append(self.explore[option]["say"])
            if self.explore[option]["result"]:
                result = self.explore[option]["result"]
                if result == "open_door":
                    room1 = self.id.split("---")[0]
                    room2 = self.id.split("---")[1]
                    self.state.unlock_door(room1, room2)
                elif result == "add_to_inventory":
                    item_data = self.__dict__
                    self.state.get_player().character.items.add_item(self.id, item_data=item_data)
                elif result == "good_ending":
                    self.output_builder.append(self.state.get_dm().get_good_ending())
                    self.state.gameover()
                    return
            self.solve()
        logger.debug("(SESSION {s}) Returning from Puzzle.explore_success_func: {p}".format(s=self.state.session.session_id, p=self.id))
    
    def investigate_success_func(self, option: str) -> None:
        """Method to construct investigate success function"""
        logger.debug("(SESSION {s}) Puzzle.investigate_success_func: {p}".format(s=self.state.session.session_id, p=self.id))
        solve = False
        if not self.id in self.state.solved_puzzles:
            logger.debug("(SESSION {s}) {p} not in state.solved_puzzles".format(s=self.state.session.session_id, p=self.id))
            if "say" in self.investigate[option]:
                self.output_builder.append(self.investigate[option]["say"])
            if "result" in self.investigate[option] and self.investigate[option]["result"]:
                result = self.investigate[option]["result"]
                if result == "open_door":
                    room1 = self.id.split("---")[0]
                    room2 = self.id.split("---")[1]
                    self.state.unlock_door(room1, room2)
                    solve = True
                elif result == "add_to_inventory":
                    item_data = self.__dict__
                    self.state.get_player().character.items.add_item(self.id, item_data=item_data)
                    solve = True
                elif result == "explore":
                    if self.investigate[option]["id"]:
                        explore_id = self.investigate[option]["id"]
                        puzzle = self.state.get_current_room().puzzles.get_puzzle(self.investigate[option]["id"])
                        if self.state.puzzle_trigger_map[explore_id]["explore"][option]:
                            puzzle.explore_success_func(option)
                elif result == "good_ending":
                    self.output_builder.append(self.state.get_dm().get_good_ending())
                    self.state.gameover()
                    return
                elif self.type == "trap":
                    self.state.puzzle_trigger_map[self.id]["solution"][option] = False
                    result = self.investigate[option]["result"]
                    # TODO support non-monster results
                    if self.state.get_entity(result):
                        self.state.set_current_status(result, "alive")
                        self.state.combat(result, "player")
            else:
                solve = True
            if solve:
                self.solve()
        logger.debug("(SESSION {s}) Returning from Puzzle.investigate_success_func: {p}".format(s=self.state.session.session_id, p=self.id))
    
    def get_solution_success_params(self, roll: str) -> list:
        """Method to return the function params on successful roll"""
        return [roll]
    
    def get_explore_success_params(self, roll: str) -> list:
        """Method to return the function params on successful roll following explore intent"""
        return [roll]
    
    def get_investigate_success_params(self, roll: str) -> list:
        """Method to return the function params on successful roll following investigate intent"""
        return [roll]
    
    def get_success_func(self, func: str) -> object:
        func_map = {
            "investigate": self.investigate_success_func,
            "explore": self.explore_success_func,
            "solution": self.solution_success_func
        }
        return func_map[func]

    def only_key_solution(self) -> bool:
        if not self.explore or (len(self.explore) == 1 and "describe" in self.explore):
            if not self.investigate or (len(self.investigate) == 1 and "describe" in self.investigate):
                if len(self.get_all_solutions()) == 1:
                    if self.get_solution("unlock"):
                        return True
        return False
    
    def has_key_solution(self) -> bool:
        if self.solutions["unlock"]["item"] in self.state.item_quantity:
            return True
        else:
            return False