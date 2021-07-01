from abc import ABC, abstractmethod
from dmai.utils.output_builder import OutputBuilder

from dmai.domain.actions.skill_check import SkillCheck
from dmai.game.state import State
from dmai.utils.logger import get_logger

logger = get_logger(__name__)


class Puzzle(ABC):
    def __init__(self, puzzle_data: dict) -> None:
        """Puzzle abstract class"""
        self.solved = False
        self.triggered = False
        self.explore_map = {}
        try:
            for key in puzzle_data:
                self.__setattr__(key, puzzle_data[key])
        except AttributeError as e:
            logger.error(
                "Cannot create puzzle, incorrect attribute: {e}".format(e=e))
            raise
        
        for explore in self.explore:
            self.explore_map[explore] = {
                "can_trigger": True
            }

    def __repr__(self) -> str:
        return "{c}: {n}".format(c=self.__class__.__name__, n=self.name)

    def solve(self) -> None:
        self.solved = True

    def trigger(self) -> None:
        self.triggered = True

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
        if solution in self.solutions:
            return self.solutions[solution]["dc"]
        elif solution in self.explore:
            return self.explore[solution]["dc"]
        else:
            logger.debug("Solution {s} not in puzzle {p}".format(s=solution, p=self.id))
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
        for explore in self.explore_map:
            if self.explore_map[explore]["can_trigger"]:
                if self.explore[explore]["skill"]:
                    print(explore)
                    State.set_expected_intents(["roll"])
                    skill_check = SkillCheck(self.explore[explore]["skill"], "player", target=State.get_current_room_id(), dm_request=True, puzzle=self.id)
                    skill_check.execute()
                else:
                    print("just triggers")
                self.explore_map[explore]["can_trigger"] = False
                break
    
    def success_func(self, roll: str) -> None:
        """Method to construct success function"""
        if self.explore[roll]["say"]:
            OutputBuilder.append(self.explore[roll]["say"])
        if self.explore[roll]["result"]:
            result = self.explore[roll]["result"]
            if result == "open_door":
                room1 = self.id.split("---")[0]
                room2 = self.id.split("---")[1]
                State.unlock_door(room1, room2)
            if result == "add_to_inventory":
                State.get_player().character.items.add_item(self.id)
        
    def get_explore_success_func(self) -> object:
        """Method to return the function on successful roll following explore intent"""
        return self.success_func
    
    def get_explore_success_params(self, roll: str) -> list:
        """Method to return the function params on successful roll following explore intent"""
        return [roll]